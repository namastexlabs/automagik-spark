#!/usr/bin/env python3
"""Script to replace the original workflow_tasks.py with the fixed version"""

import shutil
import os

# File paths
original_file = '/home/cezar/automagik/automagik-spark/automagik_spark/core/tasks/workflow_tasks.py'
fixed_file = '/home/cezar/automagik/automagik-spark/automagik_spark/core/tasks/workflow_tasks_fixed.py'
backup_file = '/home/cezar/automagik/automagik-spark/automagik_spark/core/tasks/workflow_tasks.py.backup'

print(f"Creating backup: {backup_file}")
shutil.copy2(original_file, backup_file)

print(f"Replacing {original_file} with fixed version")
shutil.copy2(fixed_file, original_file)

print("Verifying the changes...")
with open(original_file, 'r') as f:
    content = f.read()
    
# Check for the changes
import_fixed = 'from ...core.workflows.sync import WorkflowSyncSync' in content
usage_count = content.count('with WorkflowSyncSync(session) as sync:')

print(f"✓ Import fixed: {import_fixed}")
print(f"✓ Usage instances fixed: {usage_count}/2")

if import_fixed and usage_count == 2:
    print("SUCCESS: All fixes applied correctly!")
    # Clean up the temporary fixed file
    os.remove(fixed_file)
    print(f"Cleaned up temporary file: {fixed_file}")
else:
    print("WARNING: Not all fixes applied correctly!")

print(f"Backup saved as: {backup_file}")