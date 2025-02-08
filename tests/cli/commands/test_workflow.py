import pytest
from click.testing import CliRunner
from unittest.mock import patch, AsyncMock, MagicMock
import json

from automagik.cli.commands.workflow import workflow_group, sync_flow


def test_sync_flow_with_id(capsys):
    """Test sync_flow command when flow_id is provided."""
    # Mock the necessary dependencies
    mock_session = AsyncMock()
    mock_manager = AsyncMock()
    mock_manager.sync_flow.return_value = {"id": "new-workflow-id"}

    with patch("automagik.cli.commands.workflow.get_session", return_value=mock_session), \
         patch("automagik.cli.commands.workflow.WorkflowManager", return_value=mock_manager):
        # Run command
        runner = CliRunner()
        result = runner.invoke(workflow_group, ["sync", "test-flow-id"])

        # Verify result
        assert result.exit_code == 0
        mock_manager.sync_flow.assert_called_once_with("test-flow-id", source_url=None)
        assert "Successfully synced flow test-flow-id" in result.output


def test_sync_flow_interactive(capsys):
    """Test sync_flow command in interactive mode (no flow_id provided)."""
    # Mock the necessary dependencies
    mock_session = AsyncMock()
    mock_manager = AsyncMock()
    mock_manager.list_remote_flows.return_value = {
        "flows": [
            {"id": "flow1", "name": "Flow 1", "description": "Test flow 1", "source_url": "http://test.com"},
            {"id": "flow2", "name": "Flow 2", "description": "Test flow 2", "source_url": "http://test.com"},
        ]
    }
    mock_manager.sync_flow.return_value = {"id": "new-workflow-id"}

    with patch("automagik.cli.commands.workflow.get_session", return_value=mock_session), \
         patch("automagik.cli.commands.workflow.WorkflowManager", return_value=mock_manager):
        # Run command with simulated user input
        runner = CliRunner()
        result = runner.invoke(workflow_group, ["sync"], input="1\n")

        # Verify result
        assert result.exit_code == 0
        mock_manager.list_remote_flows.assert_called_once()
        mock_manager.sync_flow.assert_called_once_with("flow1", source_url="http://test.com")


def test_sync_flow_no_flows(capsys):
    """Test sync_flow command when no flows are available."""
    # Mock the necessary dependencies
    mock_session = AsyncMock()
    mock_manager = AsyncMock()
    mock_manager.list_remote_flows.return_value = {"flows": []}

    with patch("automagik.cli.commands.workflow.get_session", return_value=mock_session), \
         patch("automagik.cli.commands.workflow.WorkflowManager", return_value=mock_manager):
        # Run command
        runner = CliRunner()
        result = runner.invoke(workflow_group, ["sync"])

        # Verify result
        assert result.exit_code == 0
        mock_manager.list_remote_flows.assert_called_once()
        assert "No flows found" in result.output


def test_sync_flow_invalid_selection(capsys):
    """Test sync_flow command with invalid flow selection."""
    # Mock the necessary dependencies
    mock_session = AsyncMock()
    mock_manager = AsyncMock()
    mock_manager.list_remote_flows.return_value = {
        "flows": [
            {"id": "flow1", "name": "Flow 1", "description": "Test flow 1", "source_url": "http://test.com"},
            {"id": "flow2", "name": "Flow 2", "description": "Test flow 2", "source_url": "http://test.com"},
        ]
    }

    with patch("automagik.cli.commands.workflow.get_session", return_value=mock_session), \
         patch("automagik.cli.commands.workflow.WorkflowManager", return_value=mock_manager):
        # Run command with simulated user input
        runner = CliRunner()
        result = runner.invoke(workflow_group, ["sync"], input="3\n")

        # Verify result
        assert result.exit_code == 0
        mock_manager.list_remote_flows.assert_called_once()
        mock_manager.sync_flow.assert_not_called()


def test_sync_flow_invalid_component_response(capsys):
    """Test sync_flow command when component API returns invalid response."""
    # Mock the necessary dependencies
    mock_session = AsyncMock()
    mock_manager = AsyncMock()
    mock_manager.list_remote_flows.return_value = {
        "flows": [
            {"id": "flow1", "name": "Flow 1", "description": "Test flow 1", "source_url": "http://test.com"},
        ]
    }
    mock_manager.sync_flow.return_value = None

    with patch("automagik.cli.commands.workflow.get_session", return_value=mock_session), \
         patch("automagik.cli.commands.workflow.WorkflowManager", return_value=mock_manager):
        # Run command with simulated user input
        runner = CliRunner()
        result = runner.invoke(workflow_group, ["sync"], input="1\n")

        # Verify result
        assert result.exit_code == 0
        mock_manager.list_remote_flows.assert_called_once()
        mock_manager.sync_flow.assert_called_once_with("flow1", source_url="http://test.com")
        assert "Failed to sync flow" in result.output
