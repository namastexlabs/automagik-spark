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

    async def list_remote_flows(self) -> List[Dict[str, Any]]:
        """List remote flows from LangFlow API."""
        if not self.client:
            raise RuntimeError("Must be used within async context manager")
        try:
            response = await self.client.get("/api/v1/flows/")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error listing remote flows: {e}")
            raise

    async def sync_flow(self, flow_id: str, name: str = None, description: str = None, components: List[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Sync a flow from LangFlow API."""
        if not self.client:
            raise RuntimeError("Must be used within async context manager")
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
        if not self.client:
            raise RuntimeError("Must be used within async context manager")
        try:
            response = await self.client.post("/api/v1/folders/", json={"name": name})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error creating folder {name}: {e}")
            raise
