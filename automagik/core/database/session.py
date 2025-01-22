"""
Database Session Management Module

This module handles database connection and session management.
"""

import os
from sqlalchemy import create_engine
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
    # Use the provided PostgreSQL URL
    db_url = database_url
    logger.info(f"Using PostgreSQL database at {database_url}")
else:
    # Default to SQLite if no PostgreSQL URL is provided
    db_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(db_dir, 'automagik.db')
    
    # Ensure database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Create database URL with absolute path
    db_url = f'sqlite:///{os.path.abspath(db_path)}'
    logger.warning(f"No valid PostgreSQL URL found in DATABASE_URL environment variable. Falling back to SQLite at {db_path}")

# Create engine with echo for debugging
engine = create_engine(
    db_url,
    echo=os.getenv('AUTOMAGIK_DEBUG') == '1',
    pool_pre_ping=True  # Enable automatic reconnection
)

def get_db_session():
    """
    Create and return a new database session.
    
    The function will:
    1. Create the database directory if it doesn't exist
    2. Initialize the database if it's not already initialized
    3. Create and return a new session
    
    Returns:
        SQLAlchemy Session object
    """
    try:
        # Create all tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create and return new session
        return SessionLocal()
        
    except Exception as e:
        logger.error(f"Error creating database session: {str(e)}")
        raise
