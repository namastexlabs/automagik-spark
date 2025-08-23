#!/usr/bin/env python3
"""
Simple test to verify monkeypatch is working correctly.
"""
import pytest

def test_engine_urls_after_monkeypatch(monkeypatch_db_globals):
    """Test that monkeypatch correctly patches engine URLs."""
    from automagik_spark.core.database import session as db_session
    
    print(f"async_engine URL: {db_session.async_engine.url}")
    print(f"sync_engine URL: {db_session.sync_engine.url}")
    
    async_url = str(db_session.async_engine.url)
    sync_url = str(db_session.sync_engine.url)
    
    # Both should be SQLite
    assert "sqlite" in async_url.lower(), f"async_engine should use SQLite, got: {async_url}"
    assert "sqlite" in sync_url.lower(), f"sync_engine should use SQLite, got: {sync_url}"
    
    # async should use aiosqlite, sync should use regular sqlite
    assert "sqlite+aiosqlite" in async_url.lower(), f"async_engine should use aiosqlite driver, got: {async_url}"
    assert sync_url.startswith("sqlite://"), f"sync_engine should use regular sqlite driver, got: {sync_url}"
    
    print("✅ Engine URLs are correctly monkeypatched!")

@pytest.mark.asyncio
async def test_database_isolation_works(session, monkeypatch_db_globals):
    """Test that database isolation actually works."""
    from automagik_spark.core.database.models import WorkflowSource
    
    # Create a source
    source = WorkflowSource(
        name="Test Source",
        base_url="http://localhost:1234",
        source_type="test",
        version_info={"version": "1.0.0"}
    )
    session.add(source)
    await session.commit()
    await session.refresh(source)
    
    print(f"✅ Successfully created source with ID: {source.id}")
    
    # Verify it exists
    from sqlalchemy import text
    result = await session.execute(text("SELECT COUNT(*) FROM workflow_sources"))
    count = result.scalar()
    
    assert count == 1, f"Expected 1 source, found {count}"
    print(f"✅ Database contains {count} source(s) as expected")