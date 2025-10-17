"""AutoMagik Hive source type handler."""

from typing import Dict, Any, Optional, List
import httpx
from fastapi import HTTPException
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class AutomagikHiveManager:
    """Manager for AutoMagik Hive source type.
    
    AutoMagik Hive provides three types of execution entities:
    - Agents: Individual AI agents
    - Teams: Multi-agent coordinated teams
    - Workflows: Structured multi-step processes
    """

    def __init__(self, api_url: str, api_key: str, source_id: Optional[UUID] = None):
        """Initialize the AutoMagik Hive manager.
        
        Args:
            api_url: Base URL for the AutoMagik Hive API (e.g., http://localhost:8886)
            api_key: API key for authentication
            source_id: Optional source ID for tracking
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.source_id = source_id
        self._client = None

    async def __aenter__(self):
        """Enter async context."""
        self._client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "accept": "application/json",
                "x-api-key": self.api_key
            },
            verify=False,  # TODO: Make this configurable
            timeout=30.0  # 30 second timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def __enter__(self):
        """Enter sync context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sync context."""
        pass  # Nothing to clean up for sync context

    async def validate(self) -> Dict[str, Any]:
        """Validate the AutoMagik Hive source.
        
        Returns:
            Dict[str, Any]: Status and service information
        
        Raises:
            HTTPException: If validation fails
        """
        try:
            # Create a new client if one isn't already initialized
            client = self._client
            should_close_client = False
            
            if client is None:
                client = httpx.AsyncClient(
                    base_url=self.api_url,
                    headers={
                        "accept": "application/json",
                        "x-api-key": self.api_key
                    },
                    verify=False,
                    timeout=30.0
                )
                should_close_client = True
                
            try:
                # Check health endpoint
                health_response = await client.get("/api/v1/health")
                health_response.raise_for_status()
                health_data = health_response.json()
                
                if health_data.get('status') != "success":
                    raise HTTPException(
                        status_code=400,
                        detail=f"AutoMagik Hive health check failed: {health_data}"
                    )

                # Return health info from AgentOS v2
                return {
                    'version': health_data.get('utc', 'unknown'),
                    'name': health_data.get('service', 'Automagik Hive Multi-Agent System'),
                    'description': 'AutoMagik Hive Multi-Agent System with agents, teams, and workflows',
                    'status': health_data.get('status', 'unknown'),
                    'timestamp': health_data.get('utc'),
                    'environment': 'production'
                }
            finally:
                # Close the client if we created it
                if should_close_client and client is not None:
                    await client.aclose()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to validate AutoMagik Hive source: {str(e)}"
            )

    async def list_agents(self) -> List[Dict[str, Any]]:
        """List available agents from AutoMagik Hive.
        
        Returns:
            List[Dict[str, Any]]: List of available agents
        """
        try:
            client = await self._get_client()
            should_close = client != self._client
            
            try:
                response = await client.get("/agents")
                response.raise_for_status()
                agents = response.json()
                
                # Transform agent data to match Spark workflow format
                transformed_agents = []
                for agent in agents:
                    # Prioritize 'id' field, then 'agent_id', then 'name' as fallback
                    agent_id = agent.get('id') or agent.get('agent_id') or agent.get('name', 'unknown')
                    transformed_agents.append({
                        'id': agent_id,
                        'name': agent.get('name', agent_id),
                        'description': agent.get('description', f"AutoMagik Hive Agent: {agent_id}"),
                        'data': {
                            'type': 'hive_agent',
                            'model': agent.get('model', {}),
                            'tools': agent.get('tools', []),
                            'memory': agent.get('memory', {}),
                            'storage': agent.get('storage', {}),
                            'instructions': agent.get('instructions'),
                            'add_context': agent.get('add_context', True)
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': 'Agents',
                        'icon': '🤖',
                        'icon_bg_color': '#4F46E5',
                        'liked': False,
                        'tags': ['agent', 'hive'],
                        'created_at': None,
                        'updated_at': None
                    })
                return transformed_agents
            finally:
                if should_close:
                    await client.aclose()
        except Exception as e:
            logger.error(f"Failed to list agents from Hive: {str(e)}")
            raise

    async def list_teams(self) -> List[Dict[str, Any]]:
        """List available teams from AutoMagik Hive.
        
        Returns:
            List[Dict[str, Any]]: List of available teams
        """
        try:
            client = await self._get_client()
            should_close = client != self._client
            
            try:
                response = await client.get("/teams")
                response.raise_for_status()
                teams = response.json()
                
                # Transform team data to match Spark workflow format
                transformed_teams = []
                for team in teams:
                    # Prioritize 'id' field, then 'team_id', then 'name' as fallback
                    team_id = team.get('id') or team.get('team_id') or team.get('name', 'unknown')
                    members_count = len(team.get('members', []))
                    transformed_teams.append({
                        'id': team_id,
                        'name': team.get('name', team_id),
                        'description': team.get('description', f"AutoMagik Hive Team with {members_count} members"),
                        'data': {
                            'type': 'hive_team',
                            'mode': team.get('mode', 'coordinate'),
                            'model': team.get('model', {}),
                            'members': team.get('members', []),
                            'memory': team.get('memory', {}),
                            'storage': team.get('storage', {}),
                            'members_count': members_count
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': 'Teams',
                        'icon': '👥',
                        'icon_bg_color': '#059669',
                        'liked': False,
                        'tags': ['team', 'multi-agent', 'hive'],
                        'created_at': None,
                        'updated_at': None
                    })
                return transformed_teams
            finally:
                if should_close:
                    await client.aclose()
        except Exception as e:
            logger.error(f"Failed to list teams from Hive: {str(e)}")
            raise

    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List available workflows from AutoMagik Hive.
        
        Returns:
            List[Dict[str, Any]]: List of available workflows
        """
        try:
            client = await self._get_client()
            should_close = client != self._client
            
            try:
                response = await client.get("/workflows")
                response.raise_for_status()
                workflows = response.json()
                
                # Transform workflow data to match Spark workflow format
                transformed_workflows = []
                for workflow in workflows:
                    # Prioritize 'id' field, then 'workflow_id', then 'name' as fallback
                    workflow_id = workflow.get('id') or workflow.get('workflow_id') or workflow.get('name', 'unknown')
                    transformed_workflows.append({
                        'id': workflow_id,
                        'name': workflow.get('name', workflow_id),
                        'description': workflow.get('description', f"AutoMagik Hive Workflow: {workflow_id}"),
                        'data': {
                            'type': 'hive_workflow',
                            'steps': workflow.get('steps', []),
                            'workflow_data': workflow
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': 'Workflows',
                        'icon': '⚡',
                        'icon_bg_color': '#DC2626',
                        'liked': False,
                        'tags': ['workflow', 'multi-step', 'hive'],
                        'created_at': None,
                        'updated_at': None
                    })
                return transformed_workflows
            finally:
                if should_close:
                    await client.aclose()
        except Exception as e:
            logger.error(f"Failed to list workflows from Hive: {str(e)}")
            raise

    async def list_flows(self) -> List[Dict[str, Any]]:
        """List all available flows (agents, teams, and workflows combined).
        
        Returns:
            List[Dict[str, Any]]: Combined list of all available execution entities
        """
        try:
            agents = await self.list_agents()
            teams = await self.list_teams()
            workflows = await self.list_workflows()
            
            # Combine all flows
            all_flows = agents + teams + workflows
            return all_flows
        except Exception as e:
            logger.error(f"Failed to list flows from Hive: {str(e)}")
            raise

    async def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific flow by ID (could be agent, team, or workflow).
        
        Args:
            flow_id: ID of the flow to get
            
        Returns:
            Optional[Dict[str, Any]]: Flow data if found, None otherwise
        """
        try:
            # Try to find in agents first
            agents = await self.list_agents()
            for agent in agents:
                if agent['id'] == flow_id:
                    return agent
            
            # Try teams
            teams = await self.list_teams()
            for team in teams:
                if team['id'] == flow_id:
                    return team
            
            # Try workflows
            workflows = await self.list_workflows()
            for workflow in workflows:
                if workflow['id'] == flow_id:
                    return workflow
                    
            return None
        except Exception as e:
            logger.error(f"Failed to get flow {flow_id} from Hive: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 404:
                return None
            raise

    async def run_flow(self, flow_id: str, input_data, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Run a flow (agent, team, or workflow) with input data.
        
        Args:
            flow_id: ID of the flow to run
            input_data: Input data for the flow
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Dict[str, Any]: Flow execution result
        """
        try:
            # First, determine what type of entity this is
            flow = await self.get_flow(flow_id)
            if not flow:
                raise ValueError(f"Flow {flow_id} not found in AutoMagik Hive")
            
            flow_type = flow['data'].get('type', 'unknown')
            
            # Generate session ID if not provided
            if not session_id and self.source_id:
                session_id = f"{self.source_id}_{flow_id}"
            
            # Handle different input_data formats
            if isinstance(input_data, dict) and 'value' in input_data:
                message = input_data['value']
            elif not input_data:
                message = "Hello"  # Default greeting if no input provided
            elif not isinstance(input_data, str):
                message = str(input_data)
            else:
                message = input_data

            client = await self._get_client()
            should_close = client != self._client
            
            try:
                if flow_type == 'hive_agent':
                    return await self._run_agent(client, flow_id, message, session_id)
                elif flow_type == 'hive_team':
                    return await self._run_team(client, flow_id, message, session_id)
                elif flow_type == 'hive_workflow':
                    return await self._run_workflow(client, flow_id, message, session_id)
                else:
                    raise ValueError(f"Unknown flow type: {flow_type}")
            finally:
                if should_close:
                    await client.aclose()
                    
        except Exception as e:
            logger.error(f"Failed to run flow {flow_id}: {str(e)}")
            raise

    async def _run_agent(self, client: httpx.AsyncClient, agent_id: str, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Run a single agent."""
        payload = {
            "message": message,
            "stream": False
        }
        if session_id:
            payload["session_id"] = session_id
            
        # Use form data for agent runs
        response = await client.post(
            f"/agents/{agent_id}/runs",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        result = response.json()
        
        return {
            'result': result.get('content', str(result)),
            'session_id': result.get('session_id', session_id),
            'run_id': result.get('run_id'),
            'agent_id': result.get('agent_id'),
            'metadata': result.get('metrics', {}),
            'status': result.get('status', 'completed'),
            'success': result.get('status') in ['RUNNING', 'COMPLETED', 'completed']
        }

    async def _run_team(self, client: httpx.AsyncClient, team_id: str, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Run a team with multiple agents."""
        payload = {
            "message": message,
            "stream": False,
            "mode": "coordinate"
        }
        if session_id:
            payload["session_id"] = session_id
            
        response = await client.post(f"/teams/{team_id}/runs", data=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract coordinator response and member responses
        coordinator_content = result.get('coordinator_response', {}).get('content', '')
        member_responses = result.get('member_responses', [])
        
        # Combine all responses
        combined_result = coordinator_content
        if member_responses:
            combined_result += "\n\n" + "\n".join([
                f"**{resp.get('agent_id', 'Agent')}**: {resp.get('response', '')}"
                for resp in member_responses
            ])
        
        return {
            'result': combined_result or str(result),
            'session_id': result.get('session_id', session_id),
            'run_id': result.get('run_id'),
            'team_id': result.get('team_id'),
            'coordinator_response': result.get('coordinator_response', {}),
            'member_responses': member_responses,
            'status': result.get('status', 'completed'),
            'success': result.get('status') in ['COMPLETED', 'completed']
        }

    async def _run_workflow(self, client: httpx.AsyncClient, workflow_id: str, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Run a structured workflow."""
        payload = {
            "input_data": {
                "message": message,
                "requirements": message
            }
        }
        if session_id:
            payload["session_id"] = session_id
            
        response = await client.post(f"/workflows/{workflow_id}/runs", json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract workflow execution results
        steps_completed = result.get('steps_completed', [])
        final_output = result.get('final_output', '')
        
        # Combine step outputs if no final output
        if not final_output and steps_completed:
            final_output = "\n".join([
                f"**{step.get('step_id', 'Step')}**: {step.get('output', '')}"
                for step in steps_completed
                if step.get('status') == 'completed'
            ])
        
        return {
            'result': final_output or str(result),
            'session_id': result.get('session_id', session_id),
            'run_id': result.get('run_id'),
            'workflow_id': result.get('workflow_id'),
            'steps_completed': steps_completed,
            'final_output': final_output,
            'status': result.get('status', 'completed'),
            'success': result.get('status') in ['COMPLETED', 'completed']
        }

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create an HTTP client."""
        if self._client:
            return self._client
        
        return httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "accept": "application/json",
                "x-api-key": self.api_key
            },
            verify=False,
            timeout=30.0
        )

    # Synchronous methods for compatibility
    def list_flows_sync(self) -> List[Dict[str, Any]]:
        """Synchronous version of list_flows."""
        try:
            with httpx.Client(
                base_url=self.api_url,
                headers={
                    "accept": "application/json",
                    "x-api-key": self.api_key,
                },
                verify=False,
                timeout=30.0
            ) as client:
                # Get agents
                agents_response = client.get("/agents")
                agents_response.raise_for_status()
                agents = agents_response.json()
                
                # Get teams
                try:
                    teams_response = client.get("/teams")
                    teams_response.raise_for_status()
                    teams = teams_response.json()
                except:
                    teams = []
                
                # Get workflows
                try:
                    workflows_response = client.get("/workflows")
                    workflows_response.raise_for_status()
                    workflows = workflows_response.json()
                except:
                    workflows = []
                
                # Transform all entities
                all_flows = []
                
                # Transform agents
                for agent in agents:
                    # Prioritize 'id' field, then 'agent_id', then 'name' as fallback
                    agent_id = agent.get('id') or agent.get('agent_id') or agent.get('name', 'unknown')
                    all_flows.append({
                        'id': agent_id,
                        'name': agent.get('name', agent_id),
                        'description': agent.get('description', f"AutoMagik Hive Agent: {agent_id}"),
                        'data': {
                            'type': 'hive_agent',
                            'model': agent.get('model', {}),
                            'tools': agent.get('tools', []),
                            'memory': agent.get('memory', {}),
                            'storage': agent.get('storage', {}),
                            'instructions': agent.get('instructions'),
                            'add_context': agent.get('add_context', True)
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': 'Agents',
                        'icon': '🤖',
                        'icon_bg_color': '#4F46E5',
                        'liked': False,
                        'tags': ['agent', 'hive'],
                        'created_at': None,
                        'updated_at': None
                    })
                
                # Transform teams
                for team in teams:
                    # Prioritize 'id' field, then 'team_id', then 'name' as fallback
                    team_id = team.get('id') or team.get('team_id') or team.get('name', 'unknown')
                    members_count = len(team.get('members', []))
                    all_flows.append({
                        'id': team_id,
                        'name': team.get('name', team_id),
                        'description': team.get('description', f"AutoMagik Hive Team with {members_count} members"),
                        'data': {
                            'type': 'hive_team',
                            'mode': team.get('mode', 'coordinate'),
                            'model': team.get('model', {}),
                            'members': team.get('members', []),
                            'memory': team.get('memory', {}),
                            'storage': team.get('storage', {}),
                            'members_count': members_count
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': 'Teams',
                        'icon': '👥',
                        'icon_bg_color': '#059669',
                        'liked': False,
                        'tags': ['team', 'multi-agent', 'hive'],
                        'created_at': None,
                        'updated_at': None
                    })
                
                # Transform workflows
                for workflow in workflows:
                    # Prioritize 'id' field, then 'workflow_id', then 'name' as fallback
                    workflow_id = workflow.get('id') or workflow.get('workflow_id') or workflow.get('name', 'unknown')
                    all_flows.append({
                        'id': workflow_id,
                        'name': workflow.get('name', workflow_id),
                        'description': workflow.get('description', f"AutoMagik Hive Workflow: {workflow_id}"),
                        'data': {
                            'type': 'hive_workflow',
                            'steps': workflow.get('steps', []),
                            'workflow_data': workflow
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': 'Workflows',
                        'icon': '⚡',
                        'icon_bg_color': '#DC2626',
                        'liked': False,
                        'tags': ['workflow', 'multi-step', 'hive'],
                        'created_at': None,
                        'updated_at': None
                    })
                
                return all_flows
        except Exception as e:
            logger.error(f"Failed to list flows from Hive: {str(e)}")
            raise

    def get_flow_sync(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Synchronous version of get_flow."""
        try:
            flows = self.list_flows_sync()
            for flow in flows:
                if flow['id'] == flow_id:
                    return flow
            return None
        except Exception as e:
            logger.error(f"Failed to get flow {flow_id} from Hive: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 404:
                return None
            raise

    def run_flow_sync(self, flow_id: str, input_data, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Synchronous version of run_flow."""
        try:
            logger.info(f"AutoMagik Hive run_flow_sync called with flow_id={flow_id}, input_data={repr(input_data)}, session_id={session_id}")
            
            # First, determine what type of entity this is
            flow = self.get_flow_sync(flow_id)
            if not flow:
                raise ValueError(f"Flow {flow_id} not found in AutoMagik Hive")
            
            flow_type = flow['data'].get('type', 'unknown')
            logger.info(f"Flow type: {flow_type}")
            
            # Generate session ID if not provided
            if not session_id and self.source_id:
                session_id = f"{self.source_id}_{flow_id}"
            
            # Handle different input_data formats
            if isinstance(input_data, dict) and 'value' in input_data:
                message = input_data['value']
            elif not input_data:
                message = "Hello"  # Default greeting if no input provided
            elif not isinstance(input_data, str):
                message = str(input_data)
            else:
                message = input_data
            
            logger.info(f"Processed message: {repr(message)}")

            with httpx.Client(
                base_url=self.api_url,
                headers={
                    "accept": "application/json",
                    "x-api-key": self.api_key,
                },
                verify=False,
                timeout=30.0
            ) as client:
                if flow_type == 'hive_agent':
                    return self._run_agent_sync(client, flow_id, message, session_id)
                elif flow_type == 'hive_team':
                    return self._run_team_sync(client, flow_id, message, session_id)
                elif flow_type == 'hive_workflow':
                    return self._run_workflow_sync(client, flow_id, message, session_id)
                else:
                    raise ValueError(f"Unknown flow type: {flow_type}")
                    
        except Exception as e:
            logger.error(f"Failed to run flow {flow_id}: {str(e)}")
            raise

    def _run_agent_sync(self, client: httpx.Client, agent_id: str, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Run a single agent synchronously."""
        payload = {
            "message": message,
            "stream": False
        }
        if session_id:
            payload["session_id"] = session_id
        
        logger.info(f"Running agent {agent_id} with payload: {payload}")
        
        # Use form data for agent runs
        response = client.post(
            f"/agents/{agent_id}/runs",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"Agent run result: {result}")
        
        return {
            'result': result.get('content', str(result)),
            'session_id': result.get('session_id', session_id),
            'run_id': result.get('run_id'),
            'agent_id': result.get('agent_id'),
            'metadata': result.get('metrics', {}),
            'status': result.get('status', 'completed'),
            'success': result.get('status') in ['RUNNING', 'COMPLETED', 'completed']
        }

    def _run_team_sync(self, client: httpx.Client, team_id: str, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Run a team with multiple agents synchronously."""
        payload = {
            "message": message,
            "stream": False,
            "mode": "coordinate"
        }
        if session_id:
            payload["session_id"] = session_id
        
        logger.info(f"Running team {team_id} with payload: {payload}")
        
        response = client.post(f"/teams/{team_id}/runs", data=payload)
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"Team run result: {result}")
        
        # Extract coordinator response and member responses
        coordinator_content = result.get('coordinator_response', {}).get('content', '')
        member_responses = result.get('member_responses', [])
        
        # Combine all responses
        combined_result = coordinator_content
        if member_responses:
            combined_result += "\n\n" + "\n".join([
                f"**{resp.get('agent_id', 'Agent')}**: {resp.get('response', '')}"
                for resp in member_responses
            ])
        
        return {
            'result': combined_result or str(result),
            'session_id': result.get('session_id', session_id),
            'run_id': result.get('run_id'),
            'team_id': result.get('team_id'),
            'coordinator_response': result.get('coordinator_response', {}),
            'member_responses': member_responses,
            'status': result.get('status', 'completed'),
            'success': result.get('status') in ['COMPLETED', 'completed']
        }

    def _run_workflow_sync(self, client: httpx.Client, workflow_id: str, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Run a structured workflow synchronously."""
        payload = {
            "input_data": {
                "message": message,
                "requirements": message
            }
        }
        if session_id:
            payload["session_id"] = session_id
        
        logger.info(f"Running workflow {workflow_id} with payload: {payload}")
        
        response = client.post(f"/workflows/{workflow_id}/runs", json=payload)
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"Workflow run result: {result}")
        
        # Extract workflow execution results
        steps_completed = result.get('steps_completed', [])
        final_output = result.get('final_output', '')
        
        # Combine step outputs if no final output
        if not final_output and steps_completed:
            final_output = "\n".join([
                f"**{step.get('step_id', 'Step')}**: {step.get('output', '')}"
                for step in steps_completed
                if step.get('status') == 'completed'
            ])
        
        return {
            'result': final_output or str(result),
            'session_id': result.get('session_id', session_id),
            'run_id': result.get('run_id'),
            'workflow_id': result.get('workflow_id'),
            'steps_completed': steps_completed,
            'final_output': final_output,
            'status': result.get('status', 'completed'),
            'success': result.get('status') in ['COMPLETED', 'completed']
        }