
"""Test LangFlow manager functionality."""

import json
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import HTTPError, Request, Response

from automagik.core.workflows.remote import LangFlowManager

@pytest.fixture
async def langflow_manager(session):
    """Create a LangFlow manager."""
    async with LangFlowManager(session) as manager:
        yield manager


