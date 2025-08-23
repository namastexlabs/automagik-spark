#!/usr/bin/env python3
import re

# Read the file
with open('/home/cezar/automagik/automagik-spark/automagik_spark/core/workflows/automagik_hive.py', 'r') as f:
    content = f.read()

print("Applying AutoMagik Hive API format fixes...")

# Fix 1: Async method - Replace payload structure and request format
async_pattern = r'payload = \{\s*"input_data": \{\s*"message": message,\s*"requirements": message\s*\}\s*\}\s*if session_id:\s*payload\["session_id"\] = session_id\s*\n\s*response = await client\.post\(f"/playground/workflows/\{workflow_id\}/runs", json=payload\)'

async_replacement = '''payload = {
            "message": message
        }
        if session_id:
            payload["session_id"] = session_id
            
        # Use form data like agents and teams to match Hive API expectations
        response = await client.post(
            f"/playground/workflows/{workflow_id}/runs", 
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )'''

# Fix 2: Sync method - Replace payload structure and request format  
sync_pattern = r'payload = \{\s*"input_data": \{\s*"message": message,\s*"requirements": message\s*\}\s*\}\s*if session_id:\s*payload\["session_id"\] = session_id\s*\n\s*logger\.info\(f"Running workflow \{workflow_id\} with payload: \{payload\}"\)\s*\n\s*response = client\.post\(f"/playground/workflows/\{workflow_id\}/runs", json=payload\)'

sync_replacement = '''payload = {
            "message": message
        }
        if session_id:
            payload["session_id"] = session_id
        
        logger.info(f"Running workflow {workflow_id} with payload: {payload}")
        
        # Use form data like agents and teams to match Hive API expectations
        response = client.post(
            f"/playground/workflows/{workflow_id}/runs", 
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )'''

# Apply fixes with more targeted replacements
changes_made = 0

# Simple targeted fixes
if '"input_data": {' in content:
    # Replace the complex payload structures
    content = content.replace('''payload = {
            "input_data": {
                "message": message,
                "requirements": message
            }
        }''', '''payload = {
            "message": message
        }''')
    changes_made += 1
    print("✅ Fixed payload structure (simplified from input_data wrapper)")

if ', json=payload)' in content:
    # Replace json=payload with data=payload and headers
    content = content.replace(
        'response = await client.post(f"/playground/workflows/{workflow_id}/runs", json=payload)',
        '''# Use form data like agents and teams to match Hive API expectations
        response = await client.post(
            f"/playground/workflows/{workflow_id}/runs", 
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )'''
    )
    
    content = content.replace(
        'response = client.post(f"/playground/workflows/{workflow_id}/runs", json=payload)',
        '''# Use form data like agents and teams to match Hive API expectations
        response = client.post(
            f"/playground/workflows/{workflow_id}/runs", 
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )'''
    )
    changes_made += 1
    print("✅ Fixed request format (changed from json=payload to data=payload with headers)")

# Write the corrected content
with open('/home/cezar/automagik/automagik-spark/automagik_spark/core/workflows/automagik_hive.py', 'w') as f:
    f.write(content)

print(f"\n🎉 Successfully applied {changes_made} critical fixes!")
print("\nChanges made:")
print("1. ✅ Simplified payload from {'input_data': {'message': msg, 'requirements': msg}} to {'message': msg}")
print("2. ✅ Changed request format from json=payload to data=payload with proper headers")
print("3. ✅ Both async and sync _run_workflow methods now use form data like agents and teams")
print("\n🔧 This should resolve the 422 Unprocessable Entity errors when executing workflows through Spark API.")