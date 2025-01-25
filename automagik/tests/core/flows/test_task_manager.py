"""Test task manager functionality."""

import pytest
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.flows.task import TaskManager
from automagik.core.database.models import Task, Flow

@pytest.fixture
async def task_manager(session: AsyncSession) -> TaskManager:
    """Create a task manager for testing."""
    return TaskManager(session)

@pytest.fixture
async def test_flow(session: AsyncSession) -> Flow:
    """Create a test flow."""
    flow = Flow(
        id=uuid4(),
        name="Test Flow",
        description="Test flow for task manager",
        source="test",
        source_id=str(uuid4())
    )
    session.add(flow)
    await session.commit()
    return flow

@pytest.fixture
async def test_tasks(session: AsyncSession, test_flow: Flow) -> list[Task]:
    """Create test tasks."""
    tasks = []
    for i in range(5):
        task = Task(
            id=uuid4(),
            flow_id=test_flow.id,
            status="completed" if i % 2 == 0 else "failed",
            input_data={"test": f"input_{i}"},
            output_data={"test": f"output_{i}"} if i % 2 == 0 else None,
            error="test error" if i % 2 == 1 else None,
            tries=1,
            max_retries=3,
            created_at=datetime.utcnow()
        )
        session.add(task)
        tasks.append(task)
    await session.commit()
    return tasks

@pytest.mark.asyncio
async def test_get_task_by_truncated_id(
    session: AsyncSession,
    task_manager: TaskManager,
    test_tasks: list[Task]
):
    """Test getting a task by truncated ID."""
    # Get first task
    task = test_tasks[0]
    task_id = str(task.id)
    
    # Test with full ID
    result = await task_manager.get_task(task_id)
    assert result is not None
    assert result.id == task.id
    
    # Test with truncated ID (first 8 chars)
    result = await task_manager.get_task(task_id[:8])
    assert result is not None
    assert result.id == task.id
    
    # Test with invalid truncated ID
    result = await task_manager.get_task("12345678")
    assert result is None
    
    # Test with ambiguous truncated ID
    # Create another task with similar ID
    similar_id = task_id[:8] + "".join(['0' for _ in range(24)])
    similar_task = Task(
        id=UUID(similar_id),
        flow_id=test_tasks[0].flow_id,
        status="completed",
        input_data={"test": "similar"},
        tries=1,
        max_retries=3,
        created_at=datetime.utcnow()
    )
    session.add(similar_task)
    await session.commit()
    
    # Should return None for ambiguous ID
    result = await task_manager.get_task(task_id[:8])
    assert result is None

@pytest.mark.asyncio
async def test_list_tasks_order(
    session: AsyncSession,
    task_manager: TaskManager,
    test_tasks: list[Task]
):
    """Test that tasks are listed in correct order."""
    # List all tasks
    tasks = await task_manager.list_tasks()
    
    # Verify tasks are ordered by created_at desc
    for i in range(len(tasks) - 1):
        assert tasks[i].created_at >= tasks[i + 1].created_at

@pytest.mark.asyncio
async def test_list_tasks_limit(
    session: AsyncSession,
    task_manager: TaskManager,
    test_tasks: list[Task]
):
    """Test task listing with limit."""
    # Test with limit
    limit = 3
    tasks = await task_manager.list_tasks(limit=limit)
    assert len(tasks) == limit
    
    # Verify we got the most recent tasks
    all_tasks = await task_manager.list_tasks()
    assert tasks == all_tasks[:limit]

@pytest.mark.asyncio
async def test_list_tasks_filter(
    session: AsyncSession,
    task_manager: TaskManager,
    test_tasks: list[Task]
):
    """Test task listing with filters."""
    # Test status filter
    completed_tasks = await task_manager.list_tasks(status="completed")
    assert all(t.status == "completed" for t in completed_tasks)
    
    failed_tasks = await task_manager.list_tasks(status="failed")
    assert all(t.status == "failed" for t in failed_tasks)
    
    # Test flow filter
    flow_tasks = await task_manager.list_tasks(flow_id=str(test_tasks[0].flow_id))
    assert all(t.flow_id == test_tasks[0].flow_id for t in flow_tasks)
