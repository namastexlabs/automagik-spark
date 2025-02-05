"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from automagik.core.workflows.sync import WorkflowSync
from automagik.core.database.models import Task, Workflow

@pytest.fixture
async def workflow_sync(session: AsyncSession) -> WorkflowSync:
    """Create a workflow sync."""
    return WorkflowSync(session)

@pytest.fixture
async def test_flow(session: AsyncSession) -> Workflow:
    """Create a test flow."""
    flow = Workflow(
        id=uuid4(),
        name="Test Flow",
        source="test",
        remote_flow_id="test_id",
        input_component="input_node",
        output_component="output_node",
        data={"test": "data"},
        flow_version=1,
        is_component=False,
        gradient=False,
        liked=False
    )
    session.add(flow)
    await session.commit()
    await session.refresh(flow)
    return flow

@pytest.fixture
async def test_task(session: AsyncSession, test_flow: Workflow) -> Task:
    """Create a test task."""
    task = Task(
        id=uuid4(),
        workflow_id=test_flow.id,
        status="pending",
        input_data={"input": "test input"},
        created_at=datetime.utcnow()
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

@pytest.mark.asyncio
async def test_successful_flow_execution(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test successful flow execution."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status = AsyncMock()
    mock_response.json = AsyncMock(return_value={"outputs": [{"outputs": "success"}]})
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client
    workflow_sync._base_url = "http://test"

    # Execute workflow
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"input": "test input"}
    )

    # Verify result
    assert result == {"outputs": [{"outputs": "success"}]}
    assert test_task.status == "completed"
    assert test_task.output_data == "success"
    assert test_task.started_at is not None
    assert test_task.error is None

@pytest.mark.asyncio
async def test_failed_flow_execution(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test failed flow execution."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_response.text = "API Error Details"
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client
    workflow_sync._base_url = "http://test"

    # Execute workflow
    with pytest.raises(Exception):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"input": "test input"}
        )

    # Verify task status
    assert test_task.status == "failed"  # Status should be failed since error was raised
    assert test_task.started_at is not None
    assert test_task.error == "API Error"  # Error should be set from the exception

@pytest.mark.asyncio
async def test_input_value_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that input_value is correctly passed through the execution chain."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status = AsyncMock()
    mock_response.json = AsyncMock(return_value={"outputs": [{"outputs": "specific test value"}]})
    mock_client.post = AsyncMock(return_value=mock_response)
    workflow_sync._client = mock_client
    workflow_sync._base_url = "http://test"

    # Execute workflow with specific input_value
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"input_value": "specific test value"}
    )

    # Verify the API was called with correct payload
    assert mock_client.post.call_args is not None
    url, kwargs = mock_client.post.call_args
    assert kwargs["json"]["input_value"] == "specific test value"
    assert kwargs["json"]["output_type"] == "debug"
    assert kwargs["json"]["input_type"] == "chat"
    assert kwargs["json"]["tweaks"] == {
        test_flow.input_component: {},
        test_flow.output_component: {}
    }

    # Verify task was updated correctly
    assert test_task.status == "completed"
    assert test_task.output_data == "specific test value"
    assert test_task.input_data == {"input_value": "specific test value"}
