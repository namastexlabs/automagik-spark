"""Celery tasks and signal handlers."""

import logging
from celery.signals import (
    worker_process_init,
    worker_process_shutdown,
    beat_init,
    celeryd_after_setup,
)
from kombu.messaging import Exchange, Queue
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..database.models import Schedule
from ..database.session import get_sync_session
from .celery_app import app
from rich.console import Console
from rich.table import Table

logger = logging.getLogger(__name__)


def print_active_schedules():
    """Print active schedules and their next run times."""
    with get_sync_session() as session:
        # Get all active schedules with eager loading of workflow
        query = (
            select(Schedule)
            .where(Schedule.status == "active")
            .options(joinedload(Schedule.workflow))
        )
        result = session.execute(query)
        schedules = result.scalars().all()

        console = Console()

        if not schedules:
            console.print("\n[yellow]No active schedules found[/yellow]")
            return

        # Create table
        table = Table(
            title="Active Schedules", caption=f"Total: {len(schedules)} schedule(s)"
        )
        table.add_column("ID", justify="left", style="bright_blue", no_wrap=True)
        table.add_column("Workflow", justify="left", style="green")
        table.add_column("Type", justify="left", style="magenta")
        table.add_column("Next Run", justify="left", style="cyan")
        table.add_column("Input", justify="left", style="yellow")

        for schedule in schedules:
            next_run = (
                schedule.next_run_at.strftime("%Y-%m-%d %H:%M:%S UTC")
                if schedule.next_run_at
                else "Not scheduled"
            )
            workflow_name = schedule.workflow.name if schedule.workflow else "Unknown"
            table.add_row(
                str(schedule.id),
                workflow_name,
                schedule.schedule_type,
                next_run,
                (
                    str(schedule.input_data)[:50] + "..."
                    if len(str(schedule.input_data)) > 50
                    else str(schedule.input_data)
                ),
            )

        console.print("\n")
        console.print(table)
        console.print("\n")


@worker_process_init.connect
def configure_worker(**kwargs):
    """Configure worker process on initialization."""
    logger.info("Initializing worker process")

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Print active schedules
    print_active_schedules()

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

    # Print active schedules
    print_active_schedules()

    # Any beat-specific initialization can go here
    logger.info("Beat scheduler initialized")


@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    """Setup direct queue after worker initialized."""
    logger.info(f"Setting up direct queue for worker {sender}")
    app.conf.task_queues = [
        Queue("celery", Exchange("celery"), routing_key="celery"),
        Queue("direct", Exchange("direct"), routing_key="direct"),
    ]
