import httpx
from typing import Dict, List, Optional, Any
import json
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
from .db import get_db_session
from .models import FlowDB
from .logger import setup_logger

load_dotenv()

logger = setup_logger()

class LangflowClient:
    def __init__(self, base_url: str = None, api_key: str = None):
        """Initialize Langflow client.
        
        Args:
            base_url: Langflow API base URL. If not provided, uses LANGFLOW_API_URL env var.
            api_key: API key for authentication. If not provided, uses LANGFLOW_API_KEY env var.
        """
        self.base_url = base_url or os.getenv('LANGFLOW_API_URL')
        if not self.base_url:
            raise ValueError("Langflow API URL not provided and LANGFLOW_API_URL env var not set")
        
        self.api_key = api_key or os.getenv('LANGFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("API key not provided and LANGFLOW_API_KEY env var not set")
        
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def _make_url(self, endpoint: str) -> str:
        """Create full URL from endpoint."""
        # Remove any leading slashes from endpoint
        endpoint = endpoint.lstrip('/')
        return urljoin(self.base_url, endpoint)

    async def list_flows(self) -> List[Dict[str, Any]]:
        """List all available flows."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._make_url('/api/v1/flows/'),
                headers=self.headers,
                follow_redirects=True
            )
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
            response.raise_for_status()
            return response.json()

    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """Get details of a specific flow."""
        url = self._make_url(f'/api/v1/flows/{flow_id}/')
        logger.debug(f"\nGetting flow details:")
        logger.debug(f"URL: {url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=self.headers,
                follow_redirects=True
            )
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
            
            if response.status_code == 404:
                return None
                
            response.raise_for_status()
            return response.json()

    async def delete_flow(self, flow_id: str) -> bool:
        """Delete a flow."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._make_url(f'/api/v1/flows/{flow_id}/'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return True

    async def run_flow(self, 
                      flow_name: str, 
                      input_value: Optional[str] = None,
                      input_type: str = "chat",
                      output_type: str = "chat",
                      tweaks: Optional[Dict[str, Dict[str, Any]]] = None,
                      stream: bool = False) -> Dict[str, Any]:
        """Run a flow with optional tweaks.
        
        Args:
            flow_name: Name of the flow to run
            input_value: Optional input value for the flow
            input_type: Type of input (default: "chat")
            output_type: Type of output (default: "chat")
            tweaks: Optional component tweaks
            stream: Whether to stream the response
        """
        payload = {
            "input_type": input_type,
            "output_type": output_type,
            "tweaks": tweaks or {}
        }
        
        if input_value is not None:
            payload["input_value"] = input_value

        url = self._make_url(f'api/v1/run/{flow_name}')  # Removed leading slash
        if stream:
            url += "?stream=true"
        else:
            url += "?stream=false"

        logger.debug(f"\nLangflow API Request:")
        logger.debug(f"  URL: {url}")
        logger.debug(f"  Headers: {json.dumps({k: '***' if k == 'x-api-key' else v for k, v in self.headers.items()}, indent=2)}")
        logger.debug(f"  Payload: {json.dumps(payload, indent=2)}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
                follow_redirects=True
            )
            logger.debug(f"\nLangflow API Response:")
            logger.debug(f"  Status: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.debug(f"  Response JSON: {json.dumps(response_json, indent=2)}")
                response.raise_for_status()
                return response_json
            except json.JSONDecodeError:
                logger.debug(f"  Raw Response Text: {response.text}")
                if response.status_code == 200:
                    # If status is 200 but response is not JSON, return empty dict
                    return {}
                else:
                    response.raise_for_status()
                    return {}

    async def get_components(self) -> Dict[str, Any]:
        """Get all available components and their configurations."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._make_url('/api/v1/components/'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()

    async def validate_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a flow configuration."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._make_url('/api/v1/validate/flow/'),
                headers=self.headers,
                json=flow_data,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()

    async def process_flow(self, flow_id: str, input_data: Dict[str, Any], tweaks: Optional[Dict[str, Any]] = None, stream: bool = False) -> Dict[str, Any]:
        """Process a flow by its ID with input data.
        
        Args:
            flow_id: ID of the flow to process
            input_data: Input data for the flow
            tweaks: Optional component tweaks
            stream: Whether to stream the response
        """
        logger.debug(f"\nProcessing flow {flow_id}")
        logger.debug(f"  Input data: {json.dumps(input_data, indent=2)}")
        logger.debug(f"  Tweaks: {json.dumps(tweaks, indent=2)}")
        
        # Get flow from database
        db = get_db_session()
        flow = db.query(FlowDB).filter(FlowDB.id == flow_id).first()
        if not flow:
            raise ValueError(f"Flow {flow_id} not found")
            
        if not flow.name:
            raise ValueError(f"Flow {flow_id} has no name")
            
        # Convert input_data to input_value
        input_value = input_data.get('input')
        if input_value is None:
            raise ValueError("No 'input' key found in input_data")
            
        flow_endpoint = flow.data.get('endpoint') if flow.data else None
        if not flow_endpoint:
            # Fallback to flow ID if no endpoint
            flow_endpoint = str(flow.id)
            
        logger.debug(f"  Using flow endpoint: {flow_endpoint}")
        logger.debug(f"  Input value: {input_value}")
            
        # Use run_flow with endpoint and tweaks
        return await self.run_flow(
            flow_name=flow_endpoint,
            input_value=input_value,
            tweaks=tweaks
        )

class FlowComponent:
    """Helper class to manage flow component configurations."""
    def __init__(self, component_id: str, component_type: str, config: Dict[str, Any] = None):
        self.id = component_id
        self.type = component_type
        self.config = config or {}

    def update_config(self, **kwargs):
        """Update component configuration."""
        self.config.update(kwargs)

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Convert component to dictionary format for API."""
        return {self.id: self.config}

class FlowBuilder:
    """Helper class to build flow configurations."""
    def __init__(self):
        self.components: Dict[str, FlowComponent] = {}

    def add_component(self, component_id: str, component_type: str, **config) -> FlowComponent:
        """Add a component to the flow."""
        component = FlowComponent(component_id, component_type, config)
        self.components[component_id] = component
        return component

    def get_tweaks(self) -> Dict[str, Dict[str, Any]]:
        """Get the complete tweaks configuration for the flow."""
        return {
            comp_id: comp.config 
            for comp_id, comp in self.components.items()
        }
