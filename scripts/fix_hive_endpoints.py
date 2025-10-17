#!/usr/bin/env python3
"""
Fix Hive API endpoints to use AgentOS v2 paths (/api/v1/ prefix).

This script updates automagik_hive.py to use the correct endpoint paths
for listing and running agents, teams, and workflows from Hive.

Issue: https://github.com/namastexlabs/automagik-spark/issues/16
"""

import os
import sys
from pathlib import Path

def main():
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    file_path = project_root / "automagik_spark" / "core" / "workflows" / "automagik_hive.py"

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    print(f"Fixing Hive endpoints in: {file_path}")

    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Create backup
    backup_path = str(file_path) + '.bak'
    with open(backup_path, 'w') as f:
        f.write(content)
    print(f"Backup created: {backup_path}")

    # Apply replacements
    replacements = [
        # List endpoints
        ('client.get("/agents")', 'client.get("/api/v1/agents")'),
        ('client.get("/teams")', 'client.get("/api/v1/teams")'),
        ('client.get("/workflows")', 'client.get("/api/v1/workflows")'),
        # Run endpoints
        ('f"/agents/{agent_id}/runs"', 'f"/api/v1/agents/{agent_id}/runs"'),
        ('f"/teams/{team_id}/runs"', 'f"/api/v1/teams/{team_id}/runs"'),
        ('f"/workflows/{workflow_id}/runs"', 'f"/api/v1/workflows/{workflow_id}/runs"'),
    ]

    changes_made = 0
    for old, new in replacements:
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            changes_made += count
            print(f"  ✓ Replaced '{old}' ({count} occurrences)")

    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)

    print(f"\n✓ Fix completed successfully!")
    print(f"✓ Total changes: {changes_made}")
    print(f"\nNext steps:")
    print(f"  1. Review the changes: diff {backup_path} {file_path}")
    print(f"  2. Run tests: pytest tests/core/workflows/test_automagik_hive.py")
    print(f"  3. Test sync: automagik workflow sync <flow-id> --source http://localhost:8886")

if __name__ == "__main__":
    main()
