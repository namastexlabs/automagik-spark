"""Test configuration and fixtures."""

import os
import asyncio
import pytest
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager

from automagik.core.database.models import Base
from automagik.api.app import app
from automagik.api.dependencies import get_session, get_async_session
from automagik.core.database.session import async_session as production_session

# Use in-memory SQLite for testing with a shared connection
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test API key
TEST_API_KEY = "mock-api-key-12345"

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up test environment."""
    os.environ["AUTOMAGIK_ENV"] = "testing"
    os.environ["AUTOMAGIK_API_KEY"] = TEST_API_KEY
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL  # Override database URL
    yield
    os.environ.pop("AUTOMAGIK_ENV", None)
    os.environ.pop("AUTOMAGIK_API_KEY", None)
    os.environ.pop("DATABASE_URL", None)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
        echo=True  # Enable SQL logging for debugging
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

@pytest.fixture(scope="session")
async def test_session_factory(engine):
    """Create a test session factory."""
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

@pytest.fixture
async def session(test_session_factory) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with test_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture
async def override_get_session(session):
    """Override the get_session dependency."""
    async def _get_session():
        yield session

    return _get_session

@pytest.fixture
async def client(override_get_session) -> AsyncGenerator[TestClient, None]:
    """Create a test client with an overridden database session."""
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_async_session] = override_get_session
    
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
