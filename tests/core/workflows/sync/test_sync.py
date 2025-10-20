"""Test flow synchronization functionality."""

import pytest


from automagik_spark.core.workflows.manager import WorkflowManager


@pytest.fixture
def flow_manager(session):
    """Create a workflow manager for testing."""
    return WorkflowManager(session)
