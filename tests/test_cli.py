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

class TestScheduleCommands:
    """Test schedule-related CLI commands"""

    def test_schedules_list(self, runner, mock_db_session, sample_schedule, sample_flow, monkeypatch):
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
        
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def get_schedules(self, schedule_type=None, status=None):
                return [sample_schedule]

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(sample_schedule.id) in result.output
        assert sample_schedule.schedule_type in result.output
        assert sample_schedule.schedule_expr in result.output
        assert sample_schedule.status in result.output
        assert "2025-01-23 04:51:38" in result.output

    def test_schedules_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a schedule"""
        # Mock the flow relationship and query results
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0

        # Mock the scheduler service
        from automagik.core.scheduler.scheduler import SchedulerService
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                pass

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                return type('MockSchedule', (), {
                    'id': uuid.uuid4(),
                    'next_run_at': datetime.now()
                })

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)

        # Simulate user input:
        # 0 - Select the first flow
        # 0 - Select interval type
        # 5m - Set interval to 5 minutes
        # y - Yes to set input value
        # vai filhote - The input value
        result = runner.invoke(schedules, ['create'], input='0\n0\n5m\ny\nvai filhote\n')

        assert result.exit_code == 0
        assert "Schedule created successfully" in result.output

    def test_invalid_json_input(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test handling invalid JSON input"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                pass

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                return type('MockSchedule', (), {
                    'id': uuid.uuid4(),
                    'next_run_at': datetime.now()
                })

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)

        # Mock the flow query
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0

        # Since the CLI accepts any string input, we'll test that it properly wraps it in a dict
        result = runner.invoke(schedules, ['create'], input='0\n0\n5m\ny\n{invalid json}\n')
        assert result.exit_code == 0
        assert "Schedule created successfully" in result.output

    def test_oneshot_schedule_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    schedule = Schedule(
                        id=uuid.uuid4(),
                        schedule_type='oneshot',
                        schedule_expr=schedule_expr,
                        next_run_at=datetime.fromisoformat(schedule_expr),
                        status='active',
                        flow=sample_flow,
                        flow_id=sample_flow.id
                    )
                    return schedule
                raise Exception("Unexpected schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Create a one-time schedule for tomorrow
        future_time = datetime.now() + timedelta(days=1)
        schedule_time = future_time.strftime("%Y-%m-%dT%H:%M:%S")
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,  # Pass flow name directly
            '--type', 'oneshot',
            '--expr', schedule_time,
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 0
        assert "Created schedule" in result.output
        assert "oneshot" in result.output
        assert schedule_time in result.output

    def test_oneshot_schedule_past_time(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule with past time"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    dt = datetime.fromisoformat(schedule_expr)
                    if dt <= datetime.now():
                        from automagik.core.scheduler.exceptions import InvalidScheduleError
                        raise InvalidScheduleError("One-time schedule must be in the future")
                return Schedule(
                    id=uuid.uuid4(),
                    next_run_at=datetime.now()
                )

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Try to create a schedule for yesterday
        past_time = datetime.now() - timedelta(days=1)
        schedule_time = past_time.strftime("%Y-%m-%dT%H:%M:%S")
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,  # Pass flow name directly
            '--type', 'oneshot',
            '--expr', schedule_time,
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code != 0
        assert "One-time schedule must be in the future" in result.output

    def test_oneshot_schedule_invalid_format(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule with invalid datetime format"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    try:
                        datetime.fromisoformat(schedule_expr)
                    except ValueError as e:
                        from automagik.core.scheduler.exceptions import InvalidScheduleError
                        raise InvalidScheduleError(f"Invalid datetime format: {str(e)}")
                return Schedule(
                    id=uuid.uuid4(),
                    next_run_at=datetime.now()
                )

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Try to create a schedule with invalid datetime format
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,  # Pass flow name directly
            '--type', 'oneshot',
            '--expr', '2025-13-45 25:99:99',  # Invalid datetime
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code != 0
        assert "Invalid datetime format" in result.output

    def test_list_oneshot_schedules(self, runner, mock_db_session, sample_flow):
        """Test listing one-time schedules with different statuses"""
        # Create sample one-time schedules
        future_time = datetime.now() + timedelta(days=1)
        past_time = datetime.now() - timedelta(hours=1)

        active_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=future_time.isoformat(),
            next_run_at=future_time,
            status="active"
        )

        completed_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=past_time.isoformat(),
            next_run_at=past_time,
            status="completed"
        )

        # Mock the query to return both schedules
        mock_db_session.query.return_value.all.return_value = [active_schedule, completed_schedule]

        # Test listing all schedules
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) in result.output
        assert "oneshot" in result.output
        assert "active" in result.output
        assert "completed" in result.output

        # Test filtering by type
        mock_db_session.query.return_value.filter.return_value.all.return_value = [active_schedule, completed_schedule]
        result = runner.invoke(schedules, ['list', '--type', 'oneshot'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) in result.output

        # Test filtering by status
        mock_db_session.query.return_value.filter.return_value.all.return_value = [completed_schedule]
        result = runner.invoke(schedules, ['list', '--status', 'completed'])
        assert result.exit_code == 0
        assert str(completed_schedule.id) in result.output
        assert str(active_schedule.id) not in result.output

    def test_invalid_schedule_type(self, runner, mock_db_session, sample_flow):
        """Test creating schedule with invalid type"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow
        mock_db_session.query.return_value.all.return_value = [sample_flow]
        
        result = runner.invoke(schedules, ['create'], input='0\n99\n')  # Invalid schedule type
        assert "Invalid schedule type" in result.output

