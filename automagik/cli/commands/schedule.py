"""
Schedule Management Commands

Provides CLI commands for managing flow schedules:
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

from ...core.flows import FlowManager
from ...core.scheduler import SchedulerManager
from ...core.database.session import get_session

logger = logging.getLogger(__name__)

@click.group(name='schedule')
def schedule_group():
    """Manage flow schedules."""
    pass

@schedule_group.command()
def create():
    """Create a new schedule."""
    async def _create_schedule():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            scheduler_manager = SchedulerManager(session, flow_manager)
            flows = await flow_manager.list_flows()
            
            if not flows:
                click.echo("No flows available")
                return
            
            # Show available flows
            click.echo("\nAvailable Flows:")
            for i, flow in enumerate(flows):
                schedule_count = len(flow.schedules)
                click.echo(f"{i}: {flow.name} ({schedule_count} schedules)")
            
            # Get flow selection
            flow_idx = click.prompt("\nSelect a flow", type=int, default=0)
            if flow_idx < 0 or flow_idx >= len(flows):
                click.echo("Invalid flow selection")
                return
            
            flow = flows[flow_idx]
            
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
                
                # Calculate first run
                now = datetime.now(timezone.utc)
                
                if interval[-1] == 'm':
                    first_run = now + timedelta(minutes=value)
                elif interval[-1] == 'h':
                    first_run = now + timedelta(hours=value)
                else:  # days
                    first_run = now + timedelta(days=value)
                click.echo(f"\nFirst run will be at: {first_run.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                
            else:
                click.echo("\nCron Examples:")
                click.echo("  0 8 * * *     - Every day at 8 AM")
                click.echo("  */30 * * * *  - Every 30 minutes")
                click.echo("  0 */4 * * *   - Every 4 hours")
                
                schedule_expr = click.prompt("\nEnter cron expression")
                
                # Validate cron expression
                try:
                    now = datetime.now(timezone.utc)
                    cron = croniter(schedule_expr, now)
                    first_run = cron.get_next(datetime)
                    click.echo(f"\nFirst run will be at: {first_run.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                except ValueError as e:
                    click.echo(f"Invalid cron expression: {e}")
                    return
                
            # Get input value
            input_value = click.prompt("\nEnter input value")
            
            # Create schedule
            schedule = await scheduler_manager.create_schedule(
                flow.id,
                schedule_type,
                schedule_expr,
                {'input_value': input_value}
            )
            
            if schedule:
                click.echo("\nSchedule created successfully!")
                click.echo(f"Flow: {flow.name}")
                click.echo(f"Type: {schedule_type}")
                
                if schedule_type == 'interval':
                    click.echo(f"Interval: Every {schedule_expr}")
                else:
                    click.echo(f"Cron: {schedule_expr}")
                    
                click.echo(f"\nInput value: {input_value}")
                click.echo(f"\nNext run at: {schedule.next_run_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            else:
                click.echo("Failed to create schedule")
    
    asyncio.run(_create_schedule())

@schedule_group.command()
def list():
    """List all schedules."""
    async def _list_schedules():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            scheduler_manager = SchedulerManager(session, flow_manager)
            schedules = await scheduler_manager.list_schedules()
            
            if not schedules:
                click.echo("No schedules found")
                return
            
            # Prepare table data
            rows = []
            for schedule in schedules:
                flow_name = schedule.flow.name if schedule.flow else "Unknown"
                schedule_type = schedule.schedule_type
                schedule_expr = schedule.schedule_expr
                status = schedule.status
                next_run = schedule.next_run_at.strftime('%Y-%m-%d %H:%M:%S UTC') if schedule.next_run_at else 'N/A'
                
                rows.append([
                    str(schedule.id),
                    flow_name,
                    schedule_type,
                    schedule_expr,
                    status,
                    next_run
                ])
            
            # Display table
            headers = ['ID', 'Flow', 'Type', 'Expression', 'Status', 'Next Run']
            click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
    
    asyncio.run(_list_schedules())

@schedule_group.command()
@click.argument('schedule_id')
@click.argument('action', type=click.Choice(['pause', 'resume', 'stop']))
def update(schedule_id: str, action: str):
    """Update schedule status."""
    async def _update_schedule():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            scheduler_manager = SchedulerManager(session, flow_manager)
            result = await scheduler_manager.update_schedule_status(schedule_id, action)
            
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
            flow_manager = FlowManager(session)
            scheduler_manager = SchedulerManager(session, flow_manager)
            result = await scheduler_manager.update_schedule_expression(schedule_id, expression)
            
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
            flow_manager = FlowManager(session)
            scheduler_manager = SchedulerManager(session, flow_manager)
            result = await scheduler_manager.delete_schedule(UUID(schedule_id))
            
            if result:
                click.echo(f"Schedule {schedule_id} deleted successfully")
            else:
                click.echo(f"Failed to delete schedule {schedule_id}")
    
    asyncio.run(_delete_schedule())
