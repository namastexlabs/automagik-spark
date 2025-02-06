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
    """Workflow synchronization class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize workflow sync."""
        self.session = session
        self._manager = None
        self._client = None

    async def _get_manager(self) -> LangFlowManager:
        """Get or create LangFlow manager."""
        if not self._manager:
            self._manager = LangFlowManager(self.session)
        return self._manager

    async def __aenter__(self):
        """Enter the async context."""
        self._manager = await self._get_manager()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        if self._manager:
            await self._manager.close()
            self._manager = None

    async def execute_workflow(
        self,
        workflow: Workflow,
        task: Task,
        input_data: str
    ) -> Dict[str, Any]:
        """Execute a workflow with the given input data."""
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

        manager = self._manager
        if not manager:
            raise RuntimeError("Manager not initialized")

        try:
            # Update task status to running
            task.status = "running"
            task.started_at = datetime.now(timezone.utc)
            await self.session.commit()

            # Execute workflow
            result = await manager.run_flow(workflow.remote_flow_id, input_data)

            # Update task status to completed
            task.status = "completed"
            task.output_data = json.dumps(result)  # Store the entire result object
            task.finished_at = datetime.now(timezone.utc)
            await self.session.commit()

            return result

        except Exception as e:
            # Log error with traceback
            task.status = "failed"
            task.error = str(e)
            task.finished_at = datetime.now(timezone.utc)
            await self.session.commit()

            # Create error log with full traceback
            error_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level="error",
                message=f"{str(e)}\n{traceback.format_exc()}",
                created_at=datetime.now(timezone.utc)
            )
            self.session.add(error_log)
            await self.session.commit()

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
