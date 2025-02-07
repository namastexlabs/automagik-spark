"""LangFlow API integration."""

import json
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from ...api.config import get_langflow_api_url, get_langflow_api_key
from ...api.models import (
    WorkflowBase,
    WorkflowCreate,
    WorkflowResponse,
)
from ..database.models import Workflow
from ..database.session import get_session

logger = logging.getLogger(__name__)

LANGFLOW_API_URL = get_langflow_api_url()
LANGFLOW_API_KEY = get_langflow_api_key()


class LangFlowManager:
    """Manager for remote LangFlow operations."""

    def __init__(
        self,
        session: AsyncSession,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """Initialize LangFlow manager."""
        self.session = session
        self.api_url = api_url.rstrip("/") if api_url else LANGFLOW_API_URL.rstrip("/")  # Use default if not provided
        self.api_key = api_key if api_key else LANGFLOW_API_KEY  # Use default if not provided
        logger.debug(f"Initializing LangFlow manager with URL: {self.api_url} and API key: {self.api_key}")
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        if self.api_key:
            # Add API key to header
            self.headers["x-api-key"] = self.api_key
        logger.info(f"Headers: {self.headers}")
        self.client = None

    async def __aenter__(self):
        """Enter the async context."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                verify=False,
                headers=self.headers,
                base_url=f"{self.api_url}/api/v1",
                follow_redirects=True
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        if self.client:
            await self.client.aclose()

    async def list_remote_flows(self) -> List[Dict[str, Any]]:
        """List remote flows from LangFlow API."""
        try:
            url = "/flows/"  

            await self._ensure_client()
            logger.debug(f"Requesting flows from {url}")
            response = await self.client.get(url, follow_redirects=True)
            logger.debug(f"Response text: {response.text}")

            if response.status_code == 200:
                all_items = response.json()
                # Filter out components using the is_component flag
                flows = [item for item in all_items if not item.get("is_component", False)]
                return flows
            else:
                response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Failed to list flows: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            logger.error(f"Response content was: {response.content}")
            logger.error(f"Response text was: {response.text}")
            raise

    async def sync_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Sync a flow from the remote API."""
        try:
            await self._ensure_client()
            logger.info(f"Requesting flow {flow_id}")
            response = await self.client.get(f"/flows/{flow_id}", follow_redirects=True)
          
            if response.status_code == 200:
                try:
                    flow_data = response.json()
                    return flow_data
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse flow data as JSON: {str(e)}")
                    return None
            elif response.status_code == 404:
                logger.warning(f"Flow {flow_id} not found")
                return None
            else:
                logger.error(f"Unexpected status code {response.status_code} when fetching flow {flow_id}")
                response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error syncing flow {flow_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error syncing flow {flow_id}: {str(e)}")
            return None

    async def get_flow_components(self, flow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get components used in a flow."""
        try:
            components = []
            for node in flow_data.get("data", {}).get("nodes", []):
                node_data = node.get("data", {})
                if node_data.get("node"):
                    component = node_data["node"]
                    # Add the node ID to the component data
                    component["id"] = node.get("id")
                    components.append(component)
            return components
        except Exception as e:
            logger.error(f"Failed to get flow components: {e}")
            raise

    async def create_folder(self, name: str) -> Dict[str, Any]:
        """Create a folder in LangFlow."""
        await self._ensure_client()
        try:
            logger.info(f"Creating folder {name} in LangFlow")
            response = await self.client.post("/folders/", json={"name": name})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error creating folder {name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating folder {name}: {e}")
            raise

    async def run_flow(
        self,
        flow_id: str,
        input_data: str,
        debug: bool = True  # This parameter is kept for backward compatibility
    ) -> Dict[str, Any]:
        """Execute a flow with the given input data.
        
        Args:
            flow_id: ID of the flow to execute
            input_data: Input string for the flow
            debug: Whether to run in debug mode (always True)
        
        Returns:
            Dict containing the flow output
        """
        await self._ensure_client()

        try:
            # Parse input_data as JSON if it's a valid JSON string
            try:
                input_value = json.loads(input_data)
            except json.JSONDecodeError:
                input_value = input_data

            # Build API payload
            payload = {
                "input_value": input_value,
                "tweaks": {},
                "output_type": "debug"  # We always want debug output since it returns everything
            }
            
            # Execute the flow
            logger.info(f"Executing flow {flow_id} with input_data: {input_data}")
            logger.info(f"API payload: {payload}")
            logger.info(f"Langflow Source: {self.api_url}")
            logger.info(f"Headers: {self.headers}")
            response = await self.client.post(
                f"/run/{flow_id}", 
                json=payload,
                timeout=600,  # 10 minutes
                follow_redirects=True
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")

            if response.status_code >= 400:
                error_text = response.text  # Get error text synchronously
                logger.error(f"LangFlow API error response: {error_text}")
                raise httpx.HTTPStatusError(f"HTTP {response.status_code}: {error_text}", request=response.request, response=response)

            # Check content type
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            elif 'text/html' in content_type:
                # If we got HTML when expecting JSON, there might be an issue with the API
                logger.error(f"Received HTML response when expecting JSON. Response: {response.text[:200]}...")
                raise ValueError("Received HTML response when expecting JSON. The API endpoint may be incorrect or the server may be misconfigured.")
            else:
                # For other content types, try JSON first, fallback to text
                try:
                    return response.json()
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse response as JSON. Content-Type: {content_type}, Response: {response.text[:200]}...")
                    raise ValueError(f"Failed to parse response as JSON. Content-Type: {content_type}")
        except Exception as e:
            logger.error(f"Failed to execute flow {flow_id}: {e}")
            raise

    async def _ensure_client(self):
        """Ensure client is initialized."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=f"{self.api_url}/api/v1",
                verify=False,
                headers=self.headers,
                follow_redirects=True
            )

    async def close(self):
        """Close the client."""
        if self.client:
            await self.client.aclose()
            self.client = None
