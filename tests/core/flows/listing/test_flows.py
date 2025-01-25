"""Tests for flow listing functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from automagik.core.flows.manager import FlowManager
from automagik.core.database.models import Flow

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
async def test_list_remote_flows(flow_manager, mock_folders, mock_flows):
    """Test listing remote flows from LangFlow."""
    # Create response for /folders/
    folders_response = AsyncMock()
    folders_response.raise_for_status = AsyncMock()
    folders_response.json = AsyncMock(return_value=mock_folders)

    # Create response for /flows/
    flows_response = AsyncMock()
    flows_response.raise_for_status = AsyncMock()
    flows_response.json = AsyncMock(return_value=mock_flows)

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
        flows = await flow_manager.list_remote_flows()
        
        # Verify we have exactly two folders as per mock data
        assert len(mock_folders) == 2
        folder_ids = {f["id"] for f in mock_folders}
        folder_names = {f["name"] for f in mock_folders}
        assert "My Projects" in folder_names
        assert "pastinha_automatica" in folder_names
        
        # Verify flows are properly filtered and grouped
        for folder_name, folder_flows in flows.items():
            # All flows in this folder should have a folder_id that exists
            for flow in folder_flows:
                assert flow.get("folder_id") in folder_ids, f"Flow {flow['id']} has invalid folder_id"

        # Count total flows and verify distribution
        total_flows = sum(len(folder_flows) for folder_flows in flows.values())
        assert total_flows == 2, f"Expected 2 total flows, got {total_flows}"
        
        # Verify each folder has exactly one flow
        for folder_name, folder_flows in flows.items():
            assert len(folder_flows) == 1, f"Folder {folder_name} should have exactly 1 flow, got {len(folder_flows)}"

        # Verify example flows (flows with non-existent folder_ids) are excluded
        all_flows = [flow for flows_list in flows.values() for flow in flows_list]
        for flow in mock_flows:
            if flow.get("folder_id") not in folder_ids:
                assert flow not in all_flows, f"Example flow {flow['id']} was not filtered out"
