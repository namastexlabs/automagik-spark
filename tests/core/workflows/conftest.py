"""Test fixtures for flow tests."""

import pytest
from unittest.mock import AsyncMock


class AsyncClientMock(AsyncMock):
    """Mock for httpx.AsyncClient."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get = AsyncMock()
        self.post = AsyncMock()
        self.put = AsyncMock()
        self.delete = AsyncMock()
        self.aclose = AsyncMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()


@pytest.fixture
def mock_http_client():
    """Create a mock HTTP client."""
    return AsyncClientMock()


@pytest.fixture
def mock_flows():
    """Create mock flows for testing."""
    return [
        {
            "id": "flow1",
            "name": "Test Flow 1",
            "description": "Test flow 1 description",
            "data": {
                "nodes": [{"id": "node1", "type": "input", "data": {"value": "test"}}],
                "edges": [],
            },
        },
        {
            "id": "flow2",
            "name": "Test Flow 2",
            "description": "Test flow 2 description",
            "data": {
                "nodes": [{"id": "node1", "type": "input", "data": {"value": "test"}}],
                "edges": [],
            },
        },
    ]
