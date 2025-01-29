"""
Worker Command Module

Provides CLI commands for running the worker that executes scheduled flows.
"""

import asyncio
import click
import logging
import os
import socket
from pathlib import Path
import psutil
from datetime import datetime, timezone, timedelta
import signal
import sys
import uuid
import re
from sqlalchemy import select

from ...core.flows import FlowManager
from ...core.scheduler import SchedulerManager
from ...core.database.session import get_session
from ...core.database.models import Task, TaskLog, Worker

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

async def run_flow(flow_manager: FlowManager, task: Task) -> bool:
    """Run a flow."""
    try:
        # Get flow
        flow = await flow_manager.get_flow(str(task.flow_id))
        if not flow:
            logger.error(f"Flow {task.flow_id} not found")
            return False
        
        # Update task status
        task.status = 'running'
        task.started_at = datetime.now(timezone.utc)
        await flow_manager.session.commit()
        
        # Run flow using source_id for API call
        logger.info(f"Running flow {flow.name} (source_id: {flow.source_id}) for task {task.id}")
        result = await flow_manager.run_flow(flow.source_id, task.input_data)
        
        # Task status is managed by run_flow
        return result is not None
        
    except Exception as e:
        logger.error(f"Failed to run flow: {str(e)}")
        task.status = 'failed'
        task.error = str(e)
        task.finished_at = datetime.now(timezone.utc)
        await flow_manager.session.commit()
        return False

def parse_interval(interval_str: str) -> timedelta:
    """Parse an interval string into a timedelta.
    
    Supported formats:
    - Xm: X minutes (e.g., "30m")
    - Xh: X hours (e.g., "1h")
    - Xd: X days (e.g., "7d")
    
    Args:
        interval_str: Interval string to parse
        
    Returns:
        timedelta object
        
    Raises:
        ValueError: If the interval format is invalid
    """
    if not interval_str:
        raise ValueError("Interval cannot be empty")
        
    match = re.match(r'^(\d+)([mhd])$', interval_str)
    if not match:
        raise ValueError(
            f"Invalid interval format: {interval_str}. "
            "Must be a number followed by 'm' (minutes), 'h' (hours), or 'd' (days). "
            "Examples: '30m', '1h', '7d'"
        )
    
    value, unit = match.groups()
    value = int(value)
    
    if value <= 0:
        raise ValueError("Interval must be positive")
    
    if unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    else:
        raise ValueError(f"Invalid interval unit: {unit}")

async def process_schedule(session, schedule, flow_manager, now=None):
    """Process a single schedule."""
    if now is None:
        now = datetime.now(timezone.utc)
        
    try:
        # Create task
        task = Task(
            id=uuid.uuid4(),
            flow_id=schedule.flow_id,
            status='pending',
            input_data=schedule.flow_params or {},
            created_at=now,
            tries=0,
            max_retries=3  # Configure max retries
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        
        logger.info(f"Created task {task.id} for schedule {schedule.id}")
        
        # Run task
        success = await run_flow(flow_manager, task)
        
        if success:
            logger.info(f"Successfully executed flow '{schedule.flow.name}'")
            task.status = 'completed'
            task.finished_at = datetime.now(timezone.utc)
        else:
            logger.error(f"Failed to execute flow '{schedule.flow.name}'")
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
                id=uuid.uuid4(),
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

async def process_schedules(session):
    """Process due schedules."""
    now = datetime.now(timezone.utc)
    
    flow_manager = FlowManager(session)
    scheduler_manager = SchedulerManager(session, flow_manager)
    
    # First, check for any failed tasks that need to be retried
    retry_query = select(Task).where(
        Task.status == 'pending',
        Task.next_retry_at <= now,
        Task.tries < Task.max_retries
    )
    retry_tasks = await session.execute(retry_query)
    for task in retry_tasks.scalars():
        logger.info(f"Retrying failed task {task.id} (attempt {task.tries + 1}/{task.max_retries})")
        await run_flow(flow_manager, task)
    
    # Now process schedules
    schedules = await scheduler_manager.list_schedules()
    active_schedules = [s for s in schedules if s.status == 'active']
    logger.info(f"Found {len(active_schedules)} active schedules")
    
    # Sort schedules by next run time
    active_schedules.sort(key=lambda s: s.next_run_at or datetime.max.replace(tzinfo=timezone.utc))
    
    # Show only the next 5 schedules
    for i, schedule in enumerate(active_schedules):
        if i >= 5:  # Skip logging after first 5
            break
            
        # Convert next_run_at to UTC if it's naive
        next_run = schedule.next_run_at
        if next_run and next_run.tzinfo is None:
            next_run = next_run.replace(tzinfo=timezone.utc)
            schedule.next_run_at = next_run
            
        if not next_run:
            logger.warning(f"Schedule {schedule.id} has no next run time")
            continue
            
        time_until = next_run - now
        total_seconds = int(time_until.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if next_run > now:
            logger.info(f"Schedule '{schedule.flow.name}' will run in {hours}h {minutes}m {seconds}s (at {next_run.strftime('%H:%M:%S UTC')})")
            continue
            
        logger.info(f"Executing schedule {schedule.id} for flow '{schedule.flow.name}'")
        await process_schedule(session, schedule, flow_manager, now)
            
    # Process all schedules regardless of display limit
    for schedule in active_schedules[5:]:
        if schedule.next_run_at and schedule.next_run_at <= now:
            await process_schedule(session, schedule, flow_manager, now)

async def worker_loop():
    """Worker loop."""
    # Skip worker registration in test environment
    if os.getenv("AUTOMAGIK_ENV") == "testing":
        logger.info("Skipping worker registration in test environment")
        return
        
    logger.info("Automagik worker started")
    
    # Register worker in database
    worker_id = str(uuid.uuid4())
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
                        worker.last_heartbeat = datetime.now(timezone.utc)
                        await session.commit()
                    
                    # Process schedules
                    await process_schedules(session)
                
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

@click.group(name='worker')
def worker_group():
    """Manage the worker process."""
    pass

@worker_group.command(name='start')
def start_worker():
    """Start the worker process."""
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
        asyncio.run(worker_loop())
    except Exception as e:
        logger.exception("Worker failed")
        sys.exit(1)

@worker_group.command(name='stop')
def stop_worker_command():
    """Stop the worker process."""
    if not is_worker_running():
        click.echo("No worker process is running")
        return
        
    click.echo("Stopping worker process...")
    stop_worker()
    click.echo("Worker process stopped")

@worker_group.command(name='status')
def worker_status():
    """Check if the worker process is running."""
    if is_worker_running():
        click.echo("Worker process is running")
    else:
        click.echo("Worker process is not running")

if __name__ == "__main__":
    worker_group()
