"""Workflow task execution."""

import json
import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ...core.database.session import get_sync_session
from ...core.database.models import Task, Workflow, Schedule
from ...core.workflows.sync import WorkflowSync

logger = logging.getLogger(__name__)


def _execute_workflow_sync(schedule_id: str) -> Optional[Task]:
    """Execute a workflow synchronously."""
    try:
        with get_sync_session() as session:
            # Get schedule
            schedule_query = select(Schedule).where(Schedule.id == UUID(schedule_id))
            schedule = session.execute(schedule_query).scalar()
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return None

            # Create task with input data as string
            input_data = schedule.input_data or ""

            task = Task(
                id=uuid4(),
                workflow_id=schedule.workflow_id,
                schedule_id=schedule.id,
                input_data=input_data,
                status="running",
                started_at=datetime.now(timezone.utc),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            session.add(task)
            session.commit()

            try:
                # Get workflow
                workflow_query = select(Workflow).where(Workflow.id == schedule.workflow_id)
                workflow = session.execute(workflow_query).scalar()
                if not workflow:
                    logger.error(f"Workflow {schedule.workflow_id} not found")
                    task.status = "failed"
                    task.error = f"Workflow {schedule.workflow_id} not found"
                    task.finished_at = datetime.now(timezone.utc)
                    task.updated_at = datetime.now(timezone.utc)
                    session.commit()
                    return task

                # Run workflow
                with WorkflowSync(session) as sync:
                    output = sync.execute_workflow(workflow, task.input_data)
                    if output:
                        # Extract and log only the result message
                        result_message = output.get('result', '')
                        if isinstance(result_message, dict):
                            result_message = result_message.get('response', str(result_message))
                        logger.info(f"Workflow result: {result_message}")
                        
                        # Store the full output in the task
                        task.output_data = json.dumps(output)
                        task.status = "completed"
                    else:
                        task.status = "failed"
                        task.error = "No output from workflow"
                    task.finished_at = datetime.now(timezone.utc)
                    task.updated_at = datetime.now(timezone.utc)
                    session.commit()
                    return task

            except Exception as e:
                logger.error(f"Failed to execute workflow: {str(e)}")
                task.status = "failed"
                task.error = str(e)
                task.finished_at = datetime.now(timezone.utc)
                task.updated_at = datetime.now(timezone.utc)
                session.commit()
                return task
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        raise e


@shared_task(bind=True, max_retries=3)
def execute_workflow(self, schedule_id: str):
    """Execute a workflow from a schedule."""
    try:
        task = _execute_workflow_sync(schedule_id)
        if task and task.status == "failed":
            # Retry the task if it failed
            raise Exception(task.error)
        return task.to_dict() if task else None
    except Exception as e:
        logger.error(f"Failed to execute workflow: {str(e)}")
        # Retry with exponential backoff
        retry_in = 2 ** self.request.retries
        try:
            raise self.retry(exc=e, countdown=retry_in, max_retries=3)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for task. Error: {str(e)}")
            raise e


@shared_task
def schedule_workflow(workflow_id: str, workflow_params: Optional[str] = None):
    """Create a task for a scheduled workflow."""
    with get_sync_session() as session:
        workflow = session.get(Workflow, UUID(workflow_id))
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Ensure input_data is a string
        if workflow_params is None:
            workflow_params = ""
        elif not isinstance(workflow_params, str):
            workflow_params = str(workflow_params)
        
        task = Task(
            workflow_id=workflow.id,
            input_data=workflow_params,
            status="pending",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(task)
        session.commit()
        return str(task.id)


@shared_task
def process_pending_tasks():
    """Process pending tasks."""
    with get_sync_session() as session:
        # Get pending tasks
        pending_tasks_query = select(Task).where(Task.status == "pending")
        pending_tasks = session.execute(pending_tasks_query).scalars().all()
        
        for task in pending_tasks:
            try:
                # Get workflow
                workflow_query = select(Workflow).where(Workflow.id == task.workflow_id)
                workflow = session.execute(workflow_query).scalar()
                if not workflow:
                    logger.error(f"Workflow {task.workflow_id} not found")
                    task.status = "failed"
                    task.error = f"Workflow {task.workflow_id} not found"
                    task.finished_at = datetime.now(timezone.utc)
                    task.updated_at = datetime.now(timezone.utc)
                    session.commit()
                    continue

                # Run workflow
                task.status = "running"
                task.started_at = datetime.now(timezone.utc)
                task.updated_at = datetime.now(timezone.utc)
                session.commit()

                with WorkflowSync(session) as sync:
                    output = sync.execute_workflow(workflow, task.input_data)
                    if output:
                        task.output_data = json.dumps(output)
                        task.status = "completed"
                    else:
                        task.status = "failed"
                        task.error = "No output from workflow"
                    task.finished_at = datetime.now(timezone.utc)
                    task.updated_at = datetime.now(timezone.utc)
                    session.commit()

            except Exception as e:
                logger.error(f"Failed to execute workflow: {str(e)}")
                task.status = "failed"
                task.error = str(e)
                task.finished_at = datetime.now(timezone.utc)
                task.updated_at = datetime.now(timezone.utc)
                session.commit()
