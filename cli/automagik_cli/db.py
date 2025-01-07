import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from .models import Base

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Get a new database session."""
    init_db()  # Ensure tables exist
    return SessionLocal()