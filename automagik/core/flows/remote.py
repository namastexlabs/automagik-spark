"""Remote flow management module."""

import logging
from collections import defaultdict
from typing import Dict, List, Any, Optional
from uuid import UUID, uuid4

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config import LANGFLOW_API_URL, LANGFLOW_API_KEY
from ..database.models import Flow

logger = logging.getLogger(__name__)

class RemoteFlowManager:
    """Remote flow management class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize remote flow manager."""
        self.session = session
        self.client = None

    async def __aenter__(self):
        """Initialize client when entering context."""
        headers = {
            'accept': 'application/json'
        }
        if LANGFLOW_API_KEY:
            headers["x-api-key"] = LANGFLOW_API_KEY
        logger.debug(f"Using LangFlow API URL: {LANGFLOW_API_URL}")
        logger.debug(f"Headers: {headers}")
        self.client = httpx.AsyncClient(base_url=LANGFLOW_API_URL, headers=headers, verify=False)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close client when exiting context."""
        if self.client:
            await self.client.aclose()
            self.client = None

    async def _ensure_client(self):
        """Ensure client is initialized."""
        if not self.client:
            headers = {
                'accept': 'application/json'
            }
            if LANGFLOW_API_KEY:
                headers["x-api-key"] = LANGFLOW_API_KEY
            logger.debug(f"Using LangFlow API URL: {LANGFLOW_API_URL}")
            logger.debug(f"Headers: {headers}")
            self.client = httpx.AsyncClient(base_url=LANGFLOW_API_URL, headers=headers, verify=False)

    async def list_remote_flows(self) -> Dict[str, List[Dict]]:
        """List remote flows from LangFlow API."""
        try:
            await self._ensure_client()
            # Get folders first
            folders_response = await self.client.get("/folders/")
            folders_response.raise_for_status()
            folders_data = folders_response.json()
            folders = {folder["id"]: folder["name"] for folder in folders_data}

            # Get flows
            flows_response = await self.client.get("/flows/")
            flows_response.raise_for_status()
            flows = flows_response.json()

            # Group flows by folder, only including flows with valid folder IDs
            flows_by_folder = defaultdict(list)
            for flow in flows:
                folder_id = flow.get("folder_id")
                if folder_id and folder_id in folders:
                    folder_name = folders[folder_id]
                    flows_by_folder[folder_name].append(flow)

            return dict(flows_by_folder)
        except Exception as e:
            logger.error(f"Error listing remote flows: {e}")
            raise

    async def get_flow_components(self, flow_id: str) -> List[Dict[str, Any]]:
        """Get flow components from LangFlow API."""
        try:
            await self._ensure_client()
            response = await self.client.get(f"/flows/{flow_id}")
            response.raise_for_status()
            flow_data = response.json()

            # Extract components from flow data
            components = []
            for node in flow_data["data"]["nodes"]:
                node_type = node["data"].get("type")
                if node_type in ["ChatInput", "ChatOutput"]:
                    components.append({
                        "id": node["id"],
                        "type": node_type
                    })
            return components
        except Exception as e:
            logger.error(f"Error getting flow components: {e}")
            return []

    async def sync_flow(
        self,
        flow_id: str,
        input_component: str,
        output_component: str
    ) -> Optional[UUID]:
        """Sync a flow from LangFlow API."""
        try:
            await self._ensure_client()
            # Get flow data from LangFlow API
            response = await self.client.get(f"/flows/{flow_id}")
            response.raise_for_status()
            flow_data = response.json()

            # Check if flow already exists
            stmt = select(Flow).where(Flow.source_id == flow_id)
            result = await self.session.execute(stmt)
            existing_flow = result.scalar_one_or_none()

            if existing_flow:
                # Update existing flow
                existing_flow.name = flow_data.get("name", "Untitled Flow")
                existing_flow.description = flow_data.get("description", "")
                existing_flow.input_component = input_component
                existing_flow.output_component = output_component
                existing_flow.data = flow_data.get("data", {})
                existing_flow.folder_id = flow_data.get("folder_id")
                existing_flow.folder_name = flow_data.get("folder_name")
                existing_flow.icon = flow_data.get("icon")
                existing_flow.icon_bg_color = flow_data.get("icon_bg_color")
                existing_flow.gradient = bool(flow_data.get("gradient", False))
                existing_flow.flow_version += 1
                await self.session.commit()
                return existing_flow.id

            # Create new flow
            new_flow = Flow(
                id=uuid4(),
                source_id=flow_id,  # Use the original flow_id
                name=flow_data.get("name", "Untitled Flow"),
                description=flow_data.get("description", ""),
                input_component=input_component,
                output_component=output_component,
                data=flow_data.get("data", {}),
                source="langflow",
                flow_version=1,
                folder_id=flow_data.get("folder_id"),
                folder_name=flow_data.get("folder_name"),
                icon=flow_data.get("icon"),
                icon_bg_color=flow_data.get("icon_bg_color"),
                gradient=bool(flow_data.get("gradient", False))
            )

            self.session.add(new_flow)
            await self.session.commit()
            return new_flow.id
        except Exception as e:
            logger.error(f"Error syncing flow: {e}")
            return None
