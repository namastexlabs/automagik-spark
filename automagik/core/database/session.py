"""
Database Session Management

Provides functionality for creating and managing database sessions.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://automagik:automagik@localhost:5432/automagik')
if not DATABASE_URL.startswith('postgresql+asyncpg://'):
    DATABASE_URL = f"postgresql+asyncpg://{DATABASE_URL.split('://', 1)[1]}"

logger.info(f"Using {DATABASE_URL.split('@')[1].split('/')[0]} database")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Create session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for getting a database session."""
    async with async_session() as session:
        yield session
