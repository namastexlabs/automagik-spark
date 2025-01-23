"""Tests for flow-related CLI commands"""
import pytest
import uuid
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from automagik.cli.commands.flows import flows
from automagik.core.database.models import FlowDB

@pytest.fixture
def runner():
    """Create a CLI runner"""
    return CliRunner()

@pytest.fixture
def mock_db_session():
    """Create a mock database session"""
    return MagicMock()

@pytest.fixture
def sample_flow():
    """Create a sample flow"""
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
def mock_langflow_client():
    """Create a mock LangFlow client"""
    return MagicMock()

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
