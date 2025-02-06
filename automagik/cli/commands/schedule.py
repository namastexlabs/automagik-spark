"""
Schedule Management Commands

Provides CLI commands for managing workflow schedules:
- Create schedules
- List schedules
- Update schedule status (pause/resume/stop)
- Delete schedules
"""

import asyncio
import click
from typing import Optional
import logging
from tabulate import tabulate
from datetime import datetime, timedelta, timezone
from uuid import UUID
from croniter import croniter
from sqlalchemy import select

from ...core.workflows import WorkflowManager
from ...core.scheduler.scheduler import WorkflowScheduler
from ...core.database.session import get_session
from ...core.database.models import Workflow

logger = logging.getLogger(__name__)

@click.group(name='schedules')
def schedule_group():
    """Manage workflow schedules."""
    pass

@schedule_group.command()
def create():
    """Create a new schedule."""
    async def _create_schedule():
        async with get_session() as session:
            workflow_manager = WorkflowManager(session)
            scheduler = WorkflowScheduler(session, workflow_manager)
            workflows = await workflow_manager.list_workflows(options={"joinedload": ["schedules"]})
            
            if not workflows:
                click.echo("No workflows available")
                return
            
            # Show available workflows
            click.echo("\nAvailable Workflows:")
            for i, workflow in enumerate(workflows):
                # Get schedule count safely
                schedule_count = len(workflow.schedules) if hasattr(workflow, 'schedules') and workflow.schedules else 0
                click.echo(f"{i}: {workflow.name} ({schedule_count} schedules)")
            
            # Get workflow selection
            workflow_idx = click.prompt("\nSelect a workflow", type=int, default=0)
            if workflow_idx < 0 or workflow_idx >= len(workflows):
                click.echo("Invalid workflow selection")
                return
            
            workflow = workflows[workflow_idx]
            
            # Get schedule type
            click.echo("\nSchedule Type:")
            click.echo("  0: Interval (e.g., every 30 minutes)")
            click.echo("  1: Cron (e.g., every day at 8 AM)")
            
            schedule_type = click.prompt("\nSelect schedule type", type=int, default=0)
            if schedule_type not in [0, 1]:
                click.echo("Invalid schedule type")
                return
            
            schedule_type = 'interval' if schedule_type == 0 else 'cron'
            
            # Get schedule expression
            if schedule_type == 'interval':
                click.echo("\nInterval Examples:")
                click.echo("  5m  - Every 5 minutes")
                click.echo("  30m - Every 30 minutes")
                click.echo("  1h  - Every hour")
                click.echo("  4h  - Every 4 hours")
                click.echo("  1d  - Every day")
                
                interval = click.prompt("\nEnter interval")
                
                # Validate interval format
                if not interval[-1].lower() in ['m', 'h', 'd']:
                    click.echo("Invalid interval unit")
                    return
                    
                try:
                    value = int(interval[:-1])
                    if value <= 0:
                        click.echo("Interval value must be positive")
                        return
                except ValueError:
                    click.echo("Invalid interval format")
                    return
                
                # Use the interval string directly
                schedule_expr = interval.lower()
                
            else:  # cron
                click.echo("\nCron Examples:")
                click.echo("  * * * * *     - Every minute")
                click.echo("  */5 * * * *   - Every 5 minutes")
                click.echo("  0 * * * *     - Every hour")
                click.echo("  0 0 * * *     - Every day at midnight")
                click.echo("  0 8 * * *     - Every day at 8 AM")
                click.echo("  0 8 * * 1-5   - Every weekday at 8 AM")
                
                schedule_expr = click.prompt("\nEnter cron expression")
                
                # Validate cron expression
                if not croniter.is_valid(schedule_expr):
                    click.echo("Invalid cron expression")
                    return
            
            # Get input data
            input_value = click.prompt("\nEnter input value", default="")
            
            # Create schedule
            try:
                schedule = await scheduler.create_schedule(
                    workflow.id,
                    schedule_type,
                    schedule_expr,
                    workflow_params=input_value
                )
                if schedule:
                    click.echo(f"\nSchedule created successfully with ID: {schedule.id}")
                else:
                    click.echo("\nFailed to create schedule")
            except Exception as e:
                click.echo(f"Error creating schedule: {str(e)}")
                return
    
    asyncio.run(_create_schedule())

@schedule_group.command()
def list():
    """List all schedules."""
    async def _list_schedules():
        async with get_session() as session:
            workflow_manager = WorkflowManager(session)
            scheduler = WorkflowScheduler(session, workflow_manager)
            schedules = await scheduler.list_schedules()
            
            if not schedules:
                click.echo("No schedules found")
                return
            
            headers = ["ID", "Workflow", "Type", "Expression", "Next Run", "Status"]
            rows = []
            
            for schedule in schedules:
                # Get workflow name safely without lazy loading
                workflow_id = schedule.workflow_id
                workflow_result = await session.execute(
                    select(Workflow).where(Workflow.id == workflow_id)
                )
                workflow = workflow_result.scalar_one_or_none()
                workflow_name = workflow.name if workflow else "Unknown"
                
                rows.append([
                    str(schedule.id),
                    workflow_name,
                    schedule.schedule_type,
                    schedule.schedule_expr,
                    schedule.next_run_at.strftime("%Y-%m-%d %H:%M:%S") if schedule.next_run_at else "N/A",
                    schedule.status
                ])
            
            click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
    
    asyncio.run(_list_schedules())

@schedule_group.command()
@click.argument('schedule_id')
@click.argument('action', type=click.Choice(['pause', 'resume', 'stop']))
def update(schedule_id: str, action: str):
    """Update schedule status."""
    async def _update_schedule():
        async with get_session() as session:
            workflow_manager = WorkflowManager(session)
            scheduler = WorkflowScheduler(session, workflow_manager)
            result = await scheduler.update_schedule_status(schedule_id, action)
            
            if result:
                click.echo(f"Schedule {schedule_id} {action}d successfully")
            else:
                click.echo(f"Failed to {action} schedule {schedule_id}")
    
    asyncio.run(_update_schedule())

@schedule_group.command()
@click.argument('schedule_id')
@click.argument('expression')
def set_expression(schedule_id: str, expression: str):
    """Update schedule expression."""
    async def _update_expression():
        async with get_session() as session:
            workflow_manager = WorkflowManager(session)
            scheduler = WorkflowScheduler(session, workflow_manager)
            result = await scheduler.update_schedule_expression(schedule_id, expression)
            
            if result:
                click.echo(f"Schedule {schedule_id} expression updated to '{expression}'")
            else:
                click.echo(f"Failed to update schedule {schedule_id} expression")
    
    asyncio.run(_update_expression())

@schedule_group.command()
@click.argument('schedule_id')
def delete(schedule_id: str):
    """Delete a schedule."""
    async def _delete_schedule():
        async with get_session() as session:
            workflow_manager = WorkflowManager(session)
            scheduler = WorkflowScheduler(session, workflow_manager)
            result = await scheduler.delete_schedule(UUID(schedule_id))
            
            if result:
                click.echo(f"Schedule {schedule_id} deleted successfully")
            else:
                click.echo(f"Failed to delete schedule {schedule_id}")
    
    asyncio.run(_delete_schedule())
