"""
Task Runner Service

This module provides functionality for managing and executing tasks.
"""

from datetime import datetime
import uuid
from typing import Optional, Dict, Any, List
import logging
import json
from sqlalchemy.orm import Session

from automagik.core.database.models import Task, Log, FlowDB
from automagik.core.services.langflow_client import LangflowClient

logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self, session: Session, langflow_client: LangflowClient):
        """Initialize TaskRunner.
        
        Args:
            session: SQLAlchemy database session
            langflow_client: Client for interacting with LangFlow API
        """
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
            status="pending",
            tries=0,
            max_retries=3
        )
        self.session.add(task)
        self.session.commit()
        return task

    def _extract_output_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract useful information from the LangFlow response."""
        output_data = {
            "session_id": response.get("session_id"),
            "messages": [],
            "artifacts": [],
            "logs": []
        }
        
        # Extract messages and outputs
        for output in response.get("outputs", []):
            for result in output.get("outputs", []):
                # Get messages
                messages = result.get("messages", [])
                output_data["messages"].extend(messages)
                
                # Get artifacts
                artifacts = result.get("artifacts", [])
                output_data["artifacts"].extend(artifacts)
                
                # Get logs
                logs = result.get("logs", [])
                output_data["logs"].extend(logs)
        
        return output_data

    def _log_message(self, task_id: uuid.UUID, level: str, message: str):
        """Add a log message for a task."""
        log = Log(
            task_id=task_id,
            level=level,
            message=message,
            created_at=datetime.utcnow()
        )
        self.session.add(log)
        self.session.commit()

    async def run_task(self, task_id: uuid.UUID) -> bool:
        """Run a task."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")

        try:
            # Update task status
            task.status = "running"
            task.tries += 1
            task.updated_at = datetime.utcnow()
            self.session.commit()
            
            self._log_message(task.id, "info", f"Starting task execution (attempt {task.tries}/{task.max_retries})")
            
            # Run the flow
            flow_response = await self.langflow_client.run_flow(
                str(task.flow_id),
                task.input_data
            )
            
            # Process response
            output_data = self._extract_output_data(flow_response)
            task.output_data = output_data
            task.status = "completed"
            task.updated_at = datetime.utcnow()
            
            self._log_message(task.id, "info", "Task completed successfully")
            
            self.session.commit()
            return True
            
        except Exception as e:
            error_message = str(e)
            self._log_message(task.id, "error", f"Task execution failed: {error_message}")
            
            # Handle retries
            if task.tries < task.max_retries:
                task.status = "pending"
            else:
                task.status = "failed"
            
            task.updated_at = datetime.utcnow()
            self.session.commit()
            return False

    def get_task_logs(self, task_id: uuid.UUID) -> List[Log]:
        """Get all logs for a task."""
        return self.session.query(Log).filter(Log.task_id == task_id).order_by(Log.created_at).all()