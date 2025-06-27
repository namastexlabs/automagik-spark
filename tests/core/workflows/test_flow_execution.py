"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
import httpx
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from automagik_spark.core.workflows.sync import WorkflowSync
from automagik_spark.core.database.models import Task, Workflow, TaskLog

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
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow
        result = await sync.execute_workflow(
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
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect error
        with pytest.raises(httpx.HTTPStatusError):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        # Verify error handling
        assert test_task.status == "failed"
        assert test_task.error is not None
        assert test_task.started_at is not None
        assert test_task.finished_at is not None

@pytest.mark.asyncio
async def test_input_value_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test input value handling."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = {"result": "success"}
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Test with different input types
        await sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="string input"
        )
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
    mock_manager.run_flow.side_effect = httpx.NetworkError("Connection failed")
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect error
        with pytest.raises(httpx.NetworkError):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        # Verify error handling
        assert test_task.status == "failed"
        assert "Connection failed" in test_task.error

@pytest.mark.asyncio
async def test_invalid_input_data(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test execution with invalid input data."""
    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.run_flow.side_effect = ValueError("Invalid input")
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow with invalid input
        with pytest.raises(ValueError):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data=None
            )

        # Verify error handling
        assert test_task.status == "failed"
        assert "Invalid input" in test_task.error

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
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect timeout
        with pytest.raises(httpx.TimeoutException):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        # Verify error handling
        assert test_task.status == "failed"
        assert "Request timed out" in test_task.error

@pytest.mark.asyncio
async def test_missing_components(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test execution with missing input/output components."""
    # Remove components
    test_flow.input_component = None
    test_flow.output_component = None
    await session.commit()

    # Mock the manager
    mock_manager = AsyncMock()
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect error
        with pytest.raises(ValueError, match="Missing input/output components"):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        # Verify error handling
        assert test_task.status == "failed"
        assert "Missing input/output components" in test_task.error

@pytest.mark.asyncio
async def test_malformed_response(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test handling of malformed response."""
    # Mock the manager to return invalid JSON
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = object()  # Un-serializable object
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect JSON error
        with pytest.raises(TypeError):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        # Verify error handling
        assert test_task.status == "failed"
        assert test_task.error is not None

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
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager

    # Verify close was called
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
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect error
        with pytest.raises(Exception):
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        # Verify error log was created
        error_log = await session.execute(
            select(TaskLog).where(TaskLog.task_id == test_task.id)
        )
        error_log = error_log.scalar_one()
        assert error_log.level == "error"
        assert "Test error" in error_log.message
        assert "Traceback" in error_log.message

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
    mock_manager.run_flow.side_effect = httpx.HTTPStatusError(
        "Unauthorized",
        request=MagicMock(),
        response=MagicMock(status_code=401, text="Invalid API key")
    )
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Execute workflow and expect auth error
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await sync.execute_workflow(
                workflow=test_flow,
                task=test_task,
                input_data="test input"
            )

        assert exc_info.value.response.status_code == 401
        assert test_task.status == "failed"
        assert "Invalid API key" in test_task.error

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
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Test with integer input
        await sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data=123
        )
        mock_manager.run_flow.assert_called_once()

@pytest.mark.asyncio
async def test_manager_initialization(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that manager is properly initialized when using context manager."""
    mock_manager = AsyncMock()
    mock_manager.run_flow.return_value = {"result": "success"}
    mock_manager.close = AsyncMock()

    async with workflow_sync as sync:
        sync._manager = mock_manager
        # Manager should be initialized
        assert sync._manager is not None
        assert sync._initialized is True
        result = await sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )
        assert result is not None

@pytest.mark.asyncio
async def test_manager_not_initialized_error(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that using WorkflowSync without context manager raises appropriate error."""
    # Don't use context manager, should raise error
    with pytest.raises(RuntimeError, match="Manager not initialized"):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data="test input"
        )


