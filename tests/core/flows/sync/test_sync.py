"""Tests for flow sync functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

from automagik.core.workflows.manager import WorkflowManager

@pytest.fixture
def flow_manager(session):
    """Create a WorkflowManager instance."""
    return WorkflowManager(session)

@pytest.fixture
def mock_data_dir():
    """Get the mock data directory."""
    return Path(__file__).parent.parent.parent.parent / "mock_data" / "flows"

@pytest.fixture
def mock_flows(mock_data_dir):
    """Load mock flow data."""
    with open(mock_data_dir / "flows.json") as f:
        return json.load(f)

@pytest.mark.asyncio
async def test_sync_flow_success(flow_manager, mock_flows):
    """Test successful flow sync."""
    # Use the first flow from our mock data
    flow_data = mock_flows[0]
    flow_id = flow_data["id"]
    
    # Get input/output components from the flow
    nodes = flow_data["data"]["nodes"]
    input_node = next(n for n in nodes if "ChatInput" in n["data"]["type"])
    output_node = next(n for n in nodes if "ChatOutput" in n["data"]["type"])
    input_component = input_node["id"]
    output_component = output_node["id"]

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value=flow_data)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
        assert isinstance(flow_uuid, UUID)

        # Verify flow was created correctly
        flow = await flow_manager.get_flow(flow_uuid)
        assert flow is not None
        assert flow.name == flow_data["name"]
        assert flow.description == flow_data.get("description", "")
        assert flow.source == "langflow"
        assert flow.remote_flow_id == flow_id
        assert flow.input_component == input_component
        assert flow.output_component == output_component
        assert flow.folder_id == flow_data.get("folder_id")
        assert flow.folder_name == flow_data.get("folder_name")

@pytest.mark.asyncio
async def test_sync_flow_invalid_component(flow_manager, mock_flows):
    """Test flow sync with invalid component IDs."""
    # Use the first flow from our mock data but with invalid components
    flow_data = mock_flows[0]
    flow_id = flow_data["id"]
    input_component = "invalid-input"
    output_component = "invalid-output"

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value=flow_data)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
        assert isinstance(flow_uuid, UUID)  # Flow should be created even with invalid components
        
        # Verify flow was created with invalid components
        flow = await flow_manager.get_flow(flow_uuid)
        assert flow is not None
        assert flow.input_component == input_component
        assert flow.output_component == output_component

@pytest.mark.asyncio
async def test_sync_flow_http_error(flow_manager):
    """Test flow sync with HTTP error."""
    flow_id = "test-flow-1"
    input_component = "comp-1"
    output_component = "comp-2"

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=Exception("HTTP Error"))
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
        assert flow_uuid is None
