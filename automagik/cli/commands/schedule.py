
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
import json
from typing import Optional
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID
from croniter import croniter
from sqlalchemy import select, func, case

from ...core.workflows import WorkflowManager
from ...core.scheduler.scheduler import WorkflowScheduler
from ...core.database.session import get_session
from ...core.database.models import Workflow, Schedule, Task
from ..utils.table_styles import (
    create_rich_table,
    format_timestamp,
    get_status_style,
    print_table
)

logger = logging.getLogger(__name__)

@click.group(name='schedule')
def schedule_group():
    """Manage workflow schedules."""
    pass

@schedule_group.command()
def create():
    """Create a new schedule. Interactive command."""
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
                schedule_count = len(workflow.get('schedules', [])) if isinstance(workflow, dict) else len(workflow.schedules) if hasattr(workflow, 'schedules') else 0
                name = workflow.get('name', 'Unnamed') if isinstance(workflow, dict) else workflow.name
                click.echo(f"{i}: {name} ({schedule_count} schedules)")
            
            # Get workflow selection
            workflow_idx = click.prompt("\nSelect a workflow", type=int, default=0)
            if workflow_idx < 0 or workflow_idx >= len(workflows):
                click.echo("Invalid workflow selection")
                return
            
            workflow = workflows[workflow_idx]
            workflow_id = workflow.get('id') if isinstance(workflow, dict) else workflow.id
            
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
                    workflow_id,
                    schedule_type,
                    schedule_expr,
                    input_data=input_value
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
                click.secho("\n No schedules found", fg="yellow")
                return
            
            # Create table with consistent styling
            table = create_rich_table(
                title="Workflow Schedules",
                caption=f"Total: {len(schedules)} schedule(s)",
                columns=[
                    {"name": "ID", "justify": "left", "style": "bright_blue", "no_wrap": True},
                    {"name": "Workflow", "justify": "left", "style": "green"},
                    {"name": "Type", "justify": "center", "style": "magenta"},
                    {"name": "Expression", "justify": "left", "style": "cyan"},
                    {"name": "Next Run", "justify": "left", "style": "yellow"},
                    {"name": "Tasks (Failed)", "justify": "center", "style": "red"},
                    {"name": "Input Params", "justify": "left", "style": "cyan"},
                    {"name": "Status", "justify": "center", "style": "bold"}
                ]
            )
            
            for schedule in schedules:
                # Get workflow name safely without lazy loading
                workflow_id = schedule.workflow_id
                workflow_result = await session.execute(
                    select(Workflow).where(Workflow.id == workflow_id)
                )
                workflow = workflow_result.scalar_one_or_none()
                workflow_name = workflow.name if workflow else "[dim italic]Unknown[/dim italic]"
                
                # Get task statistics
                task_stats = await session.execute(
                    select(
                        func.count(Task.id).label('total'),
                        func.count(case((Task.status == 'failed', 1))).label('failed')
                    ).where(Task.schedule_id == schedule.id)
                )
                stats = task_stats.first()
                task_stats_str = f"[white]{stats.total}[/white] ([red]{stats.failed}[/red])"
                
                # Format input parameters
                input_params = schedule.input_data
                if input_params:
                    try:
                        # Try to parse as JSON for better formatting
                        params_dict = json.loads(input_params)
                        input_display = str(params_dict)
                    except json.JSONDecodeError:
                        input_display = input_params
                    # Truncate if too long
                    if len(input_display) > 30:
                        input_display = input_display[:27] + "..."
                    input_display = f"[cyan]{input_display}[/cyan]"
                else:
                    input_display = "[dim]none[/dim]"
                
                # Format schedule type
                schedule_type = f"[magenta italic]{schedule.schedule_type}[/magenta italic]"
                
                # Format expression based on type
                if schedule.schedule_type == 'interval':
                    expr = f"[cyan]every {schedule.schedule_expr}[/cyan]"
                else:
                    expr = f"[cyan]{schedule.schedule_expr}[/cyan]"
                
                # Format next run
                next_run = format_timestamp(schedule.next_run_at) if schedule.next_run_at else "[dim]N/A[/dim]"
                
                # Get status with icon
                status_map = {
                    'active': '[bold green]●[/bold green] ACTIVE',
                    'paused': '[bold yellow]⏸[/bold yellow] PAUSED',
                    'stopped': '[bold red]■[/bold red] STOPPED'
                }
                status = status_map.get(schedule.status.lower(), f"[bold white]{schedule.status.upper()}[/bold white]")
                
                # Add row
                table.add_row(
                    str(schedule.id),
                    workflow_name,
                    schedule_type,
                    expr,
                    next_run,
                    task_stats_str,
                    input_display,
                    status
                )
            
            print_table(table)
    
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

@schedule_group.command(name='set-input')
@click.argument('schedule_id')
@click.argument('input_data')
def set_input(schedule_id: str, input_data: str):
    """Update schedule input data."""
    async def _set_input():
        try:
            async with get_session() as session:
                # Get schedule
                stmt = select(Schedule).where(Schedule.id == UUID(schedule_id))
                result = await session.execute(stmt)
                schedule = result.scalar_one_or_none()
                
                if not schedule:
                    click.echo(f"Schedule {schedule_id} not found")
                    return
                
                # Update input data
                schedule.input_data = input_data
                await session.commit()
                
                click.echo(f"Updated input data for schedule {schedule_id}")
        except Exception as e:
            click.echo(f"Error updating schedule input data: {e}")
    
    asyncio.run(_set_input())

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


