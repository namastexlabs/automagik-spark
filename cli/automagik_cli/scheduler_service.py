from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from croniter import croniter
from datetime import timedelta

from .models import Schedule, FlowDB, Base

class SchedulerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str, from_time=None) -> datetime:
        """Calculate the next run time based on schedule type and expression."""
        if from_time is None:
            from_time = datetime.utcnow()

        if schedule_type == 'interval':
            # Parse interval expression (e.g., '30m', '1h', '1d')
            value = int(schedule_expr[:-1])
            unit = schedule_expr[-1]
            
            if unit == 'm':
                return from_time + timedelta(minutes=value)
            elif unit == 'h':
                return from_time + timedelta(hours=value)
            elif unit == 'd':
                return from_time + timedelta(days=value)
            else:
                raise ValueError(f"Invalid interval unit: {unit}")
                
        elif schedule_type == 'cron':
            # Use croniter to calculate next run time
            cron = croniter(schedule_expr, from_time)
            return cron.get_next(datetime)
        else:
            raise ValueError(f"Invalid schedule type: {schedule_type}")

    def create_schedule(self, flow_name: str, schedule_type: str, schedule_expr: str, flow_params: dict = None) -> Schedule:
        """Create a new schedule for a flow."""
        # Get the flow
        flow = self.db_session.query(FlowDB).filter(FlowDB.name == flow_name).first()
        if not flow:
            raise ValueError(f"Flow with name {flow_name} not found")

        # Verify flow has input/output components
        if not flow.input_component or not flow.output_component:
            raise ValueError(f"Flow {flow_name} does not have input/output components configured")

        # Create schedule
        next_run = self._calculate_next_run(schedule_type, schedule_expr)
        schedule = Schedule(
            flow_id=flow.id,
            schedule_type=schedule_type,
            schedule_expr=schedule_expr,
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
        now = datetime.utcnow()
        return (self.db_session.query(Schedule)
                .filter(Schedule.status == 'active')
                .filter(Schedule.next_run_at <= now)
                .all())
