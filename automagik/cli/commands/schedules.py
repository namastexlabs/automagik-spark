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
@click.argument('flow_id')
@click.option('--type', type=click.Choice(['interval', 'cron', 'oneshot']), required=True, help='Schedule type')
@click.option('--expr', required=True, help='Schedule expression (e.g., "5m" for interval, "0 * * * *" for cron, or ISO datetime for oneshot)')
@click.option('--input', 'input_json', required=True, help='Input JSON for the flow')
def create(flow_id: str, type: str, expr: str, input_json: str):
    """Create a new schedule"""
    try:
        # Initialize scheduler service
        db_session = get_db_session()
        scheduler_service = SchedulerService(db_session)

        # Parse input JSON
        try:
            input_data = json.loads(input_json)
        except json.JSONDecodeError:
            click.echo("Invalid JSON input", err=True)
            click.get_current_context().exit(1)

        # Try to get flow by ID first, then by name
        try:
            flow_uuid = uuid.UUID(flow_id)
            flow = db_session.query(FlowDB).filter(FlowDB.id == flow_uuid).first()
        except ValueError:
            flow = db_session.query(FlowDB).filter(FlowDB.name == flow_id).first()

        if not flow:
            click.echo(f"Flow not found: {flow_id}", err=True)
            click.get_current_context().exit(1)

        # Create schedule
        try:
            schedule = scheduler_service.create_schedule(
                flow_name=flow.name,
                schedule_type=type,
                schedule_expr=expr,
                flow_params=input_data
            )

            if schedule:
                click.echo("Created schedule successfully!")
                click.echo(f"ID: {schedule.id}")
                click.echo(f"Type: {schedule.schedule_type}")
                click.echo(f"Expression: {schedule.schedule_expr}")
                click.echo(f"Next run: {schedule.next_run_at}")
            else:
                click.echo("Failed to create schedule", err=True)
                click.get_current_context().exit(1)

        except InvalidScheduleError as e:
            click.echo(f"Invalid schedule: {str(e)}", err=True)
            click.get_current_context().exit(1)

    except Exception as e:
        click.echo(f"Error creating schedule: {str(e)}", err=True)
        click.get_current_context().exit(1)

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
@click.option('--type', 'schedule_type', type=click.Choice(['interval', 'cron', 'oneshot']), help='Filter by schedule type')
@click.option('--status', type=click.Choice(['active', 'completed', 'failed']), help='Filter by status')
def list(schedule_type=None, status=None):
    """List all schedules"""
    try:
        # Initialize scheduler service
        db_session = get_db_session()
        scheduler_service = SchedulerService(db_session)

        # Get schedules
        schedules = scheduler_service.list_schedules(status=status)

        # Filter by type if specified
        if schedule_type:
            schedules = [s for s in schedules if s.schedule_type == schedule_type]

        if not schedules:
            click.echo("No schedules found")
            return

        # Format schedules for display
        headers = ["ID", "Flow", "Type", "Expression", "Status", "Next Run"]
        rows = []

        for schedule in schedules:
            rows.append([
                str(schedule.id),
                schedule.flow.name if schedule.flow else "Unknown",
                schedule.schedule_type,
                schedule.schedule_expr,
                schedule.status,
                schedule.next_run_at.strftime("%Y-%m-%d %H:%M:%S") if schedule.next_run_at else "N/A"
            ])

        click.echo(tabulate(rows, headers=headers, tablefmt="grid"))

    except Exception as e:
        click.echo(f"Error listing schedules: {str(e)}", err=True)
