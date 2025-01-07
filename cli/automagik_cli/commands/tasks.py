import click
from tabulate import tabulate
from sqlalchemy import select, desc
import json
import os
import pytz
from datetime import datetime
from ..models import Task, Log
from ..db import engine
from sqlalchemy.orm import Session

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
def list():
    """List all tasks"""
    session = Session(engine)
    tasks = session.execute(
        select(Task).order_by(desc(Task.created_at))
    ).scalars()
    
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
    click.echo(tabulate(rows, headers=headers))

@tasks.command()
@click.argument('task_id')
def logs(task_id):
    """Show logs for a specific task"""
    session = Session(engine)
    logs = session.execute(
        select(Log).where(Log.task_id == task_id)
    ).scalars()
    
    rows = []
    for log in logs:
        rows.append([
            format_datetime(log.created_at),
            log.level,
            log.message
        ])
    
    headers = ['Timestamp', 'Level', 'Message']
    click.echo(tabulate(rows, headers=headers))

@tasks.command()
@click.argument('task_id')
def output(task_id):
    """Show output data for a specific task"""
    try:
        session = Session(engine)
        task = session.execute(
            select(Task).where(Task.id == task_id)
        ).scalar_one_or_none()
        
        if not task:
            click.echo(f"Task {task_id} not found")
            return
            
        click.echo("\nTask Details:")
        click.echo(f"Flow: {task.flow.name}")
        click.echo(f"Status: {task.status}")
        click.echo(f"Tries: {task.tries}/{task.max_retries}")
        
        click.echo("\nInput Data:")
        click.echo(json.dumps(task.input_data, indent=2))
        
        click.echo("\nOutput Data:")
        click.echo(json.dumps(task.output_data, indent=2))
        
        click.echo("\nTask Logs:")
        for log in task.logs:
            click.echo(f"[{log.level.upper()}] {format_datetime(log.created_at)}: {log.message}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)