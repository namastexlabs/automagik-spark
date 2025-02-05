"""
Database Session Management

Provides functionality for creating and managing database sessions.
"""

import os
import logging
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)

# Get database URL from environment, ensure it uses asyncpg driver
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Only enforce PostgreSQL check in non-testing environments
if os.getenv('AUTOMAGIK_ENV') != 'testing':
    if not DATABASE_URL.startswith('postgresql+asyncpg://'):
        if DATABASE_URL.startswith('postgresql://'):
            DATABASE_URL = f"postgresql+asyncpg://{DATABASE_URL.split('://', 1)[1]}"
        else:
            raise ValueError("DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'")

logger.info(f"Using database at {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else DATABASE_URL}")

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Create sync engine for CLI commands
sync_engine = create_engine(
    DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://'),
    echo=False,
    future=True
)

# Create session factories
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

sync_session = sessionmaker(
    sync_engine,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    """Get a sync database session for CLI commands."""
    session = sync_session()
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
    return async_engine

async def get_async_session():
    """FastAPI dependency for getting a database session."""
    async with get_session() as session:
        yield session
