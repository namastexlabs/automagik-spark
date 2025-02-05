"""Task management."""

import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Task, Workflow, TaskLog

logger = logging.getLogger(__name__)


class TaskManager:
    """Task management class."""

    def __init__(self, session: AsyncSession):
        """Initialize task manager."""
        self.session = session

    def _to_uuid(self, id_: Union[str, UUID]) -> UUID:
        """Convert string to UUID if needed."""
        if isinstance(id_, str):
            return UUID(id_)
        return id_

    async def get_task(self, task_id: Union[str, UUID]) -> Optional[Task]:
        """Get task by ID."""
        task_id = self._to_uuid(task_id)
        result = await self.session.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def list_tasks(
        self,
        workflow_id: Optional[Union[str, UUID]] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks with optional filters."""
        query = select(Task)
        
        if workflow_id:
            workflow_id = self._to_uuid(workflow_id)
            query = query.where(Task.workflow_id == workflow_id)
        if status:
            query = query.where(Task.status == status)
            
        query = query.order_by(Task.created_at.desc()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create_task(self, task: Dict[str, Any]) -> Task:
        """Create task."""
        if 'workflow_id' in task and isinstance(task['workflow_id'], str):
            task['workflow_id'] = UUID(task['workflow_id'])
        if 'id' not in task:
            task['id'] = uuid4()
        new_task = Task(**task)
        self.session.add(new_task)
        await self.session.commit()
        return new_task

    async def update_task(self, task_id: Union[str, UUID], task: Dict[str, Any]) -> Optional[Task]:
        """Update task."""
        task_id = self._to_uuid(task_id)
        existing = await self.get_task(task_id)
        if not existing:
            return None

        if 'workflow_id' in task and isinstance(task['workflow_id'], str):
            task['workflow_id'] = UUID(task['workflow_id'])

        for key, value in task.items():
            setattr(existing, key, value)

        await self.session.commit()
        return existing

    async def delete_task(self, task_id: Union[str, UUID]) -> bool:
        """Delete task."""
        task_id = self._to_uuid(task_id)
        task = await self.get_task(task_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def get_pending_tasks(self) -> List[Task]:
        """Get pending tasks."""
        result = await self.session.execute(
            select(Task)
            .where(Task.status == "pending")
            .order_by(Task.created_at.asc())
        )
        return result.scalars().all()

    async def get_failed_tasks(self) -> List[Task]:
        """Get failed tasks."""
        result = await self.session.execute(
            select(Task)
            .where(Task.status == "failed")
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def get_completed_tasks(self) -> List[Task]:
        """Get completed tasks."""
        result = await self.session.execute(
            select(Task)
            .where(Task.status == "completed")
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def get_running_tasks(self) -> List[Task]:
        """Get running tasks."""
        result = await self.session.execute(
            select(Task)
            .where(Task.status == "running")
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def get_tasks_by_workflow(self, workflow_id: Union[str, UUID]) -> List[Task]:
        """Get tasks by workflow ID."""
        workflow_id = self._to_uuid(workflow_id)
        result = await self.session.execute(
            select(Task)
            .where(Task.workflow_id == workflow_id)
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def retry_task(self, task_id: Union[str, UUID]) -> Optional[Task]:
        """Retry a failed task."""
        task_id = self._to_uuid(task_id)

        # Get task
        result = await self.session.execute(
            select(Task).filter(Task.id == task_id)
        )
        task = result.scalars().first()
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Check task status
        if task.status != "failed":
            raise ValueError("Task is not in failed state")

        # Check max retries
        if task.tries >= task.max_retries:
            raise ValueError("Task has reached maximum retries")

        # Create a retry log preserving the previous error
        previous_error = task.error
        if previous_error:
            task_log = TaskLog(
                id=uuid4(),
                task_id=task_id,
                level="error",
                message=f"Previous error: {previous_error}",
                created_at=datetime.now(timezone.utc)
            )
            self.session.add(task_log)

        # Reset task for retry with exponential backoff
        task.status = "pending"
        task.tries += 1
        task.error = None
        task.started_at = None
        task.finished_at = None
        task.next_retry_at = datetime.now(timezone.utc) + timedelta(seconds=2 ** task.tries)

        await self.session.commit()
        return task
