"""Database-backed Celery beat scheduler."""

import logging
from datetime import datetime, timezone, timedelta
from celery.beat import Scheduler, ScheduleEntry
from celery.schedules import schedule as celery_schedule, crontab
from dateutil import parser
from sqlalchemy import select
from ..database.session import get_sync_session
from ..database.models import Schedule

logger = logging.getLogger(__name__)

# Global scheduler instance
_scheduler_instance = None

class DatabaseScheduler(Scheduler):
    """Custom scheduler that loads schedules from database."""

    def __init__(self, *args, **kwargs):
        """Initialize scheduler."""
        global _scheduler_instance
        logger.info("Initializing DatabaseScheduler")
        self.schedule_changed = True
        super().__init__(*args, **kwargs)
        
        # Store instance globally before updating database
        logger.info("Storing scheduler instance globally")
        _scheduler_instance = self
        logger.info(f"Stored scheduler instance: {_scheduler_instance}")
        
        # Set app on the instance
        if 'app' in kwargs:
            self.app = kwargs['app']
        
        # Now update from database
        self.update_from_database()

    def setup_schedule(self):
        """Set up the schedule."""
        self.update_from_database()
        self.merge_inplace(self.app.conf.beat_schedule)

    def update_from_database(self):
        """Update schedule from database."""
        logger.info("Updating beat schedule from database")
        try:
            # Update scheduler
            self.schedule = {}
            
            # Get all active schedules
            with get_sync_session() as session:
                stmt = select(Schedule).where(
                    Schedule.status == 'active'
                ).with_for_update()
                result = session.execute(stmt)
                schedules = result.scalars().all()
                logger.info(f"Found {len(schedules)} active schedules")
                
                for schedule in schedules:
                    schedule_id = str(schedule.id)
                    schedule_name = f"schedule_{schedule_id}"
                    
                    # Common task options
                    task_options = {
                        'expires': 600,  # Task expires after 10 minutes
                        'retry': True,
                        'retry_policy': {
                            'max_retries': 3,
                            'interval_start': 0,
                            'interval_step': 0.2,
                            'interval_max': 0.2,
                        },
                    }
                    
                    try:
                        if schedule.schedule_type == 'interval':
                            # Parse interval string (e.g., "1m")
                            value = int(schedule.schedule_expr[:-1])
                            unit = schedule.schedule_expr[-1]
                            
                            # Convert to seconds
                            seconds = {
                                's': lambda x: x,
                                'm': lambda x: x * 60,
                                'h': lambda x: x * 3600,
                                'd': lambda x: x * 86400,
                            }.get(unit, lambda x: x)(value)
                            
                            entry = ScheduleEntry(
                                name=schedule_name,
                                schedule=celery_schedule(timedelta(seconds=seconds)),
                                task='automagik.core.tasks.workflow_tasks.execute_workflow',
                                args=(schedule_id,),
                                kwargs={},
                                options=task_options,
                                app=self.app
                            )
                            self.schedule[schedule_name] = entry
                            
                        elif schedule.schedule_type == 'cron':
                            cron_parts = schedule.schedule_expr.split()
                            if len(cron_parts) != 5:
                                logger.error(f"Invalid cron expression for schedule {schedule_id}")
                                continue
                                
                            minute, hour, day_of_month, month_of_year, day_of_week = cron_parts
                            
                            entry = ScheduleEntry(
                                name=schedule_name,
                                schedule=crontab(
                                    minute=minute,
                                    hour=hour,
                                    day_of_month=day_of_month,
                                    month_of_year=month_of_year,
                                    day_of_week=day_of_week
                                ),
                                task='automagik.core.tasks.workflow_tasks.execute_workflow',
                                args=(schedule_id,),
                                kwargs={},
                                options=task_options,
                                app=self.app
                            )
                            self.schedule[schedule_name] = entry
                            
                        elif schedule.schedule_type == 'one-time':
                            # Parse datetime
                            if schedule.schedule_expr.lower() == 'now':
                                run_time = datetime.now(timezone.utc)
                            else:
                                run_time = parser.parse(schedule.schedule_expr)
                                if not run_time.tzinfo:
                                    run_time = run_time.replace(tzinfo=timezone.utc)
                                else:
                                    run_time = run_time.astimezone(timezone.utc)
                            
                            now = datetime.now(timezone.utc)
                            
                            # Skip if in the past
                            if run_time < now and schedule.schedule_expr.lower() != 'now':
                                continue
                            
                            entry = ScheduleEntry(
                                name=schedule_name,
                                schedule=celery_schedule(timedelta(seconds=0), relative=True),
                                task='automagik.core.tasks.workflow_tasks.execute_workflow',
                                args=(schedule_id,),
                                kwargs={},
                                options=task_options,
                                app=self.app
                            )
                            self.schedule[schedule_name] = entry
                            
                    except Exception as e:
                        logger.error(f"Error processing schedule {schedule_id}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error updating schedule from database: {e}")

    def tick(self, *args, **kwargs):
        """Called by the beat service periodically."""
        self.update_from_database()
        return super().tick(*args, **kwargs)

def get_scheduler_instance():
    """Get the current scheduler instance."""
    return _scheduler_instance

def notify_scheduler_change():
    """Notify the scheduler that schedules have changed."""
    global _scheduler_instance
    logger.info(f"Notifying scheduler change, scheduler instance: {_scheduler_instance}")
    if _scheduler_instance is not None:
        _scheduler_instance.update_from_database()
    else:
        logger.warning("No scheduler instance found!")
