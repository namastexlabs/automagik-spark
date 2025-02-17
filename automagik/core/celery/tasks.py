"""Celery tasks and signal handlers."""

import logging
import os
from celery.signals import (
    worker_process_init,
    worker_process_shutdown,
    beat_init,
    celeryd_after_setup
)
from kombu.messaging import Exchange, Queue
from .celery_app import app

logger = logging.getLogger(__name__)

@worker_process_init.connect
def configure_worker(**kwargs):
    """Configure worker process on initialization."""
    logger.info("Initializing worker process")
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize any worker-specific resources here
    logger.info("Worker process initialized")

@worker_process_shutdown.connect
def cleanup_worker(**kwargs):
    """Cleanup tasks when worker shuts down."""
    logger.info("Worker process shutting down")

@beat_init.connect
def init_scheduler(sender=None, **kwargs):
    """Initialize the scheduler."""
    logger.info("Initializing beat scheduler")
    
    # Any beat-specific initialization can go here
    logger.info("Beat scheduler initialized")

@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    """Setup direct queue after worker initialized."""
    logger.info(f"Setting up direct queue for worker {sender}")
    app.conf.task_queues = [
        Queue('celery', Exchange('celery'), routing_key='celery'),
        Queue('direct', Exchange('direct'), routing_key='direct'),
    ]
