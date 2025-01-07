import click
import json
import uuid
from datetime import datetime
from tabulate import tabulate

from automagik_cli.scheduler_service import SchedulerService
from automagik_cli.db import get_db_session

def format_datetime(dt):
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "N/A"

def format_uuid(id):
    """Format UUID for display."""
    return str(id) if id else "N/A"

@click.group()
def schedules():
    """Manage schedules"""
    pass

@schedules.command()
@click.option('--flow', required=True, help='Name of the flow to schedule')
@click.option('--type', 'schedule_type', type=click.Choice(['interval', 'cron']), required=True,
              help='Type of schedule (interval or cron)')
@click.option('--expr', 'schedule_expr', required=True,
              help='Schedule expression (e.g., "30m" for interval, "0 * * * *" for cron)')
@click.option('--params', 'flow_params', type=str, help='Flow parameters as JSON string')
def create(flow, schedule_type, schedule_expr, flow_params):
    """Create a new schedule for a flow"""
    try:
        db = get_db_session()
        scheduler = SchedulerService(db)
        
        # Parse flow parameters if provided
        params = json.loads(flow_params) if flow_params else None
        
        schedule = scheduler.create_schedule(
            flow_name=flow,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=params
        )
        
        click.echo(f"Created schedule {schedule.id} for flow {flow}")
        click.echo(f"Next run at: {format_datetime(schedule.next_run_at)}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except json.JSONDecodeError:
        click.echo("Error: Invalid JSON format for flow parameters", err=True)

@schedules.command()
@click.option('--flow', help='Filter schedules by flow name')
def list(flow):
    """List all schedules or filter by flow"""
    db = get_db_session()
    scheduler = SchedulerService(db)
    
    schedules = scheduler.list_schedules(flow_name=flow)
    
    if not schedules:
        click.echo("No schedules found")
        return

    # Prepare table data
    headers = ["ID", "Flow", "Type", "Expression", "Status", "Next Run"]
    rows = []
    
    for schedule in schedules:
        flow_name = schedule.flow.name if schedule.flow else "N/A"
        rows.append([
            format_uuid(schedule.id),
            flow_name,
            schedule.schedule_type,
            schedule.schedule_expr,
            schedule.status,
            format_datetime(schedule.next_run_at)
        ])
    
    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))

@schedules.command()
@click.argument('schedule_id')
def delete(schedule_id):
    """Delete a schedule"""
    try:
        db = get_db_session()
        scheduler = SchedulerService(db)
        
        if scheduler.delete_schedule(uuid.UUID(schedule_id)):
            click.echo(f"Deleted schedule {schedule_id}")
        else:
            click.echo(f"Schedule {schedule_id} not found", err=True)
    except ValueError:
        click.echo("Invalid schedule ID format", err=True)

@schedules.command()
def due():
    """List all schedules that are due to run"""
    db = get_db_session()
    scheduler = SchedulerService(db)
    
    schedules = scheduler.get_due_schedules()
    
    if not schedules:
        click.echo("No schedules due to run")
        return

    # Prepare table data
    headers = ["ID", "Flow", "Type", "Expression", "Next Run"]
    rows = []
    
    for schedule in schedules:
        flow_name = schedule.flow.name if schedule.flow else "N/A"
        rows.append([
            format_uuid(schedule.id),
            flow_name,
            schedule.schedule_type,
            schedule.schedule_expr,
            format_datetime(schedule.next_run_at)
        ])
    
    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))