"""
Database Session Management Module

This module handles database connection and session management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment or use default
database_url = os.getenv('DATABASE_URL')

if database_url and database_url.startswith('postgresql'):
    # Use the provided PostgreSQL URL
    db_url = database_url
else:
    # Default to SQLite if no PostgreSQL URL is provided
    db_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(db_dir, 'automagik.db')
    
    # Ensure database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Create database URL with absolute path
    db_url = f'sqlite:///{os.path.abspath(db_path)}'

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
        Base.metadata.create_all(engine)
        
        # Create session factory
        Session = sessionmaker(bind=engine)
        
        # Create and return new session
        return Session()
        
    except Exception as e:
        logger.error(f"Error creating database session: {str(e)}")
        raise
