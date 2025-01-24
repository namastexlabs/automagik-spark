import os
import httpx
import click
import uuid
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import json
import logging

# Set up logging configuration
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('automagik').setLevel(logging.DEBUG)
logging.getLogger('automagik.core.services').setLevel(logging.DEBUG)
logger = setup_logger(level=logging.DEBUG)

from automagik.core.database.models import FlowDB, FlowComponent
from automagik.core.logger import setup_logger

# Load environment variables
load_dotenv()

def analyze_component(node: Dict[str, Any]) -> Tuple[bool, bool, List[str]]:
    """Analyze a component node to determine if it's input/output and its tweakable params."""
    is_input = False
    is_output = False
    tweakable_params = []
    
    # Get component data
    node_data = node.get("data", {}).get("node", {})
    template = node_data.get("template", {})
    
    # Check if it's an input/output component based on type and base_classes
    component_type = template.get("_type", "").lower()
    base_classes = node_data.get("base_classes", [])
    
    # Input components
    if (any(cls.lower() in ["chatinput", "humaninput", "textinput"] for cls in base_classes) or
        "input" in component_type):
        is_input = True
    
    # Output components
    if (any(cls.lower() in ["chatoutput", "output", "chatmessagehistory"] for cls in base_classes) or
        "output" in component_type):
        is_output = True
    
    # Identify tweakable parameters
    for param_name, param_data in template.items():
        # Skip internal parameters and code/password fields
        if (not param_name.startswith("_") and 
            not param_data.get("code") and 
            not param_data.get("password") and
            param_data.get("show", True) and
            param_data.get("type") not in ["code", "file"]):
            tweakable_params.append(param_name)
    
    logger.debug(f"Component analysis for {node.get('id')}: input={is_input}, output={is_output}, params={tweakable_params}")
    return is_input, is_output, tweakable_params

