
"""Test flow analyzer functionality."""

import pytest
from automagik.core.workflows.analyzer import FlowAnalyzer

def test_analyze_component_with_tweakable_params():
    """Test analyzing a component with tweakable parameters."""
    # Test node with various parameter types
    node = {
        "data": {
            "node": {
                "template": {
                    "text": {"type": "str", "show": True},
                    "number": {"type": "int", "show": True},
                    "_hidden": {"type": "str", "show": True},
                    "password": {"type": "str", "password": True},
                    "code": {"type": "str", "code": True},
                    "hidden_param": {"type": "str", "show": False}
                }
            }
        }
    }

    params = FlowAnalyzer.analyze_component(node)
    
    # Should only include visible, non-internal, non-password, non-code params
    assert "text" in params
    assert "number" in params
    assert "_hidden" not in params
    assert "password" not in params
    assert "code" not in params
    assert "hidden_param" not in params

def test_analyze_component_empty_node():
    """Test analyzing an empty component node."""
    node = {}
    params = FlowAnalyzer.analyze_component(node)
    assert params == []

    node = {"data": {}}
    params = FlowAnalyzer.analyze_component(node)
    assert params == []

def test_get_flow_components():
    """Test extracting components from a flow."""
    flow_data = {
        "data": {
            "nodes": [
                {
                    "id": "node1",
                    "data": {
                        "node": {
                            "display_name": "Input Node",
                            "template": {
                                "_type": "input",
                                "text": {"type": "str", "show": True}
                            }
                        }
                    }
                },
                {
                    "id": "node2",
                    "data": {
                        "node": {
                            "display_name": "Process Node",
                            "template": {
                                "_type": "process",
                                "number": {"type": "int", "show": True},
                                "_hidden": {"type": "str", "show": True}
                            }
                        }
                    }
                }
            ]
        }
    }

    components = FlowAnalyzer.get_flow_components(flow_data)
    
    assert len(components) == 2
    
    # Check first component
    assert components[0]["id"] == "node1"
    assert components[0]["name"] == "Input Node"
    assert components[0]["type"] == "input"
    assert components[0]["tweakable_params"] == ["text"]
    
    # Check second component
    assert components[1]["id"] == "node2"
    assert components[1]["name"] == "Process Node"
    assert components[1]["type"] == "process"
    assert components[1]["tweakable_params"] == ["number"]

def test_get_flow_components_empty_flow():
    """Test extracting components from an empty flow."""
    flow_data = {}
    components = FlowAnalyzer.get_flow_components(flow_data)
    assert components == []

    flow_data = {"data": {}}
    components = FlowAnalyzer.get_flow_components(flow_data)
    assert components == []

def test_get_flow_components_missing_fields():
    """Test handling of components with missing fields."""
    flow_data = {
        "data": {
            "nodes": [
                {
                    "id": "node1",
                    # Missing data.node
                },
                {
                    "data": {
                        "node": {
                            # Missing display_name and template
                        }
                    }
                }
            ]
        }
    }

    components = FlowAnalyzer.get_flow_components(flow_data)
    
    assert len(components) == 2
    for component in components:
        assert "id" in component
        assert "name" in component
        assert "type" in component
        assert "tweakable_params" in component
        assert component["tweakable_params"] == []


