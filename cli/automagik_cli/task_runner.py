import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from .models import Task, Log, FlowDB
from .langflow_client import LangflowClient

logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self, session: Session, langflow_client: LangflowClient):
        self.session = session
        self.langflow_client = langflow_client

    async def create_task(self, flow_id: uuid.UUID, input_data: Dict[str, Any] = None) -> Task:
        """Create a new task for a flow."""
        flow = self.session.query(FlowDB).filter(FlowDB.id == flow_id).first()
        if not flow:
            raise ValueError(f"Flow {flow_id} not found")
        
        task = Task(
            flow_id=flow_id,
            input_data=input_data or {},
            status="pending"
        )
        self.session.add(task)
        self.session.commit()
        return task

    async def run_task(self, task_id: uuid.UUID) -> Task:
        """Run a task."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")

        flow = task.flow
        if not flow:
            raise ValueError(f"Flow for task {task_id} not found")

        if not flow.input_component or not flow.output_component:
            raise ValueError(f"Flow {flow.id} does not have input/output components configured")

        task.status = "running"
        task.tries += 1
        self.session.commit()

        try:
            # Log start
            self._log_message(task.id, "info", f"Starting task execution for flow {flow.id}")
            
            # Execute flow
            result = await self.langflow_client.process_flow(
                flow_id=str(flow.id),
                input_data=task.input_data
            )
            
            # Update task with result
            task.output_data = result
            task.status = "completed"
            self._log_message(task.id, "info", "Task completed successfully")
            
        except Exception as e:
            # Handle failure
            error_msg = str(e)
            self._log_message(task.id, "error", f"Task failed: {error_msg}")
            task.status = "failed"
            
            # Retry logic
            if task.tries < task.max_retries:
                task.status = "pending"
                self._log_message(task.id, "info", f"Scheduling retry {task.tries}/{task.max_retries}")
            
        finally:
            self.session.commit()
            
        return task

    def _log_message(self, task_id: uuid.UUID, level: str, message: str):
        """Add a log message for a task."""
        log = Log(
            task_id=task_id,
            level=level,
            message=message
        )
        self.session.add(log)
        self.session.commit()