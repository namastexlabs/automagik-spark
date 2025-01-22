import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from automagik.core.database.models import Task, Log, FlowDB
from automagik.core.services.langflow_client import LangflowClient
from automagik.core.logger import setup_logger

logger = setup_logger()

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

    def _extract_output_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract useful information from the Langflow response."""
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

    async def run_task(self, task_id: uuid.UUID) -> Task:
        """Run a task."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            return

        flow = task.flow
        if not flow:
            logger.error(f"Flow for task {task_id} not found")
            return

        if not flow.input_component:
            logger.error(f"Flow {flow.id} does not have input component configured")
            return

        task.status = "running"
        task.tries += 1
        self.session.commit()

        try:
            # Get flow tweaks
            tweaks = flow.data.get('tweaks', {}) if flow.data else {}
            
            # Log basic info at INFO level
            logger.info(f"Running flow: {flow.name}")
            logger.info(f"Input: {task.input_data.get('input', '')}")
            
            # Log detailed info at DEBUG level
            logger.debug(f"Flow details:")
            logger.debug(f"  ID: {flow.id}")
            logger.debug(f"  Input component: {flow.input_component}")
            logger.debug(f"  Output component: {flow.output_component}")
            logger.debug(f"  Input data: {json.dumps(task.input_data, indent=2)}")
            logger.debug(f"  Tweaks: {json.dumps(tweaks, indent=2)}")
            
            # Execute flow with tweaks
            logger.debug("Sending request to Langflow API...")
            result = await self.langflow_client.process_flow(
                flow_id=str(flow.id),
                input_data=task.input_data,
                tweaks=tweaks
            )
            
            # Log full API response at DEBUG level
            logger.debug(f"Full API Response: {json.dumps(result, indent=2)}")
            
            # Extract output data
            output_data = self._extract_output_data(result)
            task.output_data = output_data
            
            # Log messages concisely at INFO level
            for msg in output_data["messages"]:
                text = msg.get("text", msg.get("message", "")).replace('\n\n', ' ').replace('\n', ' ')
                logger.info(f'Response: {text}')
            
            # Log artifacts at DEBUG level
            if output_data.get("artifacts"):
                logger.debug(f'Artifacts: {json.dumps(output_data["artifacts"], indent=2)}')
            
            # Update task
            task.status = "completed"
            task.output_data = output_data
            self.session.commit()
            
            logger.info("Task completed successfully")
            return task
            
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                error_msg += f"\nResponse status: {e.response.status_code}"
                error_msg += f"\nResponse text: {e.response.text}"
            
            logger.error(error_msg)
            task.status = "failed"
            self.session.commit()
            raise

    def _log_message(self, task_id: uuid.UUID, level: str, message: str):
        """Add a log message for a task."""
        log = Log(
            task_id=task_id,
            level=level,
            message=message
        )
        self.session.add(log)
        self.session.commit()