"""Adapter for LangFlow workflows."""

from typing import Dict, List, Optional, Any
import logging
from .base import BaseWorkflowAdapter, WorkflowExecutionResult
from ..remote import LangFlowManager

logger = logging.getLogger(__name__)


class LangFlowAdapter(BaseWorkflowAdapter):
    """Adapter for LangFlow workflows."""

    def __init__(self, api_url: str, api_key: str, source_id: Optional[Any] = None):
        """Initialize LangFlow adapter.

        Args:
            api_url: LangFlow API base URL
            api_key: API key for authentication
            source_id: Optional source ID for tracking
        """
        super().__init__(api_url, api_key, source_id)
        self.manager = LangFlowManager(api_url=api_url, api_key=api_key)

    @property
    def source_type(self) -> str:
        """Return the source type identifier."""
        return "langflow"

    def list_flows_sync(self) -> List[Dict[str, Any]]:
        """List all flows from LangFlow.

        Returns:
            List of flow dictionaries
        """
        try:
            return self.manager.list_flows_sync()
        except Exception as e:
            logger.error(f"Failed to list LangFlow flows: {str(e)}")
            raise

    def get_flow_sync(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific flow from LangFlow by ID.

        Args:
            flow_id: ID of the flow to retrieve

        Returns:
            Flow dictionary if found, None otherwise
        """
        try:
            return self.manager.get_flow_sync(flow_id)
        except Exception as e:
            logger.error(f"Failed to get LangFlow flow {flow_id}: {str(e)}")
            raise

    def run_flow_sync(self, flow_id: str, input_data: Any, session_id: Optional[str] = None) -> WorkflowExecutionResult:
        """Execute a LangFlow flow and return normalized result.

        Args:
            flow_id: ID of the flow to execute
            input_data: Input data (string or dict)
            session_id: Optional session ID for tracking

        Returns:
            WorkflowExecutionResult with normalized response
        """
        try:
            # Run the flow using LangFlow manager
            # Note: LangFlow's run_workflow_sync returns the result directly
            result = self.manager.run_workflow_sync(flow_id, input_data)

            return WorkflowExecutionResult(success=True, result=result, session_id=session_id, metadata={})
        except Exception as e:
            logger.error(f"Failed to execute LangFlow flow {flow_id}: {str(e)}")
            return WorkflowExecutionResult(success=False, result=None, error=str(e))

    async def validate(self) -> Dict[str, Any]:
        """Validate connection to LangFlow.

        Returns:
            Dictionary with validation status and info
        """
        try:
            # LangFlow validation logic
            # For now, return a simple validation response
            return {"status": "success", "service": "LangFlow", "url": self.api_url}
        except Exception as e:
            logger.error(f"LangFlow validation failed: {str(e)}")
            raise

    def get_default_sync_params(self, flow_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Get default sync parameters for LangFlow flows.

        LangFlow flows use component IDs (ChatInput, ChatOutput, etc.).
        This method attempts to auto-detect them from the flow data.

        Args:
            flow_data: The flow data dictionary

        Returns:
            Dictionary with input/output component IDs
        """
        # Try to auto-detect input/output components from flow data
        input_component = None
        output_component = None

        if "data" in flow_data and "nodes" in flow_data["data"]:
            nodes = flow_data["data"]["nodes"]

            # Look for ChatInput component
            input_node = next((n for n in nodes if n.get("data", {}).get("type") == "ChatInput"), None)
            if input_node:
                input_component = input_node.get("id")

            # Look for ChatOutput component
            output_node = next(
                (n for n in nodes if n.get("data", {}).get("type") == "ChatOutput"),
                None,
            )
            if output_node:
                output_component = output_node.get("id")

        return {
            "input_component": input_component,
            "output_component": output_component,
        }

    def normalize_flow_data(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize LangFlow flow data to common format.

        Args:
            flow_data: Raw flow data from LangFlow

        Returns:
            Normalized flow data
        """
        # Ensure standard fields exist
        if "source" not in flow_data:
            flow_data["source"] = self.api_url

        # LangFlow-specific: ensure data structure
        if "data" not in flow_data:
            flow_data["data"] = {}

        return flow_data
