import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch, AsyncMock
import uuid
from datetime import datetime, timedelta
from automagik.core.database.models import FlowDB, Schedule, Task

# Test data
TEST_FLOW_ID = str(uuid.uuid4())
TEST_SCHEDULE_ID = str(uuid.uuid4())
TEST_TASK_ID = str(uuid.uuid4())

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_db_session():
    """Mock database session"""
    with patch('automagik.core.database.get_db_session') as mock:
        session = mock()
        session.add = MagicMock()
        session.commit = MagicMock()
        
        # Mock query builder
        query = MagicMock()
        query.all = MagicMock()
        query.filter = MagicMock(return_value=query)
        query.first = MagicMock()
        query.execute = MagicMock()
        session.query = MagicMock(return_value=query)
        yield session

@pytest.fixture
def mock_langflow_client():
    """Mock LangFlow client"""
    with patch('automagik.core.services.langflow_client.LangflowClient') as mock:
        client = mock.return_value
        # Mock the async methods
        client.get_flows = MagicMock(return_value=[{
            'id': TEST_FLOW_ID,
            'name': 'Test Flow',
            'description': 'Test flow description'
        }])
        client.get_flow = MagicMock()
        client.run_flow = AsyncMock()
        yield client

@pytest.fixture
def mock_task_runner():
    """Mock TaskRunner"""
    with patch('automagik.core.services.task_runner.TaskRunner') as mock:
        runner = mock.return_value
        runner.process_schedules = MagicMock()
        runner.run_task = AsyncMock()
        yield runner

@pytest.fixture
def sample_flow():
    """Create a sample flow for testing"""
    return FlowDB(
        id=uuid.uuid4(),
        name="Test Flow",
        description="A test flow",
        source="langflow",
        source_id="test-flow-1",
        flow_version=1,
        folder_name="test-folder"
    )

@pytest.fixture
def sample_schedule(sample_flow):
    """Create a sample schedule for testing"""
    return Schedule(
        id=uuid.UUID(TEST_SCHEDULE_ID),
        flow_id=sample_flow.id,
        flow=sample_flow,
        schedule_type="interval",
        schedule_expr="5m",
        next_run_at=datetime.utcnow() + timedelta(minutes=1),
        status="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
