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

from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database.models import Worker, Schedule, Task, Workflow
from ...core.database.session import get_session
from ...core.workflows.manager import WorkflowManager
from ...core.workflows.task import TaskManager
from ...core.scheduler.scheduler import WorkflowScheduler as SchedulerManager
from tabulate import tabulate

# Initialize logger with basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

async def run_workflow(workflow_manager: WorkflowManager, task: Task) -> bool:
    """Run a workflow."""
    try:
        # Get workflow
        workflow = await workflow_manager.get_workflow(str(task.workflow_id))
        if not workflow:
            logger.error(f"Workflow {task.workflow_id} not found")
            return False
        
        # Log workflow execution
        logger.info(f"Running workflow {workflow.name} (remote_flow_id: {workflow.remote_flow_id}) for task {task.id}")
        logger.info(f"Input data: {json.dumps(task.input_data, indent=2)}")
        
        # Execute workflow
        result = await workflow_manager.run_workflow(workflow.id, task.input_data)
        
        if result:
            logger.info(f"Task {task.id} completed successfully")
            logger.info(f"Output data: {json.dumps(result.output_data, indent=2)}")
            return True
        else:
            logger.error(f"Task {task.id} failed")
            if task.error:
                logger.error(f"Error: {task.error}")
            return False
        
    except Exception as e:
        logger.error(f"Failed to run workflow: {str(e)}")
        task.status = 'failed'
        task.error = str(e)
        task.finished_at = datetime.now(timezone.utc)
        await workflow_manager.session.commit()
        return False

async def process_schedule(session, schedule, workflow_manager, now=None):
    """Process a single schedule."""
    if now is None:
        now = datetime.now(timezone.utc)
        
    try:
        # Log schedule parameters
        logger.debug(f"Processing schedule {schedule.id} for workflow {schedule.workflow_id}")
        logger.debug(f"Schedule parameters: {schedule.workflow_params}")
        
        # Create task
        task = Task(
            id=uuid4(),
            workflow_id=schedule.workflow_id,
            status='pending',
            input_data=schedule.workflow_params or {},
            created_at=now,
            tries=0,
            max_retries=3  # Configure max retries
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        
        logger.info(f"Created task {task.id} for schedule {schedule.id}")
        logger.debug(f"Task input data: {task.input_data}")
        
        # Run task
        success = await run_workflow(workflow_manager, task)
        
        if success:
            logger.info(f"Successfully executed workflow '{schedule.workflow.name}'")
            task.status = 'completed'
            task.finished_at = datetime.now(timezone.utc)
        else:
            logger.error(f"Failed to execute workflow '{schedule.workflow.name}'")
            # Only retry if we haven't exceeded max retries
            if task.tries < task.max_retries:
                task.status = 'pending'
                task.tries += 1
                task.next_retry_at = now + timedelta(minutes=5 * task.tries)  # Exponential backoff
                logger.info(f"Will retry task {task.id} in {5 * task.tries} minutes (attempt {task.tries + 1}/{task.max_retries})")
            else:
                task.status = 'failed'
                task.finished_at = datetime.now(timezone.utc)
                logger.error(f"Task {task.id} failed after {task.tries} attempts")
        
        await session.commit()
        
        # Update next run time for interval schedules
        if schedule.schedule_type == 'interval':
            try:
                delta = parse_interval(schedule.schedule_expr)
                if delta.total_seconds() <= 0:
                    raise ValueError("Interval must be positive")
                schedule.next_run_at = now + delta
                await session.commit()
                logger.info(f"Next run scheduled for {schedule.next_run_at.strftime('%H:%M:%S UTC')}")
            except ValueError as e:
                logger.error(f"Invalid interval: {e}")
                return False
        return True
    except Exception as e:
        logger.error(f"Failed to process schedule {schedule.id}: {str(e)}")
        # Create error log
        try:
            task_log = TaskLog(
                id=uuid4(),
                task_id=task.id,
                level='error',
                message=f"Schedule processing error: {str(e)}",
                created_at=now
            )
            session.add(task_log)
            await session.commit()
        except Exception as log_error:
            logger.error(f"Failed to create error log: {str(log_error)}")
        return False

def parse_interval(interval_str: str) -> timedelta:
    """Parse an interval string into a timedelta.
    
    Args:
        interval_str: String in format like "30m", "1h", "7d"
        
    Returns:
        timedelta object
        
    Raises:
        ValueError: If interval format is invalid
    """
    if not interval_str:
        raise ValueError("Interval string cannot be empty")
        
    units = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks'
    }
    
    # Extract number and unit
    match = re.match(r'^(\d+)([smhdw])$', interval_str)
    if not match:
        raise ValueError(f"Invalid interval format: {interval_str}")
        
    value, unit = match.groups()
    value = int(value)
    
    if value < 1:
        raise ValueError(f"Interval value must be positive: {value}")
        
    # Convert to timedelta
    return timedelta(**{units[unit]: value})

