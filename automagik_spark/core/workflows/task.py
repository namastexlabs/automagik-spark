
"""Task management."""

import logging
import inspect
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Task, TaskLog

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
        """Get a task by ID.
        
        Args:
            task_id (Union[str, UUID]): The ID of the task to retrieve.
            
        Returns:
            Optional[Task]: The task if found, None otherwise.
        """
        task_id = self._to_uuid(task_id)
        # Clear any cached queries
        self.session.expire_all()
        stmt = select(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        task = result.scalar_one_or_none()
        if inspect.isawaitable(task):
            task = await task
        return task

    async def update_task_fields(self, task: Task, updates: Dict[str, Any]) -> Task:
        """Update specific fields of a task.
        
        Args:
            task (Task): The task to update.
            updates (Dict[str, Any]): Dictionary of field names and values to update.
            
        Returns:
            Task: The updated task.
        """
        for field, value in updates.items():
            setattr(task, field, value)
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task

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
        return result.scalars().all()

    async def create_task(self, task: Dict[str, Any]) -> Task:
        """Create a task."""
        task_obj = Task(
            id=UUID(task.get("id")) if task.get("id") else uuid4(),
            workflow_id=UUID(task["workflow_id"]),  # Always convert to UUID
            status=task.get("status", "pending"),
            input_data=task.get("input_data"),
            error=task.get("error"),
            tries=task.get("tries", 0),
            max_retries=task.get("max_retries", 3),
            next_retry_at=task.get("next_retry_at"),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            started_at=task.get("started_at"),
            finished_at=task.get("finished_at")
        )

        self.session.add(task_obj)
        await self.session.flush()
        await self.session.commit()  # Ensure the task is persisted
        await self.session.refresh(task_obj)
        return task_obj

    async def update_task(self, task_id: Union[str, UUID], task: Dict[str, Any]) -> Optional[Task]:
        """Update a task.

        Args:
            task_id (Union[str, UUID]): The ID of the task to update.
            task (Dict[str, Any]): Dictionary of task fields to update.

        Returns:
            Optional[Task]: The updated task if successful, None otherwise.
        """
        try:
            existing_task = await self.get_task(task_id)
            if not existing_task:
                return None

            # Update task fields
            updates = {}
            for key, value in task.items():
                if hasattr(existing_task, key):
                    updates[key] = value

            # Update the task
            updated_task = await self.update_task_fields(existing_task, updates)
            await self.session.commit()
            return updated_task

        except Exception as e:
            logger.error(f"Failed to update task {task_id}: {str(e)}")
            await self.session.rollback()
            return None

    async def delete_task(self, task_id: Union[str, UUID]) -> bool:
        """Delete a task and its associated logs.

        Args:
            task_id (Union[str, UUID]): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted, False otherwise.
            
        Raises:
            ValueError: If there was an error during deletion.
        """
        try:
            task_id = self._to_uuid(task_id)
            
            # First verify the task exists
            task = await self.get_task(task_id)
            if not task:
                return False
                
            # Delete related task logs first
            await self.session.execute(
                delete(TaskLog).where(TaskLog.task_id == task_id)
            )
            
            # Delete the task
            await self.session.execute(
                delete(Task).where(Task.id == task_id)
            )
            
            # Commit the changes and clear cache
            await self.session.commit()
            self.session.expire_all()
            
            # Verify deletion
            task = await self.get_task(task_id)
            return task is None
            
        except Exception as e:
            logger.error(f"Failed to delete task {task_id}: {str(e)}")
            await self.session.rollback()
            raise ValueError(f"Failed to delete task: {str(e)}")

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
        """Retry a failed task.

        Args:
            task_id (Union[str, UUID]): The ID of the task to retry.

        Returns:
            Optional[Task]: The retried task if successful, None otherwise.
            
        Raises:
            ValueError: If the task is not found, not in failed state, or has reached max retries.
        """
        try:
            task = await self.get_task(task_id)
            if not task:
                raise ValueError("Task not found")

            # Check retry limits first
            if task.tries >= task.max_retries:
                raise ValueError("Task has reached maximum retries")

            # Ensure task is in failed state
            if task.status != "failed":
                raise ValueError("Task is not in failed state")

            # Create a task log for the previous error
            if task.error:
                error_log = TaskLog(
                    id=uuid4(),
                    task_id=task_id,
                    level="error",
                    message=f"Previous error: {task.error}",
                    created_at=datetime.utcnow()
                )
                self.session.add(error_log)

            # Create task log for retry
            retry_log = TaskLog(
                id=uuid4(),
                task_id=task_id,
                level="info",
                message=f"Retrying task after {2 ** task.tries} seconds",
                created_at=datetime.utcnow()
            )
            self.session.add(retry_log)

            # Update task for retry
            updates = {
                "status": "pending",
                "tries": task.tries + 1,
                "error": None,
                "next_retry_at": datetime.utcnow() + timedelta(seconds=2 ** task.tries),
                "updated_at": datetime.utcnow()
            }
            
            task = await self.update_task_fields(task, updates)
            await self.session.commit()
            return task

        except ValueError:
            # Re-raise ValueError with original message
            raise
        except Exception as e:
            logger.error(f"Failed to retry task {task_id}: {str(e)}")
            raise ValueError(f"Failed to retry task: {str(e)}")


