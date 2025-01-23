"""
LangFlow API Client

This module provides a client for interacting with the LangFlow API.
"""

import httpx
import os
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class FlowComponent:
    """Helper class to manage flow component configurations."""
    
    def __init__(self, component_id: str, component_type: str, config: Dict[str, Any] = None):
        self.id = component_id
        self.type = component_type
        self.config = config or {}
        
    def update_config(self, **kwargs):
        """Update component configuration."""
        self.config.update(kwargs)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary format for API."""
        return {
            "id": self.id,
            "type": self.type,
            **self.config
        }

class FlowBuilder:
    """Helper class to build flow configurations."""
    
    def __init__(self):
        self.components: Dict[str, FlowComponent] = {}
        
    def add_component(self, component_id: str, component_type: str, **config):
        """Add a component to the flow."""
        self.components[component_id] = FlowComponent(component_id, component_type, config)
        
    def get_tweaks(self) -> Dict[str, Dict[str, Any]]:
        """Get the complete tweaks configuration for the flow."""
        return {
            component_id: component.to_dict()
            for component_id, component in self.components.items()
        }

class LangflowClient:
    """Client for interacting with the LangFlow API."""
    
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize LangFlow client.
        
        Args:
            api_url: LangFlow API base URL. If not provided, uses LANGFLOW_API_URL env var.
            api_key: API key for authentication. If not provided, uses LANGFLOW_API_KEY env var.
        """
        self.api_url = (api_url or os.getenv('LANGFLOW_API_URL', '')).rstrip('/')
        if not self.api_url:
            raise ValueError("LangFlow API URL not provided and LANGFLOW_API_URL env var not set")
            
        self.api_key = api_key or os.getenv('LANGFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("API key not provided and LANGFLOW_API_KEY env var not set")
            
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        logger.debug(f"Initialized LangFlow client with API URL: {self.api_url}")
    
    def _make_url(self, endpoint: str) -> str:
        """Create full URL from endpoint."""
        endpoint = endpoint.lstrip('/')
        return urljoin(self.api_url, endpoint)
    
    async def get_flows(self) -> List[Dict[str, Any]]:
        """Get all flows from LangFlow server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._make_url('/api/v1/flows'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
            logger.debug(f"Retrieved {len(response.json())} flows")
            return response.json()
    
    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """Get flow details by ID."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._make_url(f'/api/v1/flows/{flow_id}'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def run_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run a flow with given inputs."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._make_url(f'/api/v1/flows/{flow_id}/run'),
                headers=self.headers,
                json=inputs,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def create_flow(self, name: str, description: str = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new flow."""
        payload = {
            "name": name,
            "description": description,
            "data": data or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._make_url('/api/v1/flows'),
                headers=self.headers,
                json=payload,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def update_flow(self, flow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing flow."""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                self._make_url(f'/api/v1/flows/{flow_id}'),
                headers=self.headers,
                json=data,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
    
    async def delete_flow(self, flow_id: str) -> None:
        """Delete a flow."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._make_url(f'/api/v1/flows/{flow_id}'),
                headers=self.headers,
                follow_redirects=True
            )
            response.raise_for_status()
