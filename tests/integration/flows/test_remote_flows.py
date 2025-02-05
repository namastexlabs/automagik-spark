"""Integration tests for remote flow functionality."""

import os
import pytest
import httpx
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock, patch

from automagik.core.workflows.remote import LangFlowManager
from automagik.core.config import LANGFLOW_API_URL, LANGFLOW_API_KEY

pytestmark = pytest.mark.integration

def requires_api_config(func):
    """Decorator to skip tests if API configuration is not available."""
    return pytest.mark.skipif(
        not (LANGFLOW_API_URL and LANGFLOW_API_KEY),
        reason="LangFlow API configuration (URL and API key) not found"
    )(func)

@pytest.mark.asyncio
@requires_api_config
async def test_remote_api_error_handling(session):
    """Test error handling with remote API."""
    # Test invalid API key
    async with httpx.AsyncClient(
        base_url=LANGFLOW_API_URL,
        headers={"accept": "application/json", "x-api-key": "invalid-key"},
        verify=False
    ) as client:
        with pytest.raises(httpx.HTTPStatusError):
            response = await client.get("/api/v1/flows/")
            response.raise_for_status()

@pytest.mark.asyncio
@requires_api_config
async def test_remote_api_connection(session):
    """Test basic API connection."""
    async with LangFlowManager(session) as remote:
        flows = await remote.list_remote_flows()
        assert flows is not None

@pytest.mark.asyncio
@requires_api_config
async def test_remote_flow_operations(session):
    """Test full flow operations with remote API."""
    # Mock flow data
    mock_flow_data = {
        "id": "test-flow-id",
        "name": "Test Flow",
        "description": "A test flow",
        "data": {
            "nodes": [
                {
                    "type": "test-component",
                    "id": "test-node-id",
                    "data": {
                        "description": "A test component",
                        "display_name": "Test Component"
                    }
                }
            ]
        }
    }

    # Mock component data
    mock_component_data = {
        "id": "test-component",
        "type": "test",
        "name": "Test Component",
        "description": "A test component"
    }

    # Mock responses
    mock_flow_response = MagicMock()
    mock_flow_response.raise_for_status = MagicMock()
    mock_flow_response.json = MagicMock(return_value=mock_flow_data)

    mock_component_response = MagicMock()
    mock_component_response.raise_for_status = MagicMock()
    mock_component_response.json = MagicMock(return_value=mock_component_data)

    mock_list_response = MagicMock()
    mock_list_response.raise_for_status = MagicMock()
    mock_list_response.json = MagicMock(return_value=[mock_flow_data])

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[mock_list_response, mock_flow_response, mock_component_response])
    mock_client.post = AsyncMock()
    mock_client.aclose = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        async with LangFlowManager(session) as remote:
            # List flows
            flows = await remote.list_remote_flows()
            assert isinstance(flows, list)
            assert len(flows) > 0

            # Get a specific flow if any exist
            flow_id = flows[0]["id"]
            result = await remote.sync_flow(flow_id)
            assert result is not None
            assert "flow" in result
            assert "components" in result
            assert result["flow"]["id"] == flow_id

@pytest.mark.asyncio
@requires_api_config
async def test_remote_folder_operations(session):
    """Test folder operations with remote API."""
    async with LangFlowManager(session) as remote:
        # Create a test folder
        folder_name = f"test_folder_{uuid4()}"
        folder_data = await remote.create_folder(folder_name)
        assert folder_data is not None
        assert folder_data["name"] == folder_name

        # Clean up - delete the test folder
        response = await remote.client.delete(f"/api/v1/folders/{folder_data['id']}")
        response.raise_for_status()
