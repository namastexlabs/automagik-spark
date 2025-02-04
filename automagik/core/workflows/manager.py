"""
Workflow management.

Provides the main interface for managing workflows and remote flows
"""

import logging
from typing import Dict, List, Optional, Any
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Workflow, Schedule, Task
from .remote import LangFlowManager
from .task import TaskManager

logger = logging.getLogger(__name__)


class WorkflowManager:
    """Workflow management class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize workflow manager."""
        self.session = session
        self.langflow = LangFlowManager(session)
        self.task = TaskManager(session)

    async def __aenter__(self):
        """Enter context manager."""
        await self.langflow.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        await self.langflow.__aexit__(exc_type, exc_val, exc_tb)

    # Remote flow operations
    async def list_remote_flows(self) -> Dict[str, List[Dict]]:
        """List remote flows from LangFlow API."""
        return await self.langflow.list_remote_flows()

    async def get_flow_components(self, flow_id: str) -> List[Dict[str, Any]]:
        """Get flow components from LangFlow API."""
        return await self.langflow.get_flow_components(flow_id)

    async def sync_flow(
        self,
        flow_id: str,
        input_component: str,
        output_component: str
    ) -> Optional[UUID]:
        """Sync a flow from LangFlow API into a local workflow."""
        return await self.langflow.sync_flow(flow_id, input_component, output_component)

    # Task operations
    async def run_workflow(
        self,
        workflow_id: UUID,
        input_data: Dict[str, Any]
    ) -> Optional[UUID]:
        """Run a workflow with input data."""
        return await self.task.run_workflow(workflow_id, input_data)

    async def list_tasks(
        self,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks from database."""
        return await self.task.list_tasks(workflow_id, status, limit)

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return await self.task.get_task(task_id)

    async def retry_task(self, task_id: str) -> Optional[Task]:
        """Retry a failed task."""
        return await self.task.retry_task(task_id)

    # Local workflow operations
    async def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID."""
        result = await self.session.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        return result.scalar_one_or_none()

    async def list_workflows(self) -> List[Workflow]:
        """List all workflows from the local database."""
        result = await self.session.execute(select(Workflow))
        return result.scalars().all()

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow from local database."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return False

        await self.session.delete(workflow)
        await self.session.commit()
        return True
