"""Integration tests for LangFlow API connectivity."""

import os
import pytest
from typing import AsyncGenerator, Optional
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.flows.remote import RemoteFlowManager
from automagik.core.config import LANGFLOW_API_URL, LANGFLOW_API_KEY

pytestmark = pytest.mark.integration

def requires_langflow_api():
    """Skip test if LangFlow API is not configured."""
    if not LANGFLOW_API_URL or not LANGFLOW_API_KEY:
        pytest.skip("LangFlow API URL and API Key must be configured")

@pytest.fixture
async def remote_flow_manager(session: AsyncSession) -> AsyncGenerator[RemoteFlowManager, None]:
    """Create a RemoteFlowManager instance for integration tests."""
    requires_langflow_api()
    manager = RemoteFlowManager(session)
    yield manager

@pytest.mark.asyncio
async def test_langflow_api_connectivity(remote_flow_manager: RemoteFlowManager):
    """Test basic connectivity to LangFlow API."""
    async with remote_flow_manager:
        # Test connection by listing folders
        response = await remote_flow_manager.client.get("/folders/")
        response.raise_for_status()
        folders = response.json()
        assert isinstance(folders, list), "Expected folders endpoint to return a list"

@pytest.mark.asyncio
async def test_langflow_api_flow_operations(remote_flow_manager: RemoteFlowManager):
    """Test flow-related operations with LangFlow API."""
    async with remote_flow_manager:
        # List flows
        flows_by_folder = await remote_flow_manager.list_remote_flows()
        assert isinstance(flows_by_folder, dict)
        
        # Verify folder structure
        for folder_name, flows in flows_by_folder.items():
            assert isinstance(folder_name, str)
            assert isinstance(flows, list)
            
            # Verify flow structure
            for flow in flows:
                assert "id" in flow
                assert "name" in flow
                assert "data" in flow
                assert "folder_id" in flow

@pytest.mark.asyncio
async def test_langflow_api_error_handling(remote_flow_manager: RemoteFlowManager):
    """Test error handling with LangFlow API."""
    async with remote_flow_manager:
        # Test invalid endpoint
        with pytest.raises(httpx.HTTPError):
            response = await remote_flow_manager.client.get("/nonexistent/")
            response.raise_for_status()
        
        # Test invalid API key
        original_key = remote_flow_manager.client.headers.get("x-api-key")
        remote_flow_manager.client.headers["x-api-key"] = "invalid_key"
        
        with pytest.raises(httpx.HTTPError):
            response = await remote_flow_manager.client.get("/flows/")
            response.raise_for_status()
        
        # Restore original key
        if original_key:
            remote_flow_manager.client.headers["x-api-key"] = original_key

@pytest.mark.asyncio
async def test_langflow_api_performance(remote_flow_manager: RemoteFlowManager):
    """Test API response times and performance."""
    async with remote_flow_manager:
        # Test response time for flows endpoint
        async with httpx.AsyncClient(timeout=5.0) as client:
            start_time = pytest.importorskip("time").time()
            response = await remote_flow_manager.client.get("/flows/")
            response.raise_for_status()
            end_time = pytest.importorskip("time").time()
            
            # Verify response time is under 2 seconds
            assert end_time - start_time < 2.0, "API response took too long"
            
            # Verify response size is reasonable
            response_size = len(response.content)
            assert response_size < 10 * 1024 * 1024, "API response too large"  # 10MB limit
