"""Test flow deletion functionality."""

import pytest
from uuid import uuid4

from automagik.core.workflows import WorkflowManager
from automagik.core.database.models import Workflow, Task, Schedule, WorkflowComponent


@pytest.mark.asyncio
async def test_delete_flow_with_full_uuid(session):
    """Test deleting a flow using full UUID."""
    # Create a test flow
    flow_id = uuid4()
    flow = Workflow(
        id=flow_id,
        name="Test Flow",
        description="Test Description",
        source="test",
        remote_flow_id="test_id",
        input_component="input",
        output_component="output"
    )
    session.add(flow)
    await session.commit()
    
    # Create a flow manager
    flow_manager = WorkflowManager(session)
    
    # Delete flow using full UUID
    success = await flow_manager.delete_flow(str(flow_id))
    assert success is True
    
    # Verify flow is deleted
    result = await session.get(Workflow, flow_id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_flow_with_truncated_uuid(session):
    """Test deleting a flow using truncated UUID."""
    # Create a test flow
    flow_id = uuid4()
    flow = Workflow(
        id=flow_id,
        name="Test Flow",
        description="Test Description",
        source="test",
        remote_flow_id="test_id",
        input_component="input",
        output_component="output"
    )
    session.add(flow)
    await session.commit()
    
    # Create a flow manager
    flow_manager = WorkflowManager(session)
    
    # Delete flow using truncated UUID (first 8 chars)
    truncated_id = str(flow_id)[:8]
    success = await flow_manager.delete_flow(truncated_id)
    assert success is True
    
    # Verify flow is deleted
    result = await session.get(Workflow, flow_id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_flow_with_related_objects(session):
    """Test deleting a flow with related objects (tasks, schedules, components)."""
    # Create a test flow
    flow_id = uuid4()
    flow = Workflow(
        id=flow_id,
        name="Test Flow",
        description="Test Description",
        source="test",
        remote_flow_id="test_id",
        input_component="input",
        output_component="output"
    )
    session.add(flow)
    
    # Add related objects
    task = Task(
        id=uuid4(),
        flow_id=flow_id,
        status="completed",
        input_data={"test": "data"}
    )
    schedule = Schedule(
        id=uuid4(),
        flow_id=flow_id,
        schedule_type="interval",
        schedule_expr="5m"
    )
    component = WorkflowComponent(
        id=uuid4(),
        flow_id=flow_id,
        component_id="test-component",
        type="test"
    )
    
    session.add_all([task, schedule, component])
    await session.commit()
    
    # Create a flow manager
    flow_manager = WorkflowManager(session)
    
    # Delete flow
    success = await flow_manager.delete_flow(str(flow_id))
    assert success is True
    
    # Verify flow and related objects are deleted
    result = await session.get(Workflow, flow_id)
    assert result is None
    
    task_result = await session.get(Task, task.id)
    assert task_result is None
    
    schedule_result = await session.get(Schedule, schedule.id)
    assert schedule_result is None
    
    component_result = await session.get(WorkflowComponent, component.id)
    assert component_result is None


@pytest.mark.asyncio
async def test_delete_nonexistent_flow(session):
    """Test deleting a flow that doesn't exist."""
    flow_manager = WorkflowManager(session)
    
    # Try to delete non-existent flow
    success = await flow_manager.delete_flow(str(uuid4()))
    assert success is False


@pytest.mark.asyncio
async def test_delete_flow_invalid_uuid(session):
    """Test deleting a flow with invalid UUID format."""
    flow_manager = WorkflowManager(session)
    
    # Try to delete with invalid UUID format
    success = await flow_manager.delete_flow("not-a-uuid")
    assert success is False
