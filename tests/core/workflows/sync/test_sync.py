
"""Test flow synchronization functionality."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import httpx
import json

from automagik_spark.core.database.models import Workflow
from automagik_spark.core.workflows.remote import LangFlowManager
from automagik_spark.core.workflows.manager import WorkflowManager
from conftest import AsyncClientMock  

@pytest.fixture
def flow_manager(session):
    """Create a workflow manager for testing."""
    return WorkflowManager(session)


