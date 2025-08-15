#!/usr/bin/env python3
import subprocess
import sys
import os

# Set the working directory
os.chdir('/home/cezar/automagik/automagik-spark')

# Run the Python fix script
result = subprocess.run([sys.executable, 'fix_workflow_sync.py'], capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

# Verify the changes
with open('automagik_spark/core/tasks/workflow_tasks.py', 'r') as f:
    content = f.read()
    if 'WorkflowSyncSync' in content:
        print("SUCCESS: WorkflowSyncSync found in file")
        print("Lines with WorkflowSync:")
        for i, line in enumerate(content.split('\n'), 1):
            if 'WorkflowSync' in line:
                print(f"  {i}: {line.strip()}")
    else:
        print("ERROR: WorkflowSyncSync not found in file")