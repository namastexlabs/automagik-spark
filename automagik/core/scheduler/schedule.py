"""Schedule management module."""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models import Schedule

logger = logging.getLogger(__name__)

class ScheduleManager:
    """Schedule management class."""
    
    def __init__(self, session: AsyncSession):
        """Initialize schedule manager."""
        self.session = session

    async def create_schedule(
        self,
        flow_id: UUID,
        schedule_type: str,
        schedule_expr: str,
        flow_params: Optional[Dict[str, Any]] = None
    ) -> Optional[Schedule]:
        """Create a schedule for a flow."""
        try:
            schedule = Schedule(
                id=uuid4(),
                flow_id=flow_id,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                flow_params=flow_params or {},
                next_run_at=datetime.utcnow()  # TODO: Calculate based on schedule
            )
            
            self.session.add(schedule)
            await self.session.commit()
            await self.session.refresh(schedule)
            
            return schedule
            
        except Exception as e:
            logger.error(f"Error creating schedule: {e}")
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
            
            result = await self.session.execute(
                select(Schedule)
                .where(Schedule.id == schedule_id)
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
            result = await self.session.execute(
                select(Schedule)
                .where(Schedule.id == schedule_id)
            )
            schedule = result.scalar_one_or_none()
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return False
            
            # Ensure next_run is timezone-aware
            if next_run.tzinfo is None:
                next_run = next_run.replace(tzinfo=datetime.utcnow().tzinfo)
            
            schedule.next_run_at = next_run
            await self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule next run: {str(e)}")
            await self.session.rollback()
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
