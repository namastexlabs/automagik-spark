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

    def __init__(self, session: AsyncSession):
        """Initialize the LangFlow manager."""
        self.session = session
        self.api_url = LANGFLOW_API_URL
        self.api_key = LANGFLOW_API_KEY
        self.headers = {
            "accept": "application/json",
        }
        if self.api_key:
            self.headers["x-api-key"] = self.api_key
        self.client = None

    async def __aenter__(self):
        """Enter the async context."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=self.api_url,
                headers=self.headers,
                verify=False
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def close(self):
        """Close the client."""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def _ensure_client(self):
        """Ensure client is initialized."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=self.api_url,
                headers=self.headers,
                verify=False
            )

    async def list_remote_flows(self) -> List[Dict[str, Any]]:
        """List remote flows from LangFlow API."""
        await self._ensure_client()
        try:
            response = await self.client.get("/api/v1/flows/")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error listing remote flows: {e}")
            raise

    async def sync_flow(self, flow_id: str, name: str = None, description: str = None, components: List[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Sync a flow from LangFlow API."""
        await self._ensure_client()
        try:
            response = await self.client.get(f"/api/v1/flows/{flow_id}")
            response.raise_for_status()
            flow_data = response.json()
            
            # Update flow data with provided values
            if name:
                flow_data["name"] = name
            if description:
                flow_data["description"] = description
            
            # Get components if not provided
            if components is None:
                components = await self.get_flow_components(flow_data)
            
            return {
                "flow": flow_data,
                "components": components
            }
        except httpx.HTTPError as e:
            logger.error(f"Failed to sync flow {flow_id}: {e}")
            return None

    async def get_flow_components(self, flow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get components used in a flow."""
        try:
            components = []
            for node in flow_data.get("data", {}).get("nodes", []):
                if node.get("data", {}).get("node"):
                    components.append(node["data"]["node"])
            return components
        except Exception as e:
            logger.error(f"Failed to get flow components: {e}")
            raise

    async def create_folder(self, name: str) -> Dict[str, Any]:
        """Create a folder in LangFlow."""
        await self._ensure_client()
        try:
            response = await self.client.post("/api/v1/folders/", json={"name": name})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error creating folder {name}: {e}")
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
            logger.debug(f"Executing flow {flow_id} with input_data: {input_data}")
            logger.debug(f"API payload: {payload}")
            response = await self.client.post(
                f"/api/v1/run/{flow_id}",  # Use the /run/{flow_id} endpoint
                json=payload,
                timeout=600  # 10 minutes
            )
            
            if response.status_code >= 400:
                error_text = response.text  # Get error text synchronously
                logger.error(f"LangFlow API error response: {error_text}")
                raise httpx.HTTPStatusError(f"HTTP {response.status_code}: {error_text}", request=response.request, response=response)
                
            try:
                result = response.json()  # Get JSON synchronously since we already have the response
                logger.debug(f"Flow execution result: {result}")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON response: {response.text}")
                raise

        except Exception as e:
            logger.error(f"Failed to execute flow {flow_id}: {e}")
            raise
