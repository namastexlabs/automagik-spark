#!/usr/bin/env python3

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to Python path to find sync_flows
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.base import Base
from agents.models import Agent
from sync_flows.models import FlowDB

def init_db():
    """Initialize database tables."""
    load_dotenv()
    
    engine = create_engine(os.getenv("DATABASE_URL"))
    
    # Drop tables using raw SQL to avoid dependency issues
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS agents CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS flows CASCADE"))
        conn.commit()
    
    # Create all tables at once using shared Base
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
