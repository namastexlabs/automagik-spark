"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from automagik.core.flows.task import TaskManager
from automagik.core.database.models import Task, Flow
from automagik.core.flows.sync import FlowSync

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
    # Mock the execute_flow method of FlowSync
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
        task_id = await task_manager.run_flow(
            flow_id=test_flow.id,
            input_data={"input": "test input"}
        )
        assert task_id is not None
        
        task = await task_manager.get_task(str(task_id))
        assert task.status == "completed"
        assert task.output_data == mock_output
        assert task.started_at is not None
        assert task.finished_at is not None

@pytest.mark.asyncio
async def test_failed_flow_execution(
    session: AsyncSession,
    task_manager: TaskManager,
    test_flow: Flow
):
    """Test failed flow execution."""
    error_message = "Test error"
    async def mock_execute(*args, **kwargs):
        task = kwargs['task']
        task.status = "failed"
        task.error = error_message
        task.started_at = datetime.utcnow()
        task.finished_at = datetime.utcnow()
        await session.commit()
        raise Exception(error_message)

    with patch('automagik.core.flows.sync.FlowSync.execute_flow', new=mock_execute):
        # When a flow fails, run_flow returns None
        task_id = await task_manager.run_flow(
            flow_id=test_flow.id,
            input_data={"input": "test input"}
        )
        assert task_id is None
        
        # But the task should still be created and marked as failed
        result = await session.execute(
            select(Task).where(Task.flow_id == test_flow.id)
            .order_by(Task.created_at.desc())
        )
        task = result.scalar_one()
        assert task.status == "failed"
        assert task.error == error_message
        assert task.started_at is not None
        assert task.finished_at is not None

@pytest.mark.asyncio
async def test_flow_not_found(
    session: AsyncSession,
    task_manager: TaskManager
):
    """Test execution with non-existent flow."""
    task_id = await task_manager.run_flow(
        flow_id=uuid4(),
        input_data={"input": "test input"}
    )
    assert task_id is None

@pytest.mark.asyncio
async def test_task_status_not_overwritten(
    session: AsyncSession,
    task_manager: TaskManager,
    test_flow: Flow
):
    """Test that completed tasks are not re-run."""
    # Create a completed task
    task = Task(
        id=uuid4(),
        flow_id=test_flow.id,
        status="completed",
        input_data={"input": "test input"},
        output_data={"result": "success"},
        created_at=datetime.utcnow(),
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow()
    )
    session.add(task)
    await session.commit()
    
    async def mock_execute(*args, **kwargs):
        task = kwargs['task']
        task.status = "completed"
        task.output_data = {"result": "new success"}
        task.started_at = datetime.utcnow()
        task.finished_at = datetime.utcnow()
        await session.commit()
        return True
    
    # Try to run a new task for the same flow
    with patch('automagik.core.flows.sync.FlowSync.execute_flow', new=mock_execute):
        task_id = await task_manager.run_flow(
            flow_id=test_flow.id,
            input_data={"input": "test input"}
        )
    
        # A new task should be created
        assert task_id is not None
        new_task = await task_manager.get_task(str(task_id))
        assert new_task.id != task.id
        assert new_task.status == "completed"
        assert new_task.output_data == {"result": "new success"}
    
        # Original task should remain unchanged
        await session.refresh(task)
        assert task.status == "completed"
        assert task.output_data == {"result": "success"}

@pytest.mark.asyncio
async def test_input_value_handling(
    session: AsyncSession,
    task_manager: TaskManager,
    test_flow: Flow
):
    """Test that input_value is correctly passed through the execution chain."""
    test_input = "test message"
    expected_payload = {
        "input_value": test_input,
        "output_type": "debug",
        "input_type": "chat",
        "tweaks": {
            "input_node": {},
            "output_node": {}
        }
    }

    # Create a mock to capture the API call payload
    actual_payload = None
    async def mock_execute(*args, **kwargs):
        nonlocal actual_payload
        task = kwargs['task']
        flow = kwargs['flow']
        input_data = kwargs['input_data']
        
        # Build payload exactly as FlowSync does
        actual_payload = {
            "input_value": input_data.get("input_value", ""),
            "output_type": "debug",
            "input_type": "chat",
            "tweaks": {
                flow.input_component: {},
                flow.output_component: {}
            }
        }
        
        task.status = "completed"
        task.started_at = datetime.utcnow()
        task.finished_at = datetime.utcnow()
        task.output_data = {"result": "success"}
        await session.commit()
        return {"result": "success"}

    with patch('automagik.core.flows.sync.FlowSync.execute_flow', new=mock_execute):
        # Run flow with input_value
        task_id = await task_manager.run_flow(
            flow_id=test_flow.id,
            input_data={"input_value": test_input}
        )
        assert task_id is not None
        
        # Verify task was created and completed
        task = await task_manager.get_task(str(task_id))
        assert task.status == "completed"
        assert task.input_data == {"input_value": test_input}
        
        # Verify payload was constructed correctly
        assert actual_payload == expected_payload
