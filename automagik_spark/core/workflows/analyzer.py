"""
Flow Analyzer Module

Provides functionality for analyzing LangFlow components and their properties.
Handles detection of input/output nodes and parameter analysis.
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class FlowAnalyzer:
    """Analyzes flow components and their properties."""

    @staticmethod
    def analyze_component(node: Dict[str, Any]) -> List[str]:
        """
        Analyze a component node to determine its tweakable params.

        Args:
            node: The node data from the flow

        Returns:
            List of parameters that can be modified
        """
        logger.debug(f"Analyzing component node: {node}")

        # Extract component type and template
        template = node.get("data", {}).get("node", {}).get("template", {})

        # Get tweakable parameters
        tweakable_params = []
        for param_name, param_data in template.items():
            # Skip internal parameters and code/password fields
            if (
                not param_name.startswith("_")
                and not param_data.get("code")
                and not param_data.get("password")
                and param_data.get("show", True)
            ):
                tweakable_params.append(param_name)

        return tweakable_params

    @staticmethod
    def get_flow_components(flow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract components from a flow.

        Args:
            flow_data: The complete flow data

        Returns:
            List of components with their details
        """
        components = []

        for node in flow_data.get("data", {}).get("nodes", []):
            params = FlowAnalyzer.analyze_component(node)
            node_info = {
                "id": node.get("id"),
                "name": node.get("data", {})
                .get("node", {})
                .get("display_name", "Unnamed"),
                "type": node.get("data", {})
                .get("node", {})
                .get("template", {})
                .get("_type", "Unknown"),
                "tweakable_params": params,
            }
            components.append(node_info)

        return components
