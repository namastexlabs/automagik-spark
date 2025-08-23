#!/usr/bin/env python3
"""Debug lazy initialization vs fixture engine creation."""

import asyncio
import os
import tempfile
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Create a temporary SQLite file just like conftest.py does
_test_db_fd, _test_db_path = tempfile.mkstemp(suffix='.db', prefix='test_automagik_')
os.close(_test_db_fd)  # Close file descriptor but keep the path

# Set test environment exactly like conftest.py
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = f"sqlite+aiosqlite:///{_test_db_path}"

print(f"Test database path: {_test_db_path}")
print(f"Test database URL: {os.environ['AUTOMAGIK_SPARK_DATABASE_URL']}")

async def test_lazy_vs_fixture():
    # Import after env setup (like in real tests)
    from automagik_spark.core.database.base import Base
    import automagik_spark.core.database.models  # noqa: F401
    from automagik_spark.core.database import session as db_session
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import StaticPool
    from sqlalchemy import text
    
    print("\n=== Testing Lazy Initialization ===")
    # Test lazy initialization (what the monkeypatch replaces)
    lazy_engine = db_session.get_async_engine_lazy()
    print(f"Lazy engine URL: {lazy_engine.url}")
    
    # Check if lazy engine has tables
    async with lazy_engine.begin() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Lazy engine tables: {tables}")
    
    print("\n=== Testing Fixture-style Engine ===")
    # Test fixture-style engine creation (what the fixture does)
    fixture_engine = create_async_engine(
        f"sqlite+aiosqlite:///{_test_db_path}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    # Create tables like the fixture does
    async with fixture_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print(f"Fixture engine URL: {fixture_engine.url}")
    
    # Check if fixture engine has tables
    async with fixture_engine.begin() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Fixture engine tables: {tables}")
    
    print("\n=== Testing Lazy Engine After Fixture Created Tables ===")
    # Since both use the same file, lazy engine should now see the tables
    async with lazy_engine.begin() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Lazy engine tables after fixture: {tables}")
    
    # Cleanup
    await lazy_engine.dispose()
    await fixture_engine.dispose()
    
    # Clean up the test database file
    try:
        if os.path.exists(_test_db_path):
            os.unlink(_test_db_path)
    except Exception as e:
        print(f"Error cleaning up test database: {e}")

if __name__ == "__main__":
    asyncio.run(test_lazy_vs_fixture())