#!/usr/bin/env python3
"""Debug test to see what's happening with the lazy initialization."""

import os

# Set test environment BEFORE imports - critical for this test
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888" 
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

print("=== DEBUG TEST START ===")
print(f"Environment before import: {os.getenv('ENVIRONMENT')}")
print(f"Database URL before import: {os.getenv('AUTOMAGIK_SPARK_DATABASE_URL')}")

# Now import and see what happens
print("\n--- Importing session module ---")
from automagik_spark.core.database import session as db_session

print("\n--- Accessing DATABASE_URL ---")
print(f"DATABASE_URL: {db_session.DATABASE_URL}")

print("\n--- Accessing async_engine ---")
engine = db_session.async_engine()
print(f"Engine URL: {engine.url}")

print("\n--- Testing import chain ---")
# This simulates the problematic import chain from tests
from automagik_spark.api import app
print("App imported")

# Check if engine is still SQLite
engine2 = db_session.async_engine()
print(f"Engine URL after app import: {engine2.url}")

print("\n=== DEBUG TEST END ===")