"""
CLI commands package.

This package contains all the CLI commands for the automagik application.
"""

from .flow import flow_group
from .schedule import schedule_group
from .worker import worker
from .task import task_group
from .db import db_group

__all__ = [
    'flow_group',
    'schedule_group',
    'task_group',
    'worker',
    'db_group',
]
