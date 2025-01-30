"""
Flow synchronization module.

Handles synchronization of flows between LangFlow and Automagik.
Provides functionality for fetching, filtering, and syncing flows.
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

from ..config import LANGFLOW_API_URL
from ..database.models import Flow, FlowComponent, Task, TaskLog
from ..database.session import get_session

logger = logging.getLogger(__name__)


class FlowSync:
    """Flow synchronization class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize flow sync."""
        self.session = session
        self._client = None
        self._base_url = None

    async def execute_flow(
        self,
        flow: Flow,
        task: Task,
        input_data: Dict[str, Any],
        debug: bool = True  # This parameter is kept for backward compatibility
    ) -> Dict[str, Any]:
        """Execute a flow with the given input data.
        
        Args:
            flow: Flow to execute
            task: Task being executed
            input_data: Input data for the flow
            debug: Whether to run in debug mode (always True)
        
        Returns:
            Dict containing the flow output
        """
        # Get the client
        client = await self._get_client()
        
        # Build the request payload
        payload = {
            **input_data,
            "output_type": "debug",  # Always run in debug mode
            "input_type": "chat"
        }
        
        try:
            # Update task status
            task.status = "running"
            task.started_at = datetime.utcnow()
            await self.session.commit()

            # Execute the flow
            response = await client.post(
                f"/run/{flow.source_id}?stream=false",
                json=payload,
                timeout=600  # 10 minutes
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                # Get error details from response
                error_content = response.text
                logger.error(f"LangFlow API error response: {error_content}")
                raise
                
            result = response.json()

            # Log component outputs in debug mode
            if "logs" in result:
                for log_entry in result["logs"]:
                    # Create task log for each component output
                    task_log = TaskLog(
                        id=uuid4(),
                        task_id=task.id,
                        level="debug",
                        component_id=log_entry.get("component_id"),
                        message=f"Component output: {log_entry.get('component_type')}",
                        data={
                            "inputs": log_entry.get("inputs"),
                            "output": log_entry.get("output"),
                            "type": log_entry.get("component_type")
                        }
                    )
                    self.session.add(task_log)

            # Extract output from the specified output component
            output = None
            if flow.output_component and "logs" in result:
                for log_entry in result["logs"]:
                    if log_entry.get("component_id") == flow.output_component:
                        output = log_entry.get("output")
                        break

            # If no specific output component or output not found, use the final result
            if output is None:
                output = result.get("output", result)

            # Update task with success
            task.status = "completed"
            task.finished_at = datetime.utcnow()
            task.output_data = output
            await self.session.commit()

            return output

        except Exception as e:
            import traceback
            # Log the error with a string representation of the traceback
            error_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level="error",
                message=str(e),
                data={"traceback": "".join(traceback.format_tb(e.__traceback__))}
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
            self._client = httpx.AsyncClient(
                base_url=self._get_base_url(),
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
