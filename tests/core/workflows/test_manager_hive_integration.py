"""Test WorkflowManager integration with AutoMagik Hive."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from automagik_spark.core.workflows.manager import WorkflowManager
from automagik_spark.core.workflows.automagik_hive import AutomagikHiveManager
from automagik_spark.core.database.models import WorkflowSource
from automagik_spark.core.schemas.source import SourceType


class TestWorkflowManagerHiveIntegration:
    """Test WorkflowManager integration with AutoMagik Hive."""

    @pytest.fixture
    def mock_session(self):
        """Mock async session."""
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def workflow_manager(self, mock_session):
        """Create WorkflowManager with mock session."""
        return WorkflowManager(mock_session)

    @pytest.fixture
    def mock_hive_source(self):
        """Mock AutoMagik Hive source."""
        source = MagicMock(spec=WorkflowSource)
        source.id = uuid4()
        source.url = "http://localhost:8886"
        source.source_type = SourceType.AUTOMAGIK_HIVE
        source.encrypted_api_key = "encrypted_key"
        return source

    @pytest.fixture
    def mock_hive_flows(self):
        """Mock Hive flows response."""
        return [
            {
                "id": "master-genie",
                "name": "Master Genie Agent",
                "description": "Ultimate development companion",
                "data": {"type": "hive_agent"},
                "folder_name": "Agents",
                "tags": ["agent", "hive"]
            },
            {
                "id": "genie-team",
                "name": "Genie Team",
                "description": "Multi-agent development team", 
                "data": {"type": "hive_team", "members_count": 3},
                "folder_name": "Teams",
                "tags": ["team", "multi-agent", "hive"]
            },
            {
                "id": "dev-workflow",
                "name": "Development Workflow",
                "description": "Complete development process",
                "data": {"type": "hive_workflow", "steps": [{"step_id": "analyze"}]},
                "folder_name": "Workflows", 
                "tags": ["workflow", "multi-step", "hive"]
            }
        ]

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key')
    async def test_get_source_manager_hive(self, mock_decrypt, workflow_manager, mock_hive_source):
        """Test getting AutoMagik Hive source manager."""
        mock_decrypt.return_value = "decrypted_key"
        
        manager = await workflow_manager._get_source_manager(source=mock_hive_source)
        
        assert isinstance(manager, AutomagikHiveManager)
        assert manager.api_url == "http://localhost:8886"
        assert manager.api_key == "decrypted_key"
        assert manager.source_id == mock_hive_source.id

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key')
    async def test_list_remote_flows_hive(self, mock_decrypt, 
                                        workflow_manager, mock_hive_source, mock_hive_flows):
        """Test listing remote flows from Hive source."""
        mock_decrypt.return_value = "decrypted_key"
        
        # Mock manager instance
        mock_manager = MagicMock()
        mock_manager.list_flows_sync.return_value = mock_hive_flows
        mock_manager.api_url = mock_hive_source.url
        
        with patch.object(workflow_manager, '_get_source_manager', return_value=mock_manager):
            # Mock session query for sources
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [mock_hive_source]
            workflow_manager.session.execute.return_value = mock_result
            
            flows = await workflow_manager.list_remote_flows(source_url=mock_hive_source.url)
            
            assert len(flows) == 3
            assert flows[0]["id"] == "master-genie"
            assert flows[1]["id"] == "genie-team" 
            assert flows[2]["id"] == "dev-workflow"
            
            # Check that source info was added
            for flow in flows:
                assert flow["source_url"] == mock_hive_source.url
                assert "instance" in flow

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key')
    async def test_get_remote_flow_hive(self, mock_decrypt,
                                      workflow_manager, mock_hive_source, mock_hive_flows):
        """Test getting specific remote flow from Hive source."""
        mock_decrypt.return_value = "decrypted_key"
        
        # Mock the _get_source_manager method to return a mock manager
        mock_manager = AsyncMock()
        mock_manager.get_flow.return_value = mock_hive_flows[0]  # Return master-genie
        mock_manager.api_url = mock_hive_source.url
        
        with patch.object(workflow_manager, '_get_source_manager', return_value=mock_manager):
            # Mock session query for source
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = mock_hive_source
            workflow_manager.session.execute.return_value = mock_result
            
            flow = await workflow_manager.get_remote_flow("master-genie", mock_hive_source.url)
            
            assert flow is not None
            assert flow["id"] == "master-genie"
            assert flow["data"]["type"] == "hive_agent"
            assert flow["source_url"] == mock_hive_source.url

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key')
    async def test_sync_flow_hive(self, mock_decrypt,
                                workflow_manager, mock_hive_source, mock_hive_flows):
        """Test syncing flow from Hive source."""
        mock_decrypt.return_value = "decrypted_key"
        
        # Mock manager instance
        mock_manager = MagicMock()
        mock_manager.list_flows_sync.return_value = mock_hive_flows
        mock_manager.get_flow_sync.return_value = mock_hive_flows[0]
        
        with patch.object(workflow_manager, '_get_source_manager', return_value=mock_manager):
            # Mock session queries
            mock_source_result = MagicMock()
            mock_source_result.scalar_one_or_none.return_value = mock_hive_source
            workflow_manager.session.execute.return_value = mock_source_result
            
            # Mock _create_or_update_workflow
            expected_workflow_data = {"id": "workflow_123", "name": "Master Genie Agent"}
            with patch.object(workflow_manager, '_create_or_update_workflow', 
                             return_value=expected_workflow_data) as mock_create:
                
                result = await workflow_manager.sync_flow(
                    flow_id="master-genie",
                    input_component="input",
                    output_component="output", 
                    source_url=mock_hive_source.url
                )
                
                assert result == expected_workflow_data
                mock_create.assert_called_once()
                
                # Verify flow data was enhanced with components
                call_args = mock_create.call_args[0][0]
                assert call_args['input_component'] == "input"
                assert call_args['output_component'] == "output"

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key') 
    async def test_unsupported_source_type_error(self, mock_decrypt, workflow_manager):
        """Test error for unsupported source type."""
        mock_decrypt.return_value = "decrypted_key"
        
        # Create source with unsupported type
        mock_source = MagicMock(spec=WorkflowSource)
        mock_source.source_type = "unsupported-type"
        
        with pytest.raises(ValueError, match="Unsupported source type: unsupported-type"):
            await workflow_manager._get_source_manager(source=mock_source)

    def test_source_type_enum_values(self):
        """Test all expected source type enum values."""
        assert SourceType.LANGFLOW == "langflow"
        assert SourceType.AUTOMAGIK_AGENTS == "automagik-agents"
        assert SourceType.AUTOMAGIK_HIVE == "automagik-hive"

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key')
    async def test_hive_source_handles_empty_flows(self, mock_decrypt,
                                                 workflow_manager, mock_hive_source):
        """Test Hive source handles empty flows gracefully."""
        mock_decrypt.return_value = "decrypted_key"
        
        # Mock manager returning empty flows
        mock_manager = MagicMock()
        mock_manager.list_flows_sync.return_value = []
        mock_manager.api_url = mock_hive_source.url
        
        with patch.object(workflow_manager, '_get_source_manager', return_value=mock_manager):
            # Mock session query for sources
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [mock_hive_source]
            workflow_manager.session.execute.return_value = mock_result
            
            flows = await workflow_manager.list_remote_flows(source_url=mock_hive_source.url)
            
            assert flows == []

    @patch('automagik_spark.core.workflows.manager.WorkflowSource.decrypt_api_key')
    async def test_hive_source_connection_error(self, mock_decrypt,
                                              workflow_manager, mock_hive_source):
        """Test Hive source handles connection errors gracefully."""
        mock_decrypt.return_value = "decrypted_key"
        
        # Mock manager raising connection error
        mock_manager = MagicMock()
        mock_manager.list_flows_sync.side_effect = Exception("Connection failed")
        mock_manager.api_url = mock_hive_source.url
        
        with patch.object(workflow_manager, '_get_source_manager', return_value=mock_manager):
            # Mock session query for sources
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [mock_hive_source]
            workflow_manager.session.execute.return_value = mock_result
            
            flows = await workflow_manager.list_remote_flows(source_url=mock_hive_source.url)
            
            # Should return empty list on error (errors are logged but not raised)
            assert flows == []