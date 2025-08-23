#!/usr/bin/env python3
"""Test the final database isolation fix."""

import os
import sys
import asyncio

# Critical: Set environment variables BEFORE any imports
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

async def test_fix():
    print("=== FINAL FIX TEST ===")
    print(f"Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Database URL: {os.getenv('AUTOMAGIK_SPARK_DATABASE_URL')}")
    
    # Test 1: Import session module (should use lazy initialization)
    print("\n1. Testing session module import...")
    from automagik_spark.core.database import session as db_session
    
    # This should trigger lazy initialization with SQLite
    engine = db_session.async_engine()
    print(f"   Engine URL: {engine.url}")
    
    if "sqlite" not in str(engine.url):
        print(f"   ❌ FAIL: Engine using {engine.url}, expected SQLite")
        return False
    print("   ✅ PASS: Engine using SQLite")
    
    # Test 2: Import app (this was the problematic chain)
    print("\n2. Testing app import chain...")
    from automagik_spark.api.app import app
    print("   App imported successfully")
    
    # Verify engine is still SQLite
    engine2 = db_session.async_engine()
    if str(engine.url) != str(engine2.url):
        print(f"   ❌ FAIL: Engine changed from {engine.url} to {engine2.url}")
        return False
    print("   ✅ PASS: Engine URL consistent after app import")
    
    # Test 3: Test the session functionality
    print("\n3. Testing session functionality...")
    async with db_session.get_session() as session:
        # Simple query to verify it's working
        result = await session.execute("SELECT 1 as test")
        row = result.fetchone()
        if row[0] != 1:
            print("   ❌ FAIL: Database query failed")
            return False
        print("   ✅ PASS: Database session working")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Database isolation fix should now work correctly!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_fix())
    sys.exit(0 if success else 1)