import click
from tabulate import tabulate
from sqlalchemy import select
import json
from ..models import Task, Log
from ..db import engine
from sqlalchemy.orm import Session

@click.group()
def tasks():
    """Manage tasks"""
    pass

@tasks.command()
def list():
    """List all tasks"""
    session = Session(engine)
    tasks = session.execute(select(Task)).scalars()
    
    rows = []
    for task in tasks:
        flow_name = task.flow.name if task.flow else "N/A"
        rows.append([
            str(task.id),
            flow_name,
            task.status,
            task.tries,
            task.created_at,
            task.updated_at
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
            log.created_at,
            log.level,
            log.message
        ])
    
    headers = ['Timestamp', 'Level', 'Message']
    click.echo(tabulate(rows, headers=headers))

@tasks.command()
@click.argument('task_id')
def output(task_id):
    """Show output data for a specific task"""
    session = Session(engine)
    task = session.execute(
        select(Task).where(Task.id == task_id)
    ).scalar_one_or_none()
    
    if not task:
        click.echo(f"Task {task_id} not found")
        return
    
    flow_name = task.flow.name if task.flow else "N/A"
    click.echo("\nTask Details:")
    click.echo(f"Flow: {flow_name}")
    click.echo(f"Status: {task.status}")
    click.echo(f"Tries: {task.tries}/{task.max_retries}")
    click.echo("\nInput Data:")
    click.echo(json.dumps(task.input_data, indent=2))
    click.echo("\nOutput Data:")
    click.echo(json.dumps(task.output_data, indent=2))