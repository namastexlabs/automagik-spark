"""
Flow Scheduler Module

Handles scheduling and execution of flows based on cron expressions or intervals.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import uuid
from croniter import croniter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Schedule, Task, Flow
from ..flows.manager import FlowManager

logger = logging.getLogger(__name__)

class FlowScheduler:
    """Manages flow scheduling and execution."""
    
    def __init__(self, session: AsyncSession, flow_manager: FlowManager):
        """
        Initialize scheduler.
        
        Args:
            session: Database session
            flow_manager: Flow manager instance
        """
        self.session = session
        self.flow_manager = flow_manager
        self._running = False
        self._tasks: Dict[uuid.UUID, asyncio.Task] = {}
    
    async def start(self):
        """Start the scheduler."""
        if self._running:
            return
            
        self._running = True
        logger.info("Starting flow scheduler")
        
        # Start monitoring loop
        asyncio.create_task(self._monitor_loop())
    
    async def stop(self):
        """Stop the scheduler."""
        if not self._running:
            return
            
        self._running = False
        logger.info("Stopping flow scheduler")
        
        # Cancel all running tasks
        for task in self._tasks.values():
            task.cancel()
        
        # Wait for tasks to finish
        if self._tasks:
            await asyncio.gather(*self._tasks.values(), return_exceptions=True)
        
        self._tasks.clear()
    
    async def _monitor_loop(self):
        """Main monitoring loop."""
        while self._running:
            try:
                # Get active schedules
                query = select(Schedule).filter(Schedule.status == 'active')
                result = await self.session.execute(query)
                schedules = result.scalars().all()
                
                for schedule in schedules:
                    # Skip if already running
                    if schedule.id in self._tasks:
                        continue
                    
                    # Check if it's time to run
                    if self._should_run(schedule):
                        task = asyncio.create_task(
                            self._run_schedule(schedule.id)
                        )
                        self._tasks[schedule.id] = task
                
                # Clean up finished tasks
                finished = [sid for sid, task in self._tasks.items() if task.done()]
                for sid in finished:
                    self._tasks.pop(sid)
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
            
            await asyncio.sleep(60)  # Check every minute
    
    def _should_run(self, schedule: Schedule) -> bool:
        """Check if a schedule should run now."""
        now = datetime.utcnow()
        
        # Skip if no next run time
        if not schedule.next_run_at:
            return self._calculate_next_run(schedule, now)
        
        # Check if it's time
        return now >= schedule.next_run_at
    
    def _calculate_next_run(self, schedule: Schedule, from_time: datetime) -> bool:
        """Calculate next run time for a schedule."""
        try:
            if schedule.schedule_type == 'cron':
                # Use croniter to calculate next run
                cron = croniter(schedule.schedule_expr, from_time)
                next_run = cron.get_next(datetime)
            else:
                # Interval in minutes
                interval = int(schedule.schedule_expr)
                next_run = from_time + timedelta(minutes=interval)
            
            schedule.next_run_at = next_run
            return False
            
        except Exception as e:
            logger.error(f"Error calculating next run for schedule {schedule.id}: {str(e)}")
            return False
    
    async def _run_schedule(self, schedule_id: uuid.UUID):
        """Execute a scheduled flow."""
        try:
            # Get schedule
            query = select(Schedule).filter(Schedule.id == schedule_id)
            result = await self.session.execute(query)
            schedule = result.scalar_one_or_none()
            
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return
            
            # Create task
            task = Task(
                id=uuid.uuid4(),
                flow_id=schedule.flow_id,
                schedule_id=schedule.id,
                status='pending',
                created_at=datetime.utcnow()
            )
            
            self.session.add(task)
            await self.session.commit()
            
            # Execute flow
            try:
                task.status = 'running'
                task.started_at = datetime.utcnow()
                await self.session.commit()
                
                result = await self.flow_manager.execute_flow(
                    flow_id=schedule.flow_id,
                    input_data=schedule.flow_params or {}
                )
                
                task.status = 'completed'
                task.output_data = result
                task.completed_at = datetime.utcnow()
                
            except Exception as e:
                task.status = 'failed'
                task.error = str(e)
                task.completed_at = datetime.utcnow()
                logger.error(f"Error executing flow for schedule {schedule_id}: {str(e)}")
            
            # Calculate next run time
            self._calculate_next_run(schedule, datetime.utcnow())
            
            await self.session.commit()
            
        except Exception as e:
            logger.error(f"Error running schedule {schedule_id}: {str(e)}")
            try:
                await self.session.rollback()
            except:
                pass
