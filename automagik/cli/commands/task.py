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
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
from rich.panel import Panel
from uuid import UUID
from typing import Optional, Any, Callable, List, Dict
from sqlalchemy import select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import asyncio

from automagik.core.database import get_sync_session, get_session
from automagik.core.database.models import Task, Workflow
from automagik.core.workflows.manager import WorkflowManager
from automagik.core.workflows.sync import WorkflowSync
from automagik.core.workflows.remote import LangFlowManager
from automagik.cli.utils.async_helper import handle_async_command
from automagik.cli.utils.log import get_logger

# Set up logging
logger = get_logger(__name__)

def handle_sync_command(func: Callable) -> Any:
    """Helper function to handle running sync commands."""
    try:
        return func()
    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        raise click.ClickException(str(e))

@click.group(name='tasks')
def task_group():
    """Manage workflow tasks."""
    pass

async def _list_tasks(workflow_id: Optional[str] = None, status: Optional[str] = None, limit: int = 50, show_logs: bool = False) -> int:
    """List tasks."""
    async with get_session() as session:
        stmt = select(Task).order_by(Task.created_at.asc()).options(joinedload(Task.workflow))
        if workflow_id:
            stmt = stmt.where(Task.workflow_id == workflow_id)
        if status:
            stmt = stmt.where(Task.status == status)
        if limit:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        tasks = result.unique().scalars().all()

        # Create a beautiful table with Rich
        table = Table(
            title="[bold blue]Workflow Tasks[/bold blue]",
            caption="[dim]Showing most recent tasks last[/dim]",
            box=box.ROUNDED,
            header_style="bold cyan",
            show_lines=True,
            padding=(0, 1)
        )
        
        # Add columns with styled headers
        table.add_column("ID", justify="left", no_wrap=True, style="bright_blue")
        table.add_column("Workflow", justify="left", style="green")
        table.add_column("Status", justify="center", style="bold")
        table.add_column("Created", justify="left", style="yellow")
        table.add_column("Updated", justify="left", style="yellow")

        # Status color mapping
        status_styles = {
            "completed": "[bold green]✓[/bold green] COMPLETED",
            "failed": "[bold red]✗[/bold red] FAILED",
            "running": "[bold yellow]⟳[/bold yellow] RUNNING",
            "pending": "[bold blue]⋯[/bold blue] PENDING",
            "error": "[bold red]![/bold red] ERROR"
        }

        for task in tasks:
            # Style the status
            status_display = status_styles.get(
                task.status.lower(), 
                f"[bold white]{task.status.upper()}[/bold white]"
            )
            
            # Format timestamps
            created_at = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
            updated_at = task.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            
            # Add row with styling
            table.add_row(
                str(task.id),
                task.workflow.name if task.workflow else "[dim italic]N/A[/dim italic]",
                status_display,
                created_at,
                updated_at
            )

        console = Console()
        console.print()  # Add some spacing
        console.print(table)
        console.print()  # Add some spacing

        if show_logs and tasks:
            for task in tasks:
                if task.logs:
                    console.print(f"[bold blue]Logs for task {task.id}:[/bold blue]")
                    console.print(Panel(task.logs, title="Task Logs", border_style="blue"))
                    console.print()  # Add spacing between logs

    return 0

@task_group.command()
@click.option("--workflow-id", help="Filter by workflow ID")
@click.option("--status", help="Filter by status")
@click.option("--limit", default=50, help="Limit number of results")
@click.option("--show-logs", is_flag=True, help="Show task logs")
def list(workflow_id: Optional[str], status: Optional[str], limit: int, show_logs: bool):
    """List tasks."""
    return asyncio.run(_list_tasks(workflow_id, status, limit, show_logs))

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
