"""Tests for flow listing functionality."""

import json
import pytest
from pathlib import Path
from sqlalchemy import delete
from sqlalchemy import select
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from automagik.core.workflows.manager import WorkflowManager
from automagik.core.workflows.remote import LangFlowManager
from automagik.core.database.models import Workflow


@pytest.fixture
def flow_manager(session):
    """Create a FlowManager instance."""
    return WorkflowManager(session)


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


@pytest.fixture
def mock_httpx_client(monkeypatch):
    """Mock httpx client."""
    mock_client = AsyncMock()
    mock_client.aclose = AsyncMock()
    
    def mock_client_factory(*args, **kwargs):
        return mock_client
    
    monkeypatch.setattr("httpx.AsyncClient", mock_client_factory)
    return mock_client


@pytest.mark.asyncio
async def test_list_flows_empty(flow_manager):
    """Test listing flows when there are none."""
    mock_result = MagicMock()
    mock_result.unique.return_value.scalars.return_value.all.return_value = []

    # Mock the session execute
    flow_manager.session.execute = AsyncMock(return_value=mock_result)

    flows = await flow_manager.list_workflows()
    assert flows == []


@pytest.mark.asyncio
async def test_list_flows_with_data(flow_manager, mock_flows):
    """Test listing flows with data."""
    # Create test workflows
    workflows = []
    for flow_data in mock_flows:
        workflow = Workflow(
            id=flow_data["id"],
            name=flow_data["name"],
            description=flow_data.get("description"),
            source=flow_data.get("source", "langflow"),
            remote_flow_id=flow_data["id"],
            data=flow_data.get("data", {}),
        )
        workflows.append(workflow)

    mock_result = MagicMock()
    mock_result.unique.return_value.scalars.return_value.all.return_value = workflows

    # Mock the session execute
    flow_manager.session.execute = AsyncMock(return_value=mock_result)

    flows = await flow_manager.list_workflows()
    assert len(flows) == len(mock_flows)
    for flow, mock_flow in zip(flows, mock_flows):
        assert str(flow.id) == mock_flow["id"]
        assert flow.name == mock_flow["name"]


@pytest.mark.asyncio
async def test_list_remote_flows(mock_httpx_client, flow_manager):
    """Test listing remote flows from LangFlow API."""
    # Load mock data
    with open("tests/mock_data/flows/flow.json") as f:
        mock_data = json.load(f)

    # Set a proper UUID for the flow
    flow_id = str(uuid4())
    mock_data["id"] = flow_id

    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_data]
    mock_response.raise_for_status.return_value = None

    mock_httpx_client.get.return_value = mock_response

    # Test listing remote flows
    async with flow_manager:
        flows = await flow_manager.list_remote_flows()
        assert len(flows) == 1
        assert flows[0]["id"] == flow_id
        assert flows[0]["name"] == mock_data["name"]
        assert flows[0]["description"] == mock_data["description"]


@pytest.mark.asyncio
async def test_synced_vs_remote_flows(mock_httpx_client, flow_manager):
    """Test comparing synced vs remote flows."""
    # Load mock data
    with open("tests/mock_data/flows/flow.json") as f:
        mock_data = json.load(f)

    # Set a proper UUID for the flow
    flow_id = str(uuid4())
    mock_data["id"] = flow_id

    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_data]
    mock_response.raise_for_status.return_value = None

    mock_httpx_client.get.return_value = mock_response

    # Test listing remote flows
    async with flow_manager:
        flows = await flow_manager.list_remote_flows()
        assert len(flows) == 1
        assert flows[0]["id"] == flow_id
        assert flows[0]["name"] == mock_data["name"]
        assert flows[0]["description"] == mock_data["description"]


@pytest.mark.asyncio
@patch('automagik.core.workflows.remote.LANGFLOW_API_KEY', 'test_key')
async def test_remote_flow_manager_client_config():
    """Test LangFlow manager client configuration."""
    session = AsyncMock()
    manager = LangFlowManager(session)
    assert manager.api_key == 'test_key'


@pytest.mark.asyncio
@patch('automagik.core.workflows.remote.LANGFLOW_API_URL', 'http://test.example.com')
async def test_remote_flow_manager_client_lifecycle(mock_httpx_client):
    """Test LangFlow manager client lifecycle."""
    session = AsyncMock()
    manager = LangFlowManager(session)

    async with manager:
        assert manager.client is not None
        assert not mock_httpx_client.aclose.called

    assert mock_httpx_client.aclose.called
