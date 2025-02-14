
"""
Workflow synchronization module.

Handles synchronization of workflows between LangFlow and Automagik.
Provides functionality for fetching, filtering, and syncing workflows.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from datetime import timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..config import LANGFLOW_API_URL, LANGFLOW_API_KEY
from ..database.models import Workflow, WorkflowComponent, Task, TaskLog, WorkflowSource
from ..database.session import get_session
from .remote import LangFlowManager  # Import from .remote module

logger = logging.getLogger(__name__)


class WorkflowSync:
    """Workflow synchronization class.
    
    This class must be used as a context manager to ensure proper initialization:
    
    with WorkflowSync(session) as sync:
        result = sync.execute_workflow(...)
    """

    def __init__(self, session: Session):
        """Initialize workflow sync."""
        self.session = session
        self._manager = None
        self._initialized = False

    def __enter__(self):
        """Enter the context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context."""
        if self._manager:
            if hasattr(self._manager, 'close'):
                self._manager.close()
            self._manager = None

    def _get_workflow_source(self, workflow_id: str) -> Optional[WorkflowSource]:
        """Get the workflow source for a given workflow ID."""
        workflow = self.session.get(Workflow, workflow_id)
        if not workflow:
            return None
        
        # Return the associated workflow source
        return workflow.workflow_source

    def execute_workflow(self, workflow: Workflow, input_data: str | Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a workflow with the given input data."""
        try:
            # Get workflow source
            source = self._get_workflow_source(str(workflow.id))
            if not source:
                raise ValueError(f"No source found for workflow {workflow.id}")

            logger.info(f"Using workflow source: {source.url}")
            logger.info(f"Remote flow ID: {workflow.remote_flow_id}")

            # Initialize LangFlow manager with the correct source settings
            api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
            self._manager = LangFlowManager(self.session, api_url=source.url, api_key=api_key)
            
            # Run the workflow
            result = self._manager.run_workflow_sync(workflow.remote_flow_id, input_data)
            if not result:
                raise ValueError("No result from workflow execution")

            return result
        except Exception as e:
            logger.error(f"Failed to execute workflow: {str(e)}")
            raise e


class WorkflowSyncSync:
    """Workflow synchronization class for synchronous workflow execution.
    
    This class must be used as a context manager to ensure proper initialization:
    
    with WorkflowSyncSync(session) as sync:
        result = sync.execute_workflow(...)
    """

    def __init__(self, session: Session):
        """Initialize workflow sync."""
        self.session = session
        self._manager = None
        self._initialized = False

    def __enter__(self):
        """Enter the context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context."""
        if self._manager:
            if hasattr(self._manager, 'close'):
                self._manager.close()
            self._manager = None

    def _get_workflow_source(self, workflow_id: str) -> Optional[WorkflowSource]:
        """Get the workflow source for a given workflow ID."""
        workflow = self.session.get(Workflow, workflow_id)
        if not workflow:
            return None
        
        # Return the associated workflow source
        return workflow.workflow_source

    def execute_workflow(self, workflow: Workflow, input_data: str) -> Optional[Dict[str, Any]]:
        """Execute a workflow with the given input data."""
        try:
            # Get workflow source
            source = self._get_workflow_source(str(workflow.id))
            if not source:
                raise ValueError(f"No source found for workflow {workflow.id}")

            logger.info(f"Using workflow source: {source.url}")
            logger.info(f"Remote flow ID: {workflow.remote_flow_id}")

            # Initialize LangFlow manager with the correct source settings
            api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
            self._manager = LangFlowManager(self.session, api_url=source.url, api_key=api_key)
            
            # Run the workflow
            result = self._manager.run_workflow_sync(workflow.remote_flow_id, input_data)
            if not result:
                raise ValueError("No result from workflow execution")

            return result
        except Exception as e:
            logger.error(f"Failed to execute workflow: {str(e)}")
            raise e


