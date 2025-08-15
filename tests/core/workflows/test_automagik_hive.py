"""Test AutoMagik Hive integration functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
import json
from uuid import uuid4

from automagik_spark.core.workflows.automagik_hive import AutomagikHiveManager
from automagik_spark.core.schemas.source import SourceType


class TestAutomagikHiveManager:
    """Test AutoMagik Hive manager functionality."""

    @pytest.fixture
    def manager(self):
        """Create AutoMagik Hive manager for testing."""
        return AutomagikHiveManager(
            api_url="http://localhost:8886",
            api_key="test_key",
            source_id=uuid4()
        )

    @pytest.fixture
    def mock_agents_response(self):
        """Mock agents API response."""
        return [
            {
                "agent_id": "master-genie",
                "name": "🧞 Master Genie",
                "description": "Ultimate development companion",
                "model": {"name": "OpenAIChat", "model": "gpt-4o"},
                "tools": [],
                "memory": {"name": "Memory"},
                "storage": {"name": "PostgresStorage"},
                "instructions": "Help with development tasks",
                "add_context": True
            },
            {
                "agent_id": "test-agent",
                "name": "Test Agent",
                "description": "Test agent for validation",
                "model": {"name": "OpenAIChat", "model": "gpt-4"},
                "tools": ["search", "code"],
                "memory": {"name": "Memory"},
                "storage": {"name": "PostgresStorage"},
                "instructions": None,
                "add_context": False
            }
        ]

    @pytest.fixture
    def mock_teams_response(self):
        """Mock teams API response."""
        return [
            {
                "team_id": "genie",
                "name": "🧞 Genie Team",
                "description": "Multi-agent development team",
                "mode": "coordinate",
                "model": {"name": "OpenAIChat", "model": "gpt-4o"},
                "members": [
                    {"agent_id": "genie-dev", "name": "Dev Coordinator"},
                    {"agent_id": "genie-test", "name": "Test Coordinator"}
                ],
                "memory": {"name": "Memory"},
                "storage": {"name": "PostgresStorage"}
            }
        ]

    @pytest.fixture
    def mock_workflows_response(self):
        """Mock workflows API response."""
        return [
            {
                "workflow_id": "template-workflow",
                "name": "Template Workflow",
                "description": "Template workflow for testing",
                "steps": [
                    {"step_id": "analyze", "agent_id": "genie-dev"},
                    {"step_id": "implement", "agent_id": "genie-dev"},
                    {"step_id": "test", "agent_id": "genie-test"}
                ]
            }
        ]

    @pytest.fixture
    def mock_health_response(self):
        """Mock health API response."""
        return {
            "status": "success",
            "service": "Automagik Hive Multi-Agent System",
            "utc": "2025-08-15T15:00:00.000000+00:00",
            "message": "System operational"
        }

    @pytest.fixture
    def mock_status_response(self):
        """Mock status API response."""
        return {
            "status": "running",
            "app_id": "automagik-hive",
            "agents_loaded": 6,
            "teams_loaded": 2,
            "workflows_loaded": 1,
            "database": "connected",
            "mcp_servers": ["claude-mcp", "postgres", "zen"]
        }

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager.api_url == "http://localhost:8886"
        assert manager.api_key == "test_key"
        assert manager.source_id is not None
        assert manager._client is None

    @pytest.mark.asyncio
    async def test_validate_success(self, manager, mock_health_response, mock_status_response):
        """Test successful validation."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            # Mock health response
            mock_health_resp = MagicMock()
            mock_health_resp.raise_for_status = MagicMock()
            mock_health_resp.json = MagicMock(return_value=mock_health_response)
            
            # Mock status response
            mock_status_resp = MagicMock()
            mock_status_resp.raise_for_status = MagicMock()
            mock_status_resp.json = MagicMock(return_value=mock_status_response)
            
            mock_client.get.side_effect = [mock_health_resp, mock_status_resp]
            
            result = await manager.validate()
            
            assert result["status"] == "success"
            assert result["name"] == "Automagik Hive Multi-Agent System"
            assert result["agents_loaded"] == 6
            assert result["teams_loaded"] == 2
            assert result["workflows_loaded"] == 1

    @pytest.mark.asyncio
    async def test_validate_health_failure(self, manager):
        """Test validation with health check failure."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = AsyncMock()
            mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Service unavailable", request=MagicMock(), response=MagicMock()
            )
            mock_client.get.return_value = mock_resp
            
            with pytest.raises(Exception):
                await manager.validate()

    @pytest.mark.asyncio
    async def test_list_agents(self, manager, mock_agents_response):
        """Test listing agents."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json = MagicMock(return_value=mock_agents_response)
            mock_client.get.return_value = mock_resp
            
            agents = await manager.list_agents()
            
            assert len(agents) == 2
            assert agents[0]["id"] == "master-genie"
            assert agents[0]["name"] == "🧞 Master Genie"
            assert agents[0]["data"]["type"] == "hive_agent"
            assert agents[0]["folder_name"] == "Agents"
            assert agents[0]["icon"] == "🤖"
            assert "agent" in agents[0]["tags"]
            assert "hive" in agents[0]["tags"]

    @pytest.mark.asyncio
    async def test_list_teams(self, manager, mock_teams_response):
        """Test listing teams."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json = MagicMock(return_value=mock_teams_response)
            mock_client.get.return_value = mock_resp
            
            teams = await manager.list_teams()
            
            assert len(teams) == 1
            assert teams[0]["id"] == "genie"
            assert teams[0]["name"] == "🧞 Genie Team"
            assert teams[0]["data"]["type"] == "hive_team"
            assert teams[0]["folder_name"] == "Teams"
            assert teams[0]["icon"] == "👥"
            assert teams[0]["data"]["members_count"] == 2
            assert "team" in teams[0]["tags"]
            assert "multi-agent" in teams[0]["tags"]

    @pytest.mark.asyncio
    async def test_list_workflows(self, manager, mock_workflows_response):
        """Test listing workflows."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json = MagicMock(return_value=mock_workflows_response)
            mock_client.get.return_value = mock_resp
            
            workflows = await manager.list_workflows()
            
            assert len(workflows) == 1
            assert workflows[0]["id"] == "template-workflow"
            assert workflows[0]["name"] == "Template Workflow"
            assert workflows[0]["data"]["type"] == "hive_workflow"
            assert workflows[0]["folder_name"] == "Workflows"
            assert workflows[0]["icon"] == "⚡"
            assert len(workflows[0]["data"]["steps"]) == 3
            assert "workflow" in workflows[0]["tags"]
            assert "multi-step" in workflows[0]["tags"]

    @pytest.mark.asyncio
    async def test_list_flows_combined(self, manager, mock_agents_response, mock_teams_response, mock_workflows_response):
        """Test listing all flows combines agents, teams, and workflows."""
        with patch.object(manager, 'list_agents', return_value=mock_agents_response), \
             patch.object(manager, 'list_teams', return_value=mock_teams_response), \
             patch.object(manager, 'list_workflows', return_value=mock_workflows_response):
            
            flows = await manager.list_flows()
            
            # Should combine all three types
            assert len(flows) == 4  # 2 agents + 1 team + 1 workflow

    @pytest.mark.asyncio
    async def test_get_flow_agent(self, manager, mock_agents_response):
        """Test getting a specific agent flow."""
        with patch.object(manager, 'list_agents', return_value=[{
            'id': 'master-genie', 'name': 'Master Genie', 'data': {'type': 'hive_agent'}
        }]), \
             patch.object(manager, 'list_teams', return_value=[]), \
             patch.object(manager, 'list_workflows', return_value=[]):
            
            flow = await manager.get_flow('master-genie')
            
            assert flow is not None
            assert flow['id'] == 'master-genie'
            assert flow['data']['type'] == 'hive_agent'

    @pytest.mark.asyncio
    async def test_get_flow_not_found(self, manager):
        """Test getting non-existent flow."""
        with patch.object(manager, 'list_agents', return_value=[]), \
             patch.object(manager, 'list_teams', return_value=[]), \
             patch.object(manager, 'list_workflows', return_value=[]):
            
            flow = await manager.get_flow('nonexistent')
            
            assert flow is None

    @pytest.mark.asyncio
    async def test_run_agent(self, manager):
        """Test running an agent."""
        mock_flow = {'data': {'type': 'hive_agent'}}
        mock_response = {
            'response': {'content': 'Agent response'},
            'session_id': 'session123',
            'run_id': 'run456',
            'agent_id': 'test-agent',
            'status': 'completed'
        }
        
        with patch.object(manager, 'get_flow', return_value=mock_flow), \
             patch('httpx.AsyncClient') as mock_client_class:
            
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json = MagicMock(return_value=mock_response)
            mock_client.post.return_value = mock_resp
            
            result = await manager.run_flow('test-agent', 'Hello world', 'session123')
            
            assert result['result'] == 'Agent response'
            assert result['session_id'] == 'session123'
            assert result['run_id'] == 'run456'
            assert result['status'] == 'completed'
            assert result['success'] == True

    @pytest.mark.asyncio
    async def test_run_team(self, manager):
        """Test running a team."""
        mock_flow = {'data': {'type': 'hive_team'}}
        mock_response = {
            'coordinator_response': {'content': 'Coordinator response'},
            'member_responses': [
                {'agent_id': 'dev', 'response': 'Dev response'},
                {'agent_id': 'test', 'response': 'Test response'}
            ],
            'session_id': 'session123',
            'run_id': 'run456',
            'team_id': 'test-team',
            'status': 'completed'
        }
        
        with patch.object(manager, 'get_flow', return_value=mock_flow), \
             patch('httpx.AsyncClient') as mock_client_class:
            
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json = MagicMock(return_value=mock_response)
            mock_client.post.return_value = mock_resp
            
            result = await manager.run_flow('test-team', 'Complex task', 'session123')
            
            assert 'Coordinator response' in result['result']
            assert '**dev**: Dev response' in result['result']
            assert '**test**: Test response' in result['result']
            assert result['session_id'] == 'session123'
            assert result['success'] == True

    @pytest.mark.asyncio
    async def test_run_workflow(self, manager):
        """Test running a workflow."""
        mock_flow = {'data': {'type': 'hive_workflow'}}
        mock_response = {
            'steps_completed': [
                {'step_id': 'analyze', 'status': 'completed', 'output': 'Analysis done'},
                {'step_id': 'implement', 'status': 'completed', 'output': 'Implementation done'}
            ],
            'final_output': 'Workflow completed successfully',
            'session_id': 'session123',
            'run_id': 'run456',
            'workflow_id': 'test-workflow',
            'status': 'completed'
        }
        
        with patch.object(manager, 'get_flow', return_value=mock_flow), \
             patch('httpx.AsyncClient') as mock_client_class:
            
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json = MagicMock(return_value=mock_response)
            mock_client.post.return_value = mock_resp
            
            result = await manager.run_flow('test-workflow', 'Build feature', 'session123')
            
            assert result['result'] == 'Workflow completed successfully'
            assert result['session_id'] == 'session123'
            assert len(result['steps_completed']) == 2
            assert result['success'] == True

    @pytest.mark.asyncio
    async def test_run_flow_not_found(self, manager):
        """Test running non-existent flow."""
        with patch.object(manager, 'get_flow', return_value=None):
            
            with pytest.raises(ValueError, match="Flow .* not found in AutoMagik Hive"):
                await manager.run_flow('nonexistent', 'test')

    def test_sync_list_flows(self, manager, mock_agents_response, mock_teams_response, mock_workflows_response):
        """Test synchronous list flows."""
        with patch('httpx.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            # Mock responses for agents, teams, workflows
            mock_agents_resp = MagicMock()
            mock_agents_resp.raise_for_status.return_value = None
            mock_agents_resp.json.return_value = mock_agents_response
            
            mock_teams_resp = MagicMock()
            mock_teams_resp.raise_for_status.return_value = None
            mock_teams_resp.json.return_value = mock_teams_response
            
            mock_workflows_resp = MagicMock()
            mock_workflows_resp.raise_for_status.return_value = None
            mock_workflows_resp.json.return_value = mock_workflows_response
            
            mock_client.get.side_effect = [mock_agents_resp, mock_teams_resp, mock_workflows_resp]
            
            flows = manager.list_flows_sync()
            
            assert len(flows) == 4  # 2 agents + 1 team + 1 workflow
            # Check that all types are present
            types = [flow["data"]["type"] for flow in flows]
            assert "hive_agent" in types
            assert "hive_team" in types  
            assert "hive_workflow" in types

    def test_sync_get_flow(self, manager):
        """Test synchronous get flow."""
        mock_flows = [
            {'id': 'test-agent', 'name': 'Test Agent', 'data': {'type': 'hive_agent'}}
        ]
        
        with patch.object(manager, 'list_flows_sync', return_value=mock_flows):
            flow = manager.get_flow_sync('test-agent')
            
            assert flow is not None
            assert flow['id'] == 'test-agent'
            assert flow['data']['type'] == 'hive_agent'

    def test_sync_run_agent(self, manager):
        """Test synchronous agent run."""
        mock_flow = {'data': {'type': 'hive_agent'}}
        mock_response = {
            'response': {'content': 'Agent response'},
            'session_id': 'session123',
            'status': 'completed'
        }
        
        with patch.object(manager, 'get_flow_sync', return_value=mock_flow), \
             patch('httpx.Client') as mock_client_class:
            
            mock_client = MagicMock()
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            mock_resp = MagicMock()
            mock_resp.raise_for_status.return_value = None
            mock_resp.json.return_value = mock_response
            mock_client.post.return_value = mock_resp
            
            result = manager.run_flow_sync('test-agent', 'Hello world', 'session123')
            
            assert result['result'] == 'Agent response'
            assert result['session_id'] == 'session123'
            assert result['success'] == True

    def test_context_managers(self, manager):
        """Test context manager functionality."""
        # Test sync context manager
        with manager:
            assert True  # Should not raise
        
        # Test that async context manager sets up client
        assert manager._client is None

    @pytest.mark.asyncio
    async def test_async_context_manager(self, manager):
        """Test async context manager."""
        async with manager:
            assert manager._client is not None
        assert manager._client is None


class TestSourceTypeEnum:
    """Test SourceType enum includes AUTOMAGIK_HIVE."""
    
    def test_automagik_hive_exists(self):
        """Test that AUTOMAGIK_HIVE exists in SourceType enum."""
        assert hasattr(SourceType, 'AUTOMAGIK_HIVE')
        assert SourceType.AUTOMAGIK_HIVE == "automagik-hive"
    
    def test_all_source_types(self):
        """Test all expected source types exist."""
        assert SourceType.LANGFLOW == "langflow"
        assert SourceType.AUTOMAGIK_AGENTS == "automagik-agents"
        assert SourceType.AUTOMAGIK_HIVE == "automagik-hive"