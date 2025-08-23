#!/usr/bin/env python3

import subprocess
import sys
import os

# Change to the project directory
os.chdir('/home/cezar/automagik/automagik-spark')

# Run the specific test that was failing
result = subprocess.run([
    sys.executable, '-m', 'pytest', 
    'tests/api/test_workflow_sources.py::test_create_workflow_source',
    '-xvs'
], capture_output=True, text=True)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")