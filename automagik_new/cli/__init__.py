"""
Command Line Interface

Provides the main CLI entry point and command groups.
"""

import click

from .commands.schedule import schedule_group
from .commands.worker import worker
from .commands.db import db_group

@click.group()
def cli():
    """Automagik CLI."""
    pass

cli.add_command(schedule_group)
cli.add_command(db_group)
cli.add_command(worker)
