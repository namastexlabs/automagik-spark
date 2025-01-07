import os
import httpx
import click
import uuid
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .models import FlowDB, FlowComponent

# Load environment variables
load_dotenv()

def analyze_component(node: Dict[str, Any]) -> Tuple[bool, bool, List[str]]:
    """Analyze a component node to determine if it's input/output and its tweakable params."""
    is_input = False
    is_output = False
    tweakable_params = []
    
    # Check if it's an input/output component
    component_type = node.get("data", {}).get("node", {}).get("template", {}).get("_type", "").lower()
    if "chatinput" in component_type or "chatmessages" in component_type:
        is_input = True
    elif "chatoutput" in component_type or "chatmessagehistory" in component_type:
        is_output = True
    
    # Identify tweakable parameters
    template = node.get("data", {}).get("node", {}).get("template", {})
    for param_name, param_data in template.items():
        # Skip internal parameters and code/password fields
        if (not param_name.startswith("_") and 
            not param_data.get("code") and 
            not param_data.get("password") and
            param_data.get("show", True)):
            tweakable_params.append(param_name)
    
    return is_input, is_output, tweakable_params

def get_remote_flows(langflow_api_url: str, langflow_api_key: str) -> List[Dict[str, Any]]:
    """Fetch flows from Langflow server."""
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    params = {
        "remove_example_flows": "false",
        "components_only": "false",
        "get_all": "true",
        "header_flows": "false",
        "page": "1",
        "size": "50"
    }
    
    # Ensure URL has v1 prefix
    api_url = langflow_api_url.rstrip('/')
    if not api_url.endswith('/api/v1'):
        api_url = f"{api_url}/api/v1"
    
    click.echo(f"Connecting to Langflow server at: {api_url}")
    click.echo(f"Using API key: {langflow_api_key[:8]}...")
    
    try:
        with httpx.Client(verify=False) as client:
            url = f"{api_url}/flows/"
            click.echo(f"Making request to: {url}")
            click.echo(f"With headers: {headers}")
            click.echo(f"With params: {params}")
            
            response = client.get(url, headers=headers, params=params)
            click.echo(f"Response status code: {response.status_code}")
            click.echo(f"Response text: {response.text[:200]}...")  # Show first 200 chars
            
            response.raise_for_status()
            return response.json()
    except Exception as e:
        click.echo(f"Error fetching flows: {str(e)}")
        click.echo(f"Error type: {type(e)}")
        if isinstance(e, httpx.HTTPError):
            click.echo(f"HTTP Status code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            click.echo(f"Response text: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return []

def get_flow_details(langflow_api_url: str, langflow_api_key: str, flow_id: str) -> Dict[str, Any]:
    """Fetch detailed information about a specific flow."""
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    # Ensure URL has v1 prefix
    api_url = langflow_api_url.rstrip('/')
    if not api_url.endswith('/api/v1'):
        api_url = f"{api_url}/api/v1"
    
    try:
        with httpx.Client(verify=False) as client:
            url = f"{api_url}/flows/{flow_id}"
            click.echo(f"Making request to: {url}")
            click.echo(f"With headers: {headers}")
            
            response = client.get(url, headers=headers)
            click.echo(f"Response status code: {response.status_code}")
            click.echo(f"Response text: {response.text[:200]}...")  # Show first 200 chars
            
            response.raise_for_status()
            return response.json()
    except Exception as e:
        click.echo(f"Error fetching flow details: {str(e)}")
        click.echo(f"Error type: {type(e)}")
        if isinstance(e, httpx.HTTPError):
            click.echo(f"HTTP Status code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            click.echo(f"Response text: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return {}

def get_folder_name(langflow_api_url: str, langflow_api_key: str, folder_id: str) -> Optional[str]:
    """Fetch folder name from the API."""
    if not folder_id:
        return None
        
    api_url = langflow_api_url.rstrip('/')
    if not api_url.endswith('/api/v1'):
        api_url = f"{api_url}/api/v1"
        
    url = f"{api_url}/folders/{folder_id}"
    headers = {
        "x-api-key": langflow_api_key,
        "accept": "application/json"
    }
    
    click.echo(f"\nFetching folder name for ID: {folder_id}")
    click.echo(f"Making request to: {url}")
    
    try:
        with httpx.Client(verify=False) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            folder_data = response.json()
            click.echo(f"Folder API response: {folder_data}")
            return folder_data.get('name')
    except Exception as e:
        click.echo(f"Error fetching folder name: {str(e)}")
    return None

def select_components(flow_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """Let user select input and output components."""
    nodes = flow_data.get("data", {}).get("nodes", [])
    if not nodes:
        return None, None
        
    click.echo("\nAvailable components:")
    for i, node in enumerate(nodes):
        node_id = node.get("id", "")
        node_type = node.get("data", {}).get("node", {}).get("template", {}).get("type", "unknown")
        node_name = node.get("data", {}).get("node", {}).get("template", {}).get("display_name", node_id)
        click.echo(f"{i}: {node_name} (ID: {node_id}, Type: {node_type})")
    
    input_component = None
    output_component = None
    
    # Select input component
    while True:
        try:
            selection = click.prompt("\nSelect input component by index (or -1 to skip)", type=int)
            if selection == -1:
                break
            if 0 <= selection < len(nodes):
                input_component = nodes[selection]["id"]
                break
            click.echo("Please select a valid index.")
        except ValueError:
            click.echo("Please enter a valid number.")
    
    # Select output component
    while True:
        try:
            selection = click.prompt("\nSelect output component by index (or -1 to skip)", type=int)
            if selection == -1:
                break
            if 0 <= selection < len(nodes):
                output_component = nodes[selection]["id"]
                break
            click.echo("Please select a valid index.")
        except ValueError:
            click.echo("Please enter a valid number.")
    
    return input_component, output_component

def sync_flow(db_session: Session, flow_data: Dict[str, Any], langflow_api_url: str = None, langflow_api_key: str = None) -> FlowDB:
    """Sync a flow to the local database and analyze its components."""
    source = "langflow"
    source_id = str(flow_data["id"])
    
    # Try to get folder name if we have API access
    folder_name = None
    if langflow_api_url and langflow_api_key and flow_data.get('folder_id'):
        folder_name = get_folder_name(langflow_api_url, langflow_api_key, flow_data['folder_id'])
        click.echo(f"\nFolder name from API: {folder_name}")
    
    # Let user select input/output components
    input_component, output_component = select_components(flow_data)
    
    flow_dict = {
        "id": source_id,
        "name": flow_data["name"],
        "description": flow_data.get("description", ""),
        "data": flow_data.get("data", {}),
        "source": source,
        "source_id": source_id,
        "folder_id": flow_data.get("folder_id"),
        "folder_name": folder_name,
        "is_component": flow_data.get("is_component", False),
        "icon": flow_data.get("icon"),
        "icon_bg_color": flow_data.get("icon_bg_color"),
        "gradient": flow_data.get("gradient"),
        "liked": flow_data.get("liked", False),
        "tags": flow_data.get("tags", []),
        "input_component": input_component,
        "output_component": output_component
    }
    
    # Check if flow already exists
    existing = db_session.query(FlowDB).filter_by(
        source=source,
        source_id=source_id
    ).first()
    
    if existing:
        # Update existing flow
        for key, value in flow_dict.items():
            setattr(existing, key, value)
        flow = existing
        flow.flow_version += 1
    else:
        # Create new flow
        flow = FlowDB(**flow_dict)
        flow.flow_version = 1
        db_session.add(flow)
    
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    
    return flow