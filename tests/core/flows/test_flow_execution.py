"""Test flow execution functionality."""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from automagik.core.workflows.sync import WorkflowSync
from automagik.core.database.models import Task, Workflow

@pytest.fixture
async def workflow_sync(session: AsyncSession) -> WorkflowSync:
    """Create a workflow sync."""
    return WorkflowSync(session)

@pytest.fixture
async def test_flow(session: AsyncSession) -> Workflow:
    """Create a test flow."""
    flow = Workflow(
        id=uuid4(),
        name="Test Flow",
        source="test",
        remote_flow_id="test_id",
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

@pytest.fixture
async def test_task(session: AsyncSession, test_flow: Workflow) -> Task:
    """Create a test task."""
    task = Task(
        id=uuid4(),
        workflow_id=test_flow.id,
        status="pending",
        input_data={"input": "test input"},
        created_at=datetime.utcnow()
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

@pytest.mark.asyncio
async def test_successful_flow_execution(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test successful flow execution."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = MagicMock()  # Use MagicMock for response to support status_code comparison
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}  # Match the new response format
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"message": "test input"}  # Match the expected input format
    )

    # Verify result
    assert result == {"result": "success"}
    assert test_task.status == "completed"
    assert test_task.output_data == "success"
    assert test_task.started_at is not None
    assert test_task.error is None

@pytest.mark.asyncio
async def test_failed_flow_execution(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test failed flow execution."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = MagicMock()  # Use MagicMock for response
    mock_response.status_code = 500
    mock_response.text = "API Error"
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow
    with pytest.raises(httpx.HTTPStatusError):
        await workflow_sync.execute_workflow(
            workflow=test_flow,
            task=test_task,
            input_data={"message": "test input"}  # Match the expected input format
        )

    # Verify task status
    assert test_task.status == "failed"
    assert test_task.started_at is not None
    assert "API Error" in test_task.error

@pytest.mark.asyncio
async def test_input_value_handling(
    session: AsyncSession,
    workflow_sync: WorkflowSync,
    test_flow: Workflow,
    test_task: Task
):
    """Test that input_value is correctly passed through the execution chain."""
    # Mock the HTTP client
    mock_client = AsyncMock()
    mock_response = MagicMock()  # Use MagicMock for response
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "specific test value"}  # Match the new response format
    mock_client.post.return_value = mock_response
    workflow_sync._client = mock_client

    # Execute workflow with specific input_value
    result = await workflow_sync.execute_workflow(
        workflow=test_flow,
        task=test_task,
        input_data={"message": "specific test value"}  # Match the expected input format
    )

    # Verify result
    assert result == {"result": "specific test value"}
    assert test_task.status == "completed"
    assert test_task.output_data == "specific test value"
