"""
Worker Command Module

Provides CLI commands for running the worker that executes scheduled flows.
"""

import asyncio
import click
import logging
from datetime import datetime, timezone, timedelta
import signal
import sys
import uuid
import re
from sqlalchemy import select

from ...core.flows import FlowManager
from ...core.scheduler import SchedulerManager
from ...core.database.session import get_session
from ...core.database.models import Task, TaskLog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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
    logger.info("Automagik worker started")
    while True:
        try:
            async with get_session() as session:
                await process_schedules(session)
            
        except Exception as e:
            logger.error(f"Worker error: {str(e)}")
            
        await asyncio.sleep(10)

def handle_signal(signum, frame):
    """Handle termination signals."""
    logger.info("Received termination signal. Shutting down...")
    sys.exit(0)

@click.command()
def worker():
    """Start the worker process."""
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    asyncio.run(worker_loop())
