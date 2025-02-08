"""Test delete workflow functionality."""
import pytest
from uuid import uuid4
from datetime import datetime
import pytz
from sqlalchemy import select

from automagik.core.database.models import Task, Workflow, Schedule, WorkflowComponent, TaskLog
from automagik.core.workflows.manager import WorkflowManager


@pytest.fixture
async def workflow_manager(session):
    """Create a workflow manager for testing."""
    return WorkflowManager(session)


@pytest.mark.asyncio
async def test_delete_workflow_with_full_uuid(workflow_manager, session):
    """Test deleting a workflow using full UUID."""
    # Create test workflow
    workflow = Workflow(
        id=uuid4(),
        name="Test Flow",
        description="Test flow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)
    await session.commit()

    # Delete workflow
    deleted = await workflow_manager.delete_workflow(str(workflow.id))
    assert deleted is True

    # Verify workflow is deleted
    result = await session.execute(select(Workflow).where(Workflow.id == workflow.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_workflow_with_truncated_uuid(workflow_manager, session):
    """Test deleting a workflow using truncated UUID."""
    # Create test workflow
    workflow = Workflow(
        id=uuid4(),
        name="Test Flow",
        description="Test flow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)
    await session.commit()

    # Delete workflow using truncated UUID
    truncated_id = str(workflow.id)[:8]
    deleted = await workflow_manager.delete_workflow(truncated_id)
    assert deleted is True

    # Verify workflow is deleted
    result = await session.execute(select(Workflow).where(Workflow.id == workflow.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_workflow_with_related_objects(workflow_manager, session):
    """Test deleting a workflow with related objects."""
    # Create test workflow
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)

    # Create related task
    task = Task(
        id=uuid4(),
        workflow_id=workflow.id,
        status="completed",
        input_data='{"test": "data"}',
        tries=0,
        max_retries=3
    )
    session.add(task)

    # Create related schedule
    schedule = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="interval",
        schedule_expr="5m"
    )
    session.add(schedule)

    # Create related component
    component = WorkflowComponent(
        id=uuid4(),
        workflow_id=workflow.id,
        component_id="test-component",
        type="test"
    )
    session.add(component)
    await session.commit()

    # Delete workflow
    deleted = await workflow_manager.delete_workflow(str(workflow.id))
    assert deleted is True

    # Verify workflow and related objects are deleted
    workflow_result = await session.execute(
        select(Workflow).where(Workflow.id == workflow.id)
    )
    assert workflow_result.scalar_one_or_none() is None

    task_result = await session.execute(select(Task).where(Task.id == task.id))
    assert task_result.scalar_one_or_none() is None

    schedule_result = await session.execute(select(Schedule).where(Schedule.id == schedule.id))
    assert schedule_result.scalar_one_or_none() is None

    component_result = await session.execute(select(WorkflowComponent).where(WorkflowComponent.id == component.id))
    assert component_result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_workflow_with_task_logs(workflow_manager, session):
    """Test deleting a workflow that has tasks with logs."""
    # Create test workflow
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)

    # Create related task
    task = Task(
        id=uuid4(),
        workflow_id=workflow.id,
        status="completed",
        input_data='{"test": "data"}',
        tries=0,
        max_retries=3
    )
    session.add(task)

    # Create task logs
    task_log1 = TaskLog(
        id=uuid4(),
        task_id=task.id,
        level="info",
        message="Test log 1",
        created_at=datetime.now(pytz.utc)
    )
    task_log2 = TaskLog(
        id=uuid4(),
        task_id=task.id,
        level="error",
        message="Test log 2",
        created_at=datetime.now(pytz.utc)
    )
    session.add(task_log1)
    session.add(task_log2)
    await session.commit()

    # Delete workflow
    deleted = await workflow_manager.delete_workflow(str(workflow.id))
    assert deleted is True

    # Verify workflow, task and logs are deleted
    workflow_result = await session.execute(
        select(Workflow).where(Workflow.id == workflow.id)
    )
    assert workflow_result.scalar_one_or_none() is None

    task_result = await session.execute(select(Task).where(Task.id == task.id))
    assert task_result.scalar_one_or_none() is None

    task_log_result = await session.execute(
        select(TaskLog).where(TaskLog.task_id == task.id)
    )
    assert task_log_result.scalars().all() == []


@pytest.mark.asyncio
async def test_delete_nonexistent_workflow(workflow_manager):
    """Test deleting a nonexistent workflow."""
    deleted = await workflow_manager.delete_workflow(str(uuid4()))
    assert deleted is False


@pytest.mark.asyncio
async def test_delete_workflow_invalid_uuid(workflow_manager):
    """Test deleting a workflow with invalid UUID."""
    with pytest.raises(ValueError, match="Invalid UUID format"):
        await workflow_manager.delete_workflow("invalid-uuid")
