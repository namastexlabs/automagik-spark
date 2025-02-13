
"""
CLI commands package.

This package contains all the CLI commands for the automagik application.
"""

from .api import api_group
from .db import db_group
from .worker import worker_group
from .workflow import workflow_group
from .schedule import schedule_group
from .task import task_group
from . import source

__all__ = [
    "api_group",
    "db_group",
    "worker_group",
    "workflow_group",
    "schedule_group",
    "task_group",
    "source",
]


