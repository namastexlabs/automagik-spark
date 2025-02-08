"""Test flow synchronization functionality."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import httpx
import json

from automagik.core.database.models import Workflow
from automagik.core.workflows.remote import LangFlowManager
from automagik.core.workflows.manager import WorkflowManager
from conftest import AsyncClientMock  # Import AsyncClientMock from conftest.py


@pytest.fixture
def flow_manager(session):
    """Create a workflow manager for testing."""
    return WorkflowManager(session)
