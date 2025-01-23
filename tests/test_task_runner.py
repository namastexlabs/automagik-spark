import uuid
import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from sqlalchemy.orm import Session
from automagik.core.scheduler.task_runner import TaskRunner
from automagik.core.scheduler.exceptions import TaskExecutionError, FlowNotFoundError, ComponentNotConfiguredError
from automagik.core.database.models import Task, FlowDB, Log

@pytest.fixture
def mock_session():
    session = Mock(spec=Session)
    session.commit = Mock()
    session.rollback = Mock()
    return session

@pytest.fixture
def mock_langflow_client():
    client = Mock()
    client.process_flow = AsyncMock()
    return client

@pytest.fixture
def task_runner(mock_session, mock_langflow_client):
    return TaskRunner(mock_session, mock_langflow_client)

@pytest.fixture
def sample_flow():
    return FlowDB(
        id=uuid.uuid4(),
        name="Test Flow",
        input_component="input_node",
        output_component="output_node",
        data={
            "tweaks": {
                "input_node": {"value": "test"}
            }
        }
    )

@pytest.fixture
def sample_task(sample_flow):
    return Task(
        id=uuid.uuid4(),
        flow_id=sample_flow.id,
        flow=sample_flow,
        input_data={"message": "test"},
        status="pending",
        tries=0
    )

@pytest.mark.asyncio
async def test_create_task(task_runner, mock_session, sample_flow):
    # Setup
    flow_id = sample_flow.id
    input_data = {"message": "test"}
    mock_session.query.return_value.filter.return_value.first.return_value = sample_flow

    # Execute
    task = await task_runner.create_task(flow_id, input_data)

    # Verify
    assert task.flow_id == flow_id
    assert task.input_data == input_data
    assert task.status == "pending"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_create_task_flow_not_found(task_runner, mock_session):
    # Setup
    flow_id = uuid.uuid4()
    mock_session.query.return_value.filter.return_value.first.return_value = None

    # Execute and verify
    with pytest.raises(FlowNotFoundError):
        await task_runner.create_task(flow_id)

@pytest.mark.asyncio
async def test_run_task_success(task_runner, mock_session, mock_langflow_client, sample_task):
    # Setup
    mock_session.query.return_value.filter.return_value.first.return_value = sample_task
    mock_langflow_client.process_flow.return_value = {
        "session_id": "test_session",
        "outputs": [{
            "outputs": [{
                "messages": [{"text": "test response"}],
                "artifacts": {"file": "test.txt"},
                "logs": {"node1": ["log1", "log2"]}
            }]
        }]
    }

    # Execute
    result = await task_runner.run_task(sample_task.id)

    # Verify
    assert result.status == "completed"
    assert result.tries == 1
    mock_langflow_client.process_flow.assert_called_once_with(
        flow_id=str(sample_task.flow.id),
        input_data=sample_task.input_data,
        tweaks=sample_task.flow.data["tweaks"]
    )

@pytest.mark.asyncio
async def test_run_task_not_found(task_runner, mock_session):
    # Setup
    task_id = uuid.uuid4()
    mock_session.query.return_value.filter.return_value.first.return_value = None

    # Execute and verify
    with pytest.raises(TaskExecutionError):
        await task_runner.run_task(task_id)

@pytest.mark.asyncio
async def test_run_task_no_input_component(task_runner, mock_session, sample_task):
    # Setup
    sample_task.flow.input_component = None
    mock_session.query.return_value.filter.return_value.first.return_value = sample_task

    # Execute and verify
    with pytest.raises(ComponentNotConfiguredError):
        await task_runner.run_task(sample_task.id)

@pytest.mark.asyncio
async def test_run_task_execution_error(task_runner, mock_session, mock_langflow_client, sample_task):
    # Setup
    mock_session.query.return_value.filter.return_value.first.return_value = sample_task
    mock_langflow_client.process_flow.side_effect = Exception("API Error")

    # Execute and verify
    with pytest.raises(TaskExecutionError) as exc_info:
        await task_runner.run_task(sample_task.id)
    
    assert "API Error" in str(exc_info.value)
    assert sample_task.status == "failed"
    assert sample_task.tries == 1

def test_extract_output_data(task_runner):
    # Setup
    response = {
        "session_id": "test_session",
        "outputs": [{
            "outputs": [{
                "messages": [{"text": "test message"}],
                "artifacts": {"file": "test.txt"},
                "logs": {"node1": ["log1", "log2"]}
            }]
        }]
    }

    # Execute
    output = task_runner._extract_output_data(response)

    # Verify
    assert output["session_id"] == "test_session"
    assert len(output["messages"]) == 1
    assert output["messages"][0]["text"] == "test message"
    assert len(output["artifacts"]) == 1
    assert output["artifacts"][0]["file"] == "test.txt"
    assert len(output["logs"]) == 2
    assert "log1" in output["logs"]
    assert "log2" in output["logs"]

def test_log_message(task_runner, mock_session):
    # Setup
    task_id = uuid.uuid4()
    level = "INFO"
    message = "Test log message"

    # Execute
    task_runner._log_message(task_id, level, message)

    # Verify
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    log = mock_session.add.call_args[0][0]
    assert isinstance(log, Log)
    assert log.task_id == task_id
    assert log.level == level
    assert log.message == message

def test_log_message_error(task_runner, mock_session):
    # Setup
    task_id = uuid.uuid4()
    mock_session.add.side_effect = Exception("Database error")

    # Execute
    task_runner._log_message(task_id, "INFO", "test")

    # Verify
    mock_session.rollback.assert_called_once()
