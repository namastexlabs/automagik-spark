"""Celery application configuration."""

import os
from celery import Celery
from kombu.messaging import Exchange, Queue
from ..config import get_settings

def get_celery_config():
    """Get Celery configuration."""
    settings = get_settings()
    
    # Default broker and backend URLs
    broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Define queues
    task_queues = [
        Queue('celery', Exchange('celery'), routing_key='celery'),
        Queue('direct', Exchange('direct'), routing_key='direct'),
    ]
    
    config = {
        'broker_url': broker_url,
        'result_backend': result_backend,
        'task_queues': task_queues,
        'task_default_queue': 'celery',
        'task_default_exchange': 'celery',
        'task_default_routing_key': 'celery',
        'beat_scheduler': 'automagik.core.celery.scheduler:DatabaseScheduler',
        'imports': (
            'automagik.core.celery.tasks',
            'automagik.core.tasks.workflow_tasks',
        ),
        'worker_prefetch_multiplier': 1,
        'task_track_started': True,
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'broker_connection_retry_on_startup': True,
        # Beat scheduler configuration
        'beat_max_loop_interval': 5,  # Maximum number of seconds to sleep between checking schedule
        'beat_schedule_filename': None  # Disable file-based schedule persistence since we use database
    }
    
    return config

def create_celery_app():
    """Create and configure Celery application."""
    app = Celery('automagik')
    app.conf.update(get_celery_config())
    return app

# Global Celery app instance
app = create_celery_app()
