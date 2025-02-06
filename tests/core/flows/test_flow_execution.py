"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
import httpx
import json

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
        input_data="test input",
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
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = {"result": "success"}
    workflow_sync._manager = mock_manager

    # Execute workflow
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data="test input"
    )

    # Verify result
    assert result == {"result": "success"}
    assert test_task.status == "completed"
    assert json.loads(test_task.output_data) == {"result": "success"}
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
    error_msg = "Internal Server Error"
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = httpx.HTTPStatusError(
        error_msg,
        request=MagicMock(),
        response=MagicMock(status_code=500, text=error_msg)
    )
    workflow_sync._manager = mock_manager

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    # Verify task status and error message
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert error_msg in str(test_task.error)

@pytest.mark.asyncio
async def test_input_value_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test input value handling."""
    # Create a mock manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = {"result": "success"}
    workflow_sync._manager = mock_manager

    # Test with JSON string input
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data='{"key": "value"}'
    )

    # Verify result
    assert result == {"result": "success"}
    assert test_task.status == "completed"

@pytest.mark.asyncio
async def test_network_error_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of network errors during execution."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = httpx.ConnectError("Failed to connect")
    workflow_sync._manager = mock_manager

    with pytest.raises(httpx.ConnectError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Failed to connect" in str(test_task.error)

@pytest.mark.asyncio
async def test_invalid_input_data(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test execution with invalid input data."""
    error_msg = "Invalid input data"
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = httpx.HTTPStatusError(
        error_msg,
        request=MagicMock(),
        response=MagicMock(status_code=400, text=error_msg)
    )
    workflow_sync._manager = mock_manager

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    # Verify task status and error message
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert error_msg in str(test_task.error)

@pytest.mark.asyncio
async def test_timeout_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of timeouts during execution."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = httpx.TimeoutException("Request timed out")
    workflow_sync._manager = mock_manager

    with pytest.raises(httpx.TimeoutException):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Request timed out" in str(test_task.error)

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

    with pytest.raises(ValueError, match="Missing input/output components"):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "Missing input/output components" in str(test_task.error)

@pytest.mark.asyncio
async def test_malformed_response(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of malformed response."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    workflow_sync._manager = mock_manager

    with pytest.raises(json.JSONDecodeError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    assert test_task.status == "failed"
    assert "Invalid JSON" in test_task.error

@pytest.mark.asyncio
async def test_client_close(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test client close."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = {"result": "success"}
    workflow_sync._manager = mock_manager

    async with workflow_sync:
        result = await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    mock_manager.close.assert_called_once()

@pytest.mark.asyncio
async def test_error_logging_with_traceback(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test error logging with traceback."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = Exception("Test error")
    workflow_sync._manager = mock_manager

    with pytest.raises(Exception):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )

    # Verify error logging
    result = await session.execute(
        select(TaskLog).where(TaskLog.task_id == test_task.id)
    )
    error_log = result.scalar_one()
    assert "Test error" in error_log.message
    assert "Traceback (most recent call last)" in error_log.message
    assert "execute_workflow" in error_log.message

@pytest.mark.asyncio
async def test_api_key_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that API key is properly handled."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.api_key = "test_key"
    workflow_sync._manager = mock_manager

    # Execute workflow
    mock_manager.run_flow.return_value = {"result": "success"}
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data="test input"
    )

    assert result == {"result": "success"}
    assert mock_manager.api_key == "test_key"

@pytest.mark.asyncio
async def test_input_data_formats(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test different input data formats."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = {"result": "success"}
    workflow_sync._manager = mock_manager

    # Test with empty message
    await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data=""
    )
    mock_manager.run_flow.assert_called_once()
    mock_manager.run_flow.reset_mock()

    # Test with non-string message
    await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data=123
    )
    mock_manager.run_flow.assert_called_once()
