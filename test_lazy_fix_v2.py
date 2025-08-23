#!/usr/bin/env python3
"""Test script to verify lazy initialization fix with DATABASE_URL compatibility."""

import os
import sys

# Set test environment BEFORE any imports
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

print("Environment variables set:")
print(f"ENVIRONMENT = {os.getenv('ENVIRONMENT')}")
print(f"AUTOMAGIK_SPARK_DATABASE_URL = {os.getenv('AUTOMAGIK_SPARK_DATABASE_URL')}")

# Test 1: Import session module
print("\nTest 1: Importing session module...")
from automagik_spark.core.database import session as db_session
print("✅ Session module imported successfully!")

# Test 2: Check DATABASE_URL compatibility
print(f"\nTest 2: DATABASE_URL compatibility")
print(f"DATABASE_URL type: {type(db_session.DATABASE_URL)}")
print(f"str(DATABASE_URL): {str(db_session.DATABASE_URL)}")

# Test string methods work
url_str = str(db_session.DATABASE_URL)
if "sqlite" in url_str:
    print("✅ DATABASE_URL string conversion works and contains 'sqlite'")
else:
    print(f"❌ DATABASE_URL doesn't contain 'sqlite': {url_str}")
    
# Test 3: Check engine creation
print(f"\nTest 3: Engine creation")
print(f"async_engine type: {type(db_session.async_engine)}")
engine = db_session.async_engine()
print(f"async_engine(): {engine}")
print(f"Engine URL: {engine.url}")

if "sqlite" in str(engine.url):
    print("✅ Engine is using SQLite (test database)")
else:
    print(f"❌ Engine is using {engine.url} instead of SQLite")
    sys.exit(1)

# Test 4: Test import chain that caused the original problem
print(f"\nTest 4: Testing import chain that caused original issue")
try:
    # Simulate the problematic import chain: test_sources.py → app.py → sources.py → session.py  
    from automagik_spark.api.app import app
    print("✅ FastAPI app imported successfully")
    
    # This would have triggered engine creation at import time before our fix
    from automagik_spark.api.routers.sources import router
    print("✅ Sources router imported successfully")
    
    # Verify that engines are still using SQLite after the import chain
    engine_after_import = db_session.async_engine()
    if "sqlite" in str(engine_after_import.url):
        print("✅ Engine still using SQLite after import chain")
    else:
        print(f"❌ Engine changed to {engine_after_import.url} after imports")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Import chain failed: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! Lazy initialization fix is working correctly!")
print("The database isolation issue should now be resolved.")