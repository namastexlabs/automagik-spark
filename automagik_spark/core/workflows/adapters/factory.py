"""Adapter factory and registry."""

from typing import Dict, Type, Optional, Any
from .base import BaseWorkflowAdapter


class AdapterRegistry:
    """Registry for workflow adapters."""

    _adapters: Dict[str, Type[BaseWorkflowAdapter]] = {}

    @classmethod
    def register(cls, source_type: str, adapter_class: Type[BaseWorkflowAdapter]):
        """Register an adapter for a source type.

        Args:
            source_type: Source type identifier (e.g., "langflow", "automagik-hive")
            adapter_class: Adapter class to register
        """
        cls._adapters[source_type] = adapter_class

    @classmethod
    def get_adapter(
        cls,
        source_type: str,
        api_url: str,
        api_key: str,
        source_id: Optional[Any] = None,
    ) -> BaseWorkflowAdapter:
        """Get an adapter instance for the given source type.

        Args:
            source_type: Source type identifier
            api_url: Base URL for the source API
            api_key: API key for authentication
            source_id: Optional source ID

        Returns:
            Adapter instance

        Raises:
            ValueError: If no adapter is registered for the source type
        """
        adapter_class = cls._adapters.get(source_type)
        if not adapter_class:
            raise ValueError(
                f"No adapter registered for source type: {source_type}. "
                f"Available types: {', '.join(cls.list_supported_types())}"
            )
        return adapter_class(api_url=api_url, api_key=api_key, source_id=source_id)

    @classmethod
    def list_supported_types(cls) -> list[str]:
        """List all registered source types.

        Returns:
            List of source type identifiers
        """
        return list(cls._adapters.keys())

    @classmethod
    def is_supported(cls, source_type: str) -> bool:
        """Check if a source type is supported.

        Args:
            source_type: Source type to check

        Returns:
            True if supported, False otherwise
        """
        return source_type in cls._adapters
