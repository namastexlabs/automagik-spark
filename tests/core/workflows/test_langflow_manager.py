
"""Test LangFlow manager functionality."""

import pytest

from automagik_spark.core.workflows.remote import LangFlowManager

@pytest.fixture
async def langflow_manager(session):
    """Create a LangFlow manager."""
    async with LangFlowManager(session) as manager:
        yield manager


