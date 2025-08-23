#!/usr/bin/env python3
"""
Test script to validate database isolation with Mock Engine Replacement.
Simulates the problematic test scenario to verify the fix works.

Usage: uv run python test_database_isolation.py
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set test environment
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888" 
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

async def simulate_test_isolation():
    """Simulate the test isolation scenario that was failing."""
    
    print("🧪 Simulating Database Isolation Test")
    print("=" * 50)
    
    try:
        # Import after setting environment (like conftest.py does)
        from automagik_spark.core.database.models import Base, WorkflowSource
        from automagik_spark.core.database import session as db_session
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from sqlalchemy.pool import StaticPool
        
        print("1. Creating test engine (simulating conftest.py engine fixture)...")
        
        # Create test engine like the conftest.py engine fixture
        TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
        test_engine = create_async_engine(
            TEST_DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False,
        )
        
        # Create all tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        print("   ✅ Test engine created successfully")
        
        # Create test session factory
        test_session_factory = async_sessionmaker(
            bind=test_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        print("   ✅ Test session factory created")
        
        print("\n2. Simulating monkeypatch of global components...")
        
        # Store original values
        original_async_engine = db_session.async_engine
        original_async_session_factory = db_session.async_session_factory
        original_async_session = db_session.async_session
        
        # Apply monkeypatch (simulating what the fixture does)
        db_session.async_engine = test_engine
        db_session.async_session_factory = test_session_factory
        db_session.async_session = test_session_factory
        
        print("   ✅ Global components monkeypatched")
        
        print("\n3. Testing first workflow source creation (like first test)...")
        
        # Test 1: Create first source (simulates test_create_langflow_source_success)
        async with db_session.async_session_factory() as session:
            source1 = WorkflowSource(
                name="LangFlow Test Source 1",
                base_url="http://localhost:17860",
                source_type="langflow",
                version_info={"version": "1.0.0"}
            )
            session.add(source1)
            await session.commit()
            await session.refresh(source1)
            
            print(f"   ✅ First source created with ID: {source1.id}")
            first_source_id = source1.id
            
        print("\n4. Testing second workflow source creation (like second test)...")
        
        # Test 2: Create second source (simulates test_create_automagik_agents_source_success)
        async with db_session.async_session_factory() as session:
            source2 = WorkflowSource(
                name="AutoMagik Agents Test Source",
                base_url="http://localhost:8000", 
                source_type="automagik_agents",
                version_info={"version": "1.0.0"}
            )
            session.add(source2)
            await session.commit()
            await session.refresh(source2)
            
            print(f"   ✅ Second source created with ID: {source2.id}")
            second_source_id = source2.id
            
        print("\n5. Verifying both sources exist independently...")
        
        # Verify both sources exist and are different
        async with db_session.async_session_factory() as session:
            from sqlalchemy import text
            all_sources = await session.execute(
                text("SELECT id, name, base_url, source_type FROM workflow_sources")
            )
            sources = all_sources.fetchall()
            
            print(f"   📊 Total sources in database: {len(sources)}")
            for source in sources:
                print(f"      - ID: {source.id}, Name: {source.name}, Type: {source.source_type}")
                
            if len(sources) == 2:
                print("   ✅ Both sources exist independently - no isolation issues!")
            else:
                print(f"   ❌ Expected 2 sources, found {len(sources)}")
                return False
                
        print("\n6. Testing database cleanup (simulating test teardown)...")
        
        # Simulate the cleanup that conftest.py session fixture does
        async with db_session.async_session_factory() as session:
            from sqlalchemy import text
            
            # Clean up tables in FK order (like conftest.py does)
            cleanup_tables = [
                "task_logs", "tasks", "workflow_components", 
                "workers", "schedules", "workflows", "workflow_sources"
            ]
            
            for table in cleanup_tables:
                try:
                    await session.execute(text(f"DELETE FROM {table}"))
                except Exception as e:
                    # Some tables might not exist, that's OK
                    pass
                    
            await session.commit()
            print("   ✅ Database cleanup completed")
            
        # Verify cleanup
        async with db_session.async_session_factory() as session:
            remaining = await session.execute(text("SELECT COUNT(*) FROM workflow_sources"))
            count = remaining.scalar()
            
            if count == 0:
                print("   ✅ All sources cleaned up successfully")
            else:
                print(f"   ⚠️  Warning: {count} sources remain after cleanup")
                
        print("\n7. Restoring original global components...")
        
        # Restore original values (cleanup)
        db_session.async_engine = original_async_engine
        db_session.async_session_factory = original_async_session_factory  
        db_session.async_session = original_async_session
        
        # Dispose test engine
        await test_engine.dispose()
        
        print("   ✅ Original components restored")
        
        print("\n🎉 Database isolation simulation completed successfully!")
        print("The Mock Engine Replacement approach should fix the failing tests.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Simulation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    success = await simulate_test_isolation()
    
    if success:
        print("\n✅ VALIDATION SUCCESSFUL!")
        print("The Mock Engine Replacement implementation should resolve the database isolation issues.")
        print("\nNext steps:")
        print("1. Run the actual failing tests to verify the fix")
        print("2. Consider running: uv run pytest tests/api/test_sources.py::TestSourcesCreate::test_create_langflow_source_success tests/api/test_sources.py::TestSourcesCreate::test_create_automagik_agents_source_success -v")
        return 0
    else:
        print("\n❌ VALIDATION FAILED!")
        print("Please review the implementation and fix any issues.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)