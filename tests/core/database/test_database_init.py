
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from automagik_spark.core.database.models import Base


@pytest.mark.asyncio
async def test_database_tables_exist(session: AsyncSession):
    """Test that all required database tables exist."""
    # Get all table names from our models
    model_tables = {table for table in Base.metadata.tables.keys()}
    
    # Get actual tables in the database using SQLite's sqlite_master table
    async with session.begin():
        result = await session.execute(text(
            """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """
        ))
        actual_tables = {row[0] for row in result}
    
    # Check if all required tables exist
    missing_tables = model_tables - actual_tables
    assert not missing_tables, f"Missing tables in database: {missing_tables}"
    
    # Specifically check for critical tables
    critical_tables = {"workflows", "tasks", "schedules", "task_logs"}
    missing_critical = critical_tables - actual_tables
    assert not missing_critical, f"Missing critical tables: {missing_critical}"
    
    # Test that we can query these tables
    async with session.begin():
        for table in critical_tables:
            try:
                await session.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
            except Exception as e:
                pytest.fail(f"Failed to query table {table}: {str(e)}")


