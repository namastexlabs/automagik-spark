import httpx
from typing import List, Dict, Any, Optional
from models import FlowDB
from sqlalchemy import text

def get_remote_flows(langflow_api_url: str, langflow_api_key: str) -> List[Dict[str, Any]]:
    """Fetch flows from Langflow server."""
    headers = {
        "x-api-key": langflow_api_key,  # API key in header
        "accept": "application/json"
    }
    
    # Query parameters
    params = {
        "remove_example_flows": "false",
        "components_only": "false",
        "get_all": "true",
        "header_flows": "false",
        "page": "1",
        "size": "50"
    }
    
    try:
        with httpx.Client(verify=False) as client:
            url = f"{langflow_api_url}/flows/"
            print(f"\nMaking request to: {url}")
            print(f"Headers: {headers}")
            print(f"Params: {params}")
            
            response = client.get(url, headers=headers, params=params)
            print(f"\nStatus code: {response.status_code}")
            print(f"Response text: {response.text[:500]}...")
            
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"\nHTTP Error: {str(e)}")
        raise
    except ValueError as e:
        print(f"\nJSON Parsing Error: {str(e)}")
        raise
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        raise

def select_flow(flows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Display flows and let user select one."""
    print("\nAvailable flows:")
    for i, flow in enumerate(flows):
        print(f"{i}: {flow['name']} (ID: {flow['id']})")
    
    while True:
        try:
            choice = int(input("\nSelect a flow by index: "))
            if 0 <= choice < len(flows):
                return flows[choice]
            print("Invalid index. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def get_flow_details(langflow_api_url: str, langflow_api_key: str, flow_id: str) -> Dict[str, Any]:
    """Fetch detailed information about a specific flow."""
    print(f"\nFetching details for flow {flow_id}...")
    
    # Prepare request
    url = f"{langflow_api_url}/flows/{flow_id}"
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    print(f"\nMaking request to: {url}")
    print(f"Headers: {headers}")
    
    try:
        with httpx.Client(verify=False) as client:
            response = client.get(url, headers=headers)
            print(f"\nStatus code: {response.status_code}")
            print(f"Response text: {response.text[:2000]}...")  # Print first 2000 chars
            
            response.raise_for_status()
            flow_data = response.json()
            print("\nFlow data:")
            for key in ['name', 'folder_name', 'folder_id', 'data']:
                print(f"- {key}:", flow_data.get(key, 'None'))
            return flow_data
    except httpx.HTTPError as e:
        print(f"\nHTTP Error: {str(e)}")
        raise
    except ValueError as e:
        print(f"\nJSON Parsing Error: {str(e)}")
        raise
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        raise

def get_folder_name(langflow_api_url: str, langflow_api_key: str, folder_id: str) -> Optional[str]:
    """Fetch folder name from the API."""
    if not folder_id:
        return None
        
    url = f"{langflow_api_url}/folders/{folder_id}"
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    try:
        with httpx.Client(verify=False) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes
            folder_data = response.json()
            print(f"\nFolder API response: {folder_data}")  # Debug print
            return folder_data.get('name')
    except Exception as e:
        print(f"Error fetching folder name: {str(e)}")
    return None

def sync_flow(db_session, flow_data: Dict[str, Any], langflow_api_url: str = None, langflow_api_key: str = None) -> FlowDB:
    """Sync a flow to the local database."""
    source = "langflow"
    source_id = str(flow_data["id"])
    
    # Try to get folder name if we have API access
    folder_name = None
    if langflow_api_url and langflow_api_key and flow_data.get('folder_id'):
        folder_name = get_folder_name(langflow_api_url, langflow_api_key, flow_data['folder_id'])
        print(f"\nFolder name from API: {folder_name}")
    
    # Convert to local structure
    flow_dict = {
        "id": source_id,  # Use the UUID directly
        "name": flow_data["name"],
        "description": flow_data.get("description", ""),
        "data": flow_data.get("data", {}),
        "source": source,
        "source_id": source_id,
        "user_id": flow_data.get("user_id"),
        "folder_id": flow_data.get("folder_id"),
        "is_component": flow_data.get("is_component", False),
        "icon": flow_data.get("icon"),
        "icon_bg_color": flow_data.get("icon_bg_color"),
        "gradient": flow_data.get("gradient"),
        "liked": flow_data.get("liked", False),
        "tags": flow_data.get("tags", []),
        "folder_name": folder_name
    }
    
    # Query DB for existing flow
    existing = db_session.query(FlowDB).filter_by(
        source=source,
        source_id=source_id
    ).first()
    
    if existing:
        print(f"\nUpdating existing flow: {existing.name} (Version {existing.flow_version})")
        # Update existing, increment version
        existing.flow_version += 1
        for k, v in flow_dict.items():
            setattr(existing, k, v)
        db_session.commit()
        return existing
    else:
        print(f"\nCreating new flow: {flow_dict['name']}")
        # Create new flow
        flow_dict["flow_version"] = 1
        new_flow = FlowDB(**flow_dict)
        db_session.add(new_flow)
        db_session.commit()
        return new_flow
