"""
Workflow synchronization module.

Handles synchronization of workflows between LangFlow and Automagik.
Provides functionality for fetching, filtering, and syncing workflows.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import LANGFLOW_API_URL, LANGFLOW_API_KEY
from ..database.models import Workflow, WorkflowComponent, Task, TaskLog
from ..database.session import get_session

logger = logging.getLogger(__name__)


class WorkflowSync:
    """Workflow synchronization class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize workflow sync."""
        self.session = session
        self._client = None
        self._base_url = None

    async def execute_workflow(
        self,
        workflow: Workflow,
        task: Task,
        input_data: Dict[str, Any],
        debug: bool = True  # This parameter is kept for backward compatibility
    ) -> Dict[str, Any]:
        """Execute a workflow with the given input data.
        
        Args:
            workflow: Workflow to execute
            task: Task being executed
            input_data: Input data for the workflow
            debug: Whether to run in debug mode (always True)
        
        Returns:
            Dict containing the workflow output
        """
        if not workflow.input_component or not workflow.output_component:
            task.status = "failed"
            task.error = "Missing input/output components"
            task.started_at = datetime.utcnow()
            await self.session.commit()
            raise ValueError("Missing input/output components")

        task.status = "running"
        task.started_at = datetime.utcnow()
        task.input_data = input_data
        await self.session.commit()

        # Get the client
        client = await self._get_client()
        
        # Build API payload
        payload = {
            "inputs": {"text": str(input_data.get("message", ""))},  # Convert to string
            "tweaks": {}
        }
        
        # Only add tweaks if input/output components are configured
        if workflow.input_component and workflow.output_component:
            payload["tweaks"] = {
                workflow.input_component: {"input": str(input_data.get("message", ""))},  # Convert to string
                workflow.output_component: {}
            }
        
        try:
            # Execute the workflow
            logger.debug(f"Executing workflow {workflow.remote_flow_id} with input_data: {input_data}")
            logger.debug(f"API payload: {payload}")
            response = await client.post(
                f"/api/v1/run/{workflow.remote_flow_id}",  # Use the /run/{flow_id} endpoint
                json=payload,
                timeout=600  # 10 minutes
            )
            
            if response.status_code >= 400:
                error_text = response.text  # Get error text synchronously
                logger.error(f"LangFlow API error response: {error_text}")
                raise httpx.HTTPStatusError(f"HTTP {response.status_code}: {error_text}", request=response.request, response=response)
                
            result = response.json()  # Get JSON synchronously since we already have the response
            logger.debug(f"Workflow execution result: {result}")

            # Update task with output
            if result.get("result"):  # Changed from outputs to result
                task.output_data = result["result"]

            # Update task status
            task.status = "completed"
            task.finished_at = datetime.utcnow()
            await self.session.commit()

            return result

        except Exception as e:
            import traceback
            # Log the error with a string representation of the traceback
            error_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level="error",
                message=f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}",
                created_at=datetime.utcnow()
            )
            self.session.add(error_log)

            # Update task with error
            task.status = "failed"
            task.finished_at = datetime.utcnow()
            task.error = str(e)
            await self.session.commit()

            raise

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            headers = {
                'accept': 'application/json'
            }
            if LANGFLOW_API_KEY:
                headers["x-api-key"] = LANGFLOW_API_KEY
            logger.debug(f"Using LangFlow API URL: {self._get_base_url()}")
            logger.debug(f"Headers: {headers}")
            self._client = httpx.AsyncClient(
                base_url=self._get_base_url(),
                headers=headers,
                verify=False,
                timeout=30.0
            )
        return self._client

    def _get_base_url(self) -> str:
        """Get base URL for LangFlow API."""
        if self._base_url is None:
            self._base_url = LANGFLOW_API_URL
        return self._base_url

    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
