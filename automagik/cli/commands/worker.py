
"""
Worker Command Module

Provides CLI commands for running the worker that executes scheduled workflows.
"""

import asyncio
import click
import json
import logging
import os
import psutil
import signal
import socket
import sys
import re
import subprocess
import time
from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database.models import Worker, Schedule, Task, Workflow
from ...core.database.session import get_session
from ...core.workflows.manager import WorkflowManager
from ...core.workflows.task import TaskManager
from ...core.scheduler.scheduler import WorkflowScheduler as SchedulerManager
from ...core.workflows.remote import LangFlowManager
from ...core.celery_config import app as celery_app
from ...core.tasks.workflow_tasks import execute_workflow, schedule_workflow
from tabulate import tabulate

# Initialize logger with basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Configure paths
LOG_DIR = os.path.expanduser('~/.automagik')
WORKER_PID_FILE = os.path.join(LOG_DIR, 'worker.pid')
BEAT_PID_FILE = os.path.join(LOG_DIR, 'beat.pid')

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def configure_logging():
    """Configure logging based on environment variables."""
    log_path = os.getenv('AUTOMAGIK_WORKER_LOG')
    if not log_path:
        # Check if we're in development mode (local directory exists)
        if os.path.isdir('logs'):
            log_path = os.path.expanduser('logs/worker.log')
        else:
            # Default to system logs in production
            log_path = '/var/log/automagik/worker.log'
    
    # Ensure log directory exists
    log_dir = os.path.dirname(log_path)
    os.makedirs(log_dir, exist_ok=True)
    
    # Reset root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Configure root logger
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logging.root.addHandler(file_handler)
    
    # Also add console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.root.addHandler(console_handler)
    
    # Set log level from environment or default to INFO
    log_level = os.getenv('AUTOMAGIK_LOG_LEVEL', 'INFO')
    logging.root.setLevel(getattr(logging, log_level))
    
    return log_path

