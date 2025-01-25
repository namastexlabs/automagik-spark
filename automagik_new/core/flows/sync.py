"""
Flow Sync Module

Handles synchronization of flows between LangFlow and Automagik.
Provides functionality for fetching, filtering, and syncing flows.
"""

import logging
import httpx
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class FlowSync:
    """Handles flow synchronization with LangFlow."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize FlowSync.
        
        Args:
            base_url: LangFlow API base URL
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {"Authorization": api_key} if api_key else {}
        
    async def get_remote_flows(self, remove_examples: bool = True) -> List[Dict[str, Any]]:
        """
        Get flows from LangFlow server.
        
        Args:
            remove_examples: Whether to filter out example flows
            
        Returns:
            List of flow data dictionaries
        """
        try:
            params = {"remove_example_flows": remove_examples}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.base_url, "/api/v1/flows/"),
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                flows = response.json()
                
                # Filter out flows without folders (usually examples/tests)
                return [flow for flow in flows if flow.get('folder_id')]
                
        except Exception as e:
            logger.error(f"Error fetching flows: {str(e)}")
            return []
            
    async def get_flow_data(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed flow data by ID.
        
        Args:
            flow_id: ID of the flow to fetch
            
        Returns:
            Flow data dictionary or None if not found
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.base_url, f"/api/v1/flows/{flow_id}"),
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error fetching flow {flow_id}: {str(e)}")
            return None
            
    async def validate_flow(self, flow_id: str) -> bool:
        """
        Validate a flow exists and is accessible.
        
        Args:
            flow_id: ID of the flow to validate
            
        Returns:
            True if flow exists and is accessible
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    urljoin(self.base_url, f"/api/v1/flows/{flow_id}"),
                    headers=self.headers
                )
                response.raise_for_status()
                return True
                
        except Exception:
            return False

    async def execute_flow(self, flow_id: str, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Execute a flow with given input data.
        
        Args:
            flow_id: ID of the flow to execute
            input_data: Input data for the flow
            
        Returns:
            Flow execution result or None if failed
        """
        try:
            # Prepare the payload with required fields
            payload = {
                "input_value": input_data.get("input_value", ""),
                "output_type": "debug",  # Use debug mode to get component details
                "input_type": "chat",
                "tweaks": {
                    "ChatInput-PBSQV": {},
                    "ChatOutput-WHzRB": {}
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    urljoin(self.base_url, f"/api/v1/run/{flow_id}?stream=false"),
                    headers={"Content-Type": "application/json", **self.headers},
                    json=payload
                )
                response.raise_for_status()
                
                # Try to parse response as JSON
                try:
                    result = response.json()
                    
                    # Find the ChatOutput-WHzRB component's output
                    if result and "outputs" in result:
                        for output_group in result["outputs"]:
                            if "outputs" in output_group:
                                for output in output_group["outputs"]:
                                    if output.get("component_id") == "ChatOutput-WHzRB":
                                        # Return just the message object from the output
                                        return output.get("outputs", {}).get("message", {}).get("message")
                    
                    logger.error("Could not find ChatOutput-WHzRB component output")
                    return None
                    
                except Exception as e:
                    # If response is not JSON, use the text as error message
                    error_msg = response.text or str(e)
                    logger.error(f"Error parsing flow response: {error_msg}")
                    return None
                
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (4xx, 5xx)
            error_msg = f"HTTP {e.response.status_code}"
            try:
                error_data = e.response.json()
                if isinstance(error_data, dict):
                    error_msg = error_data.get('detail', error_msg)
            except:
                error_msg = e.response.text or error_msg
            
            logger.error(f"Error executing flow {flow_id}: {error_msg}")
            return None
            
        except Exception as e:
            logger.error(f"Error executing flow {flow_id}: {str(e)}")
            return None
