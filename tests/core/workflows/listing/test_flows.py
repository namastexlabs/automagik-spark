
"""Tests for flow listing functionality."""

import json
import pytest
from pathlib import Path

from automagik_spark.core.workflows.manager import WorkflowManager


@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return WorkflowManager(session)


@pytest.fixture
def mock_data_dir():
    """Get the mock data directory."""
    return Path(__file__).parent.parent.parent.parent / "mock_data" / "flows"


@pytest.fixture
def mock_folders(mock_data_dir):
    """Load mock folder data."""
    with open(mock_data_dir / "folders.json") as f:
        return json.load(f)


@pytest.fixture
def mock_flows(mock_data_dir):
    """Load mock flow data."""
    with open(mock_data_dir / "flows.json") as f:
        return json.load(f)



