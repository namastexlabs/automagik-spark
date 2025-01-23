"""
Test CLI Commands

This module contains tests for the AutoMagik CLI commands.
"""

import os
import pytest
import uuid
import json
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta

from automagik.cli.commands.flows import flows
from automagik.cli.commands.run import run
from automagik.core.database.models import FlowDB, Schedule, Task
from automagik.core.services.langflow_client import LangflowClient
from automagik.core.services.task_runner import TaskRunner

# Test data
TEST_FLOW_ID = str(uuid.uuid4())
TEST_SCHEDULE_ID = str(uuid.uuid4())
TEST_TASK_ID = str(uuid.uuid4())

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
def runner():
    """Click test runner"""
    return CliRunner()

@pytest.fixture
def sample_flow(mock_db_session):
    """Create a sample flow for testing"""
    flow = FlowDB(
        id=uuid.uuid4(),
        name='Test Flow',
        description='A test flow',
        data={'nodes': [], 'edges': []},
        source='langflow',
        source_id=str(uuid.uuid4()),
        folder_id=str(uuid.uuid4()),
        folder_name='test-folder',
        flow_version=1,
        input_component='test_input'  # Add input component
    )
    return flow

@pytest.fixture
def sample_schedule():
    """Sample schedule data"""
    return Schedule(
        id=uuid.UUID(TEST_SCHEDULE_ID),
        flow_id=uuid.UUID(TEST_FLOW_ID),
        schedule_type="interval",
        schedule_expr="1m",
        status="active",
        next_run_at=datetime.utcnow() + timedelta(minutes=1),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

class TestFlowCommands:
    """Test flow-related CLI commands"""

    def test_flows_list(self, runner, mock_db_session, sample_flow):
        """Test listing flows"""
        # Set specific values for the flow to match expected output
        sample_flow.name = "WhatsApp Audio to Message Automation 1D (prod)"
        sample_flow.folder_name = "whatsapp-pal"
        sample_flow.id = uuid.UUID("9b6b04c3-64d0-4a02-a3ef-a9ae126b733d")
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        assert str(sample_flow.id) in result.output
        assert sample_flow.name in result.output
        assert sample_flow.folder_name in result.output

    @pytest.mark.asyncio
    async def test_flows_sync(self, runner, mock_db_session, mock_langflow_client):
        """Test syncing flows"""
        result = runner.invoke(flows, ['sync'], input='0\n')
        assert result.exit_code == 0
        assert "Flow synced successfully" in result.output

class TestRunCommands:
    """Test run-related CLI commands"""

    def test_run_test(self, runner, mock_db_session, sample_flow):
        """Test running a test"""
        # Create a mock task with the required attributes
        task_id = uuid.uuid4()
        mock_task = Task(
            id=task_id,
            flow_id=sample_flow.id,
            input_data={'input': 'test'},
            status="created"
        )

        # Mock the task runner
        mock_task_runner = MagicMock()
        mock_task_runner.create_task = MagicMock(return_value=mock_task)
        mock_task_runner.run_task = MagicMock(return_value={"status": "success", "message": "Test completed"})

        # Mock the scheduler service
        mock_scheduler = MagicMock()
        mock_scheduler.get_schedule = MagicMock(return_value=type('MockSchedule', (), {
            'id': uuid.uuid4(),
            'flow': sample_flow,
            'flow_id': sample_flow.id,
            'schedule_type': 'interval',
            'schedule_expr': '5m',
            'flow_params': {'input': 'test'}
        }))

        # Mock the LangflowClient
        mock_langflow = MagicMock()

        with patch('automagik.cli.commands.run.SchedulerService', return_value=mock_scheduler), \
             patch('automagik.cli.commands.run.TaskRunner', return_value=mock_task_runner), \
             patch('automagik.cli.commands.run.LangflowClient', return_value=mock_langflow), \
             patch('automagik.cli.commands.run.get_db_session', return_value=mock_db_session):
            result = runner.invoke(run, ['test', str(uuid.uuid4())])

        assert result.exit_code == 0
        assert "Created task" in result.output or "Test completed" in result.output

    def test_run_start_no_daemon(self, runner, mock_task_runner, caplog):
        """Test starting task processor without daemon mode"""
        with patch('automagik.cli.commands.run.TaskRunner', return_value=mock_task_runner):
            try:
                runner.invoke(run, ['start'], catch_exceptions=False)
            except RuntimeError:
                pass  # Expected asyncio error
            
            assert any("Starting AutoMagik service" in record.message for record in caplog.records)

    def test_invalid_flow_id(self, runner, mock_db_session):
        """Test handling invalid flow ID"""
        # Mock the query result to return an empty list
        mock_query = mock_db_session.query.return_value
        mock_query.all.return_value = []
        mock_query.filter.return_value.first.return_value = None
        mock_query.execute.return_value.fetchall.return_value = []

        # Mock get_db_session to return our mocked session
        from automagik.core.database import get_db_session
        from unittest.mock import patch
        with patch('automagik.cli.commands.flows.get_db_session', return_value=mock_db_session):
            result = runner.invoke(flows, ['list'])
            assert result.exit_code == 0
            # When no flows are present, expect only the header line
            assert "No flows found" in result.output
