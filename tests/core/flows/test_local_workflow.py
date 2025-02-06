"""Test local workflow management functionality."""

import pytest
from datetime import datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.database.models import Workflow, Task, Schedule, WorkflowComponent
from automagik.core.workflows.workflow import LocalWorkflowManager

@pytest.fixture(autouse=True)
async def cleanup_workflows(session: AsyncSession):
    """Clean up workflows after each test."""
    yield
    await session.execute(text("DELETE FROM task_logs"))
    await session.execute(text("DELETE FROM tasks"))
    await session.execute(text("DELETE FROM workflow_components"))
    await session.execute(text("DELETE FROM schedules"))
    await session.execute(text("DELETE FROM workflows"))
    await session.commit()

@pytest.fixture
async def workflow_manager(session: AsyncSession) -> LocalWorkflowManager:
    """Create a workflow manager."""
    return LocalWorkflowManager(session)

@pytest.fixture
async def test_workflow(session: AsyncSession) -> Workflow:
    """Create a test workflow with components, schedules, and tasks."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        description="Test Description",
        source="test",
        remote_flow_id="test_remote_id",
        input_component="input_node",
        output_component="output_node",
        data="test data",
        flow_version=1,
        is_component=False,
        gradient=False,
        liked=False
    )
    session.add(workflow)
    
    # Add components
    component = WorkflowComponent(
        id=uuid4(),
        workflow_id=workflow.id,
        component_id="test_component",
        type="test_type",
        template="test template",
        tweakable_params="test tweakable params",
        is_input=True,
        is_output=False
    )
    session.add(component)
    
    # Add schedules
    schedule = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="cron",
        schedule_expr="* * * * *",
        status="active",
        workflow_params='{"test": "data"}'
    )
    session.add(schedule)
    
    # Add tasks
    task = Task(
        id=uuid4(),
        workflow_id=workflow.id,
        status="completed",
        input_data="test input",
        output_data="test output",
        created_at=datetime.utcnow()
    )
    session.add(task)
    
    await session.commit()
    await session.refresh(workflow)
    return workflow

@pytest.mark.asyncio
async def test_get_workflow_by_id(
    session: AsyncSession,
    workflow_manager: LocalWorkflowManager,
    test_workflow: Workflow
):
    """Test getting a workflow by ID."""
    # Get by UUID
    workflow = await workflow_manager.get_workflow(str(test_workflow.id))
    assert workflow is not None
    assert workflow.id == test_workflow.id
    assert workflow.name == "Test Workflow"
    
    # Get by remote_flow_id
    workflow = await workflow_manager.get_workflow(test_workflow.remote_flow_id)
    assert workflow is not None
    assert workflow.id == test_workflow.id
    assert workflow.remote_flow_id == "test_remote_id"

@pytest.mark.asyncio
async def test_get_nonexistent_workflow(
    session: AsyncSession,
    workflow_manager: LocalWorkflowManager
):
    """Test getting a nonexistent workflow."""
    # Try with random UUID
    workflow = await workflow_manager.get_workflow(str(uuid4()))
    assert workflow is None
    
    # Try with nonexistent remote_flow_id
    workflow = await workflow_manager.get_workflow("nonexistent_remote_id")
    assert workflow is None

@pytest.mark.asyncio
async def test_list_workflows(
    session: AsyncSession,
    workflow_manager: LocalWorkflowManager,
    test_workflow: Workflow
):
    """Test listing all workflows."""
    # Create another workflow
    another_workflow = Workflow(
        id=uuid4(),
        name="Another Workflow",
        source="test",
        remote_flow_id=str(uuid4()),
        input_component="input_node",
        output_component="output_node",
        data="test data",
        flow_version=1
    )
    session.add(another_workflow)
    await session.commit()
    
    # List workflows
    workflows = await workflow_manager.list_workflows()
    assert len(workflows) == 2
    assert any(w.id == test_workflow.id for w in workflows)
    assert any(w.id == another_workflow.id for w in workflows)
    
    # Check that schedules are loaded
    workflow_with_schedule = next(w for w in workflows if w.id == test_workflow.id)
    assert len(workflow_with_schedule.schedules) == 1

@pytest.mark.asyncio
async def test_delete_workflow_by_id(
    session: AsyncSession,
    workflow_manager: LocalWorkflowManager,
    test_workflow: Workflow
):
    """Test deleting a workflow by ID."""
    # Delete by full UUID
    success = await workflow_manager.delete_workflow(str(test_workflow.id))
    assert success is True
    
    # Verify workflow and related objects are deleted
    workflow = await session.get(Workflow, test_workflow.id)
    assert workflow is None
    
    # Check that related objects are deleted
    result = await session.execute(
        text(f"SELECT COUNT(*) FROM workflow_components WHERE workflow_id = '{test_workflow.id}'")
    )
    assert result.scalar() == 0
    
    result = await session.execute(
        text(f"SELECT COUNT(*) FROM schedules WHERE workflow_id = '{test_workflow.id}'")
    )
    assert result.scalar() == 0
    
    result = await session.execute(
        text(f"SELECT COUNT(*) FROM tasks WHERE workflow_id = '{test_workflow.id}'")
    )
    assert result.scalar() == 0

@pytest.mark.asyncio
async def test_delete_workflow_by_partial_id(
    session: AsyncSession,
    workflow_manager: LocalWorkflowManager,
    test_workflow: Workflow
):
    """Test deleting a workflow by partial ID."""
    # Delete by first 8 characters of UUID
    partial_id = str(test_workflow.id)[:8]
    success = await workflow_manager.delete_workflow(partial_id)
    assert success is True
    
    # Verify workflow is deleted
    workflow = await session.get(Workflow, test_workflow.id)
    assert workflow is None

@pytest.mark.asyncio
async def test_delete_nonexistent_workflow(
    session: AsyncSession,
    workflow_manager: LocalWorkflowManager
):
    """Test deleting a nonexistent workflow."""
    # Try with random UUID
    success = await workflow_manager.delete_workflow(str(uuid4()))
    assert success is False
    
    # Try with invalid UUID format
    success = await workflow_manager.delete_workflow("invalid-uuid")
    assert success is False
