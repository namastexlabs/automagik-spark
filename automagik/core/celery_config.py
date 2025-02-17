"""Legacy Celery configuration module - imports from new modular structure."""

from .celery.celery_app import app
from .celery.scheduler import DatabaseScheduler, notify_scheduler_change, get_scheduler_instance

__all__ = ['app', 'DatabaseScheduler', 'notify_scheduler_change', 'get_scheduler_instance']