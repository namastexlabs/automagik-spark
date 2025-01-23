"""Tests for run-related CLI commands"""
import pytest
import uuid
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from automagik.cli.commands.run import run
from automagik.core.database.models import Task

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

    def test_invalid_schedule_id(self, runner, mock_db_session, caplog):
        """Test handling invalid schedule ID"""
        # Mock the scheduler service to raise an error for invalid UUID
        mock_scheduler = MagicMock()
        mock_scheduler.get_schedule.side_effect = ValueError("Invalid UUID format")

        with patch('automagik.cli.commands.run.SchedulerService', return_value=mock_scheduler), \
             patch('automagik.cli.commands.run.get_db_session', return_value=mock_db_session):
            result = runner.invoke(run, ['test', 'invalid-id'], catch_exceptions=False)

        assert result.exit_code != 0
        assert any("Error testing schedule" in record.message for record in caplog.records)
