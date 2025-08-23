#!/usr/bin/env python3
"""Test script to verify lazy initialization fix."""

import os
import sys

# Set test environment BEFORE any imports
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

print("Environment variables set:")
print(f"ENVIRONMENT = {os.getenv('ENVIRONMENT')}")
print(f"AUTOMAGIK_SPARK_DATABASE_URL = {os.getenv('AUTOMAGIK_SPARK_DATABASE_URL')}")

# Now import the session module
print("\nImporting session module...")
from automagik_spark.core.database import session as db_session

print("Session module imported successfully!")

# Check if DATABASE_URL is a function (lazy)
print(f"\nDATABASE_URL type: {type(db_session.DATABASE_URL)}")
print(f"DATABASE_URL(): {db_session.DATABASE_URL()}")

# Check if async_engine is a function (lazy)
print(f"\nasync_engine type: {type(db_session.async_engine)}")
engine = db_session.async_engine()
print(f"async_engine(): {engine}")
print(f"Engine URL: {engine.url}")

# Verify it's using SQLite
if "sqlite" in str(engine.url):
    print("\n✅ SUCCESS: Engine is using SQLite (test database)")
else:
    print(f"\n❌ FAILURE: Engine is using {engine.url} instead of SQLite")
    sys.exit(1)

print("\n✅ All checks passed! Lazy initialization is working correctly.")