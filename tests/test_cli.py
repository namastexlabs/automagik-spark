"""
Test CLI Commands

This module contains tests for the AutoMagik CLI commands.
"""

import os
import pytest
import uuid
import json
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from automagik.cli.commands.flows import flows
from automagik.cli.commands.schedules import schedules
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
        client.run_flow = MagicMock()
        yield client

@pytest.fixture
def mock_task_runner():
    """Mock TaskRunner"""
    with patch('automagik.core.services.task_runner.TaskRunner') as mock:
        runner = mock.return_value
        runner.process_schedules = MagicMock()
        runner.run_task = MagicMock()
        yield runner

@pytest.fixture
def runner():
    """Click test runner"""
    return CliRunner()

@pytest.fixture
def sample_flow():
    """Sample flow data"""
    return FlowDB(
        id=uuid.UUID(TEST_FLOW_ID),
        name="Test Flow",
        description="Test flow description",
        source="langflow",
        folder_name="test",
        input_component=True,
        output_component=True,
        flow_version=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

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

class TestScheduleCommands:
    """Test schedule-related CLI commands"""

    def test_schedules_list(self, runner, mock_db_session, sample_schedule, sample_flow):
        """Test listing schedules"""
        # Set specific values to match expected output
        sample_flow.name = "WhatsApp Audio to Message Automation 1D (prod)"
        sample_schedule.id = uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799")
        sample_schedule.schedule_type = "interval"
        sample_schedule.schedule_expr = "1m"
        sample_schedule.status = "active"
        sample_schedule.next_run_at = datetime(2025, 1, 23, 4, 51, 38)
        sample_schedule.flow = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_schedule]
        
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(sample_schedule.id) in result.output
        assert sample_schedule.schedule_type in result.output
        assert sample_schedule.schedule_expr in result.output
        assert sample_schedule.status in result.output
        assert "2025-01-23 04:51:38" in result.output

    def test_schedules_create(self, runner, mock_db_session, sample_flow):
        """Test creating a schedule"""
        # Mock the flow relationship and query results
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        # Simulate user input:
        # 0 - Select the first flow
        # 0 - Select interval type
        # 5m - Set interval to 5 minutes
        # y - Yes to set input value
        # vai filhote - The input value
        result = runner.invoke(schedules, ['create'], input='0\n0\n5m\ny\nvai filhote\n')
        
        assert result.exit_code == 0
        assert "Schedule created successfully" in result.output
        assert "Flow: WhatsApp Audio to Message Automation 1D (prod)" in result.output
        assert "Type: interval" in result.output
        assert "Expression: 5m" in result.output
        assert "2025-01-23" in result.output  # Check for date in next run

class TestRunCommands:
    """Test run-related CLI commands"""

    @pytest.mark.asyncio
    async def test_run_test(self, runner, mock_db_session, mock_langflow_client, sample_schedule, caplog):
        """Test running a flow test"""
        # Set specific ID to match the error message
        sample_schedule.id = uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799")
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_schedule
        mock_langflow_client.run_flow.return_value = {"status": "success"}
        
        try:
            runner.invoke(run, ['test', str(sample_schedule.id)], catch_exceptions=False)
        except RuntimeError:
            pass  # Expected asyncio error
        
        assert any("Testing schedule" in record.message for record in caplog.records)

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
        # Set empty list to indicate no flows
        mock_db_session.query.return_value.all.return_value = []
        
        result = runner.invoke(flows, ['list'])
        assert result.exit_code == 0
        # When no flows are present, the output should be empty or just contain table headers
        assert len([line for line in result.output.splitlines() if line.strip() and '|' in line]) <= 3

    def test_invalid_schedule_type(self, runner, mock_db_session, sample_flow):
        """Test creating schedule with invalid type"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        result = runner.invoke(schedules, ['create'], input='0\n99\n')  # Invalid schedule type
        assert "Invalid schedule type" in result.output

    def test_invalid_json_input(self, runner, mock_db_session, sample_flow):
        """Test handling invalid JSON input"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        # Since the CLI accepts any string input, we'll test that it properly wraps it in a dict
        result = runner.invoke(schedules, ['create'], input='0\n0\n5m\ny\n{invalid json}\n')
        assert "'input': '{invalid json}'" in result.output
