"""
Workflow synchronization module.

Handles synchronization of workflows between LangFlow and Automagik.
Provides functionality for fetching, filtering, and syncing workflows.
"""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4
from datetime import timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import LANGFLOW_API_URL, LANGFLOW_API_KEY
from ..database.models import Workflow, WorkflowComponent, Task, TaskLog
from ..database.session import get_session
from .remote import LangFlowManager  # Import from .remote module

logger = logging.getLogger(__name__)


class WorkflowSync:
    """Workflow synchronization class.
    
    This class must be used as an async context manager to ensure proper initialization:
    
    async with WorkflowSync(session) as sync:
        result = await sync.execute_workflow(...)
    """
    
    def __init__(self, session: AsyncSession):
        """Initialize workflow sync."""
        self.session = session
        self._manager = None
        self._client = None
        self._initialized = False

    async def _get_manager(self) -> LangFlowManager:
        """Get or create LangFlow manager."""
        if not self._manager:
            self._manager = LangFlowManager(self.session)
        return self._manager

    async def __aenter__(self):
        """Enter the async context."""
        if not self._initialized:
            self._manager = await self._get_manager()
            self._initialized = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        if self._manager:
            await self._manager.close()
            self._manager = None
            self._initialized = False

    def _check_initialized(self):
        """Check if the manager is properly initialized."""
        if not self._initialized or not self._manager:
            raise RuntimeError(
                "Manager not initialized. WorkflowSync must be used as a context manager:\n"
                "async with WorkflowSync(session) as sync:\n"
                "    result = await sync.execute_workflow(...)"
            )

    async def execute_workflow(
        self,
        workflow: Workflow,
        task: Task,
        input_data: str
    ) -> Dict[str, Any]:
        """Execute a workflow with the given input data."""
        # Check initialization
        self._check_initialized()

        if not workflow.input_component or not workflow.output_component:
            task.status = "failed"
            task.error = "Missing input/output components"
            task.started_at = datetime.now(timezone.utc)
            await self.session.commit()
            
            # Create error log
            error_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level="error",
                message=f"Missing input/output components",
                created_at=datetime.now(timezone.utc)
            )
            self.session.add(error_log)
            await self.session.commit()
            
            raise ValueError("Missing input/output components")

        try:
            # Update task status to running
            task.status = "running"
            task.started_at = datetime.now(timezone.utc)
            await self.session.commit()

            # Execute workflow
            result = await self._manager.run_flow(workflow.remote_flow_id, input_data)

            # Update task status to completed
            task.status = "completed"
            task.output_data = json.dumps(result)  # Store the entire result object
            task.finished_at = datetime.now(timezone.utc)
            await self.session.commit()

            return result

        except httpx.HTTPStatusError as e:
            error_msg = f"Failed to execute workflow: {e} - {e.response.text}"
            task.error = error_msg
            task.status = "failed"
            task.finished_at = datetime.now(timezone.utc)
            await self.session.commit()
            
            # Log the error with traceback
            error_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level="error",
                message=f"{error_msg}\n{traceback.format_exc()}",
                created_at=datetime.now(timezone.utc)
            )
            self.session.add(error_log)
            await self.session.commit()
            
            # Re-raise the exception
            raise

        except Exception as e:
            # Log the error with full traceback
            error_msg = f"Failed to execute workflow: {str(e)}"
            error_traceback = traceback.format_exc()
            
            # Update task status
            task.status = "failed"
            task.error = error_msg
            task.finished_at = datetime.now(timezone.utc)
            await self.session.commit()
            
            # Create error log with traceback
            error_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level="error",
                message=f"{error_msg}\n{error_traceback}",
                created_at=datetime.now(timezone.utc)
            )
            self.session.add(error_log)
            await self.session.commit()
            
            # Re-raise the exception
            raise

    def _get_base_url(self) -> str:
        """Get base URL for LangFlow API."""
        if not hasattr(self, '_base_url') or self._base_url is None:
            self._base_url = LANGFLOW_API_URL
        return self._base_url

    async def close(self):
        """Close LangFlowManager."""
        if self._manager:
            await self._manager.close()
            self._manager = None
