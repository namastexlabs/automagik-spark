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

@click.group()
def schedules():
    """Manage flow schedules"""
    pass

@schedules.command()
def create():
    """Create a new schedule for a flow"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        # Get flows with schedule count
        flows = db_session.query(FlowDB).all()
        
        if not flows:
            click.secho("No flows found", fg='red')
            return
            
        # Show available flows
        click.secho("\nAvailable flows:", bold=True)
        for i, flow in enumerate(flows):
            schedule_count = db_session.query(Schedule).filter(Schedule.flow_id == flow.id).count()
            schedule_text = f"({schedule_count} schedules)" if schedule_count else "(no schedules)"
            click.echo(f"  {i}: {click.style(flow.name, fg='green')} {click.style(schedule_text, fg='blue')}")
            
        # Get flow selection
        flow_idx = click.prompt("\nSelect a flow", type=int, prompt_suffix=' → ')
        if flow_idx < 0 or flow_idx >= len(flows):
            click.secho("Invalid flow index", fg='red')
            return
            
        selected_flow = flows[flow_idx]
        
        # Show schedule types
        click.secho("\nSchedule Type:", bold=True)
        click.echo(f"  0: {click.style('Interval', fg='green')} (e.g., every 30 minutes)")
        click.echo(f"  1: {click.style('Cron', fg='green')} (e.g., every day at 8 AM)")
        
        # Get schedule type
        schedule_type_idx = click.prompt("\nSelect schedule type", type=int, prompt_suffix=' → ')
        if schedule_type_idx not in [0, 1]:
            click.secho("Invalid schedule type", fg='red')
            return
            
        schedule_type = 'interval' if schedule_type_idx == 0 else 'cron'
        
        # Get schedule expression
        if schedule_type == 'interval':
            click.secho("\nInterval Examples:", bold=True)
            click.echo("  5m  - Every 5 minutes")
            click.echo("  30m - Every 30 minutes")
            click.echo("  1h  - Every hour")
            click.echo("  4h  - Every 4 hours")
            click.echo("  1d  - Every day")
            schedule_expr = click.prompt("\nEnter interval", prompt_suffix=' → ')
        else:
            click.secho("\nCron Examples:", bold=True)
            click.echo("  */30 * * * * - Every 30 minutes")
            click.echo("  0 * * * *   - Every hour")
            click.echo("  0 8 * * *   - Every day at 8 AM")
            click.echo("  0 8 * * 1-5 - Every weekday at 8 AM")
            schedule_expr = click.prompt("\nEnter cron expression", prompt_suffix=' → ')
            
        # Get input value
        if click.confirm("\nDo you want to set an input value?", prompt_suffix=' → '):
            input_value = click.prompt("Enter input value", prompt_suffix=' → ')
            flow_params = {"input": input_value}
        else:
            flow_params = {}
            
        try:
            # Create schedule
            schedule = scheduler.create_schedule(
                flow_name=selected_flow.name,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                flow_params=flow_params
            )
            
            # Show success message
            click.secho("\nSchedule created successfully!", fg='green', bold=True)
            click.echo(f"\nDetails:")
            click.echo(f"  ID: {click.style(str(schedule.id), fg='blue')}")
            click.echo(f"  Flow: {click.style(selected_flow.name, fg='blue')}")
            click.echo(f"  Type: {click.style(schedule_type, fg='blue')}")
            click.echo(f"  Expression: {click.style(schedule_expr, fg='blue')}")
            click.echo(f"  Next Run: {click.style(str(schedule.next_run_at), fg='blue')}")
            if flow_params:
                click.echo(f"  Flow Params: {click.style(str(flow_params), fg='blue')}")
                
        except InvalidScheduleError as e:
            click.secho(f"\nInvalid schedule: {str(e)}", fg='red')
        except FlowNotFoundError as e:
            click.secho(f"\nFlow not found: {str(e)}", fg='red')
        except ComponentNotConfiguredError as e:
            click.secho(f"\nComponent not configured: {str(e)}", fg='red')
        except SchedulerError as e:
            click.secho(f"\nScheduler error: {str(e)}", fg='red')
            
    except Exception as e:
        click.secho(f"\nError creating schedule: {str(e)}", fg='red')

@schedules.command()
@click.argument('schedule_id')
def delete(schedule_id: str):
    """Delete a schedule"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        try:
            schedule_uuid = uuid.UUID(schedule_id)
        except ValueError:
            click.secho("Invalid schedule ID format", fg='red')
            return
            
        if scheduler.delete_schedule(schedule_uuid):
            click.secho("Schedule deleted successfully", fg='green')
        else:
            click.secho("Schedule not found", fg='red')
            
    except Exception as e:
        click.secho(f"Error deleting schedule: {str(e)}", fg='red')

@schedules.command()
@click.option('--flow', help='Filter schedules by flow name')
@click.option('--status', help='Filter schedules by status (active/paused)')
def list(flow: Optional[str] = None, status: Optional[str] = None):
    """List all schedules"""
    try:
        db_session = get_db_session()
        scheduler = SchedulerService(db_session)
        
        schedules = scheduler.list_schedules(flow_name=flow, status=status)
        
        if not schedules:
            click.echo("No schedules found")
            return
            
        rows = []
        for schedule in schedules:
            next_run = schedule.next_run_at.strftime('%Y-%m-%d %H:%M:%S') if schedule.next_run_at else 'N/A'
            rows.append([
                str(schedule.id),
                schedule.flow.name,
                schedule.schedule_type,
                schedule.schedule_expr,
                schedule.status,
                next_run
            ])
            
        headers = ['ID', 'Flow', 'Type', 'Expression', 'Status', 'Next Run']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.secho(f"Error listing schedules: {str(e)}", fg='red')
