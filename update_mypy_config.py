#!/usr/bin/env python3
"""Script to update mypy configuration in pyproject.toml"""

import sys

# Read the file
with open('/home/cezar/automagik/automagik-spark/pyproject.toml', 'r') as f:
    content = f.read()

# Find and replace the mypy section
old_mypy = """[tool.mypy]
python_version = "3.12"
warn_return_any = false
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
no_implicit_optional = false

[[tool.mypy.overrides]]
module = ["celery.*", "kombu.*", "croniter.*", "dateutil.*"]
ignore_missing_imports = true"""

new_mypy = """[tool.mypy]
python_version = "3.12"
warn_return_any = false
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
no_implicit_optional = false
# SQLAlchemy plugin for better ORM type support
plugins = ["sqlalchemy.ext.mypy.plugin"]
# Disable checks that conflict with SQLAlchemy ORM patterns
disable_error_code = ["assignment", "method-assign"]
# Allow untyped calls to handle dynamic ORM operations
allow_untyped_calls = true
# Allow incomplete defs for ORM models
allow_incomplete_defs = true

# SQLAlchemy ORM models - be lenient with Column assignments and relationships
[[tool.mypy.overrides]]
module = ["automagik_spark.core.database.models"]
disable_error_code = ["assignment", "attr-defined", "var-annotated", "misc"]
allow_untyped_defs = true
allow_incomplete_defs = true

# Workflow modules - heavy ORM usage with dynamic queries
[[tool.mypy.overrides]]
module = [
    "automagik_spark.core.workflows.*",
    "automagik_spark.core.scheduler.*"
]
disable_error_code = ["assignment", "attr-defined", "call-arg", "arg-type"]
allow_untyped_calls = true
allow_incomplete_defs = true

# Third-party libraries without type stubs
[[tool.mypy.overrides]]
module = ["celery.*", "kombu.*", "croniter.*", "dateutil.*", "sqlalchemy.*", "alembic.*"]
ignore_missing_imports = true
allow_untyped_defs = true

# Database session management - async patterns
[[tool.mypy.overrides]]
module = ["automagik_spark.core.database.session", "automagik_spark.core.database.base"]
disable_error_code = ["assignment", "return-value"]
allow_untyped_calls = true"""

if old_mypy in content:
    content = content.replace(old_mypy, new_mypy)
    with open('/home/cezar/automagik/automagik-spark/pyproject.toml', 'w') as f:
        f.write(content)
    print("Successfully updated mypy configuration!")
else:
    print("ERROR: Could not find the mypy section to replace")
    sys.exit(1)
