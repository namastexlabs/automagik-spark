"""Base workflow adapter interface."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class WorkflowExecutionResult:
    """Unified result format across all workflow sources."""
    success: bool
    result: Any  # The actual response content
    session_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class BaseWorkflowAdapter(ABC):
    """Abstract base adapter for workflow sources."""

    def __init__(self, api_url: str, api_key: str, source_id: Optional[Any] = None):
        """Initialize adapter.

        Args:
            api_url: Base URL for the workflow source API
            api_key: API key for authentication
            source_id: Optional source ID for tracking
        """
        self.api_url = api_url
        self.api_key = api_key
        self.source_id = source_id

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return the source type identifier."""
        pass

    @abstractmethod
    def list_flows_sync(self) -> List[Dict[str, Any]]:
        """List available flows from this source (synchronous).

        Returns:
            List of flow dictionaries
        """
        pass

    @abstractmethod
    def get_flow_sync(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific flow by ID (synchronous).

        Args:
            flow_id: ID of the flow to retrieve

        Returns:
            Flow dictionary if found, None otherwise
        """
        pass

    @abstractmethod
    def run_flow_sync(
        self,
        flow_id: str,
        input_data: Any,
        session_id: Optional[str] = None
    ) -> WorkflowExecutionResult:
        """Execute a flow and return normalized result (synchronous).

        Args:
            flow_id: ID of the flow to execute
            input_data: Input data for the flow
            session_id: Optional session ID for tracking

        Returns:
            WorkflowExecutionResult with normalized response
        """
        pass

    @abstractmethod
    async def validate(self) -> Dict[str, Any]:
        """Validate connection to the source.

        Returns:
            Dictionary with validation status and info
        """
        pass

    def get_default_sync_params(self, flow_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Get default parameters for syncing this flow type.

        Override this in subclasses for source-specific defaults.

        Args:
            flow_data: The flow data dictionary

        Returns:
            Dictionary with 'input_component' and 'output_component' keys
        """
        return {
            "input_component": "message",
            "output_component": "result"
        }

    def normalize_flow_data(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize flow data to common format.

        Override this in subclasses for source-specific transformations.

        Args:
            flow_data: Raw flow data from source

        Returns:
            Normalized flow data
        """
        return flow_data

    def __enter__(self):
        """Enter sync context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sync context manager."""
        pass
