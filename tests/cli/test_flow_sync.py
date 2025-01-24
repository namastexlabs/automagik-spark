import pytest
import uuid
from unittest.mock import patch, Mock
import httpx
from automagik.cli.flow_sync import (
    analyze_component,
    get_remote_flows,
    get_flow_details,
    get_folder_name,
    select_components,
    sync_flow
)
from automagik.core.database.models import FlowDB


def test_analyze_component():
    component = {
        "data": {
            "node": {
                "template": {
                    "_type": "ChatInput",
                    "param1": {"show": True}
                }
            }
        }
    }
    result = analyze_component(component)
    assert result[0] is True
    assert result[1] is False
    assert result[2] == ["param1"]


@pytest.mark.asyncio
async def test_get_remote_flows():
    mock_response = [
        {"id": "1", "name": "Flow 1"},
        {"id": "2", "name": "Flow 2"}
    ]
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value=mock_response)
        )
        
        flows = await get_remote_flows("http://test", "test-key")
        assert len(flows) == 2
        assert flows[0]["id"] == "1"
        assert flows[0]["name"] == "Flow 1"
        assert flows[1]["id"] == "2"
        assert flows[1]["name"] == "Flow 2"

@pytest.mark.asyncio
async def test_get_flow_details():
    mock_flow = {
        "id": "1",
        "name": "Test Flow",
        "data": {"nodes": []}
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value=mock_flow)
        )
        
        flow = await get_flow_details("http://test", "test-key", "1")
        assert flow["name"] == "Test Flow"
        assert flow["id"] == "1"
        assert "data" in flow

@pytest.mark.asyncio
async def test_get_folder_name():
    mock_folder = {
        "id": "1",
        "name": "Test Folder"
    }
    
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value=mock_folder)
        )
        
        name = await get_folder_name("http://test", "test-key", "1")
        assert name == "Test Folder"


def test_select_components():
    components = [
        {
            "id": "1",
            "data": {
                "node": {
                    "template": {
                        "_type": "ChatInput"
                    }
                }
            }
        },
        {
            "id": "2",
            "data": {
                "node": {
                    "template": {
                        "_type": "ChatOutput"
                    }
                }
            }
        }
    ]
    input_id, output_id, _ = select_components({"data": {"nodes": components}})
    assert input_id == "1"
    assert output_id == "2"


@pytest.mark.asyncio
async def test_sync_flow(db_session):
    flow_id = uuid.uuid4()
    flow_data = {
        "id": str(flow_id),
        "name": "Test Flow",
        "folder_id": "test-folder",
        "data": {
            "nodes": [
                {
                    "id": "1",
                    "data": {
                        "node": {
                            "template": {
                                "_type": "ChatInput",
                                "param1": {"show": True}
                            }
                        }
                    }
                },
                {
                    "id": "2",
                    "data": {
                        "node": {
                            "template": {
                                "_type": "ChatOutput"
                            }
                        }
                    }
                }
            ]
        }
    }
    
    with patch('automagik.cli.flow_sync.get_folder_name') as mock_folder:
        mock_folder.return_value = "Test Folder"
        
        flow_db = await sync_flow(db_session, flow_data)
        assert flow_db.id == flow_id
        assert flow_db.name == "Test Flow"
        assert flow_db.source == "langflow"
        assert flow_db.source_id == str(flow_id)
        assert flow_db.folder_id == "test-folder"
        assert flow_db.folder_name == "Test Folder"
        assert len(flow_db.components) == 2
