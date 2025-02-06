"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from automagik.core.workflows.sync import WorkflowSync
from automagik.core.database.models import Task, Workflow, TaskLog

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
    mock_response = MagicMock()  # Use MagicMock for response to support status_code comparison
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}  # Match the new response format
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"message": "test input"}  # Match the expected input format
    )

    # Verify result
    assert result == {"result": "success"}
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
    mock_response = MagicMock()  # Use MagicMock for response
    mock_response.status_code = 500
    mock_response.text = "API Error"
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow
    with pytest.raises(httpx.HTTPStatusError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}  # Match the expected input format
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "API Error" in test_task.error

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
    mock_response = MagicMock()  # Use MagicMock for response
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "specific test value"}  # Match the new response format
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow with specific input_value
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"message": "specific test value"}  # Match the expected input format
    )

    # Verify result
    assert result == {"result": "specific test value"}
    assert test_task.status == "completed"
    assert test_task.output_data == "specific test value"

@pytest.mark.asyncio
async def test_network_error_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of network errors during execution."""
    # Mock the HTTP client to raise a connection error
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.ConnectError("Failed to connect")
    workflow_sync._client = mock_client

    # Execute workflow
    with pytest.raises(httpx.ConnectError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Failed to connect" in test_task.error

@pytest.mark.asyncio
async def test_invalid_input_data(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test execution with invalid input data."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Invalid input data"
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow with invalid input
    with pytest.raises(httpx.HTTPStatusError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"invalid": "data"}
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Invalid input data" in test_task.error

@pytest.mark.asyncio
async def test_timeout_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of timeouts during execution."""
    # Mock the HTTP client to raise a timeout
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.TimeoutException("Request timed out")
    workflow_sync._client = mock_client

    # Execute workflow
    with pytest.raises(httpx.TimeoutException):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Request timed out" in test_task.error

@pytest.mark.asyncio
async def test_missing_components(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test execution with missing input/output components."""
    # Remove input/output components from flow
    test_flow.input_component = None
    test_flow.output_component = None
    await session.commit()

    # Execute workflow
    with pytest.raises(ValueError, match="Missing input/output components"):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Missing input/output components" in test_task.error

@pytest.mark.asyncio
async def test_malformed_response(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of malformed response from API."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow
    with pytest.raises(ValueError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Invalid JSON" in test_task.error

@pytest.mark.asyncio
async def test_client_close(
    session: AsyncSession,
    workflow_sync: WorkflowSync
):
    """Test that client is properly closed."""
    # Create a mock client
    mock_client = AsyncMock()
    workflow_sync._client = mock_client

    # Close the client
    await workflow_sync.close()

    # Verify client was closed and reset
    mock_client.aclose.assert_called_once()
    assert workflow_sync._client is None

@pytest.mark.asyncio
async def test_error_logging_with_traceback(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that errors are logged with traceback."""
    # Mock the HTTP client to raise an exception with a traceback
    mock_client = AsyncMock()
    mock_client.post.side_effect = ValueError("Test error")
    workflow_sync._client = mock_client

    # Execute workflow
    with pytest.raises(ValueError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}
        )

    # Verify error log was created with traceback
    result = await session.execute(
        select(TaskLog).where(TaskLog.task_id == test_task.id)
    )
    error_log = result.scalar_one()
    assert error_log.level == "error"
    assert "Test error" in error_log.message
    assert "File" in error_log.message  # Check for file path in traceback
    assert "line" in error_log.message  # Check for line number in traceback
    assert "in execute_workflow" in error_log.message  # Check for function name

@pytest.mark.asyncio
async def test_input_data_formats(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test different input data formats."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Test with empty message
    await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={}
    )
    # Verify empty message is handled
    mock_client.post.assert_called_with(
        f"/api/v1/run/{test_flow.remote_flow_id}",
        json={"inputs": {"text": ""}, "tweaks": {
            test_flow.input_component: {"input": ""},
            test_flow.output_component: {}
        }},
        timeout=600
    )

    # Test with non-string message
    await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"message": 123}
    )
    # Verify non-string message is converted to string
    mock_client.post.assert_called_with(
        f"/api/v1/run/{test_flow.remote_flow_id}",
        json={"inputs": {"text": "123"}, "tweaks": {
            test_flow.input_component: {"input": "123"},
            test_flow.output_component: {}
        }},
        timeout=600
    )

@pytest.mark.asyncio
@patch('automagik.core.workflows.sync.LANGFLOW_API_KEY', 'test_key')
async def test_api_key_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that API key is properly handled."""
    # Get client to initialize it with API key
    client = await workflow_sync._get_client()

    # Verify API key is in headers
    assert client.headers.get('x-api-key') == 'test_key'

    # Mock response for execution
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    client.post = AsyncMock(return_value=mock_response)

    # Execute workflow
    await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"message": "test"}
    )

    # Verify API key was used in request
    client.post.assert_called_once()
    assert client.headers.get('x-api-key') == 'test_key'
