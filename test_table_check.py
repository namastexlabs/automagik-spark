#!/usr/bin/env python3
"""Check if tables exist in the test database"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set test environment
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

async def check_tables():
    # Import after env setup (like in real tests)
    from automagik_spark.core.database import session as db_session
    
    # Since async_engine is now a function, we need to call it
    engine = db_session.async_engine()
    print(f"Engine URL: {engine.url}")
    
    # Check if tables exist
    async with engine.begin() as conn:
        # Try to query table names
        try:
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
            print(f"Tables in database: {tables}")
            print(f"workflow_sources table exists: {'workflow_sources' in tables}")
            return 'workflow_sources' in tables
        except Exception as e:
            print(f"Error checking tables: {e}")
            return False

if __name__ == "__main__":
    from sqlalchemy import text
    result = asyncio.run(check_tables())
    print(f"Table check result: {result}")