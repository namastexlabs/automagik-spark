"""Tests for the FlowManager class."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime, timezone

from automagik.core.flows.manager import FlowManager
from automagik.core.database.models import Flow, Schedule

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return FlowManager(session)

@pytest.fixture
async def sample_flow(session):
    """Create a sample flow in the database."""
    flow = Flow(
        id=uuid4(),
        name="Test Flow",
        description="A test flow",
        data={"nodes": []},
        source="langflow",
        source_id="test-flow-1",
        flow_version=1,
        input_component="input-1",
        output_component="output-1"
    )
    session.add(flow)
    await session.commit()
    await session.refresh(flow)
    return flow

@pytest.mark.asyncio
async def test_list_flows_empty(flow_manager):
    """Test listing flows when there are none."""
    flows = await flow_manager.list_flows()
    assert len(flows) == 0

@pytest.mark.asyncio
async def test_list_flows_with_data(flow_manager, sample_flow):
    """Test listing flows with data."""
    flows = await flow_manager.list_flows()
    assert len(flows) == 1
    assert flows[0].id == sample_flow.id
    assert flows[0].name == "Test Flow"

@pytest.mark.asyncio
async def test_list_remote_flows(flow_manager):
    """Test listing remote flows from LangFlow."""
    mock_flows = {
        "My Projects": [
            {
                "id": "flow-1",
                "name": "Flow 1",
                "description": "Test flow 1",
                "folder_id": "folder-1"
            }
        ]
    }
    
    folders_data = [{"id": "folder-1", "name": "My Projects"}]
    flows_data = [
        {
            "id": "flow-1",
            "name": "Flow 1",
            "description": "Test flow 1",
            "folder_id": "folder-1"
        }
    ]

    async def mock_get(url):
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        if url == "/folders/":
            mock_response.json = AsyncMock(return_value=folders_data)
        elif url == "/flows/":
            mock_response.json = AsyncMock(return_value=flows_data)
        return mock_response

    mock_client = AsyncMock()
    mock_client.get = mock_get
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        flows = await flow_manager.list_remote_flows()
        assert flows == mock_flows

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
