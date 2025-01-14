import click
from typing import Optional
from datetime import datetime
from sqlalchemy import text
from ..scheduler_service import SchedulerService
from ..db import get_db_session
from ..logger import setup_logger
from tabulate import tabulate

logger = setup_logger()

@click.group()
def schedules():
    """Manage flow schedules"""
    pass

@schedules.command()
def create():
    """Create a new schedule for a flow"""
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
            click.secho("No flows found", fg='red')
            return
            
        # Show available flows
        click.secho("\nAvailable flows:", bold=True)
        for i, flow in enumerate(flows):
            schedule_text = f"({flow.schedule_count} schedules)" if flow.schedule_count else "(no schedules)"
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
            
        # Create schedule
        schedule = scheduler.create_schedule(
            flow_name=selected_flow.name,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params
        )
        
        # Calculate and show next run
        next_run = scheduler._calculate_next_run(schedule_type, schedule_expr)
        
        # Show success message
        click.secho("\nSchedule created successfully!", fg='green', bold=True)
        click.echo(f"\nDetails:")
        click.echo(f"  ID: {click.style(str(schedule.id), fg='blue')}")
        click.echo(f"  Flow: {click.style(selected_flow.name, fg='green')}")
        click.echo(f"  Type: {schedule_type}")
        click.echo(f"  Expression: {schedule_expr}")
        if flow_params:
            click.echo(f"  Input: {input_value}")
        click.echo(f"  Next run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        click.secho(f"Error creating schedule: {str(e)}", fg='red')
        raise click.ClickException(str(e))

@schedules.command()
@click.argument('schedule_id')
def delete(schedule_id: str):
    """Delete a schedule"""
    try:
        db = get_db_session()
        scheduler = SchedulerService(db)
        
        # Get the schedule
        schedule = scheduler.get_schedule(schedule_id)
        if not schedule:
            click.secho(f"Schedule {schedule_id} not found", fg='red')
            return
        
        # Delete the schedule
        scheduler.delete_schedule(schedule_id)
        click.secho(f"Deleted schedule {schedule_id}", fg='green')
        
    except Exception as e:
        click.secho(f"Error deleting schedule: {str(e)}", fg='red')
        raise click.ClickException(str(e))

@schedules.command()
@click.option('--flow', help='Filter schedules by flow name')
def list(flow: Optional[str] = None):
    """List all schedules or filter by flow"""
    try:
        db = get_db_session()
        scheduler = SchedulerService(db)
        
        schedules = scheduler.list_schedules(flow_name=flow)
        
        if not schedules:
            click.secho("No schedules found", fg='yellow')
            return

        # Prepare table data
        headers = ["ID", "Flow", "Type", "Expression", "Status", "Next Run"]
        rows = []
        
        for schedule in schedules:
            flow_name = schedule.flow.name if schedule.flow else "N/A"
            rows.append([
                str(schedule.id),
                flow_name,
                schedule.schedule_type,
                schedule.schedule_expr,
                schedule.status,
                schedule.next_run_at.strftime("%Y-%m-%d %H:%M:%S") if schedule.next_run_at else "N/A"
            ])
        
        # Print table with a title
        click.secho("\nSchedules:", bold=True)
        click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
        click.echo()
            
    except Exception as e:
        click.secho(f"Error listing schedules: {str(e)}", fg='red')
        raise click.ClickException(str(e))
