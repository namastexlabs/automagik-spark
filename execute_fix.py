#!/usr/bin/env python3
import subprocess
import sys
import os

# Set working directory
os.chdir('/home/cezar/automagik/automagik-spark')

# Execute the replacement
try:
    result = subprocess.run([sys.executable, 'replace_file.py'], 
                          capture_output=True, text=True, check=True)
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        
    # Verify the fix worked
    print("\nVerifying fix by checking current content:")
    with open('automagik_spark/core/tasks/workflow_tasks.py', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if 'WorkflowSync' in line:
                print(f"Line {i}: {line.strip()}")
                
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    print(f"STDOUT: {e.stdout}")
    print(f"STDERR: {e.stderr}")
except Exception as e:
    print(f"Unexpected error: {e}")

print("\nDone!")