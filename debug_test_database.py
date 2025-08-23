#!/usr/bin/env python3
"""Debug test database file creation and sharing."""

import asyncio
import os
import tempfile
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Create the same temporary SQLite file as conftest.py
_test_db_fd, _test_db_path = tempfile.mkstemp(suffix='.db', prefix='test_automagik_')
os.close(_test_db_fd)

# Set environment like conftest.py
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = f"sqlite+aiosqlite:///{_test_db_path}"

print(f"Test database file: {_test_db_path}")

async def simulate_test_flow():
    from automagik_spark.core.database.base import Base
    import automagik_spark.core.database.models  # noqa: F401
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.pool import StaticPool
    from sqlalchemy import text
    
    # Step 1: Create engine like the `engine` fixture
    print("\n=== Step 1: Create engine (like engine fixture) ===")
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{_test_db_path}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    # Create tables like the engine fixture
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print(f"Engine created with URL: {engine.url}")
    
    # Verify tables exist
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables created: {tables}")
    
    # Step 2: Create session factory like the `test_session_factory` fixture
    print("\n=== Step 2: Create session factory (like test_session_factory fixture) ===")
    test_session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    print("Session factory created")
    
    # Step 3: Create session like the `session` fixture
    print("\n=== Step 3: Create session (like session fixture) ===")
    async with test_session_factory() as session:
        # Try to query a table
        try:
            result = await session.execute(text("SELECT COUNT(*) FROM workflow_sources"))
            count = result.scalar()
            print(f"Successfully queried workflow_sources table, count: {count}")
        except Exception as e:
            print(f"ERROR querying workflow_sources: {e}")
        
        # Step 4: Simulate the dependency override
        print("\n=== Step 4: Simulate dependency override ===")
        
        # This is what override_get_session does
        async def _get_session():
            yield session
            
        print("Dependency override function created")
        
        # Test if the session can be used for queries like the API would
        async with _get_session() as api_session:
            try:
                # This simulates the query in the API
                query = text("SELECT * FROM workflow_sources WHERE url = :url")
                result = await api_session.execute(query, {"url": "http://localhost:7860"})
                rows = result.fetchall()
                print(f"API-style query successful, found {len(rows)} rows")
            except Exception as e:
                print(f"ERROR in API-style query: {e}")
    
    await engine.dispose()
    
    # Clean up
    try:
        if os.path.exists(_test_db_path):
            os.unlink(_test_db_path)
    except Exception as e:
        print(f"Error cleaning up: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_test_flow())