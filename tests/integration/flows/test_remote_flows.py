
"""Integration tests for remote flow functionality."""

import pytest
import httpx
from unittest.mock import MagicMock, AsyncMock, patch

from automagik_spark.core.workflows.remote import LangFlowManager
from automagik_spark.core.config import LANGFLOW_API_URL, LANGFLOW_API_KEY

pytestmark = pytest.mark.integration

def requires_api_config(func):
    """Decorator to skip tests if API configuration is not available."""
    return pytest.mark.skipif(
        not (LANGFLOW_API_URL and LANGFLOW_API_KEY),
        reason="LangFlow API configuration (URL and API key) not found"
    )(func)

@pytest.mark.asyncio
@requires_api_config
async def test_remote_api_error_handling(session):
    """Test error handling with remote API."""
    # Mock client that raises an error
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.HTTPStatusError(
        message="Invalid API key",
        request=MagicMock(),
        response=MagicMock(status_code=401)
    ))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock()

    with patch("httpx.AsyncClient", return_value=mock_client):
        async with LangFlowManager(session) as remote:
            with pytest.raises(httpx.HTTPStatusError):
                await remote.list_remote_flows()


