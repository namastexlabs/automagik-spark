"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.flows.task import TaskManager
from automagik.core.database.models import Task, Flow

@pytest.fixture
async def task_manager(session: AsyncSession) -> TaskManager:
    """Create a task manager."""
    return TaskManager(session)

@pytest.fixture
async def test_flow(session: AsyncSession) -> Flow:
    """Create a test flow."""
    flow = Flow(
        id=uuid4(),
        name="Test Flow",
        source="test",
        source_id=str(uuid4()),
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

@pytest.mark.asyncio
async def test_successful_flow_execution(
    session: AsyncSession,
    task_manager: TaskManager,
    test_flow: Flow
):
    """Test successful flow execution."""
    # Mock the execute_flow method
    mock_output = {"result": "success"}
    async def mock_execute(*args, **kwargs):
        task = kwargs['task']
        task.status = "completed"
        task.started_at = datetime.utcnow()
        task.finished_at = datetime.utcnow()
        task.output_data = mock_output
        await session.commit()
        return mock_output

    with patch('automagik.core.flows.sync.FlowSync.execute_flow', new=mock_execute):
        # Run flow
        task_id = await task_manager.run_flow(test_flow.id, {"input": "test"})
        
        # Verify task was created and completed successfully
        assert task_id is not None
        task = await task_manager.get_task(str(task_id))
        assert task is not None
        assert task.status == "completed"
        assert task.output_data == mock_output
        assert task.error is None
        assert task.started_at is not None
        assert task.finished_at is not None

@pytest.mark.asyncio
async def test_failed_flow_execution(
    session: AsyncSession,
    task_manager: TaskManager,
    test_flow: Flow
):
    """Test failed flow execution."""
    # Mock the execute_flow method to raise an exception
    error_message = "Test execution error"
    async def mock_execute(*args, **kwargs):
        task = kwargs['task']
        task.status = "failed"
        task.error = error_message
        task.finished_at = datetime.utcnow()
        await session.commit()
        raise Exception(error_message)

    with patch('automagik.core.flows.sync.FlowSync.execute_flow', new=mock_execute):
        # Run flow
        task_id = await task_manager.run_flow(test_flow.id, {"input": "test"})
        
        # Verify task was created and marked as failed
        assert task_id is None  # Should return None on failure
        
        # Get the most recent task
        tasks = await task_manager.list_tasks(flow_id=str(test_flow.id), limit=1)
        assert len(tasks) == 1
        task = tasks[0]
        
        assert task.status == "failed"
        assert task.error == error_message
        assert task.output_data is None
        assert task.started_at is None  # Failed before execution started
        assert task.finished_at is not None

@pytest.mark.asyncio
async def test_flow_not_found(
    session: AsyncSession,
    task_manager: TaskManager
):
    """Test execution with non-existent flow."""
    # Try to run non-existent flow
    task_id = await task_manager.run_flow(uuid4(), {"input": "test"})
    
    # Verify no task was created
    assert task_id is None

@pytest.mark.asyncio
async def test_task_status_not_overwritten(
    session: AsyncSession,
    task_manager: TaskManager,
    test_flow: Flow
):
    """Test that task status set by execute_flow is not overwritten."""
    # Mock execute_flow to simulate setting task status
    async def mock_execute_flow(*args, **kwargs):
        task = kwargs['task']
        task.status = "completed"
        task.output_data = {"result": "success"}
        task.started_at = datetime.utcnow()
        task.finished_at = datetime.utcnow()
        await session.commit()
        return task.output_data

    with patch('automagik.core.flows.sync.FlowSync.execute_flow', new=mock_execute_flow):
        # Run flow
        task_id = await task_manager.run_flow(test_flow.id, {"input": "test"})
        
        # Verify task status was preserved
        assert task_id is not None
        task = await task_manager.get_task(str(task_id))
        assert task is not None
        assert task.status == "completed"
        assert task.output_data == {"result": "success"}
