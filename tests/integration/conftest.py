"""Configuration for integration tests."""

import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from automagik.core.database.models import Base

# Note: We're not defining event_loop fixture anymore as we're using pytest-asyncio's built-in one
# with the loop scope configured in pytest.ini

@pytest.fixture(scope="session")
async def engine():
    """Create a test database engine."""
    # Create an in-memory SQLite database for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Close the engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def session(engine):
    """Create a test database session."""
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()
        await session.close()
