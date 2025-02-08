"""Tests for flow listing functionality."""

import json
import pytest
from pathlib import Path
from sqlalchemy import delete
from sqlalchemy import select
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from automagik.core.workflows.manager import WorkflowManager
from automagik.core.workflows.remote import LangFlowManager
from automagik.core.database.models import Workflow, WorkflowSource


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

