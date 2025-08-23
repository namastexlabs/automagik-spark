#!/usr/bin/env python3

import os

# Set up test environment exactly like conftest.py
os.environ["ENVIRONMENT"] = "testing"
os.environ["AUTOMAGIK_SPARK_API_KEY"] = "namastex888"
os.environ["AUTOMAGIK_SPARK_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

print("=== Testing imports like the ORIGINAL conftest.py ===")
try:
    # Original import (what was failing)
    from automagik_spark.core.database.models import Base as OriginalBase
    print(f"Original Base: {OriginalBase}")
    print(f"Original Base metadata tables: {list(OriginalBase.metadata.tables.keys())}")
except Exception as e:
    print(f"Error with original import: {e}")

print("\n=== Testing imports like the NEW conftest.py ===")
try:
    # New import (what I changed to)
    from automagik_spark.core.database.base import Base as NewBase
    import automagik_spark.core.database.models  # noqa: F401
    print(f"New Base: {NewBase}")
    print(f"New Base metadata tables: {list(NewBase.metadata.tables.keys())}")
except Exception as e:
    print(f"Error with new import: {e}")

print("\n=== Comparison ===")
try:
    from automagik_spark.core.database.models import Base as OriginalBase
    from automagik_spark.core.database.base import Base as NewBase
    import automagik_spark.core.database.models  # noqa: F401
    
    print(f"Are they the same object? {OriginalBase is NewBase}")
    print(f"Original tables: {sorted(OriginalBase.metadata.tables.keys())}")
    print(f"New tables: {sorted(NewBase.metadata.tables.keys())}")
    
    if 'workflow_sources' in OriginalBase.metadata.tables:
        print("✅ workflow_sources found in ORIGINAL Base")
    else:
        print("❌ workflow_sources NOT found in ORIGINAL Base")
        
    if 'workflow_sources' in NewBase.metadata.tables:
        print("✅ workflow_sources found in NEW Base")
    else:
        print("❌ workflow_sources NOT found in NEW Base")
        
except Exception as e:
    print(f"Error in comparison: {e}")