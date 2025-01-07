import click
from ..task_runner import TaskRunner

@click.command()
@click.option('--daemon', is_flag=True, help='Run in daemon mode')
def run(daemon):
    """Run the task processor"""
    runner = TaskRunner()
    
    if daemon:
        # Run continuously
        runner.run()
    else:
        # Process current pending tasks once
        tasks = runner.get_pending_tasks()
        for task in tasks:
            runner.execute_task(task) 