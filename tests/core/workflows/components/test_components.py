
"""Tests for flow components functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, call

from automagik.core.workflows.manager import WorkflowManager

@pytest.fixture
def flow_manager(session):
    """Create a WorkflowManager instance."""
    return WorkflowManager(session)

@pytest.fixture
def mock_data_dir():
    """Get the mock data directory."""
    return Path(__file__).parent.parent.parent.parent / "mock_data" / "flows"

@pytest.fixture
def mock_flows(mock_data_dir):
    """Load mock flow data."""
    with open(mock_data_dir / "flows.json") as f:
        return json.load(f)

@pytest.mark.asyncio
async def test_get_flow_components(flow_manager, mock_flows):
    """Test getting flow components."""
    # Create a simple mock flow with known components
    flow_data = {
        "id": "test-flow-id",
        "data": {
            "nodes": [
                {
                    "type": "ChatInput",
                    "id": "ChatInput-1",
                    "data": {
                        "node": {
                            "id": "input1",
                            "type": "ChatInput",
                            "name": "Chat Input",
                            "description": "A chat input component"
                        }
                    }
                },
                {
                    "type": "ChatOutput",
                    "id": "ChatOutput-1",
                    "data": {
                        "node": {
                            "id": "output1",
                            "type": "ChatOutput",
                            "name": "Chat Output",
                            "description": "A chat output component"
                        }
                    }
                },
                {
                    "type": "Prompt",
                    "id": "Prompt-1",
                    "data": {
                        "node": {
                            "id": "prompt1",
                            "type": "Prompt",
                            "name": "Prompt",
                            "description": "A prompt component"
                        }
                    }
                }
            ]
        }
    }

    # Mock the LangFlow manager
    mock_langflow = AsyncMock()
    mock_langflow.sync_flow = AsyncMock(return_value={"flow": flow_data})
    flow_manager._get_langflow_manager = AsyncMock(return_value=mock_langflow)

    # Get components
    components = await flow_manager.get_flow_components("test-flow-id")
    
    # Verify the components
    assert len(components) == 3  # We should get 3 components
    assert all(isinstance(comp, dict) for comp in components)
    assert all(comp.get("id") for comp in components)
    assert all(comp.get("type") for comp in components)
    assert all(comp.get("name") for comp in components)
    assert all(comp.get("description") for comp in components)

    # Verify specific components
    component_types = {comp["type"] for comp in components}
    assert component_types == {"ChatInput", "ChatOutput", "Prompt"}


