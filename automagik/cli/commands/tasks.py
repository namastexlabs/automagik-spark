import click
from tabulate import tabulate
import json
import os
import pytz
import uuid
from datetime import datetime
from sqlalchemy import desc

from automagik.core.database.session import get_db_session
from automagik.core.database.models import Task, FlowDB, Log
from automagik.core.scheduler import TaskRunner
from automagik.core.scheduler.exceptions import TaskExecutionError

@click.group()
def tasks():
    """Manage tasks"""
    pass

def get_local_timezone():
    """Get configured timezone from .env or default to UTC"""
    return pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

def format_datetime(dt):
    """Format datetime in local timezone"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    local_tz = get_local_timezone()
    local_dt = dt.astimezone(local_tz)
    return local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

@tasks.command()
@click.option('--flow', help='Filter tasks by flow name')
@click.option('--status', help='Filter tasks by status')
@click.option('--limit', type=int, default=50, help='Limit number of tasks shown')
def list(flow: str = None, status: str = None, limit: int = 50):
    """List all tasks"""
    try:
        db_session = get_db_session()
        
        # Build query
        query = db_session.query(Task).order_by(desc(Task.created_at))
        
        if flow:
            query = query.join(Task.flow).filter(FlowDB.name == flow)
        if status:
            query = query.filter(Task.status == status)
            
        tasks = query.limit(limit).all()
        
        if not tasks:
            click.echo("No tasks found")
            return
        
        rows = []
        for task in tasks:
            flow_name = task.flow.name if task.flow else "N/A"
            rows.append([
                str(task.id),
                flow_name,
                task.status,
                task.tries,
                format_datetime(task.created_at),
                format_datetime(task.updated_at)
            ])
        
        headers = ['ID', 'Flow', 'Status', 'Tries', 'Created', 'Updated']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.secho(f"Error listing tasks: {str(e)}", fg='red')

@tasks.command()
@click.argument('task_id')
def logs(task_id: str):
    """Show logs for a specific task"""
    try:
        db_session = get_db_session()
        
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            click.secho("Invalid task ID format", fg='red')
            return
        
        task = db_session.query(Task).filter(Task.id == task_uuid).first()
        if not task:
            click.secho(f"Task {task_id} not found", fg='red')
            return
        
        if not task.logs:
            click.echo("No logs found for this task")
            return
        
        rows = []
        for log in task.logs:
            rows.append([
                format_datetime(log.created_at),
                log.level.upper(),
                log.message
            ])
        
        headers = ['Timestamp', 'Level', 'Message']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.secho(f"Error retrieving logs: {str(e)}", fg='red')

@tasks.command()
@click.argument('task_id')
def output(task_id: str):
    """Show output data for a specific task"""
    try:
        db_session = get_db_session()
        
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            click.secho("Invalid task ID format", fg='red')
            return
        
        task = db_session.query(Task).filter(Task.id == task_uuid).first()
        if not task:
            click.secho(f"Task {task_id} not found", fg='red')
            return
            
        click.echo("\nTask Details:")
        click.echo(f"Flow: {click.style(task.flow.name, fg='blue')}")
        click.echo(f"Status: {click.style(task.status, fg='green' if task.status == 'completed' else 'yellow')}")
        click.echo(f"Tries: {task.tries}/{task.max_retries}")
        click.echo(f"Created: {format_datetime(task.created_at)}")
        click.echo(f"Updated: {format_datetime(task.updated_at)}")
        
        if task.input_data:
            click.echo("\nInput Data:")
            click.echo(json.dumps(task.input_data, indent=2))
        
        if task.output_data:
            click.echo("\nOutput Data:")
            click.echo(json.dumps(task.output_data, indent=2))
        
        if task.logs:
            click.echo("\nTask Logs:")
            for log in task.logs:
                level_color = {
                    'debug': 'blue',
                    'info': 'green',
                    'warning': 'yellow',
                    'error': 'red'
                }.get(log.level.lower(), 'white')
                
                click.echo(
                    f"[{click.style(log.level.upper(), fg=level_color)}] "
                    f"{format_datetime(log.created_at)}: {log.message}"
                )
        
    except Exception as e:
        click.secho(f"Error retrieving task output: {str(e)}", fg='red')