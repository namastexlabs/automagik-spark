"""
Task CLI Commands

Provides commands for:
- List tasks
- View task details
- Retry failed tasks
- Create a new task
"""

import asyncio
import click
from typing import Optional
from uuid import UUID
import logging
from tabulate import tabulate
from datetime import datetime
import json
import uuid
from sqlalchemy import select, func, cast
from sqlalchemy.types import String

from ...core.flows import FlowManager
from ...core.database.session import get_session
from ...core.database.models import Task, Flow, TaskLog

logger = logging.getLogger(__name__)

@click.group(name='task')
def task_group():
    """Manage flow tasks."""
    pass

@task_group.command()
@click.option('--flow-id', help='Filter tasks by flow ID')
@click.option('--status', type=click.Choice(['pending', 'running', 'completed', 'failed']), help='Filter tasks by status')
@click.option('--limit', type=int, default=10, help='Maximum number of tasks to show')
@click.option('--all', is_flag=True, help='Show all tasks (default: show only most recent)')
def list(flow_id: Optional[str], status: Optional[str], limit: int, all: bool):
    """List flow execution tasks."""
    async def _list_tasks():
        nonlocal limit
        
        async with get_session() as session:
            flow_manager = FlowManager(session)
            
            # If not showing all tasks, limit to most recent
            if not all:
                limit = min(limit, 10)
            
            tasks = await flow_manager.list_tasks(flow_id=flow_id, status=status, limit=limit)
            
            if not tasks:
                click.echo("No tasks found")
                return
            
            # Prepare table data
            rows = []
            for task in tasks:
                # Format error message to be shorter
                error = task.error if task.error else ''
                if len(error) > 30:
                    error = error[:27] + '...'
                
                rows.append([
                    str(task.id)[:8],  # Show only first 8 chars of UUID
                    task.flow.name,
                    task.status,
                    task.created_at.strftime('%H:%M:%S'),  # Show only time for today
                    error
                ])
            
            # Reverse rows to show most recent at bottom
            rows.reverse()
            
            # Print table
            headers = ['ID', 'Flow', 'Status', 'Time', 'Error']
            click.echo("\nFlow Tasks:")
            click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
            
            if not all and len(tasks) == limit:
                click.echo("\nShowing most recent tasks. Use --all to see all tasks.")
    
    asyncio.run(_list_tasks())

@task_group.command()
@click.argument('task-id')
def view(task_id: str):
    """View task details."""
    async def _view_task():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            
            # Handle truncated IDs by finding the full ID
            if len(task_id) < 32:
                result = await session.execute(
                    select(Task.id).where(func.substr(cast(Task.id, String), 1, len(task_id)) == task_id)
                )
                matches = result.scalars().all()
                if not matches:
                    click.echo(f"No task found with ID starting with: {task_id}")
                    return
                if len(matches) > 1:
                    click.echo(f"Multiple tasks found with ID starting with: {task_id}")
                    click.echo("Please provide more characters to uniquely identify the task")
                    return
                task_uuid = matches[0]
            else:
                try:
                    task_uuid = uuid.UUID(task_id)
                except ValueError:
                    click.echo(f"Invalid task ID format: {task_id}")
                    return
            
            # Get task details
            task = await flow_manager.get_task(str(task_uuid))
            if not task:
                click.echo(f"Task not found: {task_id}")
                return
            
            click.echo("\nTask Details:")
            click.echo(f"ID: {task.id}")
            click.echo(f"Flow: {task.flow.name}")
            click.echo(f"Status: {task.status}")
            click.echo(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if task.started_at:
                click.echo(f"Started: {task.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            click.echo(f"\nTries: {task.tries}/{task.max_retries}")
            
            if task.input_data:
                click.echo("\nInput Data:")
                click.echo(json.dumps(task.input_data, indent=2))
            
            if task.output_data:
                click.echo("\nOutput Data:")
                click.echo(json.dumps(task.output_data, indent=2))
            
            if task.error:
                click.echo("\nError:")
                click.echo(task.error)
            
            # Load logs explicitly
            logs_result = await session.execute(
                select(TaskLog)
                .where(TaskLog.task_id == task.id)
                .order_by(TaskLog.created_at)
            )
            logs = logs_result.scalars().all()
            
            if logs:
                click.echo("\nLogs:")
                for log in logs:
                    click.echo(f"\n[{log.level}] {log.message}")
                    if log.data:
                        click.echo(json.dumps(log.data, indent=2))
            
    asyncio.run(_view_task())

@task_group.command()
@click.argument('task-id')
def retry(task_id: str):
    """Retry a failed task."""
    async def _retry_task():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            task = await flow_manager.get_task(task_id)
            
            if not task:
                click.echo(f"Task {task_id} not found")
                return
            
            if task.status != 'failed':
                click.echo("Only failed tasks can be retried")
                return
            
            new_task = await flow_manager.retry_task(task_id)
            if new_task:
                click.echo(f"Task {task_id} queued for retry")
                click.echo(f"New task ID: {new_task.id}")
            else:
                click.echo("Failed to retry task")
    
    asyncio.run(_retry_task())

@task_group.command()
@click.argument('flow-id')
@click.option('--input', 'input_data', help='Input data as JSON string')
@click.option('--max-retries', default=3, help='Maximum number of retries')
def create(flow_id: str, input_data: Optional[str] = None, max_retries: int = 3):
    """Create a new task for a flow."""
    async def _create_task():
        async with get_session() as session:
            # Get flow by ID
            try:
                flow_id_uuid = uuid.UUID(flow_id)
            except ValueError:
                click.echo(f"Invalid flow ID format: {flow_id}")
                return
                
            result = await session.execute(
                select(Flow).where(Flow.id == flow_id_uuid)
            )
            flow = result.scalar_one_or_none()
            
            if not flow:
                click.echo(f"Flow {flow_id} not found")
                return
            
            # Parse input data
            try:
                input_data_dict = json.loads(input_data) if input_data else {}
            except json.JSONDecodeError:
                click.echo("Invalid JSON input data")
                return
            
            # Create task
            task = Task(
                id=uuid.uuid4(),
                flow_id=flow.id,
                status='pending',
                input_data=input_data_dict,
                max_retries=max_retries,
                tries=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            session.add(task)
            await session.commit()
            await session.refresh(task)
            
            click.echo(f"Created task {task.id}")
            
    asyncio.run(_create_task())
