"""
Workflow management.

Provides the main interface for managing workflows and remote flows
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID, uuid4
from datetime import timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import cast
from sqlalchemy import String

from ..database.models import Workflow, Schedule, Task, WorkflowComponent, TaskLog
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
        existing_workflow = result.scalars().first()

        if existing_workflow:
            # Update existing workflow
            existing_workflow.name = flow_data["name"]
            existing_workflow.description = flow_data.get("description")
            existing_workflow.data = flow_data["data"]
            existing_workflow.input_component = input_component or flow_data.get("input_component")
            existing_workflow.output_component = output_component or flow_data.get("output_component")
            existing_workflow.folder_id = flow_data.get("folder_id")
            existing_workflow.folder_name = flow_data.get("folder_name")
            existing_workflow.icon = flow_data.get("icon")
            existing_workflow.icon_bg_color = flow_data.get("icon_bg_color")
            existing_workflow.gradient = bool(flow_data.get("gradient", False))
            existing_workflow.liked = bool(flow_data.get("liked", False))
            existing_workflow.tags = flow_data.get("tags", [])
            existing_workflow.updated_at = datetime.now(timezone.utc)

            await self.session.commit()
            # Merge the existing workflow with the session to ensure we get the same instance
            existing_workflow = await self.session.merge(existing_workflow)
            return existing_workflow
        else:
            # Create new workflow
            workflow = Workflow(
                id=uuid4(),  # Generate a new UUID for the workflow
                name=flow_data["name"],
                description=flow_data.get("description"),
                data=flow_data["data"],
                source="langflow",
                remote_flow_id=flow_id,
                flow_version=1,
                input_component=input_component,
                output_component=output_component,
                folder_id=flow_data.get("folder_id"),
                folder_name=flow_data.get("folder_name"),
                icon=flow_data.get("icon"),
                icon_bg_color=flow_data.get("icon_bg_color"),
                gradient=bool(flow_data.get("gradient", False)),
                liked=bool(flow_data.get("liked", False)),
                tags=flow_data.get("tags", [])
            )

            self.session.add(workflow)
            await self.session.commit()
            return workflow

    # Local workflow operations
    async def list_workflows(self, options: dict = None) -> List[Workflow]:
        """List all workflows from the local database."""
        stmt = select(Workflow)

        # Apply eager loading options
        if options and options.get("joinedload"):
            for relationship in options["joinedload"]:
                stmt = stmt.options(joinedload(getattr(Workflow, relationship)))

        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

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
        """Delete a workflow and all its related objects."""
        # Validate UUID format
        if not workflow_id:
            raise ValueError("Invalid UUID format")
        
        # Try exact match first (for full UUID)
        try:
            if len(workflow_id) == 36:  # Full UUID
                uuid_obj = UUID(workflow_id)
                exact_match = True
            elif len(workflow_id) >= 8 and all(c in '0123456789abcdefABCDEF' for c in workflow_id):
                exact_match = False
            else:
                raise ValueError("Invalid UUID format")
        except ValueError:
            raise ValueError("Invalid UUID format")
        
        try:
            # Build query based on match type
            query = select(Workflow).options(
                joinedload(Workflow.components),
                joinedload(Workflow.schedules),
                joinedload(Workflow.tasks).joinedload(Task.logs)
            )
            
            if exact_match:
                query = query.where(Workflow.id == uuid_obj)
            else:
                query = query.where(cast(Workflow.id, String).like(f"{workflow_id}%"))
            
            # Execute query
            result = await self.session.execute(query)
            workflow = result.unique().scalar_one_or_none()
            
            if not workflow:
                return False
            
            # Delete related objects first
            for task in workflow.tasks:
                # Delete task logs
                if task.logs:
                    for log in task.logs:
                        await self.session.delete(log)
                # Delete task
                await self.session.delete(task)
            
            # Delete schedules
            for schedule in workflow.schedules:
                await self.session.delete(schedule)
            
            # Delete components
            for component in workflow.components:
                await self.session.delete(component)
            
            # Finally delete the workflow
            await self.session.delete(workflow)
            await self.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete workflow: {str(e)}")
            await self.session.rollback()
            return False

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
        input_data: str
    ) -> Optional[Task]:
        """Run a workflow with input data."""
        workflow = await self.get_workflow(str(workflow_id))
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Create task
        task = Task(
            id=uuid4(),
            workflow_id=workflow_id,
            input_data=input_data,
            status="pending"
        )
        self.session.add(task)
        await self.session.commit()

        # Execute workflow
        from .sync import WorkflowSync
        sync = WorkflowSync(self.session)
        try:
            logger.debug(f"Executing workflow {workflow_id} with input: {input_data}")
            logger.debug(f"Workflow details: {workflow.__dict__}")
            result = await sync.execute_workflow(workflow, task, input_data)
            return task if result else None
        except Exception as e:
            logger.error(f"Failed to execute workflow: {e}", exc_info=True)
            task.status = "failed"
            task.error = str(e)
            task.finished_at = datetime.now(timezone.utc)
            await self.session.commit()
            return None
