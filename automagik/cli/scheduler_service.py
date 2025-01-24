from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from croniter import croniter
from datetime import timedelta
import pytz
import os

from automagik.core.database.models import Schedule, FlowDB, Task, Log, Base
from automagik.core.logger import setup_logger

logger = setup_logger()

class SchedulerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    def _get_current_time(self) -> datetime:
        """Get current time in local timezone."""
        return datetime.now(self.timezone).astimezone()  # Ensure it's timezone-aware

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time=None) -> datetime:
        """Calculate the next run time based on schedule type and expression."""
        if from_time is None:
            from_time = self._get_current_time().astimezone()  # Ensure it's timezone-aware
        else:
            # Ensure from_time has timezone
            if from_time.tzinfo is None:
                from_time = self.timezone.localize(from_time)

        if schedule_type == 'interval':
            # Parse interval expression (e.g., '30m', '1h', '1d')
            value = int(schedule_expr[:-1])
            unit = schedule_expr[-1]
            
            logger.debug(f"Calculating next run for interval schedule: {value}{unit}")
            
            if unit == 'm':
                next_run = from_time + timedelta(minutes=value)
            elif unit == 'h':
                next_run = from_time + timedelta(hours=value)
            elif unit == 'd':
                next_run = from_time + timedelta(days=value)
            else:
                raise ValueError(f"Invalid interval unit: {unit}")
            
            logger.debug(f"Next run calculated: {next_run}")
            return next_run
        elif schedule_type == 'cron':
            # Use croniter to calculate next run time
            cron = croniter(schedule_expr, from_time)
            next_time = cron.get_next(datetime)
            if next_time.tzinfo is None:
                next_time = self.timezone.localize(next_time)
            return next_time
        elif schedule_type == 'oneshot':
            # Parse ISO format datetime
            try:
                next_time = datetime.fromisoformat(schedule_expr)
                if next_time.tzinfo is None:
                    next_time = self.timezone.localize(next_time)
                if next_time < from_time:
                    raise ValueError("Oneshot schedule time must be in the future")
                return next_time
            except ValueError as e:
                raise ValueError(f"Invalid oneshot datetime format: {e}")
        else:
            raise ValueError(f"Unsupported schedule type: {schedule_type}")

    def create_schedule(self, flow_id: uuid.UUID, schedule_type: str, schedule_expr: str, flow_params: dict = None) -> Schedule:
        """Create a new schedule for a flow."""
        # Get the flow
        flow = self.db_session.query(FlowDB).filter(FlowDB.id == flow_id).first()
        if not flow:
            raise ValueError(f"Flow with ID {flow_id} not found")

        # Create schedule
        next_run = self._calculate_next_run(schedule_type, schedule_expr)
        if next_run is None or next_run.tzinfo is None:
            raise ValueError("Next run time must be a valid timezone-aware datetime")
        schedule = Schedule(
            flow_id=flow.id,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
            flow_params=flow_params or {},
            next_run_at=next_run,
            status='active'
        )
        
        self.db_session.add(schedule)
        self.db_session.commit()
        return schedule

    def get_schedule(self, schedule_id: uuid.UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self.db_session.query(Schedule).filter(Schedule.id == schedule_id).first()

    def list_schedules(self, flow_name: Optional[str] = None) -> List[Schedule]:
        """List all schedules, optionally filtered by flow name."""
        query = self.db_session.query(Schedule)
        
        if flow_name:
            query = query.join(Schedule.flow).filter(FlowDB.name == flow_name)
        
        return query.all()

    def delete_schedule(self, schedule_id: uuid.UUID) -> bool:
        """Delete a schedule."""
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return False

        self.db_session.delete(schedule)
        self.db_session.commit()
        return True

    def get_due_schedules(self) -> List[Schedule]:
        """Get all active schedules that are due to run."""
        now = self._get_current_time()
        
        # Find active schedules that are due
        due_schedules = self.db_session.query(Schedule).filter(
            Schedule.status == 'active',
            Schedule.next_run_at <= now
        ).all()
        
        if due_schedules:
            logger.debug(f"Found {len(due_schedules)} due schedules")
            for schedule in due_schedules:
                logger.debug(f"Schedule {schedule.id} is due:")
                logger.debug(f"    Next run was: {schedule.next_run_at}")
        
        return due_schedules

    def update_schedule_next_run(self, schedule: Schedule):
        """Update the next run time for a schedule"""
        next_run = self._calculate_next_run(
            schedule.schedule_type,
            schedule.schedule_expr,
            from_time=self._get_current_time().astimezone()  # Ensure it's timezone-aware
        )
        schedule.next_run_at = next_run
        self.db_session.commit()

    def create_task(self, schedule: Schedule) -> Task:
        """Create a task from a schedule"""
        task = Task(
            flow_id=schedule.flow_id,
            status='pending',
            input_data=schedule.flow_params
        )
        self.db_session.add(task)
        self.db_session.commit()
        return task

    def log_task_start(self, task: Task):
        """Log task start"""
        task.status = 'running'
        task.started_at = self._get_current_time()
        self.db_session.commit()

    def log_task_completion(self, task: Task, output_data: dict):
        """Log task completion"""
        task.status = 'completed'
        task.completed_at = self._get_current_time()
        task.output_data = output_data
        self.db_session.commit()

    def log_task_error(self, task: Task, error: str):
        """Log task error"""
        task.status = 'failed'
        task.completed_at = self._get_current_time()
        task.error = error
        self.db_session.commit()
