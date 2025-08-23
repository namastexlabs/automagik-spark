#!/usr/bin/env python3
"""Debug Base.metadata to see if models are registered."""

import os

# Set test environment
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

# Import Base the same way conftest.py does
from automagik_spark.core.database.base import Base
# Import models to register them with Base.metadata
import automagik_spark.core.database.models  # noqa: F401

print("Base.metadata.tables:")
for table_name in Base.metadata.tables.keys():
    print(f"  - {table_name}")

print(f"\nTotal tables: {len(Base.metadata.tables)}")
print(f"workflow_sources table exists: {'workflow_sources' in Base.metadata.tables}")