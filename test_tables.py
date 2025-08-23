#!/usr/bin/env python3

import asyncio
import os

# Set up test environment exactly like conftest.py
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

# Import using the NEW method (what I changed in conftest.py)
from automagik_spark.core.database.base import Base
import automagik_spark.core.database.models  # noqa: F401

async def test_table_creation():
    """Test if tables are created properly."""
    
    print("=== Testing Table Creation ===")
    print(f"Base: {Base}")
    print(f"Available tables in metadata: {list(Base.metadata.tables.keys())}")
    
    if 'workflow_sources' in Base.metadata.tables:
        print("✅ workflow_sources found in metadata!")
    else:
        print("❌ workflow_sources NOT found in metadata!")
        return
    
    # Create engine exactly like the test
    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,  # Enable SQL logging to see what's created
    )
    
    # Create all tables
    print("\n=== Creating Tables ===")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!")
        
        # Verify tables exist in database
        print("\n=== Verifying Tables in Database ===")
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
            print(f"Tables in database: {tables}")
            
            if 'workflow_sources' in tables:
                print("✅ workflow_sources table exists in database!")
            else:
                print("❌ workflow_sources table NOT found in database!")
                
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    from sqlalchemy import text
    asyncio.run(test_table_creation())