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

from ...core.flows import FlowManager
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
        
        # Update task status
        task.status = 'completed' if result else 'failed'
        task.finished_at = datetime.now(timezone.utc)
        task.output_data = result
        await flow_manager.session.commit()
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to run flow: {str(e)}")
        task.status = 'failed'
        task.error = str(e)
        task.finished_at = datetime.now(timezone.utc)
        await flow_manager.session.commit()
        return False

def parse_interval(interval_str: str) -> timedelta:
    """Parse interval string into timedelta.
    
    Supports formats:
    - Xm (minutes)
    - Xh (hours)
    - Xd (days)
    """
    match = re.match(r'^(\d+)([mhd])$', interval_str)
    if not match:
        raise ValueError(f"Invalid interval format: {interval_str}")
    
    value = int(match.group(1))
    unit = match.group(2)
    
    if unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    else:
        raise ValueError(f"Invalid interval unit: {unit}")

async def process_schedules(flow_manager: FlowManager):
    """Process due schedules."""
    now = datetime.now(timezone.utc)
    logger.info(f"Processing schedules at {now}")
    
    # Get fresh session for each iteration
    async with get_session() as session:
        flow_manager = FlowManager(session)
        schedules = await flow_manager.list_schedules()
        
        logger.info(f"Found {len(schedules)} schedules")
        
        for schedule in schedules:
            logger.info(f"Checking schedule {schedule.id} (status: {schedule.status}, next run: {schedule.next_run_at})")
            
            if schedule.status != 'active':
                logger.debug(f"Skipping inactive schedule {schedule.id} (status: {schedule.status})")
                continue
                
            # Convert next_run_at to UTC if it's naive
            next_run = schedule.next_run_at
            if next_run and next_run.tzinfo is None:
                next_run = next_run.replace(tzinfo=timezone.utc)
                logger.info(f"Converted naive datetime to UTC: {next_run}")
                
            if not next_run:
                logger.warning(f"Schedule {schedule.id} has no next run time")
                continue
                
            if next_run > now:
                logger.debug(f"Schedule {schedule.id} not due yet (next run: {next_run}, now: {now})")
                continue
                
            logger.info(f"Running schedule {schedule.id} for flow {schedule.flow.name}")
            
            # Create task
            task = Task(
                id=uuid.uuid4(),
                flow_id=schedule.flow_id,
                status='pending',
                input_data=schedule.flow_params,
                created_at=now
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            
            # Run task
            await run_flow(flow_manager, task)
            
            # Update next run time
            if schedule.schedule_type == 'interval':
                try:
                    delta = parse_interval(schedule.schedule_expr)
                    schedule.next_run_at = now + delta
                    await session.commit()
                except ValueError as e:
                    logger.error(f"Invalid interval: {e}")
                    continue

async def worker_loop():
    """Worker loop."""
    logger.info("Starting worker...")
    while True:
        try:
            # Get fresh session for each iteration
            async with get_session() as session:
                flow_manager = FlowManager(session)
                
                # Process schedules
                await process_schedules(flow_manager)
            
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
