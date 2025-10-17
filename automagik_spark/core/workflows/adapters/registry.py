"""Register all available workflow adapters."""

from .factory import AdapterRegistry
from .hive_adapter import HiveAdapter
from .langflow_adapter import LangFlowAdapter
from ...schemas.source import SourceType


def register_adapters():
    """Register all built-in workflow adapters."""
    AdapterRegistry.register(SourceType.LANGFLOW, LangFlowAdapter)
    AdapterRegistry.register(SourceType.AUTOMAGIK_HIVE, HiveAdapter)


# Auto-register adapters when module is imported
register_adapters()
