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
from sqlalchemy import and_

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
    
    def __init__(self, db_session: Session):
        """
        Initialize the scheduler service.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    def _get_current_time(self) -> datetime:
        """Get current time in configured timezone."""
        return datetime.now(self.timezone)

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time: Optional[datetime] = None) -> datetime:
        """
        Calculate the next run time based on schedule type and expression.
        
        Args:
            schedule_type: Type of schedule ('interval' or 'cron')
            schedule_expr: Schedule expression (e.g., '30m' for interval, '* * * * *' for cron)
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
            if schedule_type == 'interval':
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

    def create_schedule(
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
            schedule_type: Type of schedule ('interval' or 'cron')
            schedule_expr: Schedule expression
            flow_params: Optional parameters to pass to the flow
            
        Returns:
            Schedule: Created schedule object
            
        Raises:
            FlowNotFoundError: If flow doesn't exist
            ComponentNotConfiguredError: If flow components aren't configured
            InvalidScheduleError: If schedule configuration is invalid
        """
        # Validate flow
        flow = self.db_session.query(FlowDB).filter(FlowDB.name == flow_name).first()
        if not flow:
            raise FlowNotFoundError(f"Flow '{flow_name}' not found")

        if not flow.input_component:
            raise ComponentNotConfiguredError(
                f"Flow '{flow_name}' does not have an input component configured"
            )

        # Calculate next run time
        try:
            next_run = self._calculate_next_run(schedule_type, schedule_expr)
        except InvalidScheduleError as e:
            raise InvalidScheduleError(f"Invalid schedule for flow '{flow_name}': {str(e)}")

        # Create schedule
        schedule = Schedule(
            flow_id=flow.id,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params or {},
            next_run_at=next_run,
            status='active'
        )
        
        try:
            self.db_session.add(schedule)
            self.db_session.commit()
            logger.info(f"Created schedule for flow '{flow_name}', next run at {next_run}")
            return schedule
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error creating schedule: {str(e)}")

    def get_schedule(self, schedule_id: uuid.UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self.db_session.query(Schedule).filter(Schedule.id == schedule_id).first()

    def list_schedules(
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
        
        return query.all()

    def update_schedule(
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
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return None

        if status:
            schedule.status = status
        if flow_params is not None:
            schedule.flow_params = flow_params

        try:
            self.db_session.commit()
            return schedule
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error updating schedule: {str(e)}")

    def delete_schedule(self, schedule_id: uuid.UUID) -> bool:
        """
        Delete a schedule.
        
        Args:
            schedule_id: ID of schedule to delete
            
        Returns:
            True if deleted, False if not found
        """
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return False

        try:
            self.db_session.delete(schedule)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error deleting schedule: {str(e)}")

    def get_due_schedules(self) -> List[Schedule]:
        """
        Get all active schedules that are due to run.
        
        Returns:
            List of schedules that should be executed
        """
        now = self._get_current_time()
        
        try:
            due_schedules = self.db_session.query(Schedule).filter(
                and_(
                    Schedule.status == 'active',
                    Schedule.next_run_at <= now
                )
            ).all()
            
            if due_schedules:
                logger.debug(f"Found {len(due_schedules)} due schedules")
                for schedule in due_schedules:
                    logger.debug(f"Schedule {schedule.id} due at {schedule.next_run_at}")
            
            return due_schedules
        except Exception as e:
            raise SchedulerError(f"Error fetching due schedules: {str(e)}")

    def update_schedule_next_run(self, schedule: Schedule) -> None:
        """
        Update the next run time for a schedule.
        
        Args:
            schedule: Schedule to update
        """
        try:
            next_run = self._calculate_next_run(
                schedule.schedule_type,
                schedule.schedule_expr,
                self._get_current_time()
            )
            
            schedule.next_run_at = next_run
            self.db_session.commit()
            
            logger.debug(f"Updated schedule {schedule.id} next run to {next_run}")
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error updating schedule next run: {str(e)}")

    def create_task_from_schedule(self, schedule: Schedule) -> Task:
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
                flow_id=schedule.flow_id,
                input_data=schedule.flow_params,
                status="pending"
            )
            
            self.db_session.add(task)
            self.db_session.commit()
            
            logger.info(f"Created task {task.id} from schedule {schedule.id}")
            return task
            
        except Exception as e:
            self.db_session.rollback()
            raise SchedulerError(f"Error creating task from schedule: {str(e)}")