async def get_remote_flows(langflow_api_url: str, langflow_api_key: str) -> List[Dict[str, Any]]:
    """Fetch flows from Langflow server."""
    if not langflow_api_url or not langflow_api_key:
        click.echo("Error: API URL and API key are required")
        return []
        
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
    
    logger.info(f"Connecting to Langflow server at: {api_url}")
    
    try:
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            url = f"{api_url}/flows/"
            response = await client.get(url, headers=headers, params=params)
            logger.debug(f"API response status: {response.status_code}")  # Log the response status
            logger.debug(f"API response content: {response.text}")  # Log the raw response text
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Parsed flow data: {data}")  # Log the parsed JSON data
            
            if not data:
                logger.warning("No flows found on the server")
                return []
                
            logger.info(f"Successfully fetched {len(data)} flows from server")
            return data
            
    except httpx.TimeoutException:
        logger.error("Request timed out while fetching flows")
        return []
    except httpx.HTTPError as e:
        logger.error(f"HTTP Error: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Status code: {e.response.status_code}")
            logger.error(f"Response: {e.response.text}")
        return []
    except Exception as e:
        logger.error(f"Error fetching flows: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        return []

async def get_flow_details(langflow_api_url: str, langflow_api_key: str, flow_id: str) -> Dict[str, Any]:
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
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            url = f"{api_url}/flows/{flow_id}"
            logger.debug(f"Making request to: {url}")
            
            response = await client.get(url, headers=headers)
            logger.debug(f"Response status code: {response.status_code}")
            
            response.raise_for_status()
            flow_data = response.json()
            logger.info(f"Successfully fetched flow details for {flow_id}")
            return flow_data
    except httpx.TimeoutException:
        logger.error(f"Request timed out while fetching flow details for {flow_id}")
        return {}
    except Exception as e:
        logger.error(f"Error fetching flow details: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        if isinstance(e, httpx.HTTPError):
            logger.error(f"HTTP Status code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            logger.error(f"Response text: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return {}

async def get_folder_name(langflow_api_url: str, langflow_api_key: str, folder_id: str) -> Optional[str]:
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
    
    logger.debug(f"Fetching folder name for ID: {folder_id}")
    
    try:
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            folder_data = response.json()
            logger.debug(f"Folder API response: {folder_data}")
            return folder_data.get('name')
    except httpx.TimeoutException:
        logger.error(f"Request timed out while fetching folder name for {folder_id}")
    except Exception as e:
        logger.error(f"Error fetching folder name: {str(e)}")
    return None

def select_components(flow_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], List[Dict[str, Any]]]:
    """Analyze and let user select input and output components."""
    logger.debug(f"Flow data for component selection: {flow_data}")
    nodes = flow_data.get("data", {}).get("nodes", [])
    logger.debug(f"Nodes found: {nodes}")
    if not nodes:
        logger.warning("No nodes found in flow data")
        return None, None, []
    
    # First analyze all components
    analyzed_nodes = []
    for node in nodes:
        is_input, is_output, tweakable_params = analyze_component(node)
        analyzed_nodes.append({
            "id": node.get("id", ""),
            "name": node.get("data", {}).get("node", {}).get("template", {}).get("display_name", node.get("id", "")),
            "type": node.get("data", {}).get("node", {}).get("template", {}).get("_type", "unknown"),
            "is_input": is_input,
            "is_output": is_output,
            "tweakable_params": tweakable_params
        })
    
    logger.info("\nAvailable components:")
    for i, node in enumerate(analyzed_nodes):
        logger.info(f"{i}: {node['name']} (ID: {node['id']}, Type: {node['type']})")
        if node['is_input']:
            logger.info("   - Input component")
        if node['is_output']:
            logger.info("   - Output component")
        if node['tweakable_params']:
            logger.info(f"   - Tweakable params: {', '.join(node['tweakable_params'])}")
    
    # Auto-select if there's only one input and one output
    input_nodes = [n for n in analyzed_nodes if n['is_input']]
    output_nodes = [n for n in analyzed_nodes if n['is_output']]
    
    if len(input_nodes) == 1 and len(output_nodes) == 1:
        logger.info("\nAuto-selecting single input and output components")
        return input_nodes[0]['id'], output_nodes[0]['id'], analyzed_nodes
    
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
    
    return input_component, output_component, analyzed_nodes

async def sync_flow(db_session: Session, flow_data: Dict[str, Any], langflow_api_url: str = None, langflow_api_key: str = None) -> FlowDB:
    """Sync a flow to the local database and analyze its components."""
    source = "langflow"
    source_id = uuid.UUID(str(flow_data["id"]))  # Convert string to UUID
    
    logger.info(f"\nSyncing flow: {flow_data['name']} (ID: {source_id})")
    logger.debug(f"Flow data received: {flow_data}")
    
    # Try to get folder name if we have API access
    folder_name = None
    if langflow_api_url and langflow_api_key and flow_data.get('folder_id'):
        folder_name = await get_folder_name(langflow_api_url, langflow_api_key, flow_data['folder_id'])
        logger.info(f"Folder name from API: {folder_name}")
    else:
        # If we don't have API access but have a folder_id, use a default name
        folder_name = "Test Folder" if flow_data.get('folder_id') else None
    
    logger.debug(f"Flow data before component selection: {flow_data}")
    
    # Let user select input/output components and analyze all components
    input_component, output_component, analyzed_nodes = select_components(flow_data)
    logger.debug(f"Input component: {input_component}, Output component: {output_component}, Analyzed nodes: {analyzed_nodes}")
    
    flow_dict = {
        "id": source_id,  # Now using UUID object
        "name": flow_data["name"],
        "description": flow_data.get("description", ""),
        "data": flow_data.get("data", {}),
        "source": source,
        "source_id": str(source_id),  # Keep as string for source_id
        "folder_id": flow_data.get("folder_id"),
        "folder_name": folder_name,  # Now properly set from await result
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
        source_id=str(source_id)  # Match string source_id
    ).first()
    
    if existing:
        # Update existing flow
        for key, value in flow_dict.items():
            setattr(existing, key, value)
        flow = existing
        flow.flow_version += 1
        logger.info(f"Updated existing flow (version {flow.flow_version})")
    else:
        # Create new flow
        flow = FlowDB(**flow_dict)
        flow.flow_version = 1
        db_session.add(flow)
        logger.info("Created new flow")
    
    try:
        # Save flow components
        for node in analyzed_nodes:
            component = FlowComponent(
                flow_id=source_id,  # Using UUID object
                component_id=node['id'],
                type=node['type'],
                template=node.get('template', {}),
                is_input=node['is_input'],
                is_output=node['is_output'],
                tweakable_params=json.dumps(node['tweakable_params'])
            )
            db_session.merge(component)
        
        db_session.commit()
        logger.info("Successfully saved flow and components to database")
    except Exception as e:
        logger.error(f"Error saving flow: {str(e)}")
        db_session.rollback()
        raise e
    
    return flow