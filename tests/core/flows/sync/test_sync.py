"""Tests for flow synchronization functionality."""

import pytest
from unittest.mock import AsyncMock, patch
from uuid import UUID

from automagik.core.flows.manager import FlowManager

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return FlowManager(session)

@pytest.mark.asyncio
async def test_sync_flow_success(flow_manager):
    """Test successful flow sync."""
    flow_id = "test-flow-1"
    input_component = "comp-1"
    output_component = "comp-2"
    
    flow_data = {
        "name": "Test Flow",
        "description": "A test flow",
        "data": {
            "nodes": [
                {
                    "id": "comp-1",
                    "data": {
                        "node": {
                            "name": "Input",
                            "template": {"input": "string"}
                        },
                        "type": "ChatInput"
                    }
                },
                {
                    "id": "comp-2",
                    "data": {
                        "node": {
                            "name": "Output",
                            "template": {"output": "string"}
                        },
                        "type": "ChatOutput"
                    }
                }
            ]
        },
        "folder_id": "folder-1",
        "folder_name": "My Projects",
        "icon": "chat",
        "icon_bg_color": "#123456",
        "gradient": True,
        "liked": False,
        "tags": ["test"]
    }

    mock_response = AsyncMock()
    mock_response.raise_for_status = AsyncMock()
    mock_response.json = AsyncMock(return_value=flow_data)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
        assert isinstance(flow_uuid, UUID)

        # Verify flow was created correctly
        flow = await flow_manager.get_flow(flow_uuid)
        assert flow is not None
        assert flow.name == "Test Flow"
        assert flow.description == "A test flow"
        assert flow.source == "langflow"
        assert flow.source_id == flow_id
        assert flow.input_component == input_component
        assert flow.output_component == output_component
        assert flow.folder_id == "folder-1"
        assert flow.folder_name == "My Projects"
        assert flow.icon == "chat"
        assert flow.icon_bg_color == "#123456"
        assert flow.gradient is True
        assert flow.liked is False
        assert flow.tags == ["test"]

        # Verify components were created correctly
        assert len(flow.components) == 2
        input_comp = next(c for c in flow.components if c.component_id == input_component)
        output_comp = next(c for c in flow.components if c.component_id == output_component)
        
        assert input_comp.type == "ChatInput"
        assert input_comp.is_input is True
        assert input_comp.is_output is False
        assert input_comp.tweakable_params == ["input"]

        assert output_comp.type == "ChatOutput"
        assert output_comp.is_input is False
        assert output_comp.is_output is True
        assert output_comp.tweakable_params == ["output"]

@pytest.mark.asyncio
async def test_sync_flow_invalid_component(flow_manager):
    """Test flow sync with invalid component IDs."""
    flow_id = "test-flow-1"
    input_component = "invalid-input"
    output_component = "invalid-output"
    
    flow_data = {
        "name": "Test Flow",
        "description": "A test flow",
        "data": {
            "nodes": [
                {
                    "id": "comp-1",
                    "data": {
                        "node": {"name": "Input"},
                        "type": "ChatInput"
                    }
                }
            ]
        }
    }

    mock_response = AsyncMock()
    mock_response.raise_for_status = AsyncMock()
    mock_response.json = AsyncMock(return_value=flow_data)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
        assert flow_uuid is not None  # Flow should still be created even with invalid components

        # Verify flow was created with the invalid components
        flow = await flow_manager.get_flow(flow_uuid)
        assert flow is not None
        assert flow.input_component == input_component
        assert flow.output_component == output_component

@pytest.mark.asyncio
async def test_sync_flow_http_error(flow_manager):
    """Test flow sync with HTTP error."""
    flow_id = "invalid-flow"
    input_component = "comp-1"
    output_component = "comp-2"

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=Exception("HTTP Error"))
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
        assert flow_uuid is None  # Should return None on error
