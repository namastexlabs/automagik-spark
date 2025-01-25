"""
Scheduler management module.

Provides the main interface for managing schedules and running scheduled flows.
"""

import logging
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from croniter import croniter
import re
from dateutil import parser

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..database.models import Schedule, Task, Flow
from ..flows.manager import FlowManager
from .scheduler import FlowScheduler
from .task_runner import TaskRunner

logger = logging.getLogger(__name__)


class SchedulerManager:
    """Scheduler management class."""
    
    def __init__(self, session: AsyncSession, flow_manager: FlowManager):
        """
        Initialize scheduler manager.
        
        Args:
            session: Database session
            flow_manager: Flow manager instance for executing flows
        """
        self.session = session
        self.flow_manager = flow_manager
        self.scheduler = FlowScheduler(session, flow_manager)
        self.task_runner = TaskRunner(session, flow_manager)

    async def __aenter__(self):
        """Enter context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        await self.stop()

    async def start(self):
        """Start the scheduler."""
        await self.scheduler.start()

    async def stop(self):
        """Stop the scheduler."""
        await self.scheduler.stop()

    def _validate_interval(self, interval: str) -> bool:
        """
        Validate interval expression.
        
        Valid formats:
        - Xm: X minutes (e.g., "1m", "30m")
        - Xh: X hours (e.g., "1h", "24h")
        - Xd: X days (e.g., "1d", "7d")
        
        Where X is a positive integer.
        """
        try:
            # Must be a non-empty string
            if not interval or not isinstance(interval, str):
                return False
                
            # Must end with valid unit (m, h, d)
            if len(interval) < 2 or interval[-1].lower() not in ['m', 'h', 'd']:
                return False
                
            # Must have a value before the unit
            value_str = interval[:-1]
            if not value_str.isdigit():
                return False
                
            # Value must be a positive integer
            value = int(value_str)
            if value <= 0:
                return False
                
            # Must not have any extra characters
            if len(interval) != len(str(value)) + 1:
                return False
                
            return True
            
        except (ValueError, TypeError, AttributeError):
            return False

    def parse_interval(self, interval: str) -> timedelta:
        """
        Parse interval string into timedelta.
        
        Args:
            interval: Interval string (e.g., "30m", "1h", "1d")
            
        Returns:
            timedelta object
            
        Raises:
            ValueError if interval is invalid
        """
        if not self._validate_interval(interval):
            raise ValueError(f"Invalid interval format: {interval}")
            
        value = int(interval[:-1])
        unit = interval[-1].lower()
        
        if unit == 'm':
            return timedelta(minutes=value)
        elif unit == 'h':
            return timedelta(hours=value)
        elif unit == 'd':
            return timedelta(days=value)
        else:
            raise ValueError("Invalid interval unit")

    def _validate_cron(self, cron: str) -> bool:
        """Validate cron expression."""
        try:
            croniter(cron)
            return True
        except (ValueError, TypeError):
            return False

    def _calculate_next_run(self, schedule_type: str, schedule_expr: str) -> Optional[datetime]:
        """Calculate next run time based on schedule type and expression."""
        now = datetime.now(timezone.utc)
        
        if schedule_type == "interval":
            if not self._validate_interval(schedule_expr):
                logger.error(f"Invalid interval expression: {schedule_expr}")
                return None
            try:
                delta = self.parse_interval(schedule_expr)
                return now + delta
            except ValueError as e:
                logger.error(f"Error parsing interval: {e}")
                return None
            
        elif schedule_type == "cron":
            if not self._validate_cron(schedule_expr):
                logger.error(f"Invalid cron expression: {schedule_expr}")
                return None
            cron = croniter(schedule_expr, now)
            next_run = cron.get_next(datetime)
            return next_run.replace(tzinfo=timezone.utc)
            
        return None

    # Schedule database operations
    async def create_schedule(
        self,
        flow_id: UUID,
        schedule_type: str,
        schedule_expr: str,
        flow_params: Optional[Dict[str, Any]] = None
    ) -> Optional[Schedule]:
        """Create a schedule for a flow."""
        try:
            # Check if flow exists
            result = await self.session.execute(
                select(Flow).where(Flow.id == flow_id)
            )
            flow = result.scalar_one_or_none()
            if not flow:
                logger.error(f"Flow {flow_id} not found")
                return None

            # Validate schedule type
            if schedule_type not in ["interval", "cron"]:
                logger.error(f"Invalid schedule type: {schedule_type}")
                return None

            # Calculate next run time
            next_run = self._calculate_next_run(schedule_type, schedule_expr)
            if next_run is None:
                logger.error(f"Invalid schedule expression: {schedule_expr}")
                return None

            schedule = Schedule(
                id=uuid4(),
                flow_id=flow_id,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                flow_params=flow_params or {},
                next_run_at=next_run
            )
            
            self.session.add(schedule)
            await self.session.commit()
            await self.session.refresh(schedule)
            
            return schedule
            
        except Exception as e:
            logger.error(f"Error creating schedule: {e}")
            await self.session.rollback()
            return None

    async def list_schedules(self) -> List[Schedule]:
        """List all schedules from database."""
        result = await self.session.execute(
            select(Schedule)
            .options(joinedload(Schedule.flow))
            .order_by(Schedule.created_at)
        )
        return list(result.scalars().all())

    async def update_schedule_status(self, schedule_id: str, action: str) -> bool:
        """Update schedule status."""
        try:
            status_map = {
                'pause': 'paused',
                'resume': 'active',
                'stop': 'stopped'
            }
            
            new_status = status_map.get(action)
            if not new_status:
                logger.error(f"Invalid action: {action}")
                return False
            
            try:
                schedule_uuid = UUID(schedule_id)
            except ValueError:
                logger.error(f"Invalid schedule ID: {schedule_id}")
                return False
            
            result = await self.session.execute(
                select(Schedule)
                .where(Schedule.id == schedule_uuid)
            )
            schedule = result.scalar_one_or_none()
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            schedule.status = new_status
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule status: {str(e)}")
            await self.session.rollback()
            return False

    async def update_schedule_next_run(self, schedule_id: str, next_run: datetime) -> bool:
        """Update schedule next run time."""
        try:
            try:
                schedule_uuid = UUID(schedule_id)
            except ValueError:
                logger.error(f"Invalid schedule ID: {schedule_id}")
                return False
            
            result = await self.session.execute(
                select(Schedule)
                .where(Schedule.id == schedule_uuid)
            )
            schedule = result.scalar_one_or_none()
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            # Ensure next_run is timezone-aware
            if next_run.tzinfo is None:
                next_run = next_run.replace(tzinfo=timezone.utc)
            
            schedule.next_run_at = next_run
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule next run: {str(e)}")
            await self.session.rollback()
            return False

    async def update_schedule_expression(
        self,
        schedule_id: UUID,
        schedule_expr: str
    ) -> bool:
        """
        Update a schedule's expression.
        
        Args:
            schedule_id: Schedule ID
            schedule_expr: New schedule expression
            
        Returns:
            True if update was successful
        """
        try:
            # Get schedule
            result = await self.session.execute(
                select(Schedule).where(Schedule.id == schedule_id)
            )
            schedule = result.scalar_one()
            
            # Validate new expression
            if schedule.schedule_type == 'interval':
                if not self._validate_interval(schedule_expr):
                    logger.error(f"Invalid interval expression: {schedule_expr}")
                    return False
            else:  # cron
                if not self._validate_cron(schedule_expr):
                    logger.error(f"Invalid cron expression: {schedule_expr}")
                    return False
            
            # Update expression
            schedule.schedule_expr = schedule_expr
            
            # Calculate and update next run time
            next_run = self._calculate_next_run(schedule.schedule_type, schedule_expr)
            if next_run:
                schedule.next_run_at = next_run
            else:
                logger.error(f"Failed to calculate next run time for expression: {schedule_expr}")
                return False
            
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule expression: {str(e)}")
            return False

    async def delete_schedule(self, schedule_id: UUID) -> bool:
        """Delete a schedule."""
        try:
            result = await self.session.execute(
                select(Schedule).where(Schedule.id == schedule_id)
            )
            schedule = result.scalar_one_or_none()
            
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            await self.session.delete(schedule)
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting schedule: {e}")
            return False

    async def get_schedule(self, schedule_id: UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        result = await self.session.execute(
            select(Schedule).where(Schedule.id == schedule_id)
        )
        return result.scalar_one_or_none()
