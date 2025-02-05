"""
Workflow management.

Provides the main interface for managing workflows and remote flows
"""

import logging
from typing import Dict, List, Optional, Any
from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Workflow, Schedule, Task, WorkflowComponent
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
        flow = await self.langflow.sync_flow(flow_id)
        if not flow:
            return []
        return flow["components"]

    async def sync_flow(
        self,
        flow_id: str,
        input_component: Optional[str] = None,
        output_component: Optional[str] = None
    ) -> Optional[Workflow]:
        """Sync a flow from LangFlow API into a local workflow."""
        result = await self.langflow.sync_flow(flow_id)
        if not result:
            return None

        flow_data = result["flow"]

        # Check if workflow already exists
        stmt = select(Workflow).where(Workflow.remote_flow_id == flow_id)
        result = await self.session.execute(stmt)
        existing_workflow = result.scalar_one_or_none()

        if existing_workflow:
            # Update existing workflow
            existing_workflow.name = flow_data["name"]
            existing_workflow.description = flow_data.get("description")
            existing_workflow.data = flow_data["data"]
            existing_workflow.folder_id = flow_data.get("folder_id")
            existing_workflow.folder_name = flow_data.get("folder_name")
            existing_workflow.icon = flow_data.get("icon")
            existing_workflow.icon_bg_color = flow_data.get("icon_bg_color")
            existing_workflow.gradient = flow_data.get("gradient", False)
            existing_workflow.liked = flow_data.get("liked", False)
            existing_workflow.tags = flow_data.get("tags", [])
            if input_component:
                existing_workflow.input_component = input_component
            if output_component:
                existing_workflow.output_component = output_component
            workflow = existing_workflow
        else:
            # Create new workflow
            workflow = Workflow(
                id=UUID(flow_data["id"]),
                name=flow_data["name"],
                description=flow_data.get("description"),
                data=flow_data["data"],
                source="langflow",
                remote_flow_id=flow_data["id"],
                input_component=input_component,
                output_component=output_component,
                folder_id=flow_data.get("folder_id"),
                folder_name=flow_data.get("folder_name"),
                icon=flow_data.get("icon"),
                icon_bg_color=flow_data.get("icon_bg_color"),
                gradient=flow_data.get("gradient", False),
                liked=flow_data.get("liked", False),
                tags=flow_data.get("tags", [])
            )
            self.session.add(workflow)

        await self.session.commit()
        return workflow

    # Local workflow operations
    async def list_workflows(self) -> List[Workflow]:
        """List all workflows from the local database."""
        result = await self.session.execute(select(Workflow))
        return result.scalars().all()

    async def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID."""
        if not workflow_id:
            return None

        if len(workflow_id) < 32:
            # Handle truncated UUID by querying all workflows and matching prefix
            result = await self.session.execute(select(Workflow))
            workflows = result.scalars().all()
            for workflow in workflows:
                if str(workflow.id).startswith(workflow_id):
                    return workflow
            return None
        try:
            uuid_obj = UUID(workflow_id)
            return await self.session.get(Workflow, uuid_obj)
        except ValueError:
            return None

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow from local database."""
        if not workflow_id:
            raise ValueError("Invalid UUID format")

        # Try to parse the UUID first to validate format
        try:
            if len(workflow_id) < 8:
                raise ValueError()
            if len(workflow_id) == 36:  # Full UUID
                UUID(workflow_id)
            elif not all(c in '0123456789abcdefABCDEF' for c in workflow_id):
                raise ValueError()
        except ValueError:
            raise ValueError("Invalid UUID format")

        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return False

        # Delete related schedules
        result = await self.session.execute(
            select(Schedule).where(Schedule.workflow_id == workflow.id)
        )
        schedules = result.scalars().all()
        for schedule in schedules:
            await self.session.delete(schedule)
        
        # Delete related tasks
        result = await self.session.execute(
            select(Task).where(Task.workflow_id == workflow.id)
        )
        tasks = result.scalars().all()
        for task in tasks:
            await self.session.delete(task)

        # Delete related components
        result = await self.session.execute(
            select(WorkflowComponent).where(WorkflowComponent.workflow_id == workflow.id)
        )
        components = result.scalars().all()
        for component in components:
            await self.session.delete(component)

        # Delete the workflow
        await self.session.delete(workflow)
        await self.session.commit()
        return True

    # Task operations
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return await self.task.get_task(task_id)

    async def list_tasks(
        self,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks from database."""
        return await self.task.list_tasks(workflow_id, status, limit)

    async def retry_task(self, task_id: str) -> Optional[Task]:
        """Retry a failed task."""
        return await self.task.retry_task(task_id)

    async def run_workflow(
        self,
        workflow_id: UUID,
        input_data: Dict[str, Any]
    ) -> Optional[Task]:
        """Run a workflow with input data."""
        workflow = await self.get_workflow(str(workflow_id))
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        task = Task(
            workflow_id=workflow_id,
            input_data=input_data,
            status="pending"
        )
        self.session.add(task)
        await self.session.commit()
        return task
