"""LangFlow API integration."""

import json
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

import httpx

from ...api.config import get_langflow_api_url, get_langflow_api_key
from ...api.models import (
    WorkflowBase,
    WorkflowCreate,
    WorkflowResponse,
)
from ..database.models import Workflow
from ..database.session import get_session

logger = logging.getLogger(__name__)


class LangFlowManager:
    """LangFlow API integration."""

    def __init__(self, session=None):
        """Initialize LangFlow manager."""
        self.session = session
        self.api_url = get_langflow_api_url()
        self.api_key = get_langflow_api_key()
        self.headers = {
            "accept": "application/json",
        }
        if self.api_key:
            self.headers["x-api-key"] = self.api_key

    async def get_workflow(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow from LangFlow API."""
        url = f"{self.api_url}/api/v1/flows/{source_id}"
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to get workflow {source_id}: {e}")
                return None

    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List workflows from LangFlow API."""
        url = f"{self.api_url}/api/v1/flows"
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to list workflows: {e}")
                return []

    async def run_workflow(
        self, source_id: str, input_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Run workflow on LangFlow API."""
        url = f"{self.api_url}/api/v1/flows/{source_id}/run"
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.post(url, json=input_data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to run workflow {source_id}: {e}")
                return None

    async def sync_workflows(self) -> List[Workflow]:
        """Sync workflows from LangFlow API."""
        # Get remote workflows
        remote_workflows = await self.list_workflows()
        if not remote_workflows:
            return []

        # Get local workflows
        async with get_session() as session:
            local_workflows = await session.execute(
                select(Workflow).where(Workflow.remote_flow_id.isnot(None))
            )
            local_workflows = {
                w.remote_flow_id: w for w in local_workflows.scalars().all()
            }

            # Update or create workflows
            synced_workflows = []
            for remote_workflow in remote_workflows:
                source_id = remote_workflow["id"]
                if source_id in local_workflows:
                    # Update existing workflow
                    workflow = local_workflows[source_id]
                    workflow.name = remote_workflow["name"]
                    workflow.description = remote_workflow.get("description")
                    workflow.metadata = remote_workflow.get("metadata", {})
                else:
                    # Create new workflow
                    workflow = Workflow(
                        name=remote_workflow["name"],
                        description=remote_workflow.get("description"),
                        remote_flow_id=source_id,
                        metadata=remote_workflow.get("metadata", {}),
                    )
                    session.add(workflow)

                synced_workflows.append(workflow)

            await session.commit()
            return synced_workflows
