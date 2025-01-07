from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from croniter import croniter
from datetime import timedelta
import pytz
import os
from .models import Schedule, FlowDB, Task, Log, Base
from .logger import setup_logger

logger = setup_logger()

class SchedulerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.timezone = pytz.timezone(os.getenv('TIMEZONE', 'UTC'))

    def _get_current_time(self) -> datetime:
        """Get current time in local timezone."""
        return datetime.now(self.timezone)

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time=None) -> datetime:
        """Calculate the next run time based on schedule type and expression."""
        if from_time is None:
            from_time = self._get_current_time()
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
            return self.timezone.localize(next_time)
        else:
            raise ValueError(f"Unsupported schedule type: {schedule_type}")

    def create_schedule(self, flow_name: str, schedule_type: str, schedule_expr: str, flow_params: dict = None) -> Schedule:
        """Create a new schedule for a flow."""
        # Get the flow
        flow = self.db_session.query(FlowDB).filter(FlowDB.name == flow_name).first()
        if not flow:
            raise ValueError(f"Flow with name {flow_name} not found")

        # Verify flow has input component
        if not flow.input_component:
            raise ValueError(f"Flow {flow_name} does not have an input component configured")

        # Create schedule
        next_run = self._calculate_next_run(schedule_type, schedule_expr)
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

    def update_schedule_next_run(self, schedule):
        """Update the next run time for a schedule"""
        now = datetime.utcnow()
        
        if schedule.schedule_type == 'cron':
            # For cron schedules, calculate next run using croniter
            cron = croniter(schedule.schedule_expr, now)
            next_run = cron.get_next(datetime)
        else:
            # For interval schedules, add the interval to now
            # TODO: Implement interval scheduling
            next_run = now
        
        schedule.last_run = now
        schedule.next_run_at = next_run
        self.db_session.commit()

    def create_task_from_schedule(self, schedule):
        """Create a task from a schedule"""
        task = Task(
            flow_id=schedule.flow_id,
            name=f"Scheduled task for {schedule.flow.name}",
            description=f"Task created from schedule {schedule.id}",
            parameters=schedule.flow_params
        )
        self.db_session.add(task)
        self.db_session.commit()
        return task
