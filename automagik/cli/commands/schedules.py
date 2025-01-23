import click
from typing import Optional
from datetime import datetime
import uuid
from tabulate import tabulate
from sqlalchemy import text

from automagik.core.scheduler.scheduler import SchedulerService
from automagik.core.database.session import get_db_session
from automagik.core.scheduler.exceptions import (
    SchedulerError,
    InvalidScheduleError,
    ScheduleNotFoundError,
    FlowNotFoundError,
    ComponentNotConfiguredError
)
from automagik.core.database.models import Schedule, FlowDB
import json
import sys

@click.group()
def schedules():
    """Manage flow schedules"""
    pass

@schedules.command()
@click.argument('flow_name', required=False)
@click.option(
    '--type',
    type=click.Choice(['interval', 'cron', 'oneshot']),
    help='Type of schedule'
)
@click.option(
    '--expr',
    help='Schedule expression. For interval: "30m", "1h", "1d". For cron: "* * * * *". For oneshot: ISO format datetime (e.g. "2025-01-24T00:00:00")'
)
@click.option(
    '--input',
    'input_json',
    help='JSON string of input parameters'
)
@click.pass_context
def create(ctx, flow_name: Optional[str], type: Optional[str], expr: Optional[str], input_json: Optional[str]):
    """Create a new schedule for a flow"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        # Non-interactive mode
        if flow_name and type and expr and input_json:
            try:
                input_data = json.loads(input_json)
            except json.JSONDecodeError as e:
                click.secho(f"Invalid JSON input: {str(e)}", fg='red', err=True)
                ctx.exit(1)
                
            try:
                schedule = scheduler.create_schedule(
                    flow_name=flow_name,
                    schedule_type=type,
                    schedule_expr=expr,
                    flow_params=input_data
                )
                
                click.secho("Created schedule successfully!", fg='green')
                click.echo(f"ID: {schedule.id}")
                click.echo(f"Flow: {flow_name}")
                click.echo(f"Type: {type}")
                click.echo(f"Expression: {expr}")
                click.echo(f"Next Run: {schedule.next_run_at}")
                click.echo(f"Status: {schedule.status}")
                
            except (InvalidScheduleError, FlowNotFoundError) as e:
                click.secho(str(e), fg='red', err=True)
                ctx.exit(1)
            return

        # Interactive mode
        # Parse input JSON if provided
        input_data = {}
        if input_json:
            try:
                input_data = json.loads(input_json)
            except json.JSONDecodeError as e:
                click.secho(f"\nInvalid JSON input: {str(e)}", fg='red', err=True)
                ctx.exit(1)
            
        # Get flows with schedule count
        flows = db_session.query(FlowDB).all()
        
        if not flows:
            click.secho("No flows found", fg='red', err=True)
            ctx.exit(1)
            
        # Show available flows
        click.secho("\nAvailable flows:", bold=True)
        for i, flow in enumerate(flows):
            schedule_count = db_session.query(Schedule).filter(Schedule.flow_id == flow.id).count()
            schedule_text = f"({schedule_count} schedules)" if schedule_count else "(no schedules)"
            click.echo(f"  {i}: {click.style(flow.name, fg='green')} {click.style(schedule_text, fg='blue')}")
            
        # Get flow selection
        flow_idx = click.prompt("\nSelect a flow", type=int, prompt_suffix=' → ')
        if flow_idx < 0 or flow_idx >= len(flows):
            click.secho("Invalid flow index", fg='red', err=True)
            ctx.exit(1)
            
        selected_flow = flows[flow_idx]
        
        # Show schedule types if not provided
        if not type:
            click.secho("\nSchedule Type:", bold=True)
            click.echo(f"  0: {click.style('Interval', fg='green')} (e.g., every 30 minutes)")
            click.echo(f"  1: {click.style('Cron', fg='green')} (e.g., every day at 8 AM)")
            click.echo(f"  2: {click.style('One-time', fg='green')} (e.g., run once at specific time)")
            
            schedule_type_idx = click.prompt("\nSelect schedule type", type=int, prompt_suffix=' → ')
            if schedule_type_idx not in [0, 1, 2]:
                click.secho("Invalid schedule type", fg='red', err=True)
                ctx.exit(1)
                
            type = ['interval', 'cron', 'oneshot'][schedule_type_idx]
        
        # Get schedule expression if not provided
        if not expr:
            if type == 'interval':
                click.secho("\nInterval Examples:", bold=True)
                click.echo("  5m  - Every 5 minutes")
                click.echo("  30m - Every 30 minutes")
                click.echo("  1h  - Every hour")
                click.echo("  4h  - Every 4 hours")
                click.echo("  1d  - Every day")
                expr = click.prompt("\nEnter interval", prompt_suffix=' → ')
            elif type == 'cron':
                click.secho("\nCron Examples:", bold=True)
                click.echo("  */30 * * * * - Every 30 minutes")
                click.echo("  0 * * * *   - Every hour")
                click.echo("  0 8 * * *   - Every day at 8 AM")
                click.echo("  0 8 * * 1-5 - Every weekday at 8 AM")
                expr = click.prompt("\nEnter cron expression", prompt_suffix=' → ')
            else:  # oneshot
                click.secho("\nOne-time Schedule Examples:", bold=True)
                click.echo("  2025-01-24T00:00:00 - Run at midnight on January 24, 2025")
                click.echo("  2025-02-15T08:30:00 - Run at 8:30 AM on February 15, 2025")
                expr = click.prompt("\nEnter datetime (ISO format)", prompt_suffix=' → ')
            
        # Get input value if not provided
        if not input_data:
            if click.confirm("\nDo you want to set an input value?", prompt_suffix=' → '):
                input_value = click.prompt("Enter input value", prompt_suffix=' → ')
                input_data = {"input": input_value}
        
        try:
            # Create schedule
            schedule = scheduler.create_schedule(
                flow_name=selected_flow.name,
                schedule_type=type,
                schedule_expr=expr,
                flow_params=input_data
            )
            
            # Show success message
            click.secho("\nSchedule created successfully!", fg='green', bold=True)
            click.echo(f"\nDetails:")
            click.echo(f"  ID: {click.style(str(schedule.id), fg='blue')}")
            click.echo(f"  Flow: {click.style(selected_flow.name, fg='blue')}")
            click.echo(f"  Type: {click.style(type, fg='blue')}")
            click.echo(f"  Expression: {click.style(expr, fg='blue')}")
            click.echo(f"  Next Run: {click.style(str(schedule.next_run_at), fg='blue')}")
            click.echo(f"  Status: {click.style(schedule.status, fg='blue')}")
            click.echo(f"  Input: {click.style(str(input_data), fg='blue')}")
                
        except (InvalidScheduleError, FlowNotFoundError) as e:
            click.secho(f"\nInvalid schedule: {str(e)}", fg='red', err=True)
            ctx.exit(1)
            
    except Exception as e:
        click.secho(f"Error creating schedule: {str(e)}", fg='red', err=True)
        ctx.exit(1)

@schedules.command()
@click.argument('schedule_id')
@click.pass_context
def delete(ctx, schedule_id: str):
    """Delete a schedule"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        try:
            schedule_uuid = uuid.UUID(schedule_id)
        except ValueError:
            click.secho("Invalid schedule ID format", fg='red', err=True)
            ctx.exit(1)
            
        try:
            scheduler.delete_schedule(schedule_uuid)
            click.secho("Schedule deleted successfully", fg='green')
        except ScheduleNotFoundError:
            click.secho("Schedule not found", fg='red', err=True)
            ctx.exit(1)
            
    except Exception as e:
        click.secho(f"Error deleting schedule: {str(e)}", fg='red', err=True)
        ctx.exit(1)

@schedules.command()
@click.option('--type', type=click.Choice(['interval', 'cron', 'oneshot']), help='Filter by schedule type')
@click.option('--status', type=click.Choice(['active', 'completed', 'failed']), help='Filter by schedule status')
@click.pass_context
def list(ctx, type: Optional[str], status: Optional[str]):
    """List all schedules"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        try:
            schedules = scheduler.get_schedules(schedule_type=type, status=status)
            
            if not schedules:
                click.secho("No schedules found", fg='yellow')
                return
                
            # Format schedules into table
            headers = ['ID', 'Flow', 'Type', 'Expression', 'Status', 'Next Run']
            rows = []
            for schedule in schedules:
                rows.append([
                    str(schedule.id),
                    schedule.flow.name if schedule.flow else 'Unknown',
                    schedule.schedule_type,
                    schedule.schedule_expr,
                    schedule.status,
                    schedule.next_run_at
                ])
                
            click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
            
        except Exception as e:
            click.secho(f"Error listing schedules: {str(e)}", fg='red', err=True)
            ctx.exit(1)
            
    except Exception as e:
        click.secho(f"Error listing schedules: {str(e)}", fg='red', err=True)
        ctx.exit(1)
