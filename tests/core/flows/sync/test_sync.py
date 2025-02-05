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


@pytest.fixture
def mock_flow():
    """Create a mock flow."""
    return {
        "id": str(uuid4()),
        "name": "Test Flow",
        "description": "Test flow description",
        "data": {
            "nodes": [
                {
                    "id": "node1",
                    "type": "input",
                    "data": {"value": "test"}
                }
            ],
            "edges": []
        }
    }


@pytest.fixture
def mock_http_client():
    """Create a mock HTTP client."""
    return AsyncClientMock()  # Use AsyncClientMock from conftest.py


@pytest.mark.asyncio
async def test_sync_flow(mock_httpx_client, flow_manager):
    """Test syncing a flow from LangFlow API."""
    # Load mock data
    with open("tests/mock_data/flows/flow.json") as f:
        mock_data = json.load(f)

    # Set a proper UUID for the flow
    flow_id = str(uuid4())
    mock_data["id"] = flow_id

    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None

    mock_httpx_client.get.return_value = mock_response

    # Test syncing a flow
    async with flow_manager:
        workflow = await flow_manager.sync_flow(flow_id)

        assert workflow is not None
        assert str(workflow.remote_flow_id) == flow_id
        assert workflow.name == mock_data["name"]
        assert workflow.description == mock_data["description"]
        assert workflow.data == mock_data["data"]

        # Verify the API call
        mock_httpx_client.get.assert_called_once_with(f"/api/v1/flows/{flow_id}")


@pytest.mark.asyncio
async def test_sync_flow_invalid_component(mock_httpx_client, flow_manager):
    """Test flow sync with invalid component."""
    # Load mock data
    with open("tests/mock_data/flows/flow.json") as f:
        mock_data = json.load(f)

    # Set a proper UUID for the flow
    flow_id = str(uuid4())
    mock_data["id"] = flow_id

    # Add invalid component
    mock_data["data"]["nodes"].append({
        "id": "node2",
        "type": "invalid_type",
        "data": {
            "node": {
                "type": "invalid_type"
            }
        }
    })

    # Mock the flow response
    mock_flow_response = MagicMock()
    mock_flow_response.status_code = 200
    mock_flow_response.json.return_value = mock_data
    mock_flow_response.raise_for_status.return_value = None

    mock_httpx_client.get.return_value = mock_flow_response

    # Test syncing a flow with invalid component
    async with flow_manager:
        workflow = await flow_manager.sync_flow(flow_id)
        
        # Verify the workflow was created but marked the component as invalid
        assert workflow is not None
        assert str(workflow.remote_flow_id) == flow_id
        assert any(node["type"] == "invalid_type" for node in workflow.data["nodes"])


@pytest.mark.asyncio
@patch('automagik.core.workflows.remote.LANGFLOW_API_URL', 'http://test/api/v1')
async def test_sync_flow_http_error(mock_httpx_client, flow_manager):
    """Test flow sync with HTTP error."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPError("Test error")
    mock_httpx_client.get.return_value = mock_response

    # Test syncing a flow
    async with flow_manager:
        result = await flow_manager.sync_flow("nonexistent-id")
        assert result is None
