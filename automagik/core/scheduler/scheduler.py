"""
Scheduler Service Module

This module provides the core scheduling functionality for flow execution.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid
import pytz
import os
import logging
from croniter import croniter
from sqlalchemy.orm import Session
from sqlalchemy import and_, text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Schedule, FlowDB, Task
from .exceptions import (
    SchedulerError,
    InvalidScheduleError,
    FlowNotFoundError,
    ComponentNotConfiguredError
)

logger = logging.getLogger(__name__)

class SchedulerService:
    """
    Service for managing flow execution schedules.
    
    This service handles:
    - Creating and managing schedules
    - Calculating next run times
    - Finding due schedules
    - Creating tasks from schedules
    """
    
    def __init__(self, db_session: AsyncSession):
        """
        Initialize the scheduler service.
        
        Args:
            db_session: SQLAlchemy asynchronous database session
        """
        self.db_session = db_session
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    async def _get_current_time(self) -> datetime:
        """Get current time in configured timezone."""
        return datetime.now(self.timezone)

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time: Optional[datetime] = None) -> datetime:
        """
        Calculate the next run time based on schedule type and expression.
        
        Args:
            schedule_type: Type of schedule ('interval', 'cron', or 'oneshot')
            schedule_expr: Schedule expression (e.g., '30m' for interval, '* * * * *' for cron, 
                         or ISO format datetime for oneshot)
            from_time: Optional base time for calculation
            
        Returns:
            datetime: Next scheduled run time
            
        Raises:
            InvalidScheduleError: If schedule type or expression is invalid
        """
        if from_time is None:
            from_time = self._get_current_time()
        elif from_time.tzinfo is None:
            from_time = self.timezone.localize(from_time)

        try:
            if schedule_type == 'oneshot':
                try:
                    # Parse ISO format datetime
                    run_time = datetime.fromisoformat(schedule_expr)
                    # Localize if naive
                    if run_time.tzinfo is None:
                        run_time = self.timezone.localize(run_time)
                    # Ensure the time is in the future
                    if run_time <= from_time:
                        raise InvalidScheduleError("One-time schedule must be in the future")
                    return run_time
                except ValueError as e:
                    raise InvalidScheduleError(f"Invalid datetime format for one-time schedule. Use ISO format (e.g. 2025-01-24T00:00:00): {str(e)}")
            elif schedule_type == 'interval':
                # Parse interval expression (e.g., '30m', '1h', '1d')
                value = int(schedule_expr[:-1])
                unit = schedule_expr[-1].lower()
                
                if unit == 'm':
                    delta = timedelta(minutes=value)
                elif unit == 'h':
                    delta = timedelta(hours=value)
                elif unit == 'd':
                    delta = timedelta(days=value)
                else:
                    raise InvalidScheduleError(f"Invalid interval unit: {unit}")
                
                return from_time + delta
                
            elif schedule_type == 'cron':
                try:
                    cron = croniter(schedule_expr, from_time)
                    next_time = cron.get_next(datetime)
                    return self.timezone.localize(next_time)
                except ValueError as e:
                    raise InvalidScheduleError(f"Invalid cron expression: {str(e)}")
            else:
                raise InvalidScheduleError(f"Unsupported schedule type: {schedule_type}")
                
        except Exception as e:
            raise InvalidScheduleError(f"Error calculating next run: {str(e)}")

    async def create_schedule(
        self,
        flow_name: str,
        schedule_type: str,
        schedule_expr: str,
        flow_params: Dict[str, Any] = None
    ) -> Schedule:
        """
        Create a new schedule for a flow.
        
        Args:
            flow_name: Name of the flow to schedule
            schedule_type: Type of schedule ('interval', 'cron', or 'oneshot')
            schedule_expr: Schedule expression
            flow_params: Optional parameters to pass to the flow
            
        Returns:
            Schedule: Created schedule object
            
        Raises:
            FlowNotFoundError: If flow doesn't exist
            ComponentNotConfiguredError: If flow components aren't configured
            InvalidScheduleError: If schedule configuration is invalid
        """
        # Get flow
        stmt = text("SELECT * FROM flows WHERE name = :name")
        result = await self.db_session.execute(stmt, {"name": flow_name})
        flow = result.first()

        if not flow:
            raise FlowNotFoundError(f"Flow not found: {flow_name}")

        # Calculate next run time
        next_run = self._calculate_next_run(schedule_type, schedule_expr)

        # Create schedule
        schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=flow.id,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params,
            next_run_at=next_run,
            status='active'
        )

        self.db_session.add(schedule)
        await self.db_session.commit()
        await self.db_session.refresh(schedule)

        return schedule

    async def get_schedule(self, schedule_id: uuid.UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return await self.db_session.get(Schedule, schedule_id)

    async def list_schedules(
        self,
        flow_name: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Schedule]:
        """
        List schedules with optional filtering.
        
        Args:
            flow_name: Optional flow name to filter by
            status: Optional status to filter by
            
        Returns:
            List of matching schedules
        """
        query = self.db_session.query(Schedule)
        
        if flow_name:
            query = query.join(Schedule.flow).filter(FlowDB.name == flow_name)
        
        if status:
            query = query.filter(Schedule.status == status)
        
        return await query.all()

    async def update_schedule(
        self,
        schedule_id: uuid.UUID,
        status: Optional[str] = None,
        flow_params: Optional[Dict[str, Any]] = None
    ) -> Optional[Schedule]:
        """
        Update a schedule's status or parameters.
        
        Args:
            schedule_id: ID of schedule to update
            status: Optional new status
            flow_params: Optional new flow parameters
            
        Returns:
            Updated schedule or None if not found
        """
        schedule = await self.get_schedule(schedule_id)
        if not schedule:
            return None

        if status:
            schedule.status = status
        if flow_params is not None:
            schedule.flow_params = flow_params

        try:
            await self.db_session.commit()
            return schedule
        except Exception as e:
            await self.db_session.rollback()
            raise SchedulerError(f"Error updating schedule: {str(e)}")

    async def delete_schedule(self, schedule_id: uuid.UUID) -> bool:
        """
        Delete a schedule.
        
        Args:
            schedule_id: ID of schedule to delete
            
        Returns:
            True if deleted, False if not found
        """
        schedule = await self.get_schedule(schedule_id)
        if not schedule:
            return False

        try:
            await self.db_session.delete(schedule)
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise SchedulerError(f"Error deleting schedule: {str(e)}")

    async def get_due_schedules(self) -> List[Schedule]:
        """
        Get all active schedules that are due to run.
        
        Returns:
            List of schedules that should be executed
        """
        current_time = await self._get_current_time()
        
        # Get all active schedules that are due
        stmt = text("""
            SELECT * FROM schedules 
            WHERE status = 'active' 
            AND next_run_at <= :current_time
        """)
        result = await self.db_session.execute(stmt, {"current_time": current_time})
        schedules = result.fetchall()
        
        return schedules

    async def update_schedule_next_run(self, schedule: Schedule):
        """
        Update the next run time for a schedule.
        
        Args:
            schedule: Schedule to update
        """
        next_run = self._calculate_next_run(
            schedule.schedule_type,
            schedule.schedule_expr,
            from_time=await self._get_current_time()
        )
        
        schedule.next_run_at = next_run
        await self.db_session.commit()

    async def create_task_from_schedule(self, schedule: Schedule) -> Task:
        """
        Create a task from a schedule.
        
        Args:
            schedule: Schedule to create task from
            
        Returns:
            Created task
            
        Raises:
            SchedulerError: If task creation fails
        """
        try:
            task = Task(
                id=uuid.uuid4(),
                flow_id=schedule.flow_id,
                status='pending',
                input_data=schedule.flow_params,
                created_at=await self._get_current_time()
            )
            
            self.db_session.add(task)
            await self.db_session.commit()
            await self.db_session.refresh(task)
            
            return task
            
        except Exception as e:
            raise SchedulerError(f"Failed to create task from schedule: {str(e)}")
