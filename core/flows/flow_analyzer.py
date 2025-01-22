"""
Flow Analyzer Module

This module provides functionality for analyzing LangFlow components and their properties.
"""

from typing import Dict, Any, Tuple, List


class FlowAnalyzer:
    @staticmethod
    def analyze_component(node: Dict[str, Any]) -> Tuple[bool, bool, List[str]]:
        """
        Analyze a component node to determine if it's input/output and its tweakable params.
        
        Args:
            node: The node data from the flow
            
        Returns:
            Tuple containing:
            - is_input (bool): Whether the component is an input component
            - is_output (bool): Whether the component is an output component
            - tweakable_params (List[str]): List of parameters that can be modified
        """
        is_input = False
        is_output = False
        tweakable_params = []
        
        # Check if it's an input/output component
        component_type = node.get("data", {}).get("node", {}).get("template", {}).get("_type", "").lower()
        if "chatinput" in component_type or "chatmessages" in component_type:
            is_input = True
        elif "chatoutput" in component_type or "chatmessagehistory" in component_type:
            is_output = True
        
        # Identify tweakable parameters
        template = node.get("data", {}).get("node", {}).get("template", {})
        for param_name, param_data in template.items():
            # Skip internal parameters and code/password fields
            if (not param_name.startswith("_") and 
                not param_data.get("code") and 
                not param_data.get("password") and
                param_data.get("show", True)):
                tweakable_params.append(param_name)
        
        return is_input, is_output, tweakable_params

    @staticmethod
    def get_component_info(node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant information from a component node.
        
        Args:
            node: The node data from the flow
            
        Returns:
            Dict containing component information including id, type, and name
        """
        return {
            "id": node.get("id", ""),
            "type": node.get("data", {}).get("node", {}).get("template", {}).get("type", "unknown"),
            "name": node.get("data", {}).get("node", {}).get("template", {}).get("display_name", node.get("id", ""))
        }
