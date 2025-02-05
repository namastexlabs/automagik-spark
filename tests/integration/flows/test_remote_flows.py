"""Integration tests for remote flow functionality."""

import os
import pytest
import httpx
from uuid import uuid4

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
async def test_remote_api_error_handling(session):
    """Test error handling with remote API."""
    # Test invalid API key
    async with httpx.AsyncClient(
        base_url=LANGFLOW_API_URL,
        headers={"accept": "application/json", "x-api-key": "invalid-key"},
        verify=False
    ) as client:
        with pytest.raises(httpx.HTTPStatusError):
            response = await client.get("/flows/")
            response.raise_for_status()

@pytest.mark.asyncio
@requires_api_config
async def test_remote_api_connection(session):
    """Test that we can connect to the remote API."""
    async with LangFlowManager(session) as remote:
        # Test basic connection
        response = await remote.client.get("/health-check")
        response.raise_for_status()
        assert response.status_code == 200

@pytest.mark.asyncio
@requires_api_config
async def test_remote_flow_operations(session):
    """Test full flow operations with remote API."""
    async with LangFlowManager(session) as remote:
        # List flows
        flows = await remote.list_remote_flows()
        assert isinstance(flows, dict)
        
        # Get a specific flow if any exist
        if flows:
            folder_name = next(iter(flows))
            flow_list = flows[folder_name]
            if flow_list:
                flow = flow_list[0]
                flow_id = flow.get("id")
                if flow_id:
                    # Test flow details endpoint
                    response = await remote.client.get(f"/flows/{flow_id}")
                    response.raise_for_status()
                    flow_details = response.json()
                    assert flow_details["id"] == flow_id

@pytest.mark.asyncio
@requires_api_config
async def test_remote_folder_operations(session):
    """Test folder operations with remote API."""
    async with LangFlowManager(session) as remote:
        # Create a test folder
        folder_name = f"test_folder_{uuid4()}"
        response = await remote.client.post("/folders/", json={"name": folder_name})
        response.raise_for_status()
        folder_data = response.json()
        assert folder_data["name"] == folder_name

        # Clean up - delete the test folder
        response = await remote.client.delete(f"/folders/{folder_data['id']}")
        response.raise_for_status()
