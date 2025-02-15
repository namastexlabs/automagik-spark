
import os
from uuid import UUID
from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown, beat_init, celeryd_after_setup
from celery.beat import Scheduler, ScheduleEntry
from kombu.connection import Connection
from kombu.messaging import Exchange, Queue
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, or_, and_
from .database.session import get_sync_session
from .database.models import Schedule
from .config import get_settings

logger = logging.getLogger(__name__)

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
            
            # Get all active schedules and uncompleted one-time schedules
            with get_sync_session() as session:
                # First check all schedules
                all_schedules = session.execute(select(Schedule)).scalars().all()
                logger.info(f"Found {len(all_schedules)} total schedules in database")
                for s in all_schedules:
                    logger.info(f"Schedule {s.id}: type={s.schedule_type}, status={s.status}, expr={s.schedule_expr}")
                
                # Only get active schedules that aren't completed
                stmt = select(Schedule).where(
                    and_(
                        Schedule.status == 'active',
                        Schedule.status != 'completed'
                    )
                ).with_for_update()
                result = session.execute(stmt)
                schedules = result.scalars().all()
                logger.info(f"Found {len(schedules)} active schedules")
                
                # Mark one-time schedules as completed immediately
                for schedule in schedules:
                    if schedule.schedule_type == 'one-time':
                        schedule.status = 'completed'
                        session.commit()
                        logger.info(f"Marked one-time schedule {schedule.id} as completed before adding to scheduler")
                
                for schedule in schedules:
                    # Skip completed schedules
                    if schedule.status == 'completed':
                        logger.info(f"Skipping completed schedule {schedule.id}")
                        continue
                        
                    schedule_id = str(schedule.id)
                    schedule_name = f"schedule_{schedule_id}"
                    
                    # Parse schedule
                    if schedule.schedule_type == 'interval':
                        try:
                            # Parse interval string (e.g., "1m")
                            value = int(schedule.schedule_expr[:-1])  # Remove last character (e.g., 'm' from '1m')
                            unit = schedule.schedule_expr[-1]  # Get last character (e.g., 'm' from '1m')
                            
                            # Convert to seconds
                            seconds = {
                                's': lambda x: x,
                                'm': lambda x: x * 60,
                                'h': lambda x: x * 3600,
                                'd': lambda x: x * 86400,
                            }.get(unit, lambda x: x)(value)
                            
                            from celery.schedules import schedule as celery_schedule
                            
                            # Create schedule entry
                            entry = ScheduleEntry(
                                name=schedule_name,
                                schedule=celery_schedule(timedelta(seconds=seconds)),
                                task='automagik.core.tasks.workflow_tasks.execute_workflow',
                                args=(schedule_id,),
                                kwargs={},
                                options={
                                    'expires': 600,  # Task expires after 10 minutes
                                    'retry': True,
                                    'retry_policy': {
                                        'max_retries': 3,
                                        'interval_start': 0,
                                        'interval_step': 0.2,
                                        'interval_max': 0.2,
                                    },
                                },
                                app=self.app
                            )
                            self.schedule[schedule_name] = entry
                        except (ValueError, KeyError) as e:
                            logger.error(f"Failed to parse interval for schedule {schedule_id}: {e}")
                            continue
                    elif schedule.schedule_type == 'cron':
                        # Create schedule entry with cron expression
                        from celery.schedules import crontab
                        try:
                            # Parse cron expression
                            cron_parts = schedule.schedule_expr.split()
                            if len(cron_parts) != 5:
                                logger.error(f"Invalid cron expression for schedule {schedule_id}: {schedule.schedule_expr}")
                                continue
                                
                            minute, hour, day_of_month, month_of_year, day_of_week = cron_parts
                            
                            # Create schedule entry
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
                                options={
                                    'expires': 600,  # Task expires after 10 minutes
                                    'retry': True,
                                    'retry_policy': {
                                        'max_retries': 3,
                                        'interval_start': 0,
                                        'interval_step': 0.2,
                                        'interval_max': 0.2,
                                    },
                                },
                                app=self.app
                            )
                            self.schedule[schedule_name] = entry
                        except Exception as e:
                            logger.error(f"Failed to parse cron expression for schedule {schedule_id}: {e}")
                            continue
                    elif schedule.schedule_type == 'one-time':
                        try:
                            # Parse datetime
                            if schedule.schedule_expr.lower() == 'now':
                                run_time = datetime.now(timezone.utc)
                            else:
                                from dateutil import parser
                                run_time = parser.parse(schedule.schedule_expr)
                                if not run_time.tzinfo:
                                    run_time = run_time.replace(tzinfo=timezone.utc)
                            
                            now = datetime.now(timezone.utc)
                            
                            # For 'now' or past schedules, trigger immediately and mark as completed
                            if schedule.schedule_expr.lower() == 'now' or run_time <= now:
                                # Only trigger if status is still 'active'
                                if schedule.status == 'active':
                                    # Create a one-time schedule that will be removed after execution
                                    from celery.schedules import schedule
                                    entry = ScheduleEntry(
                                        name=schedule_name,
                                        schedule=schedule(timedelta(seconds=0), relative=True),
                                        task='automagik.core.tasks.workflow_tasks.execute_workflow',
                                        args=(schedule_id,),
                                        kwargs={},
                                        options={
                                            'expires': 600,  # Task expires after 10 minutes
                                            'retry': True,
                                            'retry_policy': {
                                                'max_retries': 3,
                                                'interval_start': 0,
                                                'interval_step': 0.2,
                                                'interval_max': 0.2,
                                            },
                                        },
                                        app=self.app,
                                        last_run_at=None  # Set to None to ensure it runs immediately
                                    )
                                    self.schedule[schedule_name] = entry
                                    logger.info(f"Added one-time schedule {schedule_name} to scheduler")
                            else:
                                # For future schedules, create a one-time schedule entry
                                from celery.schedules import schedule
                                
                                # Calculate delay in seconds
                                delay = (run_time - now).total_seconds()
                                
                                # Create schedule entry that runs once after the delay
                                entry = ScheduleEntry(
                                    name=schedule_name,
                                    schedule=schedule(timedelta(seconds=delay), relative=True),
                                    task='automagik.core.tasks.workflow_tasks.execute_workflow',
                                    args=(schedule_id,),
                                    kwargs={},
                                    options={
                                        'expires': 600,  # Task expires after 10 minutes
                                        'retry': True,
                                        'retry_policy': {
                                            'max_retries': 3,
                                            'interval_start': 0,
                                            'interval_step': 0.2,
                                            'interval_max': 0.2,
                                        },
                                    },
                                    app=self.app
                                )
                                self.schedule[schedule_name] = entry
                        except Exception as e:
                            logger.error(f"Failed to parse datetime for schedule {schedule_id}: {e}")
                            continue
                    else:
                        logger.error(f"Unsupported schedule type for schedule {schedule_id}: {schedule.schedule_type}")
                        continue
            
            # Mark as updated
            self.schedule_changed = False
            
            logger.info("Updated scheduler from database")
        except Exception as e:
            logger.error(f"Failed to update scheduler from database: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def tick(self, *args, **kwargs):
        """Run a tick - one iteration of the scheduler.
        
        Checks the schedule to see if there are any new tasks
        that should be added to the schedule.
        """
        # Only update from database if something has changed
        if self.schedule_changed:
            self.update_from_database()
            self.schedule_changed = False
        
        # Log next scheduled tasks
        logger.debug(f"Current schedules: {self.schedule}")
        if self.schedule:
            now = datetime.now(timezone.utc)
            schedules_to_remove = []
            schedules_to_run = []
            
            # First pass: check all schedules and mark which ones to run/remove
            for name, entry in self.schedule.items():
                logger.debug(f"Processing schedule {name}")
                try:
                    # Get the next run time using is_due()
                    is_due, next_time_to_run = entry.is_due()
                    if not is_due:
                        hours = int(next_time_to_run // 3600)
                        minutes = int((next_time_to_run % 3600) // 60)
                        seconds = int(next_time_to_run % 60)
                        logger.info(f"Next run of {name} in {hours:02d}:{minutes:02d}:{seconds:02d}")
                        continue
                        
                    # Check schedule status before executing
                    schedule_id = name.replace('schedule_', '')
                    with get_sync_session() as session:
                        stmt = select(Schedule).where(Schedule.id == UUID(schedule_id))
                        schedule = session.execute(stmt).scalar_one_or_none()
                        if not schedule or schedule.status == 'completed':
                            schedules_to_remove.append(name)
                            logger.info(f"Removing completed/missing schedule {name} from scheduler")
                            continue
                            
                        if schedule.schedule_type == 'one-time':
                            # Mark one-time schedules as completed before execution
                            schedule.status = 'completed'
                            session.commit()
                            schedules_to_remove.append(name)
                            logger.info(f"Marking one-time schedule {name} as completed")
                            
                        # Add to run list if not completed
                        schedules_to_run.append((name, entry))
                        logger.info(f"Schedule {name} is due now")
                except Exception as e:
                    logger.error(f"Error processing schedule {name}: {e}")
                    schedules_to_remove.append(name)
            
            # Second pass: remove completed schedules
            for name in schedules_to_remove:
                if name in self.schedule:
                    del self.schedule[name]
                    logger.info(f"Removed schedule {name} from scheduler")
            
            # Third pass: run remaining schedules
            for name, entry in schedules_to_run:
                try:
                    # Create a dummy entry with a custom is_due that only returns True once
                    from celery.schedules import schedule
                    dummy_schedule = schedule(timedelta(seconds=0))
                    entry.schedule = dummy_schedule
                    entry.is_due()
                except Exception as e:
                    logger.error(f"Error running schedule {name}: {e}")
            
            # Remove completed one-time schedules
            for name in schedules_to_remove:
                if name in self.schedule:
                    del self.schedule[name]
                    logger.info(f"Removed one-time schedule {name} from scheduler")
        else:
            logger.debug("No schedules found in the database")
        
        # Run the actual tick
        return super().tick(*args, **kwargs)

    def close(self):
        """Close the scheduler."""
        super().close()

# Configure Celery with Redis as broker and backend
def get_celery_config():
    """Get Celery configuration."""
    return {
        'broker_url': os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        'result_backend': os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        'task_queues': (
            Queue('default', Exchange('default'), routing_key='default'),
            Queue('high_priority', Exchange('high_priority'), routing_key='high_priority'),
            Queue('low_priority', Exchange('low_priority'), routing_key='low_priority'),
        ),
        'task_default_queue': 'default',
        'task_routes': {
            'automagik.core.tasks.workflow_tasks.execute_workflow': {'queue': 'default'},
            'automagik.core.tasks.workflow_tasks.process_pending_tasks': {'queue': 'default'},
        },
        'worker_concurrency': int(os.getenv('CELERY_WORKER_CONCURRENCY', 2)),
        'task_acks_late': True,
        'task_reject_on_worker_lost': True,
        'task_retry_max_retries': 3,
        'task_retry_backoff': True,
        'task_retry_backoff_max': 600,  # 10 minutes max backoff
        'beat_schedule': {
            'process-pending-tasks': {
                'task': 'automagik.core.tasks.workflow_tasks.process_pending_tasks',
                'schedule': timedelta(seconds=10),  # Run every 10 seconds
                'options': {'queue': 'default'},
                'args': ()
            }
        },  # Will be populated dynamically with additional schedules
        'beat_max_loop_interval': 1,  
        'beat_scheduler': 'automagik.core.celery_config:DatabaseScheduler',
        'beat_schedule_filename': os.path.join(os.path.dirname(get_settings().worker_log), 'celerybeat-schedule'),
        'imports': (
            'automagik.core.tasks.workflow_tasks',
        ),
        # Worker settings
        'worker_prefetch_multiplier': 1,  # Disable prefetching
        'worker_max_tasks_per_child': 100,  # Restart worker after 100 tasks
        'worker_max_memory_per_child': 200000,  # 200MB memory limit
        'task_time_limit': 3600,  # 1 hour timeout
        'task_soft_time_limit': 3300,  # 55 minutes soft timeout
        'broker_connection_retry_on_startup': True,
        'broker_pool_limit': None,  # Disable connection pooling
        'broker_connection_max_retries': None,  # Retry forever
        'broker_connection_retry': True,
        'broker_heartbeat': 10,
        'event_queue_expires': 60,
        'worker_lost_wait': 10,
        'worker_disable_rate_limits': True,
    }

def create_celery_app():
    """Create Celery application."""
    # Set up logging first
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
    )
    
    # Add file handler
    log_dir = os.path.expanduser('/tmp/.automagik')
    os.makedirs(log_dir, exist_ok=True)
    
    # Remove existing handlers to avoid duplicate logs
    logger.handlers = []
    
    # Add file handler
    fh = logging.FileHandler(os.path.join(log_dir, 'worker.log'))
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # Create Celery app
    celery_app = Celery('automagik')
    
    # Load config
    config = get_celery_config()
    celery_app.conf.update(config)
    
    return celery_app

# Global Celery app instance
app = create_celery_app()

# Global scheduler instance
_scheduler_instance = None

def get_scheduler_instance():
    """Get the current scheduler instance."""
    return _scheduler_instance

def notify_scheduler_change():
    """Notify the scheduler that schedules have changed."""
    scheduler = get_scheduler_instance()
    logger.info(f"Notifying scheduler change, scheduler instance: {scheduler}")
    if scheduler:
        logger.info("Setting schedule_changed to True")
        scheduler.schedule_changed = True
    else:
        logger.warning("No scheduler instance found!")

def update_celery_beat_schedule():
    """Update Celery beat schedule from database schedules."""
    with get_sync_session() as session:
        try:
            # Get all active schedules
            stmt = select(Schedule).where(Schedule.status == 'active')
            result = session.execute(stmt)
            schedules = result.scalars().all()
            
            # Create new beat schedule
            beat_schedule = {}
            
            for schedule in schedules:
                schedule_id = str(schedule.id)
                schedule_name = f"schedule_{schedule_id}"
                
                # Parse schedule
                if schedule.schedule_type == 'interval':
                    try:
                        # Parse interval string (e.g., "1m")
                        value = int(schedule.schedule_expr[:-1])  # Remove last character (e.g., 'm' from '1m')
                        unit = schedule.schedule_expr[-1]  # Get last character (e.g., 'm' from '1m')
                        
                        # Convert to seconds
                        seconds = {
                            's': lambda x: x,
                            'm': lambda x: x * 60,
                            'h': lambda x: x * 3600,
                            'd': lambda x: x * 86400,
                        }.get(unit, lambda x: x)(value)
                        
                        # Create schedule entry
                        beat_schedule[schedule_name] = {
                            'task': 'automagik.core.tasks.workflow_tasks.execute_workflow',
                            'schedule': timedelta(seconds=seconds),
                            'args': (schedule_id,),
                            'kwargs': {},
                            'options': {
                                'expires': 600,  # Task expires after 10 minutes
                                'retry': True,
                                'retry_policy': {
                                    'max_retries': 3,
                                    'interval_start': 0,
                                    'interval_step': 0.2,
                                    'interval_max': 0.2,
                                },
                            },
                        }
                    except (ValueError, KeyError) as e:
                        logger.error(f"Failed to parse interval for schedule {schedule_id}: {e}")
                        continue
                elif schedule.schedule_type == 'cron':
                    # Create schedule entry with cron expression
                    from celery.schedules import crontab
                    try:
                        # Parse cron expression
                        cron_parts = schedule.schedule_expr.split()
                        if len(cron_parts) != 5:
                            logger.error(f"Invalid cron expression for schedule {schedule_id}: {schedule.schedule_expr}")
                            continue
                            
                        minute, hour, day_of_month, month_of_year, day_of_week = cron_parts
                        
                        # Create schedule entry
                        beat_schedule[schedule_name] = {
                            'task': 'automagik.core.tasks.workflow_tasks.execute_workflow',
                            'schedule': crontab(
                                minute=minute,
                                hour=hour,
                                day_of_month=day_of_month,
                                month_of_year=month_of_year,
                                day_of_week=day_of_week
                            ),
                            'args': (schedule_id,),
                            'kwargs': {},
                            'options': {
                                'expires': 600,  # Task expires after 10 minutes
                                'retry': True,
                                'retry_policy': {
                                    'max_retries': 3,
                                    'interval_start': 0,
                                    'interval_step': 0.2,
                                    'interval_max': 0.2,
                                },
                            },
                        }
                    except Exception as e:
                        logger.error(f"Failed to parse cron expression for schedule {schedule_id}: {e}")
                        continue
                else:
                    logger.error(f"Unsupported schedule type for schedule {schedule_id}: {schedule.schedule_type}")
                    continue
            
            # Update celery beat schedule
            app.conf.beat_schedule = beat_schedule
            logger.info(f"Updated beat schedule with {len(beat_schedule)} schedules")
        except Exception as e:
            logger.error(f"Failed to update beat schedule: {e}")
            raise

@worker_process_init.connect
def configure_worker(**_):
    """Configure worker process on initialization"""
    # Initialize logging
    log_path = os.getenv('AUTOMAGIK_WORKER_LOG', '/tmp/.automagik/worker.log')
    log_path = os.path.expanduser(log_path)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logging.root.addHandler(file_handler)
    
    # Set log level from environment or default to INFO
    log_level = os.getenv('AUTOMAGIK_LOG_LEVEL', 'INFO')
    logging.root.setLevel(getattr(logging, log_level))
    
    logger.info("Worker process initialized")

@worker_process_shutdown.connect
def cleanup_worker(**_):
    """Cleanup tasks when worker shuts down"""
    logger.info("Worker process shutting down")

@beat_init.connect
def init_scheduler(sender=None, **kwargs):
    """Initialize the scheduler with database schedules."""
    try:
        logger.info("Initializing beat scheduler")
        # Set up logging first
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
        )
        
        # Remove existing handlers to avoid duplicate logs
        logger.handlers = []
        
        # Add file handler
        settings = get_settings()
        fh = logging.FileHandler(settings.worker_log)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Store scheduler instance
        global _scheduler_instance
        if sender and hasattr(sender, 'scheduler'):
            logger.info("Storing beat scheduler instance from sender")
            _scheduler_instance = sender.scheduler
        elif not _scheduler_instance:
            logger.info("Creating new DatabaseScheduler instance")
            _scheduler_instance = DatabaseScheduler(app=app)
        
        logger.info(f"Using scheduler instance: {_scheduler_instance}")
        
        # Update schedule
        update_celery_beat_schedule()
        
        logger.info("Beat scheduler initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize beat scheduler: {e}")
        import traceback
        logger.error(traceback.format_exc())

@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    """Setup direct queue after worker initialized."""
    logger.info("Setting up direct queue...")
    logger.info(f"Worker {sender} initialized with instance {instance}")
    logger.info(f"Worker configuration: {app.conf}")


