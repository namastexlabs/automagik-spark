"""
Flow management module.

Provides the main interface for managing flows
"""

import logging
from typing import Dict, List, Optional, Any
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Flow, Schedule, Task
from .remote import RemoteFlowManager
from .task import TaskManager
from .local import LocalFlowManager

logger = logging.getLogger(__name__)


class FlowManager:
    """Flow management class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize flow manager."""
        self.session = session
        self.remote = RemoteFlowManager(session)
        self.task = TaskManager(session)
        self.local = LocalFlowManager(session)

    async def __aenter__(self):
        """Enter context manager."""
        await self.remote.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        await self.remote.__aexit__(exc_type, exc_val, exc_tb)

    # Remote flow operations
    async def list_remote_flows(self) -> Dict[str, List[Dict]]:
        """List remote flows from LangFlow API."""
        return await self.remote.list_remote_flows()

    async def get_flow_components(self, flow_id: str) -> List[Dict[str, Any]]:
        """Get flow components from LangFlow API."""
        return await self.remote.get_flow_components(flow_id)

    async def sync_flow(
        self,
        flow_id: str,
        input_component: str,
        output_component: str
    ) -> Optional[UUID]:
        """Sync a flow from LangFlow API."""
        return await self.remote.sync_flow(flow_id, input_component, output_component)

    # Task operations
    async def run_flow(
        self,
        flow_id: UUID,
        input_data: Dict[str, Any]
    ) -> Optional[UUID]:
        """Run a flow with input data."""
        return await self.task.run_flow(flow_id, input_data)

    async def list_tasks(
        self,
        flow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks from database."""
        return await self.task.list_tasks(flow_id, status, limit)

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return await self.task.get_task(task_id)

    async def retry_task(self, task_id: str) -> Optional[Task]:
        """Retry a failed task."""
        return await self.task.retry_task(task_id)

    # Local flow operations
    async def get_flow(self, flow_id: str) -> Optional[Flow]:
        """Get a flow by ID."""
        return await self.local.get_flow(flow_id)

    async def list_flows(self) -> List[Flow]:
        """List all flows from the local database."""
        return await self.local.list_flows()

    async def delete_flow(self, flow_id: str) -> bool:
        """Delete a flow from local database."""
        return await self.local.delete_flow(flow_id)
