import click
import os
import sys
import json
from typing import Dict, Any
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from automagik.core.services.task_runner import TaskRunner
from automagik.core.scheduler.scheduler import SchedulerService
from automagik.core.database.session import get_db_session
from automagik.core.services.langflow_client import LangflowClient
from automagik.core.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger()

@click.group()
def run():
    """Run tasks and schedules"""
    pass

@run.command()
@click.option('--daemon', is_flag=True, help='Run in daemon mode')
@click.option('--log-level', default='INFO', help='Set logging level (DEBUG, INFO, WARNING, ERROR)')
def start(daemon, log_level):
    """Start the task and schedule processor"""
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('automagik')
    
    # Log startup information
    logger.info("Starting AutoMagik service")
    logger.debug(f"Working directory: {os.getcwd()}")
    logger.debug(f"Python path: {os.getenv('PYTHONPATH')}")
    logger.debug(f"Environment variables: {dict(os.environ)}")
    
    db = get_db_session()
    langflow_client = LangflowClient()
    runner = TaskRunner(db, langflow_client)
    scheduler = SchedulerService(db)
    
    if daemon:
        logger.info("Starting schedule processor...")
        logger.info("Running in daemon mode")
    
    async def process_schedules():
        while True:
            try:
                # Get due schedules
                due_schedules = scheduler.get_due_schedules()
                if due_schedules:
                    logger.info(f"Found {len(due_schedules)} due schedules")
                    
                # Process each schedule
                for schedule in due_schedules:
                    logger.info(f"Processing schedule {schedule.id} for flow {schedule.flow.name}")
                    
                    # Create task from schedule
                    task = await runner.create_task(
                        flow_id=schedule.flow_id,
                        input_data=schedule.flow_params
                    )
                    logger.debug(f"Created task {task.id}")
                    
                    # Run the task
                    await runner.run_task(task.id)
                    
                    # Update next run time
                    next_run = scheduler._calculate_next_run(
                        schedule.schedule_type,
                        schedule.schedule_expr
                    )
                    schedule.next_run_at = next_run
                    db.commit()
                    logger.info(f"Next run scheduled for: {next_run}")
                    
            except Exception as e:
                logger.error(f"Error processing schedules: {str(e)}", exc_info=True)
                
            if not daemon:
                break
                
            # Wait 1 minute before checking again
            await asyncio.sleep(60)
    
    # Run the processor
    asyncio.run(process_schedules())

@run.command()
@click.argument('schedule_id')
def test(schedule_id):
    """Test run a schedule immediately"""
    try:
        db = get_db_session()
        langflow_client = LangflowClient()
        runner = TaskRunner(db, langflow_client)
        scheduler = SchedulerService(db)
        
        # Get the schedule
        schedule = scheduler.get_schedule(schedule_id)
        if not schedule:
            logger.error(f"Schedule {schedule_id} not found")
            return
            
        logger.info(f"\nTesting schedule {schedule.id} for flow {schedule.flow.name}")
        logger.info(f"Type: {schedule.schedule_type}")
        logger.info(f"Expression: {schedule.schedule_expr}")
        if schedule.flow_params:
            logger.info(f"Input: {schedule.flow_params.get('input')}")
            
        async def run_test():
            # Create task from schedule
            task = await runner.create_task(
                flow_id=schedule.flow_id,
                input_data=schedule.flow_params
            )
            logger.info(f"\nCreated task {task.id}")
            
            # Run the task
            await runner.run_task(task.id)
            logger.info("\nTask completed")
            
        asyncio.run(run_test())
        
    except Exception as e:
        logger.error(f"Error testing schedule: {str(e)}", exc_info=True)