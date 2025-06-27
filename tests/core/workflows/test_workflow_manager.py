
"""Test workflow manager functionality."""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
import asyncio
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from automagik_spark.core.workflows.manager import WorkflowManager
from automagik_spark.core.database.models import Workflow, Task, TaskLog, Schedule, WorkflowComponent, WorkflowSource

@pytest.fixture
async def workflow_manager(session: AsyncSession) -> WorkflowManager:
    """Create a workflow manager."""
    async with WorkflowManager(session) as manager:
        yield manager


