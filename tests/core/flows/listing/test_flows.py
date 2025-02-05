"""Tests for flow listing functionality."""

import json
import pytest
from pathlib import Path
from sqlalchemy import delete
from sqlalchemy import select
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from automagik.core.workflows.manager import WorkflowManager, LangFlowManager
from automagik.core.database.models import Workflow

@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return WorkflowManager(session)

@pytest.fixture
def remote_flow_manager(session):
    """Create a RemoteFlowManager instance."""
    return LangFlowManager(session)

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
    workflow = Workflow(
        id=uuid4(),
        remote_flow_id="test-flow-1",
        name="Test Flow",
        description="Test flow for testing",
        source="langflow",
        data={"nodes": []}
    )
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow

@pytest.fixture(autouse=True)
async def cleanup_flows(session):
    """Clean up flows before each test."""
    await session.execute(delete(Workflow))
    await session.commit()

@pytest.mark.asyncio
async def test_list_flows_empty(flow_manager):
    """Test listing flows when no flows exist."""
    result = MagicMock()
    result.scalars.return_value.all.return_value = []
    flow_manager.session.execute = AsyncMock(return_value=result)
    
    flows = await flow_manager.list_flows()
    assert flows == []

@pytest.mark.asyncio
async def test_list_flows_with_data(flow_manager, mock_flows):
    """Test listing flows with data."""
    # Create mock workflow objects
    workflows = []
    for flow_data in mock_flows:
        workflow = Workflow(
            id=flow_data["id"],
            name=flow_data["name"],
            description=flow_data.get("description"),
            data=flow_data["data"]
        )
        workflows.append(workflow)
    
    result = MagicMock()
    result.scalars.return_value.all.return_value = workflows
    flow_manager.session.execute = AsyncMock(return_value=result)
    
    flows = await flow_manager.list_flows()
    assert len(flows) == len(mock_flows)
    for flow, mock_flow in zip(flows, mock_flows):
        assert flow.id == mock_flow["id"]
        assert flow.name == mock_flow["name"]
        assert flow.description == mock_flow.get("description")
        assert flow.data == mock_flow["data"]

@pytest.mark.asyncio
async def test_list_remote_flows(flow_manager, mock_flows):
    """Test listing remote flows."""
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value={"flows": mock_flows})
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()
    
    async with patch("httpx.AsyncClient", return_value=mock_client) as mock_client_class:
        async with flow_manager.langflow:
            remote_flows = await flow_manager.langflow.list_remote_flows()
            
            # Verify client was used correctly
            mock_client.get.assert_called_once_with("/api/v1/flows")
            
            # Verify flows were returned
            assert len(remote_flows) == len(mock_flows)
            for remote_flow, mock_flow in zip(remote_flows, mock_flows):
                assert remote_flow["id"] == mock_flow["id"]
                assert remote_flow["name"] == mock_flow["name"]

@pytest.mark.asyncio
async def test_synced_vs_remote_flows(flow_manager, mock_flows):
    """Test comparing synced flows with remote flows."""
    # Mock remote flows
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value={"flows": mock_flows})
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()
    
    # Mock local flows
    local_flows = []
    for flow_data in mock_flows[:2]:  # Only first 2 flows are synced
        workflow = Workflow(
            id=flow_data["id"],
            name=flow_data["name"],
            description=flow_data.get("description"),
            data=flow_data["data"],
            remote_flow_id=flow_data["id"]
        )
        local_flows.append(workflow)
    
    result = MagicMock()
    result.scalars.return_value.all.return_value = local_flows
    flow_manager.session.execute = AsyncMock(return_value=result)
    
    async with patch("httpx.AsyncClient", return_value=mock_client) as mock_client_class:
        async with flow_manager.langflow:
            synced_flows = await flow_manager.list_flows()
            remote_flows = await flow_manager.langflow.list_remote_flows()
            
            # Verify synced flows
            assert len(synced_flows) == 2
            for synced_flow, mock_flow in zip(synced_flows, mock_flows[:2]):
                assert synced_flow.remote_flow_id == mock_flow["id"]
            
            # Verify remote flows
            assert len(remote_flows) == len(mock_flows)

@pytest.mark.asyncio
async def test_remote_flow_manager_client_config():
    """Test LangFlow manager client configuration."""
    api_url = "http://test.example.com"
    api_key = "test_key"
    
    manager = LangFlowManager(api_url=api_url, api_key=api_key)
    assert manager.api_url == api_url
    assert manager.api_key == api_key
    assert manager.client is None

@pytest.mark.asyncio
async def test_remote_flow_manager_client_lifecycle():
    """Test LangFlow manager client lifecycle."""
    manager = LangFlowManager(api_url="http://test.example.com")
    assert manager.client is None
    
    async with manager:
        assert manager.client is not None
        assert not manager.client.is_closed
        
    assert manager.client is None
