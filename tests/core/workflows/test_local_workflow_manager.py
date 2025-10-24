"""Test local workflow manager functionality."""

import pytest
from uuid import uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from automagik_spark.core.database.models import (
    Workflow,
    WorkflowComponent,
    Schedule,
    Task,
    TaskLog,
)
from automagik_spark.core.workflows.workflow import LocalWorkflowManager


@pytest.fixture
async def workflow_manager(session: AsyncSession) -> LocalWorkflowManager:
    """Create a workflow manager."""
    return LocalWorkflowManager(session)


@pytest.fixture
async def test_workflow(session: AsyncSession) -> Workflow:
    """Create a test workflow."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Flow",
        description="Test Description",
        data={"test": "data"},
        source="langflow",
        remote_flow_id="test_id",
        input_component="input_node",
        output_component="output_node",
        liked=False,
    )
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow


@pytest.fixture
async def test_workflow_with_relations(session: AsyncSession, test_workflow: Workflow) -> Workflow:
    """Create a test workflow with related objects."""
    # Add component
    component = WorkflowComponent(
        id=uuid4(),
        workflow_id=test_workflow.id,
        component_id="test_component",
        type="test",
        template={"test": "data"},
        tweakable_params=["param1"],
    )
    session.add(component)

    # Add schedule
    schedule = Schedule(
        id=uuid4(),
        workflow_id=test_workflow.id,
        schedule_type="cron",
        schedule_expr="* * * * *",
        status="active",
    )
    session.add(schedule)

    # Add task
    task = Task(
        id=uuid4(),
        workflow_id=test_workflow.id,
        status="pending",
        input_data='{"input": "test"}',  # Changed from dict to str
        tries=0,
        max_retries=3,
    )
    session.add(task)

    # Add task log
    task_log = TaskLog(id=uuid4(), task_id=task.id, level="info", message="test log")
    session.add(task_log)

    await session.commit()
    await session.refresh(test_workflow)
    return test_workflow


@pytest.mark.asyncio
async def test_get_workflow_by_id(workflow_manager: LocalWorkflowManager, test_workflow: Workflow):
    """Test getting a workflow by ID."""
    # Test with full UUID
    workflow = await workflow_manager.get_workflow(str(test_workflow.id))
    assert workflow is not None
    assert workflow.id == test_workflow.id

    # Test with invalid UUID
    workflow = await workflow_manager.get_workflow("invalid")
    assert workflow is None

    # Test with non-existent UUID
    workflow = await workflow_manager.get_workflow(str(uuid4()))
    assert workflow is None


@pytest.mark.asyncio
async def test_get_workflow_by_remote_id(session: AsyncSession):
    """Test getting workflow by remote ID."""
    workflow = Workflow(id=uuid4(), name="Test Workflow", source="test", remote_flow_id=str(uuid4()))
    session.add(workflow)
    await session.commit()

    # Delete any existing tasks
    await session.execute(delete(Task))
    await session.commit()

    # Create a new task
    task = Task(
        id=uuid4(),
        workflow_id=workflow.id,
        status="pending",
        input_data='{"input": "test"}',  # Changed from dict to str
        tries=0,
        max_retries=3,
    )
    session.add(task)
    await session.commit()

    # Get workflow by remote ID
    result = await session.execute(select(Workflow).where(Workflow.remote_flow_id == workflow.remote_flow_id))
    found_workflow = result.scalar_one_or_none()
    assert found_workflow is not None
    assert found_workflow.id == workflow.id


@pytest.mark.asyncio
async def test_list_workflows(workflow_manager: LocalWorkflowManager, test_workflow: Workflow):
    """Test listing workflows."""
    workflows = await workflow_manager.list_workflows()
    assert len(workflows) > 0
    assert any(w.id == test_workflow.id for w in workflows)

    # Verify that schedules are loaded
    workflow = next(w for w in workflows if w.id == test_workflow.id)
    assert hasattr(workflow, "schedules")


@pytest.mark.asyncio
async def test_delete_workflow_by_id(
    workflow_manager: LocalWorkflowManager,
    test_workflow_with_relations: Workflow,
    session: AsyncSession,
):
    """Test deleting a workflow by ID."""
    workflow = test_workflow_with_relations

    # Get task logs and tasks first
    result = await session.execute(select(Task).where(Task.workflow_id == workflow.id))
    task = result.scalar_one()

    result = await session.execute(select(TaskLog).where(TaskLog.task_id == task.id))
    task_log = result.scalar_one()

    # Delete task logs first
    await session.delete(task_log)
    await session.commit()

    # Now delete the workflow
    success = await workflow_manager.delete_workflow(str(workflow.id))
    assert success is True

    # Verify cascade deletion
    result = await session.execute(select(Workflow).where(Workflow.id == workflow.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(WorkflowComponent).where(WorkflowComponent.workflow_id == workflow.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(Schedule).where(Schedule.workflow_id == workflow.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(Task).where(Task.workflow_id == workflow.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_workflow_by_prefix(
    workflow_manager: LocalWorkflowManager,
    test_workflow: Workflow,
    session: AsyncSession,
):
    """Test deleting a workflow by ID prefix."""
    # Test with UUID prefix
    success = await workflow_manager.delete_workflow(str(test_workflow.id)[:8])
    assert success is True

    # Verify deletion
    result = await session.execute(select(Workflow).where(Workflow.id == test_workflow.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_workflow_failure(workflow_manager: LocalWorkflowManager):
    """Test workflow deletion failures."""
    # Test with non-existent UUID
    success = await workflow_manager.delete_workflow(str(uuid4()))
    assert success is False

    # Test with invalid UUID
    success = await workflow_manager.delete_workflow("invalid")
    assert success is False
