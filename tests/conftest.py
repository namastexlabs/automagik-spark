
"""Test configuration and fixtures."""

import os
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from automagik_spark.core.workflows import WorkflowManager  # Fix import path

# Use temporary file SQLite for testing to enable sharing between engines
import tempfile
import os
_test_db_fd, _test_db_path = tempfile.mkstemp(suffix='.db', prefix='test_automagik_')
os.close(_test_db_fd)  # Close file descriptor but keep the path
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{_test_db_path}"

# Test API key
TEST_API_KEY = "namastex888"

# Set up test environment variables
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = TEST_API_KEY
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = TEST_DATABASE_URL  # Override database URL

# Now load the models after setting up the environment  
from automagik_spark.core.database.base import Base
# Import models to register them with Base.metadata
import automagik_spark.core.database.models  # noqa: F401
from automagik_spark.api.dependencies import get_async_session

# Import the session module for monkeypatching global components
import automagik_spark.core.database.session as db_session

# DO NOT import app at module level - this will be imported in fixtures after monkeypatch is applied

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up test environment."""
    yield
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("AUTOMAGIK_SPARK_API_KEY", None)
    os.environ.pop("AUTOMAGIK_SPARK_DATABASE_URL", None)
    # Cleanup temporary database file
    try:
        if os.path.exists(_test_db_path):
            os.unlink(_test_db_path)
    except Exception:
        pass

# Configure pytest-asyncio to use session scope for event loop
pytest.mark.asyncio.loop_scope = "session"

@pytest.fixture(scope="function")
async def engine():
    """Create a test database engine with function scope for better isolation."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,  # Disable SQL logging to reduce test noise
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    try:
        yield engine
    finally:
        # Ensure complete cleanup
        try:
            await engine.dispose()
        except Exception:
            pass

@pytest.fixture(scope="function")
def test_session_factory(engine):
    """Create a test session factory with function scope for better isolation."""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

