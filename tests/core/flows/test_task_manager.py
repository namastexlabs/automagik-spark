"""Test cases for task manager."""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from automagik.core.database.models import Task, TaskLog, Workflow
from automagik.core.workflows.task import TaskManager


@pytest.fixture
async def task_manager(session):
    """Create a task manager for testing."""
    return TaskManager(session)


@pytest.fixture
async def test_flow(session):
    """Create a test flow."""
    flow = Workflow(
        id=uuid4(),
        remote_flow_id=str(uuid4()),
        name="Test Flow",
        description="A test flow",
        source="langflow",  # Required field
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(flow)
    await session.commit()
    return flow


@pytest.fixture
async def failed_task(session, test_flow):
    """Create a failed task."""
    task = Task(
        id=uuid4(),
        workflow_id=test_flow.id,
        status="failed",
        error="Test error",
        input_data={"test": "data"},
        tries=0,
        max_retries=3,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc)
    )
    session.add(task)
    await session.commit()
    return task


@pytest.mark.asyncio
async def test_retry_task_success(task_manager, failed_task):
    """Test successful task retry."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    await task_manager.session.commit()

    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 1


@pytest.mark.asyncio
async def test_retry_task_exponential_backoff(task_manager, failed_task):
    """Test task retry with exponential backoff."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    failed_task.tries = 2
    await task_manager.session.commit()

    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 3
    assert retried_task.next_retry_at > datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_retry_task_max_retries(task_manager, failed_task):
    """Test task retry with max retries reached."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    failed_task.tries = failed_task.max_retries
    await task_manager.session.commit()

    with pytest.raises(ValueError, match="Task has reached maximum retries"):
        await task_manager.retry_task(task_id)


@pytest.mark.asyncio
async def test_retry_task_non_failed(task_manager, failed_task):
    """Test that only failed tasks can be retried."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "running"
    await task_manager.session.commit()

    with pytest.raises(ValueError, match="Task is not in failed state"):
        await task_manager.retry_task(task_id)


@pytest.mark.asyncio
async def test_retry_task_logs(task_manager, failed_task, session):
    """Test that task logs are preserved when retrying."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    await session.commit()

    # Add a test log
    test_log = TaskLog(
        id=uuid4(),
        task_id=task_id,
        level="error",
        message="Test error log",
        created_at=datetime.now(timezone.utc)
    )
    session.add(test_log)
    await session.commit()

    # Retry the task
    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"

    # Check that logs are preserved
    result = await session.execute(select(TaskLog).where(TaskLog.task_id == task_id))
    logs = result.scalars().all()
    assert len(logs) == 2  # Original log + new retry log
    assert any(log.message == "Test error log" for log in logs)
    assert any(log.message == failed_task.error for log in logs)


@pytest.mark.asyncio
async def test_retry_task_success_without_session():
    """Test successfully retrying a failed task."""
    session = AsyncMock()
    task = Task(
        id=uuid4(),
        status="failed",
        tries=0,
        max_retries=3,
        error="Previous error"
    )

    # Mock the async session operations
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = task
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result

    # Configure session methods - add is sync, commit is async
    session.add = MagicMock()
    session.commit = AsyncMock()

    task_manager = TaskManager(session)
    retried_task = await task_manager.retry_task(task.id)

    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 1
    assert retried_task.next_retry_at > datetime.now(timezone.utc)
    
    # Verify session operations were called
    assert session.add.call_count == 1  # For task log
    assert session.commit.await_count == 1


@pytest.mark.asyncio
async def test_retry_task_exponential_backoff_without_session():
    """Test exponential backoff for retried tasks."""
    session = AsyncMock()
    task = Task(
        id=uuid4(),
        status="failed",
        tries=2,
        max_retries=3,
        error="Previous error"
    )

    # Mock the async session operations
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = task
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result

    # Configure session methods - add is sync, commit is async
    session.add = MagicMock()
    session.commit = AsyncMock()

    task_manager = TaskManager(session)
    retried_task = await task_manager.retry_task(task.id)

    assert retried_task is not None
    assert retried_task.status == "pending"
    assert retried_task.tries == 3
    assert retried_task.next_retry_at > datetime.now(timezone.utc)
    
    # Verify session operations were called
    assert session.add.call_count == 1  # For task log
    assert session.commit.await_count == 1


@pytest.mark.asyncio
async def test_retry_task_max_retries_without_session():
    """Test task retry when max retries reached."""
    session = AsyncMock()
    task = Task(
        id=uuid4(),
        status="failed",
        tries=3,
        max_retries=3,
        error="Previous error"
    )

    # Mock the async session operations
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = task
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result

    task_manager = TaskManager(session)
    with pytest.raises(ValueError, match="Task has reached maximum retries"):
        await task_manager.retry_task(task.id)


@pytest.mark.asyncio
async def test_retry_task_non_failed_without_session():
    """Test retrying a non-failed task."""
    session = AsyncMock()
    task = Task(
        id=uuid4(),
        status="pending",
        tries=0,
        max_retries=3
    )

    # Mock the async session operations
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = task
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result

    task_manager = TaskManager(session)
    with pytest.raises(ValueError, match="Task is not in failed state"):
        await task_manager.retry_task(task.id)


@pytest.mark.asyncio
async def test_retry_task_logs_without_session():
    """Test that task logs are preserved when retrying without a real session."""
    session = AsyncMock()
    task_id = uuid4()
    task = Task(
        id=task_id,
        status="failed",
        tries=0,
        max_retries=3,
        error="Previous error"
    )

    # Mock the async session operations
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = task
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result

    # Configure session methods - add is sync, commit is async
    session.add = MagicMock()
    session.commit = AsyncMock()

    task_manager = TaskManager(session)
    retried_task = await task_manager.retry_task(task_id)

    assert retried_task is not None
    assert retried_task.status == "pending"
    
    # Verify session operations were called
    assert session.add.call_count == 1  # For task log
    assert session.commit.await_count == 1


@pytest.mark.asyncio
async def test_retry_task_logs(task_manager, failed_task, session):
    """Test that task logs are preserved when retrying."""
    task_id = uuid4()
    failed_task.id = task_id
    failed_task.status = "failed"
    failed_task.error = "Test error log"  # Set the error message
    await session.commit()

    # Retry the task
    retried_task = await task_manager.retry_task(task_id)
    assert retried_task is not None
    assert retried_task.status == "pending"

    # Check that logs are preserved
    result = await session.execute(select(TaskLog).where(TaskLog.task_id == task_id))
    logs = result.scalars().all()
    assert len(logs) == 1  # Only the retry log
    assert any(log.message == "Previous error: Test error log" for log in logs)


@pytest.mark.asyncio
async def test_retry_task_max_retries_with_session(task_manager, failed_task):
    """Test that tasks cannot be retried beyond max_retries."""
    # Set tries to max
    failed_task.tries = failed_task.max_retries
    await task_manager.session.commit()

    # Try to retry
    with pytest.raises(ValueError, match="Task has reached maximum retries"):
        await task_manager.retry_task(str(failed_task.id))


@pytest.mark.asyncio
async def test_retry_task_non_failed_with_session(task_manager, failed_task):
    """Test that only failed tasks can be retried."""
    # Set task to running
    failed_task.status = "running"
    await task_manager.session.commit()

    # Try to retry
    with pytest.raises(ValueError, match="Task is not in failed state"):
        await task_manager.retry_task(str(failed_task.id))
