"""
Database Session Management Module

This module handles database connection and session management.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .base import Base
import logging
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add console handler if not already present
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Get database URL from environment or use default
database_url = os.getenv('DATABASE_URL')
logger.debug(f"Raw DATABASE_URL from environment: {database_url}")

if database_url and ('postgresql://' in database_url or 'postgresql+psycopg2://' in database_url):
    # Convert to asyncpg URL
    db_url = database_url.replace('postgresql://', 'postgresql+asyncpg://')
    db_url = db_url.replace('postgresql+psycopg2://', 'postgresql+asyncpg://')
    logger.info(f"Using PostgreSQL database ")
else:
    # Default to SQLite if no PostgreSQL URL is provided
    db_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(db_dir, 'automagik.db')
    
    # Ensure database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Create database URL with absolute path
    db_url = f'sqlite+aiosqlite:///{os.path.abspath(db_path)}'
    logger.warning(f"No valid PostgreSQL URL found in DATABASE_URL environment variable. Falling back to SQLite at {db_path}")

# Create async engine with echo for debugging
engine = create_async_engine(
    db_url,
    echo=os.getenv('AUTOMAGIK_DEBUG') == '1',
    future=True
)

# Create async session factory
Session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    """
    Create and return a new database session.
    
    The function will:
    1. Create the database directory if it doesn't exist
    2. Initialize the database if it's not already initialized
    3. Create and return a new session
    
    Returns:
        SQLAlchemy AsyncSession object
    """
    try:
        # Create all tables if they don't exist
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Create and return new session
        session = Session()
        return session
        
    except Exception as e:
        logger.error(f"Error creating database session: {e}")
        raise
