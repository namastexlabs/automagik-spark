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

from ...core.flows import FlowManager
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
                
                # Parse interval
                unit = interval[-1].lower()
                try:
                    value = int(interval[:-1])
                except ValueError:
                    click.echo("Invalid interval format")
                    return
                
                # Convert to minutes
                if unit == 'm':
                    minutes = value
                elif unit == 'h':
                    minutes = value * 60
                elif unit == 'd':
                    minutes = value * 60 * 24
                else:
                    click.echo("Invalid interval unit")
                    return
                
                # Calculate first run
                now = datetime.now(timezone.utc)
                first_run = now + timedelta(minutes=1)  # Start in 1 minute
                click.echo(f"\nFirst run will be at: {first_run.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                
            else:
                click.echo("\nCron Examples:")
                click.echo("  0 8 * * *     - Every day at 8 AM")
                click.echo("  */30 * * * *  - Every 30 minutes")
                click.echo("  0 */4 * * *   - Every 4 hours")
                
                minutes = 1  # TODO: Implement cron parsing
                
            # Get input value
            input_value = click.prompt("\nEnter input value")
            
            # Create schedule
            schedule = await flow_manager.create_schedule(
                str(flow.id),
                schedule_type,
                str(minutes),
                {'input_value': input_value}
            )
            
            if schedule:
                click.echo("\nSchedule created successfully!")
                click.echo(f"Flow: {flow.name}")
                click.echo(f"Type: {schedule_type}")
                
                if schedule_type == 'interval':
                    click.echo(f"Interval: Every {minutes} minutes")
                else:
                    click.echo(f"Cron: {minutes}")  # TODO: Show actual cron expression
                    
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
            schedules = await flow_manager.list_schedules()
            
            if not schedules:
                click.echo("No schedules found")
                return
            
            # Prepare table data
            rows = []
            for schedule in schedules:
                next_run = schedule.next_run_at.strftime('%Y-%m-%d %H:%M:%S') if schedule.next_run_at else 'N/A'
                
                rows.append([
                    schedule.id,
                    schedule.flow.name,
                    schedule.schedule_type,
                    schedule.schedule_expr,
                    schedule.status,
                    next_run
                ])
            
            # Print table
            headers = ['ID', 'Flow', 'Type', 'Expression', 'Status', 'Next Run']
            click.echo("\nFlow Schedules:")
            click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
    
    asyncio.run(_list_schedules())

@schedule_group.command()
@click.argument('schedule-id')
@click.argument('action', type=click.Choice(['pause', 'resume', 'stop']))
def update(schedule_id: str, action: str):
    """Update schedule status."""
    async def _update_schedule():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            success = await flow_manager.update_schedule_status(schedule_id, action)
            
            if success:
                click.echo(f"Schedule {schedule_id} {action}d successfully")
            else:
                click.echo(f"Failed to {action} schedule {schedule_id}")
    
    asyncio.run(_update_schedule())

@schedule_group.command()
@click.argument('schedule-id')
def delete(schedule_id: str):
    """Delete a schedule by its ID."""
    async def _delete_schedule():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            
            try:
                schedule_uuid = UUID(schedule_id)
            except ValueError:
                click.echo("Invalid schedule ID format")
                return
                
            if await flow_manager.delete_schedule(schedule_uuid):
                click.echo(f"Schedule {schedule_id} deleted successfully")
            else:
                click.echo(f"Failed to delete schedule {schedule_id}")
    
    asyncio.run(_delete_schedule())
