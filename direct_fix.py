#!/usr/bin/env python3
"""Direct execution to fix the workflow_tasks.py file"""

import shutil
import os

# File paths
original_file = '/home/cezar/automagik/automagik-spark/automagik_spark/core/tasks/workflow_tasks.py'
backup_file = '/home/cezar/automagik/automagik-spark/automagik_spark/core/tasks/workflow_tasks.py.backup'

# Read the original file
print("Reading original file...")
with open(original_file, 'r') as f:
    content = f.read()

# Create backup
print("Creating backup...")
shutil.copy2(original_file, backup_file)

# Apply fixes
print("Applying fixes...")
# Fix 1: Import statement
content = content.replace(
    'from ...core.workflows.sync import WorkflowSync',
    'from ...core.workflows.sync import WorkflowSyncSync'
)

# Fix 2: Usage instances
content = content.replace(
    'with WorkflowSync(session) as sync:',
    'with WorkflowSyncSync(session) as sync:'
)

# Write the fixed content back
print("Writing fixed content...")
with open(original_file, 'w') as f:
    f.write(content)

# Verify the changes
print("Verifying changes...")
with open(original_file, 'r') as f:
    new_content = f.read()

import_fixed = 'from ...core.workflows.sync import WorkflowSyncSync' in new_content
usage_count = new_content.count('with WorkflowSyncSync(session) as sync:')

print(f"✓ Import fixed: {import_fixed}")
print(f"✓ Usage instances fixed: {usage_count}/2")

if import_fixed and usage_count == 2:
    print("SUCCESS: All fixes applied correctly!")
    print("The scheduled tasks should now execute properly.")
else:
    print("WARNING: Not all fixes applied correctly!")

print(f"Backup saved as: {backup_file}")

# Also show what lines contain WorkflowSync now
print("\nCurrent lines with WorkflowSync:")
for i, line in enumerate(new_content.split('\n'), 1):
    if 'WorkflowSync' in line:
        print(f"  Line {i}: {line.strip()}")

print("\nFix completed!")

# Execute this script directly
if __name__ == "__main__":
    exec(open(__file__).read())