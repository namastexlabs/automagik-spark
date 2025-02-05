"""Tests for flow components functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, call

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
async def test_get_flow_components(flow_manager, mock_flows):
    """Test getting flow components."""
    # Create a simple mock flow with known components
    flow_data = {
        "id": "test-flow-id",
        "data": {
            "nodes": [
                {
                    "type": "ChatInput",
                    "id": "ChatInput-1",
                },
                {
                    "type": "ChatOutput",
                    "id": "ChatOutput-1",
                },
                {
                    "type": "Prompt",
                    "id": "Prompt-1",
                }
            ]
        }
    }
    flow_id = flow_data["id"]

    # Mock response for flow data
    mock_flow_response = MagicMock()
    mock_flow_response.raise_for_status = MagicMock()
    mock_flow_response.json = MagicMock(return_value=flow_data)

    # Mock response for component data
    mock_component_response = MagicMock()
    mock_component_response.raise_for_status = MagicMock()
    mock_component_response.json = MagicMock(return_value={
        "id": "test-component",
        "type": "test",
        "name": "Test Component",
        "description": "A test component"
    })

    # Create responses for each component type
    mock_responses = [mock_flow_response]
    for _ in range(3):  # We have 3 components in our mock flow
        mock_responses.append(mock_component_response)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=mock_responses)
    mock_client.post = AsyncMock()
    mock_client.aclose = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        async with flow_manager.langflow:
            result = await flow_manager.langflow.sync_flow(flow_id)
            assert result is not None
            assert "flow" in result
            assert "components" in result
            
            components = result["components"]
            assert isinstance(components, list)
            assert len(components) == 3  # We should get 3 components
            for component in components:
                assert "id" in component
                assert "type" in component
                assert "name" in component
                assert "description" in component

            # Verify the client was used correctly - first call should be to get the flow
            assert mock_client.get.call_args_list[0] == call(f"/api/v1/flows/{flow_id}")
            
            # Verify subsequent calls are to get components
            component_types = {"ChatInput", "ChatOutput", "Prompt"}
            for call_args in mock_client.get.call_args_list[1:]:
                component_type = call_args[0][0].split("/")[-1]
                assert component_type in component_types
