"""
Task Runner Module

This module handles the execution of flow tasks, including running flows
and managing their execution state.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
import uuid

from sqlalchemy.orm import Session
from ..database.models import Task, TaskLog, FlowDB
from .exceptions import TaskExecutionError, FlowNotFoundError, ComponentNotConfiguredError

logger = logging.getLogger(__name__)

class TaskRunner:
    """
    Handles the execution of flow tasks.
    
    This class is responsible for:
    - Creating and managing tasks
    - Executing flows via LangFlow
    - Managing task state and logging
    - Processing flow results
    """
    
    def __init__(self, session: Session, langflow_client: Any):
        """
        Initialize TaskRunner.
        
        Args:
            session: SQLAlchemy database session
            langflow_client: Client for interacting with LangFlow API
        """
        self.session = session
        self.langflow_client = langflow_client

    async def create_task(
        self,
        flow_id: uuid.UUID,
        input_data: Dict[str, Any] = None
    ) -> Task:
        """
        Create a new task for a flow.
        
        Args:
            flow_id: ID of the flow to create task for
            input_data: Optional input data for the flow
            
        Returns:
            Created task
            
        Raises:
            FlowNotFoundError: If flow doesn't exist
        """
        flow = self.session.query(FlowDB).filter(FlowDB.id == flow_id).first()
        if not flow:
            raise FlowNotFoundError(f"Flow {flow_id} not found")
        
        try:
            task = Task(
                flow_id=flow_id,
                input_data=input_data or {},
                status="pending"
            )
            self.session.add(task)
            self.session.commit()
            
            logger.info(f"Created task {task.id} for flow {flow_id}")
            return task
            
        except Exception as e:
            self.session.rollback()
            raise TaskExecutionError(f"Error creating task: {str(e)}")

    def _extract_output_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract useful information from the LangFlow response.
        
        Args:
            response: Raw response from LangFlow API
            
        Returns:
            Processed output data
        """
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
                if "artifacts" in result:
                    output_data["artifacts"].append(result["artifacts"])
                    
                # Get logs
                if "logs" in result:
                    for component_logs in result["logs"].values():
                        output_data["logs"].extend(component_logs)
        
        return output_data

    def _log_message(self, task_id: uuid.UUID, level: str, message: str) -> None:
        """
        Add a log message for a task.
        
        Args:
            task_id: ID of the task
            level: Log level
            message: Log message
        """
        try:
            log = TaskLog(
                task_id=task_id,
                level=level,
                message=message
            )
            self.session.add(log)
            self.session.commit()
        except Exception as e:
            logger.error(f"Error adding log message: {str(e)}")
            self.session.rollback()

    async def run_task(self, task_id: uuid.UUID) -> Task:
        """
        Run a task.
        
        Args:
            task_id: ID of the task to run
            
        Returns:
            Updated task
            
        Raises:
            TaskExecutionError: If task execution fails
        """
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskExecutionError(f"Task {task_id} not found")

        flow = task.flow
        if not flow:
            raise FlowNotFoundError(f"Flow for task {task_id} not found")

        if not flow.input_component:
            raise ComponentNotConfiguredError(
                f"Flow {flow.id} does not have input component configured"
            )

        # Update task status
        task.status = "running"
        task.tries += 1
        self.session.commit()

        try:
            # Get flow tweaks
            tweaks = flow.data.get('tweaks', {}) if flow.data else {}
            
            # Log execution details
            logger.info(f"Running flow: {flow.name}")
            logger.info(f"Input: {task.input_data.get('input', '')}")
            logger.debug(f"Flow ID: {flow.id}")
            logger.debug(f"Input component: {flow.input_component}")
            logger.debug(f"Output component: {flow.output_component}")
            logger.debug(f"Input data: {json.dumps(task.input_data, indent=2)}")
            logger.debug(f"Tweaks: {json.dumps(tweaks, indent=2)}")
            
            # Execute flow
            result = await self.langflow_client.process_flow(
                flow_id=str(flow.id),
                input_data=task.input_data,
                tweaks=tweaks
            )
            
            # Process results
            logger.debug(f"API Response: {json.dumps(result, indent=2)}")
            output_data = self._extract_output_data(result)
            
            # Log results
            for msg in output_data["messages"]:
                text = msg.get("text", msg.get("message", ""))
                logger.info(f'Response: {text}')
            
            if output_data.get("artifacts"):
                logger.debug(f'Artifacts: {json.dumps(output_data["artifacts"], indent=2)}')
            
            # Update task
            task.status = "completed"
            task.output_data = output_data
            self.session.commit()
            
            logger.info(f"Task {task_id} completed successfully")
            return task
            
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                error_msg += f"\nResponse status: {e.response.status_code}"
                error_msg += f"\nResponse text: {e.response.text}"
            
            logger.error(error_msg)
            self._log_message(task_id, "error", error_msg)
            
            task.status = "failed"
            self.session.commit()
            
            raise TaskExecutionError(
                message=f"Task execution failed: {error_msg}",
                task_id=str(task_id),
                response=getattr(e, 'response', None)
            )
