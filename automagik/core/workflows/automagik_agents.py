"""AutoMagik Agents source type handler."""

from typing import Dict, Any, Optional, List
import httpx
from fastapi import HTTPException
from pydantic import BaseModel
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class AutoMagikAgentManager:
    """Manager for AutoMagik Agents source type."""

    def __init__(self, api_url: str, api_key: str, source_id: Optional[UUID] = None):
        """Initialize the AutoMagik Agents manager.
        
        Args:
            api_url: Base URL for the AutoMagik Agents API
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
            verify=False  # TODO: Make this configurable
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def validate(self) -> Dict[str, Any]:
        """Validate the AutoMagik Agents source.
        
        Returns:
            Dict[str, Any]: Version and status information
        
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
                    verify=False  # TODO: Make this configurable
                )
                should_close_client = True
                
            try:
                # Check health
                health_response = await client.get("/health")
                health_response.raise_for_status()
                health_data = health_response.json()
                
                if health_data.get('status') != "healthy":
                    raise HTTPException(
                        status_code=400,
                        detail=f"AutoMagik Agents health check failed: {health_data}"
                    )

                # Get root info which contains version and service info
                root_response = await client.get("/")
                root_response.raise_for_status()
                root_data = root_response.json()

                # Combine health and root data
                return {
                    'version': root_data.get('version', health_data.get('version', 'unknown')),
                    'name': root_data.get('name', 'AutoMagik Agents'),
                    'description': root_data.get('description', ''),
                    'status': health_data.get('status', 'unknown'),
                    'timestamp': health_data.get('timestamp'),
                    'environment': health_data.get('environment', 'unknown')
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
                detail=f"Failed to validate AutoMagik Agents source: {str(e)}"
            )

    async def list_agents(self) -> List[Dict[str, Any]]:
        """List available agents.
        
        Returns:
            List[Dict[str, Any]]: List of available agents
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
                    verify=False  # TODO: Make this configurable
                )
                should_close_client = True
                
            try:
                response = await client.get("/api/v1/agent/list")
                response.raise_for_status()
                agents = response.json()
                
                # Transform agent data to match workflow format
                transformed_agents = []
                for agent in agents:
                    transformed_agents.append({
                        'id': agent['name'],  # Use name as ID
                        'name': agent['name'],
                        'description': agent.get('description') or f"AutoMagik Agent of type: {agent.get('type', 'Unknown')}",
                        'data': {
                            'type': agent.get('type'),
                            'model': agent.get('model'),
                            'configuration': agent.get('configuration', {})
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': None,
                        'icon': None,
                        'icon_bg_color': None,
                        'gradient': False,
                        'liked': False,
                        'tags': [agent.get('type', 'Unknown')],
                        'created_at': None,
                        'updated_at': None
                    })
                return transformed_agents
            finally:
                # Close the client if we created it
                if should_close_client and client is not None:
                    await client.aclose()
        except Exception as e:
            logger.error(f"Failed to list agents: {str(e)}")
            raise

    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID (name).
        
        Args:
            agent_id: Name of the agent to get
            
        Returns:
            Optional[Dict[str, Any]]: Agent data if found, None otherwise
        """
        try:
            # Get all agents and find the one with matching name
            agents = await self.list_agents()
            for agent in agents:
                if agent['id'] == agent_id:
                    return agent
            return None
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 404:
                return None
            raise

    async def list_flows(self) -> List[Dict[str, Any]]:
        """Alias for list_agents to maintain interface compatibility with LangFlowManager."""
        return await self.list_agents()

    async def get_flow(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get_agent to maintain interface compatibility with LangFlowManager."""
        return await self.get_agent(flow_id)

    async def run_flow(self, agent_id: str, input_data: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Run an agent with input data.
        
        Args:
            agent_id: Name of the agent to run
            input_data: Input data for the agent
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Dict[str, Any]: Agent execution result
        """
        try:
            # If no session_id provided, generate one based on source and agent
            if not session_id and self.source_id:
                session_id = f"{self.source_id}_{agent_id}"

            # Ensure input_data is not empty
            if not input_data:
                input_data = "Hello"  # Default greeting if no input provided

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
                    verify=False  # TODO: Make this configurable
                )
                should_close_client = True
            
            try:
                response = await client.post(
                    f"/api/v1/agent/{agent_id}/run",
                    json={
                        "message_content": input_data,
                        "session_id": session_id,
                        "user_id": 1,
                        "message_limit": 10,
                        "session_origin": "automagik"
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # The API returns the output directly
                return {
                    'result': result if isinstance(result, str) else str(result),
                    'session_id': session_id,
                    'conversation_id': None,  # API doesn't provide this yet
                    'tool_calls': [],  # API doesn't provide this yet
                    'memory': {}  # API doesn't provide this yet
                }
            finally:
                # Close the client if we created it
                if should_close_client and client is not None:
                    await client.aclose()
        except Exception as e:
            logger.error(f"Failed to run agent {agent_id}: {str(e)}")
            raise

    def run_flow_sync(self, agent_id: str, input_data: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Run an agent with input data synchronously.
        
        Args:
            agent_id: Name of the agent to run
            input_data: Input data for the agent
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Dict[str, Any]: Agent execution result
        """
        try:
            # If no session_id provided, generate one based on source and agent
            if not session_id and self.source_id:
                session_id = f"{self.source_id}_{agent_id}"

            # Ensure input_data is not empty
            if not input_data:
                input_data = "Hello"  # Default greeting if no input provided

            # Create a synchronous client
            with httpx.Client(
                base_url=self.api_url,
                headers={
                    "accept": "application/json",
                    "x-api-key": self.api_key
                },
                verify=False  # TODO: Make this configurable
            ) as client:
                response = client.post(
                    f"/api/v1/agent/{agent_id}/run",
                    json={
                        "message_content": input_data,
                        "session_id": session_id,
                        "user_id": 1,
                        "message_limit": 10,
                        "session_origin": "automagik"
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # The API returns the output directly
                return {
                    'result': result if isinstance(result, str) else str(result),
                    'session_id': session_id,
                    'conversation_id': None,  # API doesn't provide this yet
                    'tool_calls': [],  # API doesn't provide this yet
                    'memory': {}  # API doesn't provide this yet
                }
        except Exception as e:
            logger.error(f"Failed to run agent {agent_id}: {str(e)}")
            raise

    def list_flows_sync(self) -> List[Dict[str, Any]]:
        """Alias for list_agents_sync to maintain interface compatibility with LangFlowManager."""
        return self.list_agents_sync()

    def get_agent_sync(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID (name) synchronously.
        
        Args:
            agent_id: Name of the agent to get
            
        Returns:
            Optional[Dict[str, Any]]: Agent data if found, None otherwise
        """
        try:
            # Get all agents and find the one with matching name
            agents = self.list_agents_sync()
            for agent in agents:
                if agent['id'] == agent_id:
                    return agent
            return None
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 404:
                return None
            raise
            
    def get_flow_sync(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get_agent_sync to maintain interface compatibility with LangFlowManager."""
        return self.get_agent_sync(flow_id)

    def list_agents_sync(self) -> List[Dict[str, Any]]:
        """List available agents synchronously.
        
        Returns:
            List[Dict[str, Any]]: List of available agents
        """
        try:
            # Create a synchronous client
            with httpx.Client(
                base_url=self.api_url,
                headers={
                    "accept": "application/json",
                    "x-api-key": self.api_key
                },
                verify=False  # TODO: Make this configurable
            ) as client:
                response = client.get("/api/v1/agent/list")
                response.raise_for_status()
                agents = response.json()
                
                # Transform agent data to match workflow format
                transformed_agents = []
                for agent in agents:
                    transformed_agents.append({
                        'id': agent['name'],  # Use name as ID
                        'name': agent['name'],
                        'description': agent.get('description') or f"AutoMagik Agent of type: {agent.get('type', 'Unknown')}",
                        'data': {
                            'type': agent.get('type'),
                            'model': agent.get('model'),
                            'configuration': agent.get('configuration', {})
                        },
                        'is_component': False,
                        'folder_id': None,
                        'folder_name': None,
                        'icon': None,
                        'icon_bg_color': None,
                        'gradient': False,
                        'liked': False,
                        'tags': [agent.get('type', 'Unknown')],
                        'created_at': None,
                        'updated_at': None
                    })
                return transformed_agents
        except Exception as e:
            logger.error(f"Failed to list agents: {str(e)}")
            raise 