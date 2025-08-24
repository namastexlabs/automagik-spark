
"""Test configuration and fixtures."""

import os
import pytest
import tempfile
import atexit
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Use a fixed path for the test database to avoid multiple database files
_test_db_path = "/tmp/test_automagik_spark.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{_test_db_path}"
TEST_SYNC_DATABASE_URL = f"sqlite:///{_test_db_path}"

# Test API key
TEST_API_KEY = "namastex888"

# Set up test environment variables FIRST
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = TEST_DATABASE_URL

# Now import models and database components
from automagik_spark.core.database.base import Base
import automagik_spark.core.database.models  # noqa: F401
from automagik_spark.api.dependencies import get_async_session
from automagik_spark.core.workflows import WorkflowManager

# Clear any cached database values from the lazy loading system
import automagik_spark.core.database.session as db_session
db_session._async_engine = None
db_session._sync_engine = None
db_session._async_session_factory = None
db_session._sync_session_factory = None  
db_session._database_url = None

# Cleanup function to remove test database
def cleanup_test_db():
    try:
        if os.path.exists(_test_db_path):
            os.unlink(_test_db_path)
    except Exception:
        pass

atexit.register(cleanup_test_db)

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up test environment."""
    yield
    cleanup_test_db()

# Configure pytest-asyncio to use session scope for event loop
pytest.mark.asyncio.loop_scope = "session"

@pytest.fixture(scope="session")
async def test_engine():
    """Create a single test database engine for the entire test session."""
    # Clean up any existing test database
    if os.path.exists(_test_db_path):
        os.unlink(_test_db_path)
    
    # Create async engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    # Create all tables ONCE at the start of the test session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Verify tables were created
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = result.fetchall()
        print(f"[TEST ENGINE] Created tables: {[table[0] for table in tables]}")
        assert len(tables) > 0, "No tables were created in test database!"
    
    yield engine
    
    # Cleanup
    await engine.dispose()
    if os.path.exists(_test_db_path):
        os.unlink(_test_db_path)

@pytest.fixture(scope="session")
def test_sync_engine():
    """Create a sync engine that uses the same database file."""
    engine = create_engine(
        TEST_SYNC_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    # Tables are already created by the async engine since they share the same file
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
async def session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh session for each test with proper cleanup."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with session_factory() as session:
        try:
            yield session
        finally:
            # Clean up all tables after each test
            try:
                await session.execute(text("DELETE FROM task_logs"))
                await session.execute(text("DELETE FROM tasks"))
                await session.execute(text("DELETE FROM workflow_components"))
                await session.execute(text("DELETE FROM workers"))
                await session.execute(text("DELETE FROM schedules"))
                await session.execute(text("DELETE FROM workflows"))
                await session.execute(text("DELETE FROM workflow_sources"))
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Warning: Database cleanup failed: {e}")
            finally:
                await session.close()

@pytest.fixture
async def client(test_engine) -> AsyncGenerator[TestClient, None]:
    """Create a test client with an overridden database session."""
    from automagik_spark.api.app import app
    
    # Force clear any cached values before setting up test
    import automagik_spark.core.database.session as db_session
    db_session._async_engine = None
    db_session._sync_engine = None
    db_session._async_session_factory = None
    db_session._sync_session_factory = None  
    db_session._database_url = None
    
    # Clear the lazy string cache too
    if hasattr(db_session.DATABASE_URL, '_cached_value'):
        db_session.DATABASE_URL._cached_value = None
    
    # Override both the dependency and the lazy loading functions
    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        session_factory = async_sessionmaker(
            bind=test_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with session_factory() as session:
            yield session
    
    # Monkey patch the lazy loading functions to return our test engine
    original_get_async_engine_lazy = db_session.get_async_engine_lazy
    original_get_database_url_runtime = db_session.get_database_url_runtime
    
    def mock_get_async_engine_lazy():
        return test_engine
        
    def mock_get_database_url_runtime():
        return TEST_DATABASE_URL
    
    db_session.get_async_engine_lazy = mock_get_async_engine_lazy
    db_session.get_database_url_runtime = mock_get_database_url_runtime
    
    app.dependency_overrides[get_async_session] = _get_test_session
    
    try:
        with TestClient(app) as client:
            yield client
    finally:
        # Clean up the dependency override and monkeypatch
        if get_async_session in app.dependency_overrides:
            del app.dependency_overrides[get_async_session]
        db_session.get_async_engine_lazy = original_get_async_engine_lazy
        db_session.get_database_url_runtime = original_get_database_url_runtime

@pytest.fixture
async def workflow_manager(session):
    """Create a workflow manager for testing."""
    async with WorkflowManager(session) as manager:
        yield manager

@pytest.fixture
def mock_httpx_client(mocker):
    """Mock httpx client."""
    mock_client = mocker.AsyncMock()
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    return mock_client