async def process_schedules(session):
    """Process due schedules."""
    now = datetime.now(timezone.utc)

    workflow_manager = WorkflowManager(session)
    task_manager = TaskManager(session)

    # Get active schedules that are due
    stmt = select(Schedule).join(Workflow).where(
        Schedule.status == "active",
        Schedule.next_run_at <= now
    )
    result = await session.execute(stmt)
    schedules = result.scalars().all()

    for schedule in schedules:
        # Check if there are any running tasks for this workflow
        stmt = select(func.count()).select_from(Task).where(
            Task.workflow_id == schedule.workflow_id,
            Task.status.in_(["running", "pending"])
        )
        result = await session.execute(stmt)
        running_tasks = result.scalar()

        if running_tasks == 0:
            # Create task using TaskManager
            task_data = {
                "workflow_id": schedule.workflow_id,
                "status": "pending",
                "input_data": schedule.workflow_params or {},
                "tries": 0,
                "max_retries": 3  # Configure max retries
            }
            task = await task_manager.create_task(task_data)
            logger.info(f"Created task {task.id} for schedule {schedule.id}")

            # Update next run time
            if schedule.schedule_type == "interval":
                interval = parse_interval(schedule.schedule_expr)
                schedule.next_run_at = now + interval
                await session.commit()

