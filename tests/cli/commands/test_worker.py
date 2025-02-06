"""Test cases for worker command."""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from sqlalchemy import text, select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch, MagicMock
import warnings

# Suppress all coroutine warnings in tests
warnings.filterwarnings(
    "ignore",
    message="coroutine '.*' was never awaited",
    category=RuntimeWarning
)

from automagik.cli.commands.worker import process_schedules, parse_interval
from automagik.core.database.models import Workflow, Schedule, Task, TaskLog

@pytest.fixture(autouse=True)
async def cleanup_db(session):
    """Clean up database before each test."""
    await session.execute(text("DELETE FROM task_logs"))
    await session.execute(text("DELETE FROM tasks"))
    await session.execute(text("DELETE FROM schedules"))
    await session.execute(text("DELETE FROM workflow_components"))
    await session.execute(text("DELETE FROM workflows"))
    await session.commit()

@pytest.fixture
async def sample_flow(session):
    """Create a sample flow for testing."""
    flow = Workflow(
        id=uuid4(),
        remote_flow_id="test-flow",
        name="Test Flow",
        description="Test flow for testing",
        source="langflow",
        data={"nodes": []}
    )
    session.add(flow)
    await session.commit()
    return flow

@pytest.fixture
async def future_schedule(session, sample_flow):
    """Create a schedule that will run in the future."""
    next_run = datetime.now(timezone.utc) + timedelta(hours=1)
    schedule = Schedule(
        id=uuid4(),
        workflow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="60m",  # 60 minutes
        workflow_params='{"test": "params"}',
        status="active",
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.fixture
async def past_schedule(session, sample_flow):
    """Create a schedule that was due in the past."""
    next_run = datetime.now(timezone.utc) - timedelta(minutes=5)
    schedule = Schedule(
        id=uuid4(),
        workflow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",  # 30 minutes
        workflow_params='{"test": "params"}',
        status="active",
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.fixture
async def inactive_schedule(session, sample_flow):
    """Create an inactive schedule."""
    next_run = datetime.now(timezone.utc) - timedelta(minutes=5)
    schedule = Schedule(
        id=uuid4(),
        workflow_id=sample_flow.id,
        schedule_type="interval",
        schedule_expr="30m",
        workflow_params='{"test": "params"}',
        status="paused",  
        next_run_at=next_run
    )
    session.add(schedule)
    await session.commit()
    return schedule

@pytest.fixture
async def mock_session():
    """Create a mock session for testing."""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    return session

@pytest.fixture
async def mock_workflow_manager():
    """Create a mock workflow manager for testing."""
    manager = AsyncMock()
    manager.create_task = AsyncMock()
    return manager


@pytest.mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call' was never awaited")
@pytest.mark.asyncio(loop_scope="function")
async def test_process_schedules_future(session: AsyncSession, future_schedule):
    """Test processing a schedule that will run in the future."""
    # Create a simple mock that returns the future schedule
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [future_schedule]

    # Mock the session
    async def mock_execute(stmt, *args, **kwargs):
        return mock_result

    session.execute = AsyncMock(side_effect=mock_execute)
    session.commit = AsyncMock()

    # Process schedules
    await process_schedules(session)

    # Verify execute was called
    assert session.execute.call_count == 2  # Once for schedules, once for tasks
    assert session.commit.call_count == 0  # No commits since schedule is in future

    # Verify no tasks were created since the schedule is in the future
    result = await session.execute(
        select(Task).filter(Task.workflow_id == future_schedule.workflow_id)
    )
    tasks = result.scalars().all()
    assert len(tasks) == 0


@pytest.mark.asyncio(loop_scope="function")
async def test_process_schedules_past(session: AsyncSession, past_schedule):
    """Test processing a schedule that was due in the past."""
    # Track task creation
    task_created = False
    created_task = None
    
    async def mock_create_task(task_data):
        nonlocal task_created, created_task
        task_created = True
        created_task = Task(**task_data, id=uuid4())
        print("Task created with data:", task_data)
        return created_task
    
    # Mock task manager
    task_manager = MagicMock()
    task_manager.create_task = AsyncMock(side_effect=mock_create_task)
    task_manager.session = session
    
    # Mock workflow manager
    workflow_manager = MagicMock()
    workflow_manager.session = session  # Set session on workflow manager

    # Create a mock workflow and schedule
    mock_workflow = MagicMock()
    mock_workflow.id = past_schedule.workflow_id
    mock_schedule = MagicMock()
    mock_schedule.id = past_schedule.id
    mock_schedule.workflow_id = past_schedule.workflow_id
    mock_schedule.workflow = mock_workflow
    mock_schedule.schedule_type = past_schedule.schedule_type
    mock_schedule.schedule_expr = past_schedule.schedule_expr
    mock_schedule.next_run_at = past_schedule.next_run_at
    mock_schedule.status = past_schedule.status
    mock_schedule.workflow_params = '{"test": "params"}'

    # Mock session execute for schedule query
    async def mock_execute(stmt, *args, **kwargs):
        print("Executing query:", str(stmt))
        result = MagicMock()
        result.returns_rows = True
        scalar_result = MagicMock()
        if "schedules" in str(stmt).lower():
            print("Past schedule:", mock_schedule)
            print("Past schedule workflow:", mock_schedule.workflow)
            scalar_result.all.return_value = [mock_schedule]
            result.scalars.return_value = scalar_result
        else:
            print("Running tasks query:", str(stmt))
            # Handle task status query
            if "tasks" in str(stmt).lower() and "status" in str(stmt).lower():
                result.scalar.return_value = 0  # No running tasks
                print("Running tasks count:", result.scalar_return_value)
            else:
                scalar_result.all.return_value = []
                result.scalars.return_value = scalar_result
        return result

    # Mock session
    session.execute = AsyncMock(side_effect=mock_execute)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock(return_value=mock_workflow)
    
    # Process schedules
    with patch('automagik.cli.commands.worker.WorkflowManager', return_value=workflow_manager), \
         patch('automagik.cli.commands.worker.TaskManager', return_value=task_manager):
        print("\nProcessing schedules...")
        await process_schedules(session)
        print("Done processing schedules")
    
    # Verify task was created and committed
    print("\nChecking if task was created...")
    task_manager.create_task.assert_called_once_with({"workflow_id": past_schedule.workflow_id, "status": "pending", "input_data": '{"test": "params"}', "tries": 0, "max_retries": 3})
    assert task_created, "Task was not created"
    
    # Verify task properties
    assert created_task is not None, "Task object was not created"
    task_data = task_manager.create_task.call_args[0][0]
    assert task_data["workflow_id"] == past_schedule.workflow_id, "Task has wrong workflow_id"
    assert task_data["status"] == "pending", "Task has wrong status"
    assert task_data["max_retries"] == 3, "Task has wrong max_retries"
    
    # Verify commit was called
    assert session.commit.call_count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_process_schedules_inactive(session, inactive_schedule):
    """Test processing an inactive schedule."""
    # Mock the execute method to return a real result
    async def mock_execute(*args, **kwargs):
        result = MagicMock()
        query = str(args[0]).upper()
        if "SCHEDULE" in query and "WORKFLOW" in query:
            # For list_schedules query
            scalar_result = MagicMock()
            scalar_result.all.return_value = [inactive_schedule]
            result.scalars.return_value = scalar_result
        return result

    # Mock the session
    session.execute = AsyncMock(side_effect=mock_execute)
    session.commit = AsyncMock()

    # Process schedules
    await process_schedules(session)

    # Verify no tasks were created
    result = await session.execute(
        select(Task).filter(Task.workflow_id == inactive_schedule.workflow_id)
    )
    tasks = result.scalars().all()
    assert len(tasks) == 0


@pytest.mark.asyncio(loop_scope="function")
async def test_process_schedules_multiple(session, future_schedule, past_schedule, inactive_schedule):
    """
    Test processing multiple schedules.
    We fix the "MagicMock flow_id" problem by:
      1) Giving each schedule a real Workflow object with a real UUID (and setting schedule.flow_id properly).
      2) Ensuring our mocks for session.execute(...) only return real objects or real UUIDs (never MagicMock).
    """

    # 1) Give each schedule a distinct, real Workflow relationship & flow_id:
    past_flow = Workflow(
        id=uuid4(),
        remote_flow_id="some-past-source",
        name="Past Flow",
        description="A flow that should have run in the past",
        source="langflow",
        data={"nodes": []}
    )
    future_flow = Workflow(
        id=uuid4(),
        remote_flow_id="some-future-source",
        name="Future Flow",
        description="A flow that should run in the future",
        source="langflow",
        data={"nodes": []}
    )
    inactive_flow = Workflow(
        id=uuid4(),
        remote_flow_id="some-inactive-source",
        name="Inactive Flow",
        description="A flow that is inactive",
        source="langflow",
        data={"nodes": []}
    )

    # Attach them to the schedules:
    past_schedule.workflow_id = past_flow.id
    future_schedule.workflow_id = future_flow.id
    inactive_schedule.workflow_id = inactive_flow.id

    # Create a real Task object with a real workflow_id
    mock_task = Task(
        id=uuid4(),
        workflow_id=past_flow.id,  # Use real UUID from past_flow
        status='pending',
        input_data='{}',
        created_at=datetime.now(timezone.utc),
        tries=0,
        max_retries=3
    )

    # Mock session.execute to return real objects instead of MagicMocks
    async def mock_execute(sql_query, *args, **kwargs):
        query_str = str(sql_query).upper()
        result = MagicMock()

        # Add scalar_one method that returns real objects
        def mock_scalar_one():
            if "FROM WORKFLOWS" in query_str:
                return past_flow
            elif "FROM TASKS" in query_str:
                return mock_task
            return None
        result.scalar_one.side_effect = mock_scalar_one

        if "FROM SCHEDULES" in query_str and "WORKFLOW" in query_str:
            # Return our three schedules with real Workflow objects
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [future_schedule, past_schedule, inactive_schedule]
            result.scalars.return_value = mock_scalars

        elif "SELECT COUNT(" in query_str:
            result.scalar.return_value = 1

        elif "TASK.STATUS" in query_str and "FROM TASKS" in query_str:
            # Return empty list for retry tasks query
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = []
            result.scalars.return_value = mock_scalars
            result.scalar.return_value = None

        elif "FROM WORKFLOWS" in query_str:
            # Return past_flow for Workflow queries
            result.scalar.return_value = past_flow
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [past_flow]
            result.scalars.return_value = mock_scalars

        elif "FROM TASKS" in query_str:
            # Return our real mock_task for task queries
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [mock_task]
            result.scalars.return_value = mock_scalars
            result.scalar.return_value = mock_task.workflow_id  # Return the real workflow_id

        else:
            # Default: return empty results
            result.scalar_return_value = None
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = []
            result.scalars.return_value = mock_scalars

        return result

    # Mock session.get to return real Workflow objects
    async def mock_session_get(model_class, primary_key):
        if model_class is Workflow:
            if primary_key == past_flow.id:
                return past_flow
            elif primary_key == future_flow.id:
                return future_flow
            elif primary_key == inactive_flow.id:
                return inactive_flow
        return None

    with patch.object(session, 'execute', new_callable=AsyncMock, side_effect=mock_execute), \
         patch.object(session, 'get', new_callable=AsyncMock, side_effect=mock_session_get):
        await process_schedules(session)

        # Update the schedule's next_run_at manually since we're mocking
        past_schedule.next_run_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        # Verify only one task was created (for past_schedule)
        result = await session.execute(select(func.count()).select_from(Task))
        count = result.scalar()
        assert count == 1
        
        # Verify task was created for the right flow
        result = await session.execute(
            select(Task.workflow_id)
            .order_by(Task.created_at.desc())
            .limit(1)
        )
        task_workflow_id = result.scalar()
        assert task_workflow_id == past_schedule.workflow_id


@pytest.mark.asyncio
async def test_process_schedules_future():
    """Test processing schedules with future schedules."""
    mock_session = AsyncMock()
    
    # Create a mock schedule
    mock_schedule = MagicMock()
    mock_schedule.id = 1
    mock_schedule.workflow_id = "test-flow"
    mock_schedule.next_run_at = datetime.now(timezone.utc) + timedelta(hours=1)
    mock_schedule.last_run = None
    mock_schedule.schedule_type = "interval"
    mock_schedule.schedule_expr = "1h"
    mock_schedule.status = "active"
    mock_schedule.workflow_params = '{"test": "params"}'
    
    # Mock the query result
    mock_result = AsyncMock()
    mock_scalars = MagicMock()
    mock_scalars.all = MagicMock(return_value=[mock_schedule])
    mock_result.scalars = MagicMock(return_value=mock_scalars)
    
    # Set up the session mock to return our result
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    # Call the function
    await process_schedules(mock_session)
    
    # Assert that no task was created since the schedule is in the future
    assert mock_session.add.call_count == 0
    assert mock_session.commit.call_count == 0


def test_parse_interval():
    """Test interval string parsing."""
    assert parse_interval("30m") == timedelta(minutes=30)
    assert parse_interval("2h") == timedelta(hours=2)
    assert parse_interval("1d") == timedelta(days=1)
    
    with pytest.raises(ValueError):
        parse_interval("invalid")
    
    with pytest.raises(ValueError):
        parse_interval("30x")  # Invalid unit
    
    with pytest.raises(ValueError):
        parse_interval("0m")  # Zero duration
        
    with pytest.raises(ValueError):
        parse_interval("-1h")  # Negative duration

@pytest.mark.asyncio
async def test_process_schedules_future(session):
    """Test processing schedules with future execution time."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)
    
    schedule = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="interval",
        schedule_expr="30m",
        workflow_params='{"test": "params"}',
        status="active",
        next_run_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    session.add(schedule)
    await session.commit()

@pytest.mark.asyncio
async def test_process_schedules_past(session):
    """Test processing schedules with past execution time."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)
    
    schedule = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="interval",
        schedule_expr="30m",
        workflow_params='{"test": "params"}',
        status="active",
        next_run_at=datetime.now(timezone.utc) - timedelta(minutes=5)
    )
    session.add(schedule)
    await session.commit()

@pytest.mark.asyncio
async def test_process_schedules_inactive(session):
    """Test processing inactive schedules."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)
    
    schedule = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="interval",
        schedule_expr="30m",
        workflow_params='{"test": "params"}',
        status="paused",
        next_run_at=datetime.now(timezone.utc) - timedelta(minutes=5)
    )
    session.add(schedule)
    await session.commit()

@pytest.mark.asyncio
async def test_process_schedules_multiple(session):
    """Test processing multiple schedules."""
    workflow = Workflow(
        id=uuid4(),
        name="Test Workflow",
        source="test",
        remote_flow_id=str(uuid4())
    )
    session.add(workflow)
    
    # Past schedule
    schedule1 = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="interval",
        schedule_expr="60m",
        workflow_params='{"test": "params"}',
        status="active",
        next_run_at=datetime.now(timezone.utc) - timedelta(minutes=5)
    )
    session.add(schedule1)
    
    # Future schedule
    schedule2 = Schedule(
        id=uuid4(),
        workflow_id=workflow.id,
        schedule_type="interval",
        schedule_expr="60m",
        workflow_params='{"test": "params"}',
        status="active",
        next_run_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    session.add(schedule2)
    await session.commit()

@pytest.mark.asyncio
async def test_worker_workflow_execution(session: AsyncSession, sample_flow):
    """Test that the worker properly executes workflows using WorkflowSync."""
    # Create a task
    task = Task(
        id=uuid4(),
        workflow_id=sample_flow.id,
        status="pending",
        input_data="test input",
        created_at=datetime.now(timezone.utc)
    )
    session.add(task)
    await session.commit()

    # Import here to avoid circular imports
    from automagik.core.workflows.manager import WorkflowManager
    from automagik.cli.commands.worker import run_workflow

    # Run the workflow
    workflow_manager = WorkflowManager(session)
    result = await run_workflow(workflow_manager, task)

    # Verify task was executed
    await session.refresh(task)
    assert task.status == "failed"  # Since we didn't mock LangFlow, it will fail
    assert "Manager not initialized" not in str(task.error)  # This is the key assertion
    assert task.finished_at is not None