class TestRunCommands:
    """Test run-related CLI commands"""

    def test_run_test(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test running a test"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                pass

            def get_schedule(self, schedule_id):
                return type('MockSchedule', (), {
                    'id': schedule_id,
                    'flow': sample_flow,
                    'flow_id': sample_flow.id,
                    'schedule_type': 'interval',
                    'schedule_expr': '5m',
                    'flow_params': {'input': 'test'}
                })

        monkeypatch.setattr('automagik.cli.commands.run.SchedulerService', MockSchedulerService)

        # Mock the task runner
        class MockTaskRunner:
            def __init__(self, *args, **kwargs):
                pass

            def create_task(self, flow_id, input_data):
                return type('MockTask', (), {'id': uuid.uuid4()})

            def run_task(self, task_id):
                return {"status": "success", "message": "Test completed"}

            async def create_task_async(self, flow_id, input_data):
                return self.create_task(flow_id, input_data)

            async def run_task_async(self, task_id):
                return self.run_task(task_id)

        monkeypatch.setattr('automagik.cli.commands.run.TaskRunner', MockTaskRunner)

        # Mock the LangflowClient
        class MockLangflowClient:
            def __init__(self, *args, **kwargs):
                pass

        monkeypatch.setattr('automagik.cli.commands.run.LangflowClient', MockLangflowClient)

        result = runner.invoke(run, ['test', str(uuid.uuid4())])
        
        assert result.exit_code == 0
        assert "Test completed" in result.output

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

class TestScheduleCommands:
    """Test schedule commands"""

    def test_schedules_list(self, runner, mock_db_session, sample_schedule, sample_flow, monkeypatch):
        """Test listing schedules"""
        # Set specific values to match expected output
        sample_flow.name = "WhatsApp Audio to Message Automation 1D (prod)"
        sample_schedule.id = uuid.UUID("3cf82804-41b2-4731-9306-f77e17193799")
        sample_schedule.schedule_type = "interval"
        sample_schedule.schedule_expr = "1m"
        sample_schedule.status = "active"
        sample_schedule.next_run_at = datetime(2025, 1, 23, 4, 51, 38)
        sample_schedule.flow = sample_flow

        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def get_schedules(self, schedule_type=None, status=None):
                return [sample_schedule]

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(sample_schedule.id) in result.output

    def test_schedules_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a schedule"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                return Schedule(
                    id=uuid.uuid4(),
                    next_run_at=datetime.now(),
                    status='active',
                    schedule_type=schedule_type,
                    schedule_expr=schedule_expr,
                    flow=sample_flow,
                    flow_id=sample_flow.id
                )

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.all.return_value = [sample_flow]

        # Test creating a schedule in non-interactive mode
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'interval',
            '--expr', '5m',
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 0
        assert "Created schedule successfully" in result.output

    def test_invalid_json_input(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test handling invalid JSON input"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                return Schedule(
                    id=uuid.uuid4(),
                    next_run_at=datetime.now(),
                    status='active',
                    schedule_type=schedule_type,
                    schedule_expr=schedule_expr,
                    flow=sample_flow,
                    flow_id=sample_flow.id
                )

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Test invalid JSON input
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'interval',
            '--expr', '5m',
            '--input', '{invalid json}'
        ])

        assert result.exit_code == 1
        assert "Invalid JSON input" in result.output

    def test_oneshot_schedule_create(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    dt = datetime.fromisoformat(schedule_expr)
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=dt,
                        status='active',
                        schedule_type='oneshot',
                        schedule_expr=schedule_expr,
                        flow=sample_flow,
                        flow_id=sample_flow.id
                    )
                raise Exception("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test creating a one-time schedule
        future_time = datetime.now() + timedelta(days=1)
        schedule_time = future_time.strftime("%Y-%m-%dT%H:%M:%S")
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'oneshot',
            '--expr', schedule_time,
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 0
        assert "Created schedule successfully" in result.output

    def test_oneshot_schedule_past_time(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule with past time"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    dt = datetime.fromisoformat(schedule_expr)
                    if dt <= datetime.now():
                        from automagik.core.scheduler.exceptions import InvalidScheduleError
                        raise InvalidScheduleError("One-time schedule must be in the future")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=dt,
                        status='active',
                        schedule_type='oneshot',
                        schedule_expr=schedule_expr,
                        flow=sample_flow,
                        flow_id=sample_flow.id
                    )
                raise Exception("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Try to create a schedule for yesterday
        past_time = datetime.now() - timedelta(days=1)
        schedule_time = past_time.strftime("%Y-%m-%dT%H:%M:%S")
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'oneshot',
            '--expr', schedule_time,
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 1
        assert "One-time schedule must be in the future" in result.output

    def test_oneshot_schedule_invalid_format(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test creating a one-time schedule with invalid datetime format"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                if schedule_type == 'oneshot':
                    try:
                        dt = datetime.fromisoformat(schedule_expr)
                    except ValueError:
                        from automagik.core.scheduler.exceptions import InvalidScheduleError
                        raise InvalidScheduleError("Invalid datetime format")
                    return Schedule(
                        id=uuid.uuid4(),
                        next_run_at=dt,
                        status='active',
                        schedule_type='oneshot',
                        schedule_expr=schedule_expr,
                        flow=sample_flow,
                        flow_id=sample_flow.id
                    )
                raise Exception("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test invalid datetime format
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'oneshot',
            '--expr', 'invalid-date',
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 1
        assert "Invalid datetime format" in result.output

    def test_list_oneshot_schedules(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test listing one-time schedules with different statuses"""
        # Create sample one-time schedules
        future_time = datetime.now() + timedelta(days=1)
        past_time = datetime.now() - timedelta(hours=1)

        active_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=future_time.isoformat(),
            next_run_at=future_time,
            status="active"
        )

        completed_schedule = Schedule(
            id=uuid.uuid4(),
            flow_id=sample_flow.id,
            flow=sample_flow,
            schedule_type="oneshot",
            schedule_expr=past_time.isoformat(),
            next_run_at=past_time,
            status="completed"
        )

        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def get_schedules(self, schedule_type=None, status=None):
                schedules = [active_schedule, completed_schedule]
                if schedule_type:
                    schedules = [s for s in schedules if s.schedule_type == schedule_type]
                if status:
                    schedules = [s for s in schedules if s.status == status]
                return schedules

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Test listing all schedules
        result = runner.invoke(schedules, ['list'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) in result.output

        # Test filtering by type
        result = runner.invoke(schedules, ['list', '--type', 'oneshot'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) in result.output

        # Test filtering by status
        result = runner.invoke(schedules, ['list', '--status', 'active'])
        assert result.exit_code == 0
        assert str(active_schedule.id) in result.output
        assert str(completed_schedule.id) not in result.output

    def test_invalid_schedule_type(self, runner, mock_db_session, sample_flow, monkeypatch):
        """Test handling invalid schedule type"""
        # Mock the scheduler service
        class MockSchedulerService:
            def __init__(self, *args, **kwargs):
                self.db_session = mock_db_session

            def create_schedule(self, flow_name, schedule_type, schedule_expr, flow_params):
                raise Exception("Invalid schedule type")

        monkeypatch.setattr('automagik.cli.commands.schedules.SchedulerService', MockSchedulerService)
        monkeypatch.setattr('automagik.cli.commands.schedules.get_db_session', lambda: mock_db_session)

        # Mock the flow query
        mock_db_session.query.return_value.filter.return_value.first.return_value = sample_flow

        # Test invalid schedule type
        result = runner.invoke(schedules, [
            'create',
            sample_flow.name,
            '--type', 'invalid',
            '--expr', '5m',
            '--input', '{"key": "value"}'
        ])

        assert result.exit_code == 2  # Click returns 2 for invalid choice
        assert "Invalid value for '--type'" in result.output
