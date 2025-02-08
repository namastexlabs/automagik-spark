"""Test flow sync functionality."""

import json
from uuid import uuid4
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy import select
import httpx
from cryptography.fernet import Fernet

from automagik.core.workflows import WorkflowManager
from automagik.core.database.models import Workflow, WorkflowSource


def create_mock_response(data, url="http://test/api/v1/flows/test"):
    """Create a mock response object that behaves like httpx.Response."""
    request = httpx.Request("GET", url)
    return httpx.Response(
        status_code=200,
        content=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        request=request
    )


@pytest.mark.asyncio
async def test_sync_new_workflow(session):
    """Test syncing a new workflow."""
    # Create workflow source with encrypted key
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_key = f.encrypt(b"test_key")
    
    source = WorkflowSource(
        source_type="langflow",
        url="http://test1.langflow.org",
        encrypted_api_key=encrypted_key.decode(),
        status="active"
    )
    session.add(source)
    await session.commit()
    
    # Mock LangFlow response
    flow_id = str(uuid4())
    mock_flow_data = {
        "id": flow_id,
        "name": "Test Flow",
        "description": "Test Description",
        "data": {"test": "data"},
        "folder_id": "folder1",
        "folder_name": "Test Folder",
        "icon": "test-icon",
        "icon_bg_color": "#000000",
        "gradient": True,
        "liked": True,
        "tags": ["test"]
    }
    
    # Mock HTTP client
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=create_mock_response(mock_flow_data))
    mock_client.aclose = AsyncMock()
    
    # Mock components response
    mock_components = [
        {"id": "input1", "type": "input", "name": "Input"},
        {"id": "output1", "type": "output", "name": "Output"}
    ]
    
    with patch("httpx.AsyncClient", return_value=mock_client), \
         patch.object(WorkflowSource, "decrypt_api_key", return_value="test_key"):
        flow_manager = WorkflowManager(session)
        # Mock get_flow_components
        flow_manager.get_flow_components = AsyncMock(return_value=mock_components)
        
        # Sync flow
        async with flow_manager as manager:
            result = await manager.sync_flow(flow_id, "input1", "output1", source_url=source.url)
            assert result is not None
            assert isinstance(result, Workflow)
        
        # Verify flow was created
        stmt = select(Workflow).where(Workflow.id == result.id)
        result = await session.execute(stmt)
        flow = result.scalar_one()
        assert flow is not None
        assert flow.name == "Test Flow"
        assert flow.remote_flow_id == flow_id
        assert flow.flow_version == 1


@pytest.mark.asyncio
async def test_sync_existing_flow(session):
    """Test syncing an existing flow."""
    # Create workflow source with encrypted key
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_key = f.encrypt(b"test_key")
    
    source = WorkflowSource(
        source_type="langflow",
        url="http://test2.langflow.org",
        encrypted_api_key=encrypted_key.decode(),
        status="active"
    )
    session.add(source)
    await session.commit()
    
    # Create existing flow
    flow_id = str(uuid4())
    existing_flow = Workflow(
        id=uuid4(),
        name="Old Name",
        description="Old Description",
        data={"old": "data"},
        source="langflow",
        remote_flow_id=flow_id,
        flow_version=1,
        input_component="old_input",
        output_component="old_output"
    )
    session.add(existing_flow)
    await session.commit()
    existing_id = existing_flow.id
    
    # Mock LangFlow response with updated data
    mock_flow_data = {
        "id": flow_id,
        "name": "Updated Flow",
        "description": "Updated Description",
        "data": {"updated": "data"},
        "folder_id": "folder1",
        "folder_name": "Test Folder",
        "icon": "test-icon",
        "icon_bg_color": "#000000",
        "gradient": True,
        "liked": True,
        "tags": ["test"]
    }
    
    # Mock HTTP client
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=create_mock_response(mock_flow_data))
    mock_client.aclose = AsyncMock()
    
    # Mock components response
    mock_components = [
        {"id": "new_input", "type": "input", "name": "Input"},
        {"id": "new_output", "type": "output", "name": "Output"}
    ]
    
    with patch("httpx.AsyncClient", return_value=mock_client), \
         patch.object(WorkflowSource, "decrypt_api_key", return_value="test_key"):
        flow_manager = WorkflowManager(session)
        # Mock get_flow_components
        flow_manager.get_flow_components = AsyncMock(return_value=mock_components)
        
        # Sync flow
        async with flow_manager as manager:
            result = await manager.sync_flow(flow_id, "new_input", "new_output", source_url=source.url)
            assert result is not None
            assert isinstance(result, Workflow)
            assert result.id == existing_id
        
        # Verify flow was updated
        stmt = select(Workflow).where(Workflow.id == existing_id)
        result = await session.execute(stmt)
        flow = result.scalar_one()
        assert flow is not None
        assert flow.name == "Updated Flow"
        assert flow.description == "Updated Description"
        assert flow.data == {"updated": "data"}
        assert flow.folder_id == "folder1"
        assert flow.folder_name == "Test Folder"
        assert flow.icon == "test-icon"
        assert flow.icon_bg_color == "#000000"
        assert flow.gradient is True


@pytest.mark.asyncio
async def test_sync_workflow_with_invalid_components(session):
    """Test syncing a workflow with invalid component IDs."""
    # Create workflow source with encrypted key
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_key = f.encrypt(b"test_key")
    
    source = WorkflowSource(
        source_type="langflow",
        url="http://test3.langflow.org",
        encrypted_api_key=encrypted_key.decode(),
        status="active"
    )
    session.add(source)
    await session.commit()
    
    # Mock LangFlow response
    flow_id = str(uuid4())
    mock_flow_data = {
        "id": flow_id,
        "name": "Test Flow",
        "description": "Test Description",
        "data": {"test": "data"}
    }
    
    # Mock HTTP client
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=create_mock_response(mock_flow_data))
    mock_client.aclose = AsyncMock()
    
    # Mock components response with different components
    mock_components = [
        {"id": "other_input", "type": "input", "name": "Input"},
        {"id": "other_output", "type": "output", "name": "Output"}
    ]
    
    with patch("httpx.AsyncClient", return_value=mock_client), \
         patch.object(WorkflowSource, "decrypt_api_key", return_value="test_key"):
        flow_manager = WorkflowManager(session)
        # Mock get_flow_components
        flow_manager.get_flow_components = AsyncMock(return_value=mock_components)
        
        # Try to sync flow with invalid component IDs
        async with flow_manager as manager:
            result = await manager.sync_flow(flow_id, "invalid_input", "invalid_output", source_url=source.url)
            assert result is not None  # Flow should still be created
            assert isinstance(result, Workflow)
            
        # Verify flow was created with invalid components
        stmt = select(Workflow).where(Workflow.id == result.id)
        result = await session.execute(stmt)
        flow = result.scalar_one()
        assert flow is not None
        assert flow.input_component == "invalid_input"  # Should keep the specified components
        assert flow.output_component == "invalid_output"
