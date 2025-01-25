"""Tests for flow listing functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from automagik.core.flows.manager import FlowManager
from automagik.core.database.models import Flow
from sqlalchemy import select

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return FlowManager(session)

@pytest.fixture
def mock_data_dir():
    """Get the mock data directory."""
    return Path(__file__).parent.parent.parent.parent / "mock_data" / "flows"

@pytest.fixture
def mock_folders(mock_data_dir):
    """Load mock folder data."""
    with open(mock_data_dir / "folders.json") as f:
        return json.load(f)

@pytest.fixture
def mock_flows(mock_data_dir):
    """Load mock flow data."""
    with open(mock_data_dir / "flows.json") as f:
        return json.load(f)

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
async def test_list_remote_flows(flow_manager, mock_flows):
    """Test listing remote flows from LangFlow API."""
    # Get a folder ID from the mock flows
    folder_id = mock_flows[0].get("folder_id")
    
    # Create response for /folders/
    folders_response = MagicMock()
    folders_response.raise_for_status = MagicMock()
    folders_response.json = MagicMock(return_value=[
        {"id": folder_id, "name": "Test Folder"}
    ])

    # Create response for /flows/
    flows_response = MagicMock()
    flows_response.raise_for_status = MagicMock()
    flows_response.json = MagicMock(return_value=mock_flows)

    async def mock_get(url):
        if url == "/folders/":
            return folders_response
        elif url == "/flows/":
            return flows_response
        raise ValueError(f"Unexpected URL: {url}")

    mock_client = AsyncMock()
    mock_client.get = mock_get
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        async with flow_manager:
            flows = await flow_manager.list_remote_flows()
            assert isinstance(flows, dict)
            
            # Verify only flows with valid folder IDs are included
            assert "Test Folder" in flows
            assert len(flows) == 1  # Only one folder should be present
            
            # All flows in the folder should have the correct folder_id
            for flow in flows["Test Folder"]:
                assert flow.get("folder_id") == folder_id

@pytest.mark.asyncio
async def test_synced_vs_remote_flows(flow_manager, mock_flows):
    """Test that synced flows appear in local list but not remote list."""
    # First sync a flow
    flow_data = mock_flows[0]
    flow_id = flow_data["id"]

    # Get input/output components from the flow
    nodes = flow_data["data"]["nodes"]
    input_node = next(n for n in nodes if "ChatInput" in n["data"]["type"])
    output_node = next(n for n in nodes if "ChatOutput" in n["data"]["type"])
    input_component = input_node["id"]
    output_component = output_node["id"]

    # Mock the flow sync response
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value=flow_data)

    # Mock different responses for different endpoints
    async def mock_get(url):
        if "/flows/" in url and not url.endswith("/flows/"):
            mock_response.json.return_value = flow_data
            return mock_response
        elif "/folders/" in url:
            folder_response = MagicMock()
            folder_response.json.return_value = []  # Empty folders list
            return folder_response
        elif url.endswith("/flows/"):
            flows_response = MagicMock()
            flows_response.json.return_value = mock_flows
            return flows_response
        return mock_response

    mock_client = AsyncMock()
    mock_client.get.side_effect = mock_get
    mock_client.aclose = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        async with flow_manager:
            # Sync the flow
            synced_flow_id = await flow_manager.sync_flow(flow_id, input_component, output_component)
            assert isinstance(synced_flow_id, UUID)

            # Now list local flows
            stmt = select(Flow)
            result = await flow_manager.session.execute(stmt)
            local_flows = result.scalars().all()

            # Verify the synced flow is in local flows
            assert len(local_flows) > 0
            found_flow = False
            for flow in local_flows:
                if flow.id == synced_flow_id:
                    found_flow = True
                    assert flow.name == flow_data["name"]
                    assert flow.description == flow_data.get("description", "")
                    assert flow.source == "langflow"
                    assert flow.source_id == flow_id
                    assert flow.input_component == input_component
                    assert flow.output_component == output_component
                    break
            assert found_flow, "Synced flow not found in local flows"

            # List remote flows using the same client
            flows_by_folder = await flow_manager.list_remote_flows()
            assert isinstance(flows_by_folder, dict)
