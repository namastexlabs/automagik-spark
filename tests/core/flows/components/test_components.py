"""Tests for flow components functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from automagik.core.flows.manager import FlowManager

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return FlowManager(session)

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
    # Use the first flow from our mock data
    flow_data = mock_flows[0]
    flow_id = flow_data["id"]

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value=flow_data)

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        components = await flow_manager.get_flow_components(flow_id)

        # Verify components match our mock data
        nodes = flow_data["data"]["nodes"]
        assert len(components) == len(nodes)
        
        for node, component in zip(nodes, components):
            assert component["id"] == node["id"]
            assert component["type"] == node["data"]["type"]
            assert component["name"] == node["data"].get("display_name", "Unknown")
