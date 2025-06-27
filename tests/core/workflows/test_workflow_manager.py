
"""Test workflow manager functionality."""

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from automagik_spark.core.workflows.manager import WorkflowManager

@pytest.fixture
async def workflow_manager(session: AsyncSession) -> WorkflowManager:
    """Create a workflow manager."""
    async with WorkflowManager(session) as manager:
        yield manager


