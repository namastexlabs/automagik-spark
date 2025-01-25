"""Tests for flow components functionality."""

import pytest
from unittest.mock import AsyncMock, patch

from automagik.core.flows.manager import FlowManager

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return FlowManager(session)

@pytest.mark.asyncio
async def test_get_flow_components(flow_manager):
    """Test getting flow components."""
    flow_id = "test-flow-1"
    flow_data = {
        "data": {
            "nodes": [
                {
                    "id": "comp-1",
                    "data": {
                        "node": {"name": "Input"},
                        "type": "ChatInput"
                    }
                },
                {
                    "id": "comp-2",
                    "data": {
                        "node": {"name": "Output"},
                        "type": "ChatOutput"
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
        components = await flow_manager.get_flow_components(flow_id)
        assert len(components) == 2
        assert components[0]["id"] == "comp-1"
        assert components[0]["type"] == "ChatInput"
        assert components[1]["id"] == "comp-2"
        assert components[1]["type"] == "ChatOutput"
