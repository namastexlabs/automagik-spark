
"""Workflow scheduler."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

from croniter import croniter
from dateutil.parser import parse as parse_datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models import Schedule, Task, Workflow
from ..workflows.manager import WorkflowManager

logger = logging.getLogger(__name__)


class WorkflowScheduler:
    """Workflow scheduler."""

    def __init__(self, session: AsyncSession, workflow_manager: WorkflowManager):
        """Initialize workflow scheduler."""
        self.session = session
        self.workflow_manager = workflow_manager

    async def __aenter__(self):
        """Enter context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        await self.session.close()
        
    async def stop(self):
        """Stop the scheduler."""
        await self.session.close()

    def _get_next_run(self, schedule_type: str, schedule_expr: str) -> Optional[datetime]:
        """Get next run time for a schedule."""
        try:
            now = datetime.now(timezone.utc)
            if schedule_type == "cron":
                return croniter(schedule_expr, now).get_next(datetime)
            elif schedule_type == "interval":
                return parse_datetime(schedule_expr)
            elif schedule_type == "one-time":
                if schedule_expr.lower() == "now":
                    return now
                dt = parse_datetime(schedule_expr)
                if not dt.tzinfo:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt < now:
                    logger.error("Cannot schedule in the past")
                    return None
                return dt
            else:
                logger.error(f"Invalid schedule type: {schedule_type}")
                return None
        except Exception as e:
            logger.error(f"Error parsing schedule expression: {e}")
            return None

    async def create_schedule(
        self,
        workflow_id: UUID,
        schedule_type: str,
        schedule_expr: str,
        input_data: Optional[str] = None
    ) -> Optional[Schedule]:
        """Create a schedule for a workflow."""
        try:
            # Check if workflow exists
            result = await self.session.execute(
                select(Workflow).where(Workflow.id == workflow_id)
            )
            workflow = result.scalar_one_or_none()
            if not workflow:
                logger.error(f"Workflow {workflow_id} not found")
                return None

            # Validate schedule type
            if schedule_type not in ["cron", "interval", "one-time"]:
                logger.error(f"Invalid schedule type: {schedule_type}")
                return None

            # Calculate next run time
            next_run = self._get_next_run(schedule_type, schedule_expr)
            if not next_run:
                return None

            # Use input_data as is, defaulting to empty string if None
            final_input = input_data or ""

            # Create schedule with timezone-aware next_run_at
            schedule = Schedule(
                id=uuid4(),
                workflow_id=workflow_id,
                schedule_type=schedule_type,
                schedule_expr=schedule_expr,
                input_data=final_input,
                next_run_at=next_run,  # This is already timezone-aware from _get_next_run
                status='active'  # Set initial status to active
            )

            self.session.add(schedule)
            await self.session.commit()
            
            # Log schedule creation
            logger.info(f"Created schedule {schedule.id}: type={schedule.schedule_type}, status={schedule.status}, expr={schedule.schedule_expr}")
            
            # Notify celery scheduler
            from ..celery_config import notify_scheduler_change
            logger.info("Notifying celery scheduler of changes")
            notify_scheduler_change()
            
            return schedule
        except Exception as e:
            logger.error(f"Error creating schedule: {e}")
            await self.session.rollback()
            return None

    async def update_schedule(
        self,
        schedule_id: UUID,
        schedule_type: Optional[str] = None,
        schedule_expr: Optional[str] = None,
        input_data: Optional[str] = None,
        active: Optional[bool] = None
    ) -> Optional[Schedule]:
        """Update a schedule."""
        try:
            result = await self.session.execute(
                select(Schedule).where(Schedule.id == schedule_id)
            )
            schedule = result.scalar_one_or_none()
            if not schedule:
                logger.error(f"Schedule {schedule_id} not found")
                return None

            if schedule_type is not None:
                if schedule_type not in ["cron", "interval", "one-time"]:
                    logger.error(f"Invalid schedule type: {schedule_type}")
                    return None
                schedule.schedule_type = schedule_type

            if schedule_expr is not None:
                schedule.schedule_expr = schedule_expr

            if input_data is not None:
                schedule.input_data = input_data

            if active is not None:
                schedule.active = active

            # Update next run time if schedule type or expression changed
            if schedule_type is not None or schedule_expr is not None:
                next_run = self._get_next_run(
                    schedule.schedule_type,
                    schedule.schedule_expr
                )
                if not next_run:
                    return None
                schedule.next_run_at = next_run

            await self.session.commit()
            return schedule
        except Exception as e:
            logger.error(f"Error updating schedule: {e}")
            await self.session.rollback()
            return None

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
            await self.session.rollback()
            return False

    async def get_schedule(self, schedule_id: UUID) -> Optional[Schedule]:
        """Get a schedule by ID."""
        try:
            result = await self.session.execute(
                select(Schedule).where(Schedule.id == schedule_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting schedule: {e}")
            return None

    async def list_schedules(self) -> List[Schedule]:
        """List all schedules."""
        try:
            result = await self.session.execute(
                select(Schedule)
                .join(Workflow)
                .options(joinedload(Schedule.workflow))
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Error listing schedules: {e}")
            return []

    async def process_schedules(self) -> None:
        """Process all active schedules."""
        try:
            now = datetime.now(timezone.utc)
            # Query all active schedules
            result = await self.session.execute(
                select(Schedule).where(
                    Schedule.active == True
                )
            )
            schedules = list(result.scalars().all())

            for schedule in schedules:
                # Only process schedules that are due
                if schedule.next_run_at and schedule.next_run_at <= now:
                    # Create and run task
                    input_data = str(schedule.workflow_params) if schedule.workflow_params else ""
                    task = Task(
                        id=uuid4(),
                        workflow_id=schedule.workflow_id,
                        schedule_id=schedule.id,
                        input_data=input_data,
                        status="pending",
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc)
                    )
                self.session.add(task)
                await self.session.commit()

                # Run the workflow with the task
                await self.workflow_manager.run_workflow(
                    workflow_id=schedule.workflow_id,
                    input_data=input_data,
                    existing_task=task
                )

                # Update next run time
                next_run = self._get_next_run(
                    schedule.schedule_type,
                    schedule.schedule_expr
                )
                if next_run:
                    schedule.next_run_at = next_run
                    await self.session.commit()

        except Exception as e:
            logger.error(f"Error processing schedules: {e}")
            await self.session.rollback()

    async def start_scheduler(self) -> None:
        """Start the scheduler."""
        try:
            while True:
                # Get active schedules
                query = select(Schedule).filter(Schedule.active == True)
                result = await self.session.execute(query)
                schedules = result.scalars().all()

                for schedule in schedules:
                    # Check if it's time to run
                    if schedule.next_run_at <= datetime.now(timezone.utc):
                        # Create and run task
                        input_data = str(schedule.workflow_params) if schedule.workflow_params else ""
                        task = Task(
                            id=uuid4(),
                            workflow_id=schedule.workflow_id,
                            schedule_id=schedule.id,
                            input_data=input_data,
                            status="pending",
                            created_at=datetime.now(timezone.utc),
                            updated_at=datetime.now(timezone.utc)
                        )
                        self.session.add(task)
                        await self.session.commit()

                        # Run the workflow with the task
                        await self.workflow_manager.run_workflow(
                            workflow_id=schedule.workflow_id,
                            input_data=input_data,
                            existing_task=task
                        )

                        # Update next run time
                        next_run = self._get_next_run(
                            schedule.schedule_type,
                            schedule.schedule_expr
                        )
                        if next_run:
                            schedule.next_run_at = next_run
                            await self.session.commit()

                await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Error in scheduler loop: {str(e)}")