async def process_schedule(session, schedule, workflow_manager, now=None):
    """Process a single schedule using Celery task."""
    if now is None:
        now = datetime.now(timezone.utc)
        
    try:
        # Log schedule parameters
        logger.debug(f"Processing schedule {schedule.id} for workflow {schedule.workflow_id}")
        logger.debug(f"Schedule parameters: {schedule.workflow_params}")
        
        # Create task
        input_data = schedule.workflow_params
        if isinstance(input_data, str):
            task_input = input_data
        elif isinstance(input_data, dict):
            task_input = json.dumps(input_data)
        else:
            task_input = "{}"
            
        task = Task(
            id=uuid4(),
            workflow_id=schedule.workflow_id,
            status='pending',
            input_data=task_input,
            created_at=now,
            updated_at=now,
            tries=0,
            max_retries=3
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        
        logger.info(f"Created task {task.id} for schedule {schedule.id}")
        logger.debug(f"Task input data: {task.input_data}")
        
        # Queue task in Celery
        execute_workflow.delay(str(task.id))
        
        # Update next run time for interval schedules
        if schedule.interval:
            schedule.next_run = now + parse_interval(schedule.interval)
            await session.commit()
            
        return True
        
    except Exception as e:
        logger.error(f"Failed to process schedule {schedule.id}: {str(e)}")
        return False

def save_worker_pid(pid):
    """Save worker PID to file."""
    with open(WORKER_PID_FILE, 'w') as f:
        f.write(str(pid))

def save_beat_pid(pid):
    """Save beat scheduler PID to file."""
    with open(BEAT_PID_FILE, 'w') as f:
        f.write(str(pid))

def get_worker_pid():
    """Get worker PID from file."""
    try:
        with open(WORKER_PID_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None

def get_beat_pid():
    """Get beat scheduler PID from file."""
    try:
        with open(BEAT_PID_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None

def remove_worker_pid():
    """Remove worker PID file."""
    try:
        os.remove(WORKER_PID_FILE)
    except FileNotFoundError:
        pass

def remove_beat_pid():
    """Remove beat scheduler PID file."""
    try:
        os.remove(BEAT_PID_FILE)
    except FileNotFoundError:
        pass

worker_group = click.Group(name="worker", help="Worker management commands")

@worker_group.command()
@click.option('--threads', default=2, type=int, help='Number of worker threads')
def start(threads: int = 2):
    """Start the worker."""
    try:
        # Configure logging
        configure_logging()
        
        # Check if worker is already running
        if get_worker_pid():
            click.echo("Worker is already running")
            return
        
        # Check if beat scheduler is already running
        if get_beat_pid():
            click.echo("Beat scheduler is already running")
            return
        
        # Create log directory
        log_dir = os.path.expanduser('~/.automagik')
        os.makedirs(log_dir, exist_ok=True)
        
        # Start worker process
        worker_cmd = [
            'celery',
            '-A', 'automagik.core.celery_config',
            'worker',
            '--loglevel=INFO',
            '-P', 'prefork',
            '--concurrency', str(threads),
            '--logfile', os.path.join(log_dir, 'worker.log'),
            '--pidfile', os.path.join(log_dir, 'worker.pid'),
            '--hostname', 'celery@automagik',
            '--without-gossip',  # Disable gossip to avoid broken pipe
            '--without-mingle',  # Disable mingle to avoid broken pipe
            '--without-heartbeat',  # Disable heartbeat to avoid broken pipe
        ]
        
        # Start worker in background
        with open(os.devnull, 'w') as devnull:
            worker_process = subprocess.Popen(
                worker_cmd,
                stdout=devnull,
                stderr=devnull,
                preexec_fn=os.setsid,
                env=dict(os.environ, PYTHONUNBUFFERED='1')
            )
        
        # Save worker PID
        save_worker_pid(worker_process.pid)
        
        # Start beat scheduler process
        beat_cmd = [
            'celery',
            '-A', 'automagik.core.celery_config',
            'beat',
            '--loglevel=INFO',
            '--logfile', os.path.join(log_dir, 'beat.log'),
            '--pidfile', os.path.join(log_dir, 'beat.pid'),
            '--schedule', os.path.join(log_dir, 'celerybeat-schedule'),
            '--max-interval', '60',
        ]
        
        # Start beat scheduler in background
        with open(os.devnull, 'w') as devnull:
            beat_process = subprocess.Popen(
                beat_cmd,
                stdout=devnull,
                stderr=devnull,
                preexec_fn=os.setsid,
                env=dict(os.environ, PYTHONUNBUFFERED='1')
            )
            
        # Wait a moment to ensure processes started
        time.sleep(2)
        
        # Save beat PID
        save_beat_pid(beat_process.pid)
        
        # Verify both processes are running
        worker_running = False
        beat_running = False
        try:
            os.kill(worker_process.pid, 0)
            worker_running = True
        except ProcessLookupError:
            pass
            
        try:
            os.kill(beat_process.pid, 0)
            beat_running = True
        except ProcessLookupError:
            pass
            
        if worker_running and beat_running:
            click.echo("Worker and beat scheduler started successfully")
        else:
            if not worker_running:
                click.echo("Worker failed to start")
            if not beat_running:
                click.echo("Beat scheduler failed to start")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Failed to start worker: {e}")
        sys.exit(1)

@worker_group.command()
def stop():
    """Stop the worker."""
    try:
        # Stop worker
        worker_pid = get_worker_pid()
        if worker_pid:
            try:
                # Try to stop worker gracefully first
                os.kill(worker_pid, signal.SIGTERM)
                # Wait for process to stop
                for _ in range(10):
                    try:
                        os.kill(worker_pid, 0)  # Check if process exists
                        time.sleep(0.1)
                    except ProcessLookupError:
                        break
                else:
                    # Force kill if still running
                    try:
                        os.kill(worker_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                
                click.echo("Worker stopped successfully")
            except ProcessLookupError:
                click.echo("Worker process not found")
            finally:
                remove_worker_pid()
        else:
            click.echo("No worker is running")
        
        # Stop beat scheduler
        beat_pid = get_beat_pid()
        if beat_pid:
            try:
                # Try to stop beat scheduler gracefully first
                os.kill(beat_pid, signal.SIGTERM)
                # Wait for process to stop
                for _ in range(10):
                    try:
                        os.kill(beat_pid, 0)  # Check if process exists
                        time.sleep(0.1)
                    except ProcessLookupError:
                        break
                else:
                    # Force kill if still running
                    try:
                        os.kill(beat_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                
                click.echo("Beat scheduler stopped successfully")
            except ProcessLookupError:
                click.echo("Beat scheduler process not found")
            finally:
                remove_beat_pid()
        else:
            click.echo("No beat scheduler is running")
            
    except Exception as e:
        click.echo(f"Failed to stop worker: {e}")
        sys.exit(1)

@worker_group.command()
def status():
    """Get worker status."""
    worker_pid = get_worker_pid()
    beat_pid = get_beat_pid()
    if worker_pid:
        click.echo(f"Worker is running (PID: {worker_pid})")
        
        # Get Celery stats
        try:
            inspector = celery_app.control.inspect()
            active = inspector.active()
            scheduled = inspector.scheduled()
            reserved = inspector.reserved()
            
            if active:
                click.echo("\nActive tasks:")
                for worker_name, tasks in active.items():
                    click.echo(f"{worker_name}: {len(tasks)} tasks")
                    for task in tasks:
                        click.echo(f"  - {task['name']} (id: {task['id']})")
            
            if scheduled:
                click.echo("\nScheduled tasks:")
                for worker_name, tasks in scheduled.items():
                    click.echo(f"{worker_name}: {len(tasks)} tasks")
            
            if reserved:
                click.echo("\nReserved tasks:")
                for worker_name, tasks in reserved.items():
                    click.echo(f"{worker_name}: {len(tasks)} tasks")
                    
        except Exception as e:
            click.echo(f"Could not fetch Celery stats: {e}")
    else:
        click.echo("Worker is not running")

    if beat_pid:
        click.echo(f"Beat scheduler is running (PID: {beat_pid})")
    else:
        click.echo("Beat scheduler is not running")

if __name__ == "__main__":
    worker_group()


