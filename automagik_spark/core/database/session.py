"""
Database Session Management

Provides functionality for creating and managing database sessions.
"""

import os
import logging
import threading
from contextlib import asynccontextmanager, contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from ...api.config import get_database_url

logger = logging.getLogger(__name__)

# Thread lock for thread-safe lazy initialization
_engine_lock = threading.Lock()

# Global variables to hold the engines and session factories (lazy-initialized)
_async_engine: Optional[create_async_engine] = None
_sync_engine: Optional[create_engine] = None
_async_session_factory: Optional[async_sessionmaker] = None
_sync_session_factory: Optional[sessionmaker] = None
_database_url: Optional[str] = None

def get_database_url_runtime():
    """Get database URL at runtime (not import time) for lazy initialization."""
    global _database_url
    if _database_url is None:
        database_url = get_database_url()
        if not database_url:
            raise ValueError("AUTOMAGIK_SPARK_DATABASE_URL environment variable is not set")

        # Only enforce PostgreSQL check in non-testing environments
        if os.getenv('ENVIRONMENT') != 'testing':
            if not database_url.startswith('postgresql+asyncpg://'):
                if database_url.startswith('postgresql://'):
                    database_url = f"postgresql+asyncpg://{database_url.split('://', 1)[1]}"
                else:
                    raise ValueError("AUTOMAGIK_SPARK_DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'")

        # Debug: Log what URL we're actually using
        env = os.getenv('ENVIRONMENT', 'unknown')
        logger.info(f"[LAZY INIT] Environment: {env}, Using database URL: {database_url}")
        _database_url = database_url
    return _database_url

def get_async_engine_lazy():
    """Get the async database engine, creating it on first access."""
    global _async_engine, _sync_engine, _async_session_factory, _sync_session_factory
    
    if _async_engine is None:
        with _engine_lock:
            if _async_engine is None:  # Double-check locking pattern
                database_url = get_database_url_runtime()
                env = os.getenv('ENVIRONMENT', 'unknown')
                
                logger.info(f"[LAZY ENGINE] Creating engines - Environment: {env}, URL: {database_url}")
                
                if env == 'testing' and 'sqlite' in database_url.lower():
                    # SQLite-specific configuration for testing
                    from sqlalchemy.pool import StaticPool
                    
                    logger.info("[LAZY ENGINE] Using SQLite configuration for testing")
                    _async_engine = create_async_engine(
                        database_url,
                        echo=False,
                        future=True,
                        connect_args={"check_same_thread": False},
                        poolclass=StaticPool,
                    )
                    
                    # Create sync engine for CLI commands (convert aiosqlite to sqlite)
                    sync_database_url = database_url.replace('sqlite+aiosqlite://', 'sqlite://')
                    _sync_engine = create_engine(
                        sync_database_url,
                        echo=False,
                        future=True,
                        connect_args={"check_same_thread": False},
                        poolclass=StaticPool,
                    )
                else:
                    # PostgreSQL configuration for production
                    logger.info("[LAZY ENGINE] Using PostgreSQL configuration for production")
                    _async_engine = create_async_engine(
                        database_url,
                        echo=False,
                        future=True
                    )

                    # Create sync engine for CLI commands
                    _sync_engine = create_engine(
                        database_url.replace('postgresql+asyncpg://', 'postgresql://'),
                        echo=False,
                        future=True
                    )

                # Create session factories
                _async_session_factory = async_sessionmaker(
                    _async_engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                )

                _sync_session_factory = sessionmaker(
                    _sync_engine,
                    expire_on_commit=False
                )
                
                logger.info(f"[LAZY ENGINE] Created engines successfully. Async engine URL: {_async_engine.url}")
    
    return _async_engine

def get_sync_engine_lazy():
    """Get the sync database engine, creating it on first access."""
    get_async_engine_lazy()  # This creates both engines
    return _sync_engine

def get_async_session_factory_lazy():
    """Get the async session factory, creating it on first access."""
    get_async_engine_lazy()  # This creates both engines and session factories
    return _async_session_factory

def get_sync_session_factory_lazy():
    """Get the sync session factory, creating it on first access."""
    get_async_engine_lazy()  # This creates both engines and session factories  
    return _sync_session_factory

# For backward compatibility, we need to expose engines and session factories
# But we can't call the lazy functions at module level (that defeats the purpose)
# Instead, we'll replace any usage of these variables in this module with function calls

# For maximum backward compatibility with migrations and CLI that expect DATABASE_URL to be a string,
# we need to create a special object that acts like both a string and can be called as a function.

class _LazyString:
    """A string-like object that evaluates lazily."""
    def __init__(self, func):
        self._func = func
        self._cached_value = None
    
    def __str__(self):
        if self._cached_value is None:
            self._cached_value = self._func()
        return self._cached_value
    
    def __call__(self):
        return str(self)
    
    # String methods for backward compatibility
    def split(self, *args, **kwargs):
        return str(self).split(*args, **kwargs)
    
    def replace(self, *args, **kwargs):
        return str(self).replace(*args, **kwargs)
        
    def startswith(self, *args, **kwargs):
        return str(self).startswith(*args, **kwargs)
    
    def lower(self):
        return str(self).lower()

# Create lazy versions of the module-level variables for backward compatibility
DATABASE_URL = _LazyString(get_database_url_runtime)
async_engine = get_async_engine_lazy  
sync_engine = get_sync_engine_lazy
async_session_factory = get_async_session_factory_lazy
sync_session = get_sync_session_factory_lazy

# Expose async_session alias for backward compatibility with tests
async_session = get_async_session_factory_lazy

@asynccontextmanager
async def get_session() -> AsyncSession:
    """Get a database session.
    
    This function creates a new session for each request and ensures proper cleanup.
    It should be used with an async context manager:
    
    async with get_session() as session:
        # use session here
    """
    session_factory = get_async_session_factory_lazy()
    session = session_factory()
    try:
        yield session
    finally:
        await session.close()

@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    """Get a sync database session for CLI commands."""
    session_factory = get_sync_session_factory_lazy()
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_engine():
    """Get the database engine."""
    return get_async_engine_lazy()

async def get_async_session():
    """FastAPI dependency for getting a database session."""
    async with get_session() as session:
        yield session


