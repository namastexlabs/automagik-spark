import click
import json
import uuid
from datetime import datetime
from tabulate import tabulate
from sqlalchemy import text
from ..db import get_db_session
from ..services.models import FlowDB, Schedule
from ..scheduler_service import SchedulerService

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
def schedule():
    """Schedule a flow to run automatically"""
    try:
        db = get_db_session()
        scheduler = SchedulerService(db)
        
        # Get flows with schedule count
        flows = db.execute(text("""
            SELECT f.*, COUNT(s.id) as schedule_count
            FROM flows f
            LEFT JOIN schedules s ON f.id = s.flow_id
            GROUP BY f.id
        """)).fetchall()
        
        if not flows:
            click.echo("No flows found")
            return
            
        # Show available flows
        click.echo("\nAvailable flows:")
        for i, flow in enumerate(flows):
            schedule_text = f"({flow.schedule_count} schedules)" if flow.schedule_count else "(no schedules)"
            click.echo(f"{i}: {flow.name} {schedule_text}")
            
        # Get flow selection
        flow_idx = click.prompt("\nSelect a flow by index", type=int)
        if flow_idx < 0 or flow_idx >= len(flows):
            click.echo("Invalid flow index")
            return
            
        selected_flow = flows[flow_idx]
        
        # Show schedule types
        click.echo("\nAvailable schedule types:")
        click.echo("0: Interval (e.g., every 30 minutes)")
        click.echo("1: Cron expression (e.g., every day at 8 AM)")
        
        # Get schedule type
        schedule_type_idx = click.prompt("\nSelect schedule type by index", type=int)
        if schedule_type_idx not in [0, 1]:
            click.echo("Invalid schedule type")
            return
            
        schedule_type = 'interval' if schedule_type_idx == 0 else 'cron'
        
        # Get schedule expression
        if schedule_type == 'interval':
            click.echo("\nInterval examples:")
            click.echo("  5m - Every 5 minutes")
            click.echo("  30m - Every 30 minutes")
            click.echo("  1h - Every hour")
            click.echo("  4h - Every 4 hours")
            click.echo("  1d - Every day")
            schedule_expr = click.prompt("\nEnter interval (e.g., 30m, 1h, 1d)")
        else:
            click.echo("\nCron examples:")
            click.echo("  */30 * * * * - Every 30 minutes")
            click.echo("  0 * * * * - Every hour")
            click.echo("  0 8 * * * - Every day at 8 AM")
            click.echo("  0 8 * * 1-5 - Every weekday at 8 AM")
            schedule_expr = click.prompt("\nEnter cron expression")
            
        # Get input value
        if click.confirm("\nDo you want to set an input value?"):
            input_value = click.prompt("Enter input value")
            flow_params = {"input": input_value}
        else:
            flow_params = {}
            
        # Create schedule
        schedule = scheduler.create_schedule(
            flow_name=selected_flow.name,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params
        )
        
        click.echo(f"\nCreated schedule {schedule.id} for flow {selected_flow.name}")
        click.echo(f"Type: {schedule_type}")
        click.echo(f"Expression: {schedule_expr}")
        if flow_params:
            click.echo(f"Input value: {flow_params.get('input')}")
        click.echo(f"Next run at: {schedule.next_run_at}")
        
    except Exception as e:
        click.echo(f"Error creating schedule: {str(e)}", err=True)

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