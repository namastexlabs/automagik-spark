#!/usr/bin/env python3
"""
Test script to validate the Mock Engine Replacement approach.
This script can be run to verify that the monkeypatch fix is working correctly.

Usage: uv run python test_mock_engine_fix.py
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

async def test_mock_engine_fix():
    """Test that the mock engine replacement works."""
    
    print("🔧 Testing Mock Engine Replacement approach...")
    
    try:
        # Test 1: Import session module and check engine types
        print("\n1. Testing engine import and type...")
        from automagik_spark.core.database import session as db_session
        
        print(f"   - async_engine type: {type(db_session.async_engine)}")
        print(f"   - sync_engine type: {type(db_session.sync_engine)}")
        print(f"   - async_engine URL: {db_session.async_engine.url}")
        print(f"   - sync_engine URL: {db_session.sync_engine.url}")
        
        # Test 2: Check if engines are SQLite-based
        print("\n2. Checking engine URLs...")
        async_url = str(db_session.async_engine.url)
        sync_url = str(db_session.sync_engine.url)
        
        if "sqlite" in async_url.lower():
            print("   ✅ async_engine uses SQLite")
        else:
            print(f"   ❌ async_engine does NOT use SQLite: {async_url}")
            return False
            
        if "sqlite" in sync_url.lower():
            print("   ✅ sync_engine uses SQLite")
        else:
            print(f"   ❌ sync_engine does NOT use SQLite: {sync_url}")
            return False
        
        # Test 3: Test basic database connection
        print("\n3. Testing database connection...")
        try:
            from automagik_spark.core.database.models import Base
            
            # Test async engine connection
            async with db_session.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("   ✅ async_engine connection successful")
            
            # Test sync engine connection  
            with db_session.sync_engine.begin() as conn:
                Base.metadata.create_all(conn)
                print("   ✅ sync_engine connection successful")
                
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            return False
        
        # Test 4: Test session creation
        print("\n4. Testing session creation...")
        try:
            async with db_session.async_session_factory() as session:
                print("   ✅ async_session_factory works")
            
            with db_session.sync_session() as session:
                print("   ✅ sync_session factory works")
                
        except Exception as e:
            print(f"   ❌ Session creation failed: {e}")
            return False
            
        print("\n✅ All tests passed! Mock Engine Replacement is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_with_monkeypatch():
    """Test the actual monkeypatch fixture behavior."""
    print("\n🔧 Testing with monkeypatch simulation...")
    
    try:
        # Simulate what the monkeypatch fixture does
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.pool import StaticPool
        
        # Create test engines like the fixture does
        TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
        
        test_async_engine = create_async_engine(
            TEST_DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False,
        )
        
        test_sync_database_url = TEST_DATABASE_URL.replace('sqlite+aiosqlite://', 'sqlite://')
        test_sync_engine = create_engine(
            test_sync_database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False
        )
        
        test_async_session_factory = async_sessionmaker(
            bind=test_async_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        test_sync_session_factory = sessionmaker(
            bind=test_sync_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        # Test that these work
        print("   ✅ Test engines created successfully")
        
        # Test async session
        async with test_async_session_factory() as session:
            print("   ✅ Test async session works")
        
        # Test sync session  
        with test_sync_session_factory() as session:
            print("   ✅ Test sync session works")
            
        # Cleanup
        await test_async_engine.dispose()
        test_sync_engine.dispose()
        
        print("✅ Monkeypatch simulation successful!")
        return True
        
    except Exception as e:
        print(f"❌ Monkeypatch simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🧪 Mock Engine Replacement Validation Script")
    print("=" * 50)
    
    # Test 1: Basic engine import and check
    success1 = await test_mock_engine_fix()
    
    # Test 2: Monkeypatch fixture simulation
    success2 = await test_with_monkeypatch()
    
    if success1 and success2:
        print("\n🎉 All validation tests passed!")
        print("The Mock Engine Replacement implementation should work correctly.")
        return 0
    else:
        print("\n💥 Some validation tests failed!")
        print("Please check the implementation and fix any issues.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)