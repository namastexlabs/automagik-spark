"""Test LangFlow manager functionality."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import HTTPError, Request, Response

from automagik.core.workflows.remote import LangFlowManager

@pytest.fixture
async def langflow_manager(session):
    """Create a LangFlow manager."""
    async with LangFlowManager(session) as manager:
        yield manager

def create_mock_response(status_code: int, json_data: dict) -> Response:
    """Create a mock httpx.Response object."""
    mock_request = Request("GET", "https://example.com")
    return Response(
        status_code=status_code,
        json=lambda: json_data,
        request=mock_request
    )

@pytest.mark.asyncio
async def test_list_remote_flows(langflow_manager):
    """Test listing remote flows."""
    mock_flows = {
        "flows": [
            {
                "id": "flow1",
                "name": "Flow 1",
                "description": "Test Flow 1"
            },
            {
                "id": "flow2",
                "name": "Flow 2",
                "description": "Test Flow 2"
            }
        ]
    }

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_flows
    mock_response.raise_for_status = MagicMock()
    langflow_manager.client.get = AsyncMock(return_value=mock_response)

    flows = await langflow_manager.list_remote_flows()
    assert flows == mock_flows
    langflow_manager.client.get.assert_called_once_with("/api/v1/flows/")

    # Test error handling
    langflow_manager.client.get = AsyncMock(side_effect=HTTPError("Test error"))
    with pytest.raises(HTTPError):
        await langflow_manager.list_remote_flows()

@pytest.mark.asyncio
async def test_sync_flow(langflow_manager):
    """Test syncing a flow."""
    flow_id = "test_flow"
    mock_flow = {
        "id": flow_id,
        "name": "Test Flow",
        "description": "Test Description",
        "data": {
            "nodes": [
                {
                    "id": "node1",
                    "data": {
                        "node": {
                            "name": "Node 1",
                            "type": "input"
                        }
                    }
                }
            ]
        }
    }

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_flow
    mock_response.raise_for_status = MagicMock()
    langflow_manager.client.get = AsyncMock(return_value=mock_response)

    # Test with default parameters
    result = await langflow_manager.sync_flow(flow_id)
    assert result is not None
    assert result["flow"] == mock_flow
    assert len(result["components"]) == 1
    assert result["components"][0]["id"] == "node1"
    langflow_manager.client.get.assert_called_once_with(f"/api/v1/flows/{flow_id}")

    # Test with custom name and description
    result = await langflow_manager.sync_flow(
        flow_id,
        name="New Name",
        description="New Description"
    )
    assert result["flow"]["name"] == "New Name"
    assert result["flow"]["description"] == "New Description"

    # Test with provided components
    custom_components = [{"id": "custom1", "name": "Custom 1"}]
    result = await langflow_manager.sync_flow(
        flow_id,
        components=custom_components
    )
    assert result["components"] == custom_components

    # Test error handling
    langflow_manager.client.get = AsyncMock(side_effect=HTTPError("Test error"))
    result = await langflow_manager.sync_flow(flow_id)
    assert result is None

@pytest.mark.asyncio
async def test_get_flow_components(langflow_manager):
    """Test getting flow components."""
    flow_data = {
        "data": {
            "nodes": [
                {
                    "id": "node1",
                    "data": {
                        "node": {
                            "name": "Node 1",
                            "type": "input"
                        }
                    }
                },
                {
                    "id": "node2",
                    "data": {
                        "node": {
                            "name": "Node 2",
                            "type": "process"
                        }
                    }
                }
            ]
        }
    }

    # Test successful extraction
    components = await langflow_manager.get_flow_components(flow_data)
    assert len(components) == 2
    assert components[0]["id"] == "node1"
    assert components[1]["id"] == "node2"

    # Test with empty flow data
    components = await langflow_manager.get_flow_components({})
    assert components == []

    # Test with invalid flow data
    with pytest.raises(Exception):
        await langflow_manager.get_flow_components(None)

@pytest.mark.asyncio
async def test_create_folder(langflow_manager):
    """Test creating a folder."""
    folder_name = "Test Folder"
    mock_folder = {
        "id": "folder1",
        "name": folder_name
    }

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_folder
    mock_response.raise_for_status = MagicMock()
    langflow_manager.client.post = AsyncMock(return_value=mock_response)

    folder = await langflow_manager.create_folder(folder_name)
    assert folder == mock_folder
    langflow_manager.client.post.assert_called_once_with(
        "/api/v1/folders/",
        json={"name": folder_name}
    )

    # Test error handling
    langflow_manager.client.post = AsyncMock(side_effect=HTTPError("Test error"))
    with pytest.raises(HTTPError):
        await langflow_manager.create_folder(folder_name)

@pytest.mark.asyncio
async def test_context_manager(session):
    """Test context manager functionality."""
    # Test successful context
    async with LangFlowManager(session) as manager:
        assert manager.client is not None
        assert manager.session == session

    # Test client is closed
    assert manager.client is None  # Client should be closed and set to None

    # Test error in context
    with pytest.raises(Exception):
        async with LangFlowManager(session) as manager:
            raise Exception("Test error")
    assert manager.client is None  # Client should be closed and set to None