@pytest.fixture(scope="function")
def monkeypatch_db_globals(monkeypatch, engine, test_session_factory):
    """
    Monkeypatch the global async and sync engines and session factories
    in automagik_spark.core.database.session to use test SQLite versions.
    This ensures any code that directly imports these globals uses the test database.
    """
    from sqlalchemy import create_engine as create_sync_engine_
    from sqlalchemy.orm import sessionmaker as sync_sessionmaker_
    from sqlalchemy.pool import StaticPool as SyncStaticPool

    # Create a sync engine for testing purposes, adapting the URL for sync SQLite
    # Convert async SQLite URL to sync SQLite URL
    test_sync_database_url = TEST_DATABASE_URL.replace('sqlite+aiosqlite://', 'sqlite://')
    test_sync_engine = create_sync_engine_(
        test_sync_database_url,
        connect_args={"check_same_thread": False},
        poolclass=SyncStaticPool,
        echo=False
    )
    
    # Create tables in the sync engine (since it's a separate database from the async one)
    # IMPORTANT: Both engines now point to the same file-based SQLite, so tables are shared
    Base.metadata.create_all(test_sync_engine)

    # Create a sync session factory for testing purposes
    test_sync_session_factory = sync_sessionmaker_(
        bind=test_sync_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    # DEBUG: Add logging to verify monkeypatch is working
    def debug_get_async_engine_lazy():
        print(f"[MONKEYPATCH] get_async_engine_lazy called, returning engine: {engine.url}")
        return engine
    
    def debug_get_database_url_runtime():
        print(f"[MONKEYPATCH] get_database_url_runtime called, returning: {TEST_DATABASE_URL}")
        return TEST_DATABASE_URL
    
    # CRITICAL: Clear any cached engines and factories first
    # This ensures that the lazy initialization system starts fresh
    db_session._async_engine = None
    db_session._sync_engine = None
    db_session._async_session_factory = None
    db_session._sync_session_factory = None
    db_session._database_url = None
    
    print(f"[MONKEYPATCH] Cleared cached engines and factories")
    
    # Patch the lazy functions to return test components instead of production ones
    monkeypatch.setattr(db_session, "get_async_engine_lazy", debug_get_async_engine_lazy)
    monkeypatch.setattr(db_session, "get_sync_engine_lazy", lambda: test_sync_engine) 
    monkeypatch.setattr(db_session, "get_async_session_factory_lazy", lambda: test_session_factory)
    monkeypatch.setattr(db_session, "get_sync_session_factory_lazy", lambda: test_sync_session_factory)
    monkeypatch.setattr(db_session, "get_database_url_runtime", debug_get_database_url_runtime)

    # IMPORTANT: Module-level attributes are now FUNCTIONS in the lazy system
    # So we need to patch them to return our test objects, not be the objects
    monkeypatch.setattr(db_session, "async_engine", lambda: engine)
    monkeypatch.setattr(db_session, "sync_engine", lambda: test_sync_engine)
    monkeypatch.setattr(db_session, "async_session_factory", lambda: test_session_factory)
    monkeypatch.setattr(db_session, "sync_session", lambda: test_sync_session_factory)
    monkeypatch.setattr(db_session, "async_session", lambda: test_session_factory)
    
    # Patch DATABASE_URL (which is now a _LazyString) to return test URL
    monkeypatch.setattr(db_session.DATABASE_URL, '_func', lambda: TEST_DATABASE_URL)
    monkeypatch.setattr(db_session.DATABASE_URL, '_cached_value', None)  # Clear cache to force re-evaluation
    
    # Also patch the get_engine function if it's used directly
    monkeypatch.setattr(db_session, "get_engine", lambda: engine)

    yield

    # Dispose of the test sync engine after the test
    test_sync_engine.dispose()

@pytest.fixture
async def session(test_session_factory, monkeypatch_db_globals) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session with table cleanup.
    
    This fixture provides a database session and ensures all tables
    are cleaned after each test for proper test isolation.
    """
    async with test_session_factory() as session:
        try:
            yield session
        finally:
            # Clean up all tables after each test in reverse dependency order
            # This ensures foreign key constraints are respected during cleanup
            try:
                # Delete dependent tables first (those with foreign keys)
                await session.execute(text("DELETE FROM task_logs"))
                await session.execute(text("DELETE FROM tasks"))
                await session.execute(text("DELETE FROM workflow_components"))
                await session.execute(text("DELETE FROM workers"))
                await session.execute(text("DELETE FROM schedules"))
                await session.execute(text("DELETE FROM workflows"))
                # Delete parent table last
                await session.execute(text("DELETE FROM workflow_sources"))
                await session.commit()
            except Exception as e:
                # If cleanup fails, rollback and try to close cleanly
                await session.rollback()
                print(f"Warning: Database cleanup failed: {e}")
            finally:
                await session.close()

@pytest.fixture
async def override_get_session(engine, test_session_factory, monkeypatch_db_globals):
    """Override the get_session dependency."""
    # Import app AFTER monkeypatch is applied
    from automagik_spark.api.app import app
    
    async def _get_session() -> AsyncGenerator[AsyncSession, None]:
        # Create a fresh session from the test engine (which has tables)
        async with test_session_factory() as session:
            print(f"[OVERRIDE] Created session from engine: {engine.url}")
            yield session
    
    app.dependency_overrides[get_async_session] = _get_session
    yield
    del app.dependency_overrides[get_async_session]

@pytest.fixture
async def client(engine, monkeypatch_db_globals, override_get_session) -> AsyncGenerator[TestClient, None]:
    """Create a test client with an overridden database session."""
    # Import app AFTER monkeypatch is applied to ensure test database is used
    from automagik_spark.api.app import app
    with TestClient(app) as client:
        yield client

@pytest.fixture
async def workflow_manager(session, monkeypatch_db_globals):
    """Create a workflow manager for testing."""
    async with WorkflowManager(session) as manager:
        yield manager

@pytest.fixture
def mock_httpx_client(mocker):
    """Mock httpx client."""
    mock_client = mocker.AsyncMock()
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    return mock_client


