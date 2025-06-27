
"""
Task Runner Module

Handles execution of workflow tasks, including input/output processing and error handling.
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database.models import Task, TaskLog
from ..workflows.manager import WorkflowManager

logger = logging.getLogger(__name__)

class TaskRunner:
    """Handles execution of workflow tasks."""
    
    def __init__(self, session: AsyncSession, workflow_manager: WorkflowManager):
        """
        Initialize task runner.
        
        Args:
            session: Database session
            workflow_manager: Workflow manager instance
        """
        self.session = session
        self.workflow_manager = workflow_manager
    
    async def execute_task(self, task_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Execute a task.
        
        Args:
            task_id: ID of task to execute
            
        Returns:
            Task output data if successful
        """
        try:
            # Get task
            query = select(Task).filter(Task.id == task_id)
            result = await self.session.execute(query)
            task = result.scalar_one_or_none()
            
            if not task:
                logger.error(f"Task {task_id} not found")
                return None
            
            # Update task status
            task.status = 'running'
            task.started_at = datetime.utcnow()
            task.tries += 1  # Increment tries counter
            task.error = None  # Clear any previous error
            task.updated_at = datetime.utcnow()
            await self.session.commit()
            
            try:
                # Execute workflow
                output = await self.workflow_manager.run_workflow(task.workflow_id, task.input_data)
                if not output:
                    raise Exception("Workflow execution failed - no output returned")
                
                # Update task on success
                task.status = 'completed'
                task.completed_at = datetime.utcnow()
                task.output_data = output
                task.updated_at = datetime.utcnow()
                await self.session.commit()
                
                return output
                
            except Exception as e:
                # Handle execution error
                error_msg = str(e)
                logger.error(f"Task {task_id} failed: {error_msg}")
                await self._log_task_error(task, error_msg)
                
                # Check if should retry
                if task.tries < task.max_retries:
                    task.status = 'pending'  # Will be retried
                    logger.info(f"Task {task_id} will be retried ({task.tries}/{task.max_retries})")
                else:
                    task.status = 'failed'  # Max retries exceeded
                    logger.info(f"Task {task_id} failed after {task.tries} attempts")
                
                task.error = error_msg  # Store error message
                task.completed_at = datetime.utcnow()  # Mark completion time even for failures
                task.updated_at = datetime.utcnow()
                await self.session.commit()
                return None
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error executing task {task_id}: {error_msg}")
            
            # Try to update task status if we have the task object
            try:
                if 'task' in locals():
                    task.status = 'failed'
                    task.error = error_msg
                    task.completed_at = datetime.utcnow()
                    task.updated_at = datetime.utcnow()
                    await self.session.commit()
            except Exception:
                pass  # Ignore errors in error handling
            
            return None
    
    async def _log_task_error(self, task: Task, error: str):
        """Log a task error."""
        try:
            log = TaskLog(
                task_id=task.id,
                level='error',
                message=error
            )
            self.session.add(log)
            await self.session.commit()
            
        except Exception as e:
            logger.error(f"Error logging task error: {str(e)}")
    
    async def retry_task(self, task_id: uuid.UUID) -> bool:
        """
        Retry a failed task.
        
        Args:
            task_id: ID of task to retry
            
        Returns:
            True if retry was initiated
        """
        try:
            # Get task
            query = select(Task).filter(Task.id == task_id)
            result = await self.session.execute(query)
            task = result.scalar_one_or_none()
            
            if not task:
                logger.error(f"Task {task_id} not found")
                return False
            
            if task.status != 'failed':
                logger.error(f"Task {task_id} is not in failed state")
                return False
                
            if task.tries >= task.max_retries:
                logger.error(f"Task {task_id} has exceeded maximum retries ({task.tries}/{task.max_retries})")
                return False
            
            # Reset task status for retry
            task.status = 'pending'
            task.error = None
            task.started_at = None
            task.completed_at = None
            await self.session.commit()
            
            # Execute task
            asyncio.create_task(self.execute_task(task_id))
            return True
            
        except Exception as e:
            logger.error(f"Error retrying task {task_id}: {str(e)}")
            return False


