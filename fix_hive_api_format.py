#!/usr/bin/env python3
"""
Fix script for AutoMagik Hive API format mismatch issue.
Converts JSON payload format to form data format for workflow executions.
"""

def fix_hive_api_format():
    """Fix the API format mismatch in automagik_hive.py"""
    file_path = '/home/cezar/automagik/automagik-spark/automagik_spark/core/workflows/automagik_hive.py'
    
    # Read the current file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Async _run_workflow method
    # Replace the complex JSON payload with simple form data
    old_async_payload = '''        payload = {
            "input_data": {
                "message": message,
                "requirements": message
            }
        }
        if session_id:
            payload["session_id"] = session_id
            
        response = await client.post(f"/playground/workflows/{workflow_id}/runs", json=payload)'''
    
    new_async_payload = '''        payload = {
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
    
    # Fix 2: Sync _run_workflow_sync method  
    old_sync_payload = '''        payload = {
            "input_data": {
                "message": message,
                "requirements": message
            }
        }
        if session_id:
            payload["session_id"] = session_id
        
        logger.info(f"Running workflow {workflow_id} with payload: {payload}")
        
        response = client.post(f"/playground/workflows/{workflow_id}/runs", json=payload)'''
    
    new_sync_payload = '''        payload = {
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
    
    # Apply the fixes
    if old_async_payload in content:
        content = content.replace(old_async_payload, new_async_payload)
        print("✅ Fixed async _run_workflow method")
    else:
        print("❌ Could not find async _run_workflow pattern to fix")
        
    if old_sync_payload in content:
        content = content.replace(old_sync_payload, new_sync_payload)
        print("✅ Fixed sync _run_workflow_sync method")
    else:
        print("❌ Could not find sync _run_workflow_sync pattern to fix")
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Successfully applied fixes to {file_path}")
    print("\nFixes applied:")
    print("1. Changed JSON payload format to form data format")
    print("2. Simplified payload structure from {'input_data': {'message': message}} to {'message': message}")
    print("3. Updated HTTP requests from json=payload to data=payload with proper headers")
    print("\nThis should resolve the 422 Unprocessable Entity errors when executing workflows through Spark API.")

if __name__ == '__main__':
    fix_hive_api_format()