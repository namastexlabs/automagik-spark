"""
Task CLI Commands

Provides commands for:
- List tasks
- View task details
- Retry failed tasks
- Create a new task
"""

import json
import click
import asyncio
import logging
import sys
from typing import Optional, Any, Callable, List, Dict
from datetime import datetime
from uuid import UUID
from sqlalchemy import select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console
from rich.table import Table

from ...core.database import get_session, Task, Workflow
from ...core.workflows.workflow import LocalWorkflowManager as FlowManager
from ...core.workflows import WorkflowManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_async_command(coro: Any) -> Any:
    """Helper function to handle running async commands."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(coro)
    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        raise click.ClickException(str(e))
    finally:
        if loop and not loop.is_closed():
            loop.close()

@click.group(name='tasks')
def task_group():
    """Manage workflow tasks."""
    pass

async def _list_tasks(workflow_id: Optional[str], status: Optional[str], limit: int, show_logs: bool):
    """List tasks."""
    try:
        session: AsyncSession
        async with get_session() as session:
            workflow_manager = FlowManager(session)
            tasks = await workflow_manager.task.list_tasks(
                workflow_id=workflow_id,
                status=status,
                limit=limit
            )

            if not tasks:
                click.echo("No tasks found")
                return

            table = Table(title="Tasks")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Workflow", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Created", style="blue")
            table.add_column("Updated", style="blue")
            if show_logs:
                table.add_column("Logs", style="yellow")

            for task in tasks:
                row = [
                    str(task.id),
                    task.workflow.name if task.workflow else "N/A",
                    task.status,
                    task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ]
                if show_logs:
                    row.append("\n".join([log.message for log in task.logs]))
                table.add_row(*row)

            console = Console()
            console.print(table)

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise click.ClickException(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise click.ClickException(str(e))

@task_group.command(name='list')
@click.option('--workflow-id', help='Filter tasks by workflow ID')
@click.option('--status', help='Filter tasks by status')
@click.option('--limit', default=50, help='Maximum number of tasks to show')
@click.option('--show-logs', is_flag=True, help='Show task logs')
def list_tasks(workflow_id: Optional[str], status: Optional[str], limit: int, show_logs: bool):
    """List tasks."""
    return handle_async_command(_list_tasks(workflow_id, status, limit, show_logs))

async def _view_task(task_id: str) -> int:
    """View task details."""
    try:
        session: AsyncSession
        async with get_session() as session:
            # Get task by ID or prefix
            stmt = select(Task).where(
                cast(Task.id, String).startswith(task_id.lower())
            )
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            
            if not task:
                logger.error(f"Task {task_id} not found")
                raise click.ClickException(f"Task {task_id} not found")
            
            # Load relationships
            await session.refresh(task, ['workflow'])
            
            click.echo("\nTask Details:")
            click.echo(f"ID: {task.id}")
            click.echo(f"Workflow: {task.workflow.name}")
            click.echo(f"Status: {task.status}")
            click.echo(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if task.started_at:
                click.echo(f"Started: {task.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.finished_at:
                click.echo(f"Finished: {task.finished_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.next_retry_at:
                click.echo(f"Next retry: {task.next_retry_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            click.echo(f"\nInput:")
            click.echo(json.dumps(task.input_data, indent=2) if task.input_data else "None")
            
            if task.output_data:
                click.echo(f"\nOutput:")
                click.echo(json.dumps(task.output_data, indent=2))
            
            if task.error:
                click.echo(f"\nError:")
                click.echo(task.error)
            
            return 0
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise click.ClickException(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error viewing task: {str(e)}")
        raise click.ClickException(str(e))

@task_group.command(name='view')
@click.argument('task-id')
def view_task(task_id: str):
    """View task details."""
    return handle_async_command(_view_task(task_id))

async def _retry_task(task_id: str) -> int:
    """Retry a failed task."""
    try:
        session: AsyncSession
        async with get_session() as session:
            # Get task by ID or prefix
            stmt = select(Task).where(
                cast(Task.id, String).startswith(task_id.lower())
            )
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            
            if not task:
                logger.error(f"Task {task_id} not found")
                raise click.ClickException(f"Task {task_id} not found")
            
            workflow_manager = WorkflowManager(session)
            retried_task = await workflow_manager.retry_task(str(task.id))
            
            if retried_task:
                click.echo(f"Task {task_id} queued for retry")
                return 0
            else:
                msg = f"Failed to retry task {task_id}"
                logger.error(msg)
                raise click.ClickException(msg)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise click.ClickException(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error retrying task: {str(e)}")
        raise click.ClickException(str(e))

@task_group.command(name='retry')
@click.argument('task-id')
def retry_task(task_id: str):
    """Retry a failed task."""
    return handle_async_command(_retry_task(task_id))

async def _create_task(workflow_id: str, input_data: Optional[str] = None, max_retries: int = 3, run: bool = False) -> int:
    """Create a new task for a workflow."""
    try:
        session: AsyncSession
        async with get_session() as session:
            # Get workflow by ID or prefix
            stmt = select(Workflow).where(
                cast(Workflow.id, String).startswith(workflow_id.lower())
            )
            result = await session.execute(stmt)
            workflow = result.scalar_one_or_none()
            
            if not workflow:
                logger.error(f"Workflow {workflow_id} not found")
                raise click.ClickException(f"Workflow {workflow_id} not found")
            
            # Parse input data if provided
            input_dict = None
            if input_data:
                try:
                    input_dict = json.loads(input_data)
                except json.JSONDecodeError as e:
                    msg = f"Invalid JSON input data: {str(e)}"
                    logger.error(msg)
                    raise click.ClickException(msg)
            
            workflow_manager = WorkflowManager(session)
            task = await workflow_manager.create_task(
                workflow_id=str(workflow.id),
                input_data=input_dict,
                max_retries=max_retries
            )
            
            if not task:
                msg = f"Failed to create task for workflow {workflow_id}"
                logger.error(msg)
                raise click.ClickException(msg)
            
            click.echo(f"Created task {str(task.id)[:8]} for workflow {workflow.name}")
            
            if run:
                click.echo("Running task...")
                await workflow_manager.run_task(str(task.id))
                click.echo("Task started")
            
            return 0
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise click.ClickException(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise click.ClickException(str(e))

@task_group.command(name='create')
@click.argument('workflow-id')
@click.option('--input-data', help='JSON input data')
@click.option('--max-retries', default=3, help='Maximum number of retries')
@click.option('--run', is_flag=True, help='Run the task immediately')
def create_task(workflow_id: str, input_data: Optional[str] = None, max_retries: int = 3, run: bool = False):
    """Create a new task for a workflow."""
    return handle_async_command(_create_task(workflow_id, input_data, max_retries, run))
