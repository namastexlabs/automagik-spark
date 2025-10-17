"""Adapter for AutoMagik Hive workflows."""

from typing import Dict, List, Optional, Any
import logging
from .base import BaseWorkflowAdapter, WorkflowExecutionResult
from ..automagik_hive import AutomagikHiveManager

logger = logging.getLogger(__name__)


class HiveAdapter(BaseWorkflowAdapter):
    """Adapter for AutoMagik Hive workflows (agents, teams, and workflows)."""

    def __init__(self, api_url: str, api_key: str, source_id: Optional[Any] = None):
        """Initialize Hive adapter.

        Args:
            api_url: Hive API base URL
            api_key: API key for authentication
            source_id: Optional source ID for tracking
        """
        super().__init__(api_url, api_key, source_id)
        self.manager = AutomagikHiveManager(
            api_url=api_url,
            api_key=api_key,
            source_id=source_id
        )

    @property
    def source_type(self) -> str:
        """Return the source type identifier."""
        return "automagik-hive"

    def list_flows_sync(self) -> List[Dict[str, Any]]:
        """List all flows from Hive (agents, teams, and workflows).

        Returns:
            List of flow dictionaries
        """
        try:
            return self.manager.list_flows_sync()
        except Exception as e:
            logger.error(f"Failed to list Hive flows: {str(e)}")
            raise

    def get_flow_sync(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific flow from Hive by ID.

        Args:
            flow_id: ID of the flow to retrieve

        Returns:
            Flow dictionary if found, None otherwise
        """
        try:
            return self.manager.get_flow_sync(flow_id)
        except Exception as e:
            logger.error(f"Failed to get Hive flow {flow_id}: {str(e)}")
            raise

    def run_flow_sync(
        self,
        flow_id: str,
        input_data: Any,
        session_id: Optional[str] = None
    ) -> WorkflowExecutionResult:
        """Execute a Hive flow and return normalized result.

        Args:
            flow_id: ID of the flow to execute
            input_data: Input data (string or dict)
            session_id: Optional session ID for tracking

        Returns:
            WorkflowExecutionResult with normalized response
        """
        try:
            # Run the flow using Hive manager
            result = self.manager.run_flow_sync(flow_id, input_data, session_id)

            # Hive returns a dict with various fields
            # Extract the relevant information
            return WorkflowExecutionResult(
                success=result.get('success', True),
                result=result.get('result'),
                session_id=result.get('session_id', session_id),
                run_id=result.get('run_id'),
                metadata={
                    'agent_id': result.get('agent_id'),
                    'team_id': result.get('team_id'),
                    'workflow_id': result.get('workflow_id'),
                    'status': result.get('status'),
                    'coordinator_response': result.get('coordinator_response'),
                    'member_responses': result.get('member_responses'),
                    'steps_completed': result.get('steps_completed'),
                    'final_output': result.get('final_output')
                }
            )
        except Exception as e:
            logger.error(f"Failed to execute Hive flow {flow_id}: {str(e)}")
            return WorkflowExecutionResult(
                success=False,
                result=None,
                error=str(e)
            )

    async def validate(self) -> Dict[str, Any]:
        """Validate connection to Hive.

        Returns:
            Dictionary with validation status and info
        """
        try:
            return await self.manager.validate()
        except Exception as e:
            logger.error(f"Hive validation failed: {str(e)}")
            raise

    def get_default_sync_params(self, flow_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Get default sync parameters for Hive flows.

        Hive flows don't use component IDs like LangFlow. They follow a simple
        message/result convention.

        Args:
            flow_data: The flow data dictionary

        Returns:
            Dictionary with default input/output component names
        """
        return {
            "input_component": "message",
            "output_component": "result"
        }

    def normalize_flow_data(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Hive flow data to common format.

        Adds Hive-specific metadata to help identify flow type.

        Args:
            flow_data: Raw flow data from Hive

        Returns:
            Normalized flow data with additional metadata
        """
        # Add flow type from data
        if 'data' in flow_data and 'type' in flow_data['data']:
            flow_data['flow_type'] = flow_data['data']['type']
            # hive_agent, hive_team, or hive_workflow

        # Ensure standard fields exist
        if 'source' not in flow_data:
            flow_data['source'] = self.api_url

        return flow_data
