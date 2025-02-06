"""Test workflow manager functionality."""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.workflows.manager import WorkflowManager
from automagik.core.database.models import Workflow, Task, TaskLog, Schedule, WorkflowComponent

@pytest.fixture
async def workflow_manager(session: AsyncSession) -> WorkflowManager:
    """Create a workflow manager."""
    async with WorkflowManager(session) as manager:
        yield manager

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
        gradient=False,
        liked=False
    )
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow

@pytest.fixture
async def test_task(session: AsyncSession, test_workflow: Workflow) -> Task:
    """Create a test task."""
    task = Task(
        id=uuid4(),
        workflow_id=test_workflow.id,
        status="pending",
        input_data={"input": "test input"},
        created_at=datetime.now(timezone.utc)
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

@pytest.mark.asyncio
async def test_list_remote_flows(workflow_manager: WorkflowManager):
    """Test listing remote flows."""
    # Mock the LangFlow API response
    mock_flows = {"flows": [{"id": "1", "name": "Flow 1"}]}
    workflow_manager.langflow.list_remote_flows = AsyncMock(return_value=mock_flows)

    flows = await workflow_manager.list_remote_flows()
    assert flows == mock_flows

@pytest.mark.asyncio
async def test_get_flow_components(workflow_manager: WorkflowManager):
    """Test getting flow components."""
    # Mock the LangFlow API response
    mock_flow = {
        "flow": {"id": "1", "name": "Flow 1"},
        "components": [{"id": "comp1", "name": "Component 1"}]
    }
    workflow_manager.langflow.sync_flow = AsyncMock(return_value=mock_flow)

    components = await workflow_manager.get_flow_components("test_id")
    assert components == mock_flow["components"]

@pytest.mark.asyncio
async def test_sync_flow_new(workflow_manager: WorkflowManager):
    """Test syncing a new flow."""
    flow_id = str(uuid4())
    mock_flow = {
        "flow": {
            "id": flow_id,
            "name": "New Flow",
            "description": "Test Flow",
            "data": {"test": "data"},
            "folder_id": "folder1",
            "folder_name": "Folder 1",
            "icon": "icon1",
            "icon_bg_color": "#fff",
            "gradient": True,
            "liked": True,
            "tags": ["tag1"]
        }
    }
    workflow_manager.langflow.sync_flow = AsyncMock(return_value=mock_flow)

    workflow = await workflow_manager.sync_flow(
        flow_id,
        input_component="input1",
        output_component="output1"
    )

    assert workflow is not None
    assert workflow.name == "New Flow"
    assert workflow.remote_flow_id == flow_id
    assert workflow.input_component == "input1"
    assert workflow.output_component == "output1"

@pytest.mark.asyncio
async def test_list_workflows(
    workflow_manager: WorkflowManager,
    test_workflow: Workflow
):
    """Test listing workflows."""
    workflows = await workflow_manager.list_workflows()
    assert len(workflows) > 0
    assert any(w.id == test_workflow.id for w in workflows)

    # Test with joinedload
    workflows = await workflow_manager.list_workflows({"joinedload": ["tasks"]})
    assert len(workflows) > 0
    workflow = next(w for w in workflows if w.id == test_workflow.id)
    assert hasattr(workflow, "tasks")

@pytest.mark.asyncio
async def test_get_workflow(
    workflow_manager: WorkflowManager,
    test_workflow: Workflow
):
    """Test getting a workflow."""
    # Test with full UUID
    workflow = await workflow_manager.get_workflow(str(test_workflow.id))
    assert workflow is not None
    assert workflow.id == test_workflow.id

    # Test with prefix
    prefix = str(test_workflow.id)[:8]
    workflow = await workflow_manager.get_workflow(prefix)
    assert workflow is not None
    assert workflow.id == test_workflow.id

    # Test with invalid UUID
    workflow = await workflow_manager.get_workflow("invalid")
    assert workflow is None

@pytest.mark.asyncio
async def test_delete_workflow(
    workflow_manager: WorkflowManager,
    test_workflow: Workflow,
    test_task: Task,
    session: AsyncSession
):
    """Test deleting a workflow."""
    # Add some related objects
    task_log = TaskLog(
        id=uuid4(),
        task_id=test_task.id,
        level="info",
        message="test log"
    )
    schedule = Schedule(
        id=uuid4(),
        workflow_id=test_workflow.id,
        schedule_type="cron",
        schedule_expr="* * * * *",
        status="active"
    )
    component = WorkflowComponent(
        id=uuid4(),
        workflow_id=test_workflow.id,
        component_id="test_component",
        type="test",
        template={"test": "data"},
        tweakable_params=["param1"]
    )
    session.add_all([task_log, schedule, component])
    await session.commit()

    # Test with full UUID
    success = await workflow_manager.delete_workflow(str(test_workflow.id))
    assert success is True

    # Verify cascade deletion
    result = await session.execute(select(Workflow).where(Workflow.id == test_workflow.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(Task).where(Task.workflow_id == test_workflow.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(TaskLog).where(TaskLog.task_id == test_task.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(Schedule).where(Schedule.workflow_id == test_workflow.id))
    assert result.scalar_one_or_none() is None

    result = await session.execute(select(WorkflowComponent).where(WorkflowComponent.workflow_id == test_workflow.id))
    assert result.scalar_one_or_none() is None

@pytest.mark.asyncio
async def test_task_operations(
    workflow_manager: WorkflowManager,
    test_workflow: Workflow
):
    """Test task-related operations."""
    # First create a task
    task_id = uuid4()
    task_data = {
        "id": str(task_id),
        "workflow_id": str(test_workflow.id),
        "status": "pending",
        "input_data": {"test": "data"},
        "error": None,
        "tries": 0,
        "max_retries": 3
    }
    
    created_task = await workflow_manager.task.create_task(task_data)
    await workflow_manager.session.commit()

    # Test get_task
    task = await workflow_manager.get_task(str(created_task.id))
    assert task is not None
    assert task.id == created_task.id
    assert task.status == "pending"

    # Test update_task
    update_data = {
        "status": "running",
        "tries": 1
    }
    updated_task = await workflow_manager.task.update_task(str(created_task.id), update_data)
    assert updated_task is not None
    assert updated_task.status == "running"
    assert updated_task.tries == 1

    # Test delete_task
    result = await workflow_manager.task.delete_task(str(created_task.id))
    assert result is True

    # Verify task is deleted
    deleted_task = await workflow_manager.get_task(created_task.id)
    assert deleted_task is None

@pytest.mark.asyncio
async def test_run_workflow(
    workflow_manager: WorkflowManager,
    test_workflow: Workflow
):
    """Test running a workflow."""
    # Mock the workflow execution
    with patch("automagik.core.workflows.sync.WorkflowSync.execute_workflow") as mock_execute:
        mock_execute.return_value = {"result": "success"}
        
        # Test successful execution
        task = await workflow_manager.run_workflow(
            test_workflow.id,
            {"input": "test"}
        )
        assert task is not None
        assert task.status == "pending"
        assert task.workflow_id == test_workflow.id

        # Test failed execution
        mock_execute.side_effect = Exception("Test error")
        task = await workflow_manager.run_workflow(
            test_workflow.id,
            {"input": "test"}
        )
        assert task is None

        # Test with non-existent workflow
        with pytest.raises(ValueError):
            await workflow_manager.run_workflow(
                uuid4(),
                {"input": "test"}
            )