async def worker_loop():
    """Worker loop."""
    # Skip worker registration in test environment
    if os.getenv("AUTOMAGIK_ENV") == "testing":
        logger.info("Skipping worker registration in test environment")
        return
        
    logger.info("Automagik worker started")
    
    # Register worker in database
    worker_id = str(uuid4())
    hostname = socket.gethostname()
    pid = os.getpid()
    
    async with get_session() as session:
        worker = Worker(
            id=worker_id,
            hostname=hostname,
            pid=pid,
            status='active',
            stats={},
            last_heartbeat=datetime.now(timezone.utc)
        )
        session.add(worker)
        await session.commit()
        logger.info(f"Registered worker {worker_id} ({hostname}:{pid})")
    
    try:
        while True:
            try:
                async with get_session() as session:
                    # Update worker heartbeat
                    stmt = select(Worker).filter(Worker.id == worker_id)
                    result = await session.execute(stmt)
                    worker = result.scalar_one_or_none()
                    if worker:
                        now = datetime.now(timezone.utc)
                        worker.last_heartbeat = now
                        
                        # Get upcoming tasks in next 10 minutes
                        ten_mins_later = now + timedelta(minutes=10)
                        stmt = select(Schedule).where(
                            Schedule.status == "active",
                            Schedule.next_run_at <= ten_mins_later,
                            Schedule.next_run_at > now
                        )
                        result = await session.execute(stmt)
                        upcoming = list(result.scalars().all())
                        
                        if upcoming:
                            logger.info(f"Found {len(upcoming)} tasks to run in next 10 minutes")
                            for schedule in upcoming:
                                time_until = schedule.next_run_at - now
                                hours = int(time_until.total_seconds() // 3600)
                                minutes = int((time_until.total_seconds() % 3600) // 60)
                                seconds = int(time_until.total_seconds() % 60)
                                logger.info(f"Next task for workflow {schedule.workflow_id} will run in {hours:02d}h{minutes:02d}m{seconds:02d}s")
                        
                        await session.commit()
                    
                    # Process schedules
                    await process_schedules(session)
                    
                    # Execute pending tasks
                    workflow_manager = WorkflowManager(session)
                    stmt = select(Task).where(Task.status == "pending")
                    result = await session.execute(stmt)
                    pending_tasks = result.scalars().all()
                    
                    for task in pending_tasks:
                        try:
                            await run_workflow(workflow_manager, task)
                            logger.info(f"Executed task {task.id}")
                        except Exception as e:
                            logger.error(f"Failed to execute task {task.id}: {e}")
                
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                
            await asyncio.sleep(10)
    finally:
        # Remove worker from database on shutdown
        async with get_session() as session:
            stmt = select(Worker).filter(Worker.id == worker_id)
            result = await session.execute(stmt)
            worker = result.scalar_one_or_none()
            if worker:
                await session.delete(worker)
                await session.commit()
                logger.info(f"Unregistered worker {worker_id}")

def get_pid_file():
    """Get the path to the worker PID file."""
    pid_dir = os.path.expanduser("~/.automagik")
    return os.path.join(pid_dir, "worker.pid")

def write_pid():
    """Write the current process ID to the PID file."""
    pid_file = get_pid_file()
    logger.info(f"Writing PID {os.getpid()} to {pid_file}")
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

def read_pid():
    """Read the worker process ID from the PID file."""
    pid_file = os.path.expanduser("~/.automagik/worker.pid")
    logger.debug(f"Reading PID from {pid_file}")
    try:
        with open(pid_file, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None

def is_worker_running():
    """Check if the worker process is running."""
    pid = read_pid()
    if pid is None:
        return False
    
    try:
        # Check if process exists and is our worker
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        # Process doesn't exist
        logger.debug(f"Process {pid} not found, cleaning up PID file")
        try:
            os.unlink(get_pid_file())
        except FileNotFoundError:
            pass
        return False
    except PermissionError:
        # Process exists but we don't have permission to send signal
        return True

def stop_worker():
    """Stop the worker process."""
    pid_file = os.path.expanduser("~/.automagik/worker.pid")
    if not os.path.exists(pid_file):
        logger.info("No worker process found")
        return
        
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
            
        # Try to terminate process
        process = psutil.Process(pid)
        if process.is_running() and process.name() == "python":
            process.terminate()
            try:
                process.wait(timeout=10)  # Wait up to 10 seconds
            except psutil.TimeoutExpired:
                process.kill()  # Force kill if it doesn't terminate
            logger.info("Worker process stopped")
        else:
            logger.info("Worker process not running")
            
        os.remove(pid_file)
            
    except (ProcessLookupError, psutil.NoSuchProcess):
        logger.info("Worker process not found")
        os.remove(pid_file)
    except Exception as e:
        logger.error(f"Error stopping worker: {e}")

def handle_signal(signum, frame):
    """Handle termination signals."""
    logger.info("Received termination signal. Shutting down...")
    sys.exit(0)

def daemonize():
    """Daemonize the current process."""
    try:
        # First fork (detaches from parent)
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Parent process exits
    except OSError as err:
        logger.error(f'First fork failed: {err}')
        sys.exit(1)
    
    # Decouple from parent environment
    os.chdir('/')  # Change working directory
    os.umask(0)
    os.setsid()
    
    # Second fork (relinquish session leadership)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Parent process exits
    except OSError as err:
        logger.error(f'Second fork failed: {err}')
        sys.exit(1)
    
    # Close all open file descriptors
    for fd in range(0, 1024):
        try:
            os.close(fd)
        except OSError:
            pass
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    with open(os.devnull, 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(os.devnull, 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(os.devnull, 'a+') as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

worker_group = click.Group(name="worker", help="Worker management commands")

@worker_group.command("start")
@click.option("--threads", default=1, help="Number of worker threads")
def start_worker(threads: int):
    """Start worker process."""
    # Configure logging first
    log_path = configure_logging()
    logger.info(f"Worker logs will be written to {log_path}")

    # Check if worker is already running
    if is_worker_running():
        logger.info("Worker is already running")
        return
        
    # Write PID file
    pid_dir = os.path.dirname(get_pid_file())
    os.makedirs(pid_dir, exist_ok=True)
    write_pid()

    logger.info("Starting worker process")

    # Set up signal handlers
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    # Run the worker loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're in a test environment with a running loop
            loop.create_task(worker_loop())
        else:
            # If we're running normally
            loop.run_until_complete(worker_loop())
    except Exception as e:
        logger.exception("Worker failed")
        sys.exit(1)


@worker_group.command("stop")
@click.argument("worker_id", required=False)
def stop_worker_command(worker_id: Optional[str]):
    """Stop worker process."""
    if not is_worker_running():
        click.echo("No worker process is running")
        return
        
    click.echo("Stopping worker process...")
    stop_worker()
    click.echo("Worker process stopped")


@worker_group.command("status")
def worker_status():
    """Get worker status."""
    async def _status():
        async with get_session() as session:
            # Get all workers
            result = await session.execute(
                select(Worker).order_by(Worker.created_at.desc())
            )
            workers = result.scalars().all()

            if not workers:
                click.echo("No workers found")
                return

            # Format for display
            now = datetime.now(timezone.utc)
            rows = []
            for w in workers:
                # Check if process is running
                try:
                    proc = psutil.Process(w.pid)
                    running = proc.is_running()
                except psutil.NoSuchProcess:
                    running = False

                # Format last heartbeat
                if w.last_heartbeat:
                    last_hb = (now - w.last_heartbeat).total_seconds()
                    last_hb = f"{int(last_hb)}s ago"
                else:
                    last_hb = "Never"

                rows.append([
                    str(w.id)[:8],
                    w.hostname,
                    w.pid,
                    "Running" if running else "Dead",
                    w.status,
                    str(w.current_task_id)[:8] if w.current_task_id else "",
                    last_hb
                ])

            if rows:
                headers = ["ID", "Hostname", "PID", "State", "Status", "Task", "Last HB"]
                click.echo(tabulate(rows, headers=headers))

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're in a test environment with a running loop
            loop.create_task(_status())
        else:
            # If we're running normally
            loop.run_until_complete(_status())
    except RuntimeError:
        # If we can't get the current loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_status())
        finally:
            loop.close()
            asyncio.set_event_loop(None)

if __name__ == "__main__":
    worker_group()
