"""LangFlow API integration."""

import json
import logging
import asyncio
from typing import Any, Dict, List, Optional, TypeVar, Callable, Generic, Union
from uuid import UUID
from functools import wraps
from dataclasses import dataclass
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator, ConfigDict
from ...api.config import get_langflow_api_url, get_langflow_api_key
from ...api.models import (
    WorkflowBase,
    WorkflowCreate,
    WorkflowResponse,
)
from ..database.models import Workflow
from ..database.session import get_session

logger = logging.getLogger(__name__)

LANGFLOW_API_URL = get_langflow_api_url()
LANGFLOW_API_KEY = get_langflow_api_key()
API_VERSION = "v1"

T = TypeVar('T')
ResponseT = TypeVar('ResponseT', bound=BaseModel)

class APIError(Exception):
    """Base class for API errors."""
    pass

class APIClientError(APIError):
    """Client-side API errors (4xx)."""
    pass

class APIServerError(APIError):
    """Server-side API errors (5xx)."""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded."""
    pass

class FlowResponse(BaseModel):
    """Base model for flow responses."""
    id: str
    name: str
    description: Optional[str] = None
    data: Dict[str, Any]
    is_component: bool = False
    folder_id: Optional[str] = None
    folder_name: Optional[str] = None
    icon: Optional[str] = None
    icon_bg_color: Optional[str] = None
    gradient: Any = False  # API returns '2' instead of boolean
    liked: Optional[bool] = False
    tags: Optional[List[str]] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    source_url: Optional[str] = None  # Added for source tracking
    instance: Optional[str] = None  # Added for instance name

    # Pydantic v2 config
    model_config = ConfigDict(extra="allow")

    @field_validator('gradient', mode='before')
    def _validate_gradient(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v == '1' or v.lower() == 'true'
        return bool(v)

    @field_validator('instance', mode='after')
    def _set_instance_from_source(cls, v, info):
        if not v:
            src_url = info.data.get('source_url') if info else None
            if src_url:
                instance = src_url.split('://')[-1].split('/')[0]
                instance = instance.split('.')[0]
                return instance
        return v

class FlowComponentsResponse(BaseModel):
    """Response model for flow components."""
    components: Dict[str, Any]

class FlowExecuteRequest(BaseModel):
    """Request model for flow execution."""
    input_value: Any
    output_type: str = "debug"
    input_type: str = "chat"
    tweaks: Dict[str, Any] = Field(default_factory=dict)

class FlowExecuteResponse(BaseModel):
    """Response model for flow execution."""
    result: Any

class BaseAPIClient:
    """Base class for API clients with common functionality."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        version: str = API_VERSION,
        max_retries: int = 3,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.version = version
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "automagik/1.0"
        }
        if api_key:
            self.headers["x-api-key"] = api_key

    def _get_endpoint(self, path: str) -> str:
        """Construct API endpoint URL."""
        return f"{self.base_url}/api/{self.version}/{path.lstrip('/')}"

    @staticmethod
    def _handle_error_response(response: httpx.Response) -> None:
        """Handle error responses from the API."""
        if 400 <= response.status_code < 500:
            raise APIClientError(f"Client error: {response.status_code} - {response.text}")
        elif 500 <= response.status_code < 600:
            raise APIServerError(f"Server error: {response.status_code} - {response.text}")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        response.raise_for_status()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(APIServerError),
        reraise=True
    )
    async def _request_with_retry(
        self,
        client: httpx.AsyncClient,
        method: str,
        endpoint: str,
        **kwargs
    ) -> httpx.Response:
        """Make an HTTP request with retry logic."""
        try:
            response = await client.request(
                method,
                endpoint,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            self._handle_error_response(response)
            return response
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError):
                logger.error(f"HTTP Status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            raise

class LangFlowManager:
    """Manager for remote LangFlow operations."""

    def __init__(
        self,
        session: Optional[AsyncSession | Session] = None,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        source_id: Optional[UUID] = None,
    ):
        """Initialize LangFlow manager."""
        self.api_url = api_url if api_url else LANGFLOW_API_URL
        self.api_key = api_key if api_key else LANGFLOW_API_KEY
        self.version = API_VERSION
        self.max_retries = 3
        self.timeout = 30.0
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "automagik/1.0"
        }
        if self.api_key:
            self.headers["x-api-key"] = self.api_key
        self.session = session
        self.source_id = source_id
        self._client = None
        self.is_async = isinstance(session, AsyncSession) if session else False

    def _get_endpoint(self, path: str) -> str:
        """Construct API endpoint URL."""
        return f"{self.api_url}/api/{self.version}/{path.lstrip('/')}"

    @staticmethod
    def _handle_error_response(response: httpx.Response) -> None:
        """Handle error responses from the API."""
        if 400 <= response.status_code < 500:
            raise APIClientError(f"Client error: {response.status_code} - {response.text}")
        elif 500 <= response.status_code < 600:
            raise APIServerError(f"Server error: {response.status_code} - {response.text}")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        response.raise_for_status()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(APIServerError),
        reraise=True
    )
    async def _request_with_retry(
        self,
        client: httpx.AsyncClient,
        method: str,
        endpoint: str,
        **kwargs
    ) -> httpx.Response:
        """Make an HTTP request with retry logic."""
        try:
            response = await client.request(
                method,
                endpoint,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            self._handle_error_response(response)
            return response
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError):
                logger.error(f"HTTP Status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(APIServerError),
        reraise=True
    )
    def _request_with_retry_sync(
        self,
        client: httpx.Client,
        method: str,
        endpoint: str,
        **kwargs
    ) -> httpx.Response:
        """Make a synchronous HTTP request with retry logic."""
        try:
            # Use the client passed to the method instead of creating a new one
            response = client.request(
                method,
                endpoint,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            self._handle_error_response(response)
            return response
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError):
                logger.error(f"HTTP Status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            raise

    def _process_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Process API response into a dictionary."""
        data = response.json()
        if isinstance(data, dict):
            return dict(data)
        elif isinstance(data, list):
            return [dict(item) for item in data]
        return {}

    async def _execute_async_request(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Execute an async request with a temporary client."""
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout, verify=False) as temp_client:
            response = await temp_client.request(
                method,
                self._get_endpoint(endpoint),
                **kwargs
            )
            self._handle_error_response(response)
            return self._process_response(response)

    async def _make_request_async(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Make a request to the LangFlow API with automatic client creation.
        
        This handles the case where the client may not be initialized yet.
        """
        # Create client if it doesn't exist
        if not self._client:
            self._client = httpx.AsyncClient(verify=False, timeout=30.0)
        
        url = f"{self.api_url}/api/v1/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        try:
            # Use verb-specific method if it exists (helps with unit tests that patch .get etc.)
            verb = method.lower()
            if hasattr(self._client, verb):
                response = await getattr(self._client, verb)(
                    url,
                    headers=headers,
                    **kwargs
                )
            else:
                response = await self._client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    **kwargs
                )
            
            # Log the request URL and status
            logger.debug(f"LangFlow API request: {method} {url}")
            logger.debug(f"Response status: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Try to parse as JSON, return empty dict if not JSON
            try:
                return response.json()
            except ValueError:
                # Handle non-JSON responses (might be text or other content)
                return {"content": response.text, "status": "success"}
                
        except httpx.HTTPStatusError as e:
            # Log and re-raise so callers/tests can handle it
            logger.error(f"HTTP error for {url}: {e.response.status_code} - {e.response.text}")
            raise
            
        except httpx.RequestError as e:
            # Log and handle request errors (connection, timeout, etc.)
            logger.error(f"Request error for {url}: {str(e)}")
            return {"error": str(e), "status": "error"}
            
        except Exception as e:
            # Log and handle any other exceptions
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {"error": str(e), "status": "error"}

    def _make_request_sync(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a sync request to the API."""
        # Log a warning instead of raising an error if session type doesn't match
        if self.is_async:
            logger.warning("Calling sync method on async session. This may cause issues.")
        
        # Use a new client instance to avoid session type issues
        with httpx.Client(headers=self.headers, timeout=self.timeout, verify=False) as client:
            response = client.request(
                method,
                self._get_endpoint(endpoint),
                **kwargs
            )
            self._handle_error_response(response)
            return self._process_response(response)

    async def _get_folders(self) -> List[str]:
        """Get list of valid folder IDs."""
        folders = await self._make_request_async("GET", "folders/")
        return [folder['id'] for folder in folders]

    def _get_folders_sync(self) -> List[str]:
        """Get list of valid folder IDs (sync version)."""
        folders = self._make_request_sync("GET", "folders/")
        return [folder['id'] for folder in folders]

    async def list_flows(self, source_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all flows from LangFlow API.
        
        Args:
            source_url: Optional URL to list flows from. If provided, will temporarily
                      switch to this URL for the request.
            
        Returns:
            List[Dict[str, Any]]: List of flows, excluding:
                - Components (is_component=True)
                - Templates (flows without a valid folder_id)
        """
        # Save current API URL and key if we're switching
        current_url = None
        current_key = None
        if source_url:
            current_url = self.api_url
            current_key = self.api_key
            self.api_url = source_url
        
        try:
            # Get valid folder IDs first
            valid_folders = await self._get_folders()
            
            # Get all flows
            flows = await self._make_request_async("GET", "flows/")
            
            # Filter flows to exclude:
            # 1. Components (is_component=True)
            # 2. Templates (flows without a valid folder_id)
            return [
                flow for flow in flows 
                if not flow.get('is_component', False)  # Not a component
                and flow.get('folder_id') in valid_folders  # Has valid folder
            ]
        finally:
            # Restore original API URL and key if we switched
            if source_url:
                self.api_url = current_url
                self.api_key = current_key

    def list_flows_sync(self, source_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all flows from LangFlow API (sync version).
        
        Args:
            source_url: Optional URL to list flows from. If provided, will temporarily
                      switch to this URL for the request.
            
        Returns:
            List[Dict[str, Any]]: List of flows, excluding:
                - Components (is_component=True)
                - Templates (flows without a valid folder_id)
        """
        # Save current API URL and key if we're switching
        current_url = None
        current_key = None
        if source_url:
            current_url = self.api_url
            current_key = self.api_key
            self.api_url = source_url
        
        try:
            # Get valid folder IDs first
            valid_folders = self._get_folders_sync()
            
            # Get all flows
            flows = self._make_request_sync("GET", "flows/")
            
            # Filter flows to exclude:
            # 1. Components (is_component=True)
            # 2. Templates (flows without a valid folder_id)
            return [
                flow for flow in flows 
                if not flow.get('is_component', False)  # Not a component
                and flow.get('folder_id') in valid_folders  # Has valid folder
            ]
        finally:
            # Restore original API URL and key if we switched
            if source_url:
                self.api_url = current_url
                self.api_key = current_key

    # Alias for backward compatibility
    list_remote_flows = list_flows

    async def get_flow(self, flow_id: str) -> Dict[str, Any]:
        """Get flow details from LangFlow API."""
        return await self._make_request_async("GET", f"flows/{flow_id}")

    def get_flow_sync(self, flow_id: str) -> Dict[str, Any]:
        """Get flow details from LangFlow API (sync version)."""
        return self._make_request_sync("GET", f"flows/{flow_id}")

    async def get_flow_components(self, flow_id: str) -> Dict[str, Any]:
        """Get flow components from LangFlow API."""
        return await self._make_request_async("GET", f"flows/{flow_id}/components/")

    def get_flow_components_sync(self, flow_id: str) -> Dict[str, Any]:
        """Get flow components from LangFlow API (sync version)."""
        return self._make_request_sync("GET", f"flows/{flow_id}/components/")

    async def run_flow(self, flow_id: str, input_data: str | Dict[str, Any]) -> Dict[str, Any]:
        """Run a flow with input data."""
        try:
            # Get flow data to find component IDs
            flow_data = await self.get_flow(flow_id)
            if not flow_data:
                raise ValueError(f"Flow {flow_id} not found")

            # Get input and output component IDs
            input_component = None
            output_component = None
            for node in flow_data.get('data', {}).get('nodes', []):
                node_type = node.get('data', {}).get('type', '')
                if node_type == 'ChatInput':
                    input_component = node['id']
                elif node_type == 'ChatOutput':
                    output_component = node['id']

            if not input_component or not output_component:
                raise ValueError("Could not find chat input and output components in flow")

            request_data = FlowExecuteRequest(
                input_value=input_data,
                tweaks={
                    input_component: {},
                    output_component: {}
                }
            )
            
            # Use _make_request_async which now handles missing client
            return await self._make_request_async(
                "POST",
                f"run/{flow_id}",
                params={"stream": "false"},
                json=request_data.dict()
            )
        except Exception as e:
            logger.error(f"Error in run_flow: {str(e)}")
            raise

    def run_flow_sync(self, flow_id: str, input_data: str | Dict[str, Any]) -> Dict[str, Any]:
        """Run a flow with input data (sync version)."""
        # Get flow data to find component IDs
        flow_data = self.get_flow_sync(flow_id)
        if not flow_data:
            raise ValueError(f"Flow {flow_id} not found")

        # Get input and output component IDs
        input_component = None
        output_component = None
        for node in flow_data.get('data', {}).get('nodes', []):
            node_type = node.get('data', {}).get('type', '')
            if node_type == 'ChatInput':
                input_component = node['id']
            elif node_type == 'ChatOutput':
                output_component = node['id']

        if not input_component or not output_component:
            raise ValueError("Could not find chat input and output components in flow")

        request_data = FlowExecuteRequest(
            input_value=input_data,
            tweaks={
                input_component: {},
                output_component: {}
            }
        )
        return self._make_request_sync(
            "POST",
            f"run/{flow_id}",
            params={"stream": "false"},
            json=request_data.dict()
        )

    def run_workflow_sync(self, flow_id: str, input_data: str) -> Dict[str, Any]:
        """Run a workflow synchronously."""
        try:
            # Don't check session type here to allow this method to be called from both contexts
            # self._check_session_type(False)
            
            # Ensure input_data is a string
            if not isinstance(input_data, str):
                input_data = str(input_data)
            
            # Prepare payload
            request_data = FlowExecuteRequest(
                input_value=input_data,
                tweaks={}  # No tweaks needed for basic execution
            )
            
            # Execute workflow using a new client instance to avoid session type issues
            with httpx.Client(headers=self.headers, timeout=60.0, verify=False) as client:
                url = f"{self.api_url}/api/v1/run/{flow_id}"
                response = client.post(url, json=request_data.dict(), params={"stream": "false"})
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error executing workflow: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error executing workflow: {str(e)}")
            raise

    async def __aenter__(self):
        """Enter async context manager."""
        if self.is_async:
            self._client = httpx.AsyncClient(verify=False, follow_redirects=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager."""
        if self.is_async and self._client:
            await self._client.aclose()

    def __enter__(self):
        """Enter sync context manager."""
        if not self.is_async:
            self._client = httpx.Client(verify=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sync context manager."""
        if not self.is_async and self._client:
            self._client.close()

    def _check_session_type(self, expected_async: bool):
        """Check if the session type matches the method type."""
        if self.is_async != expected_async:
            method_type = "async" if expected_async else "sync"
            session_type = "async" if self.is_async else "sync"
            logger.warning(f"Session type mismatch: Calling {method_type} method on {session_type} session. This may cause issues.")
            # Instead of raising an error, we'll just log a warning and continue
            # This allows async methods to be called on sync sessions and vice versa
            # raise ValueError(f"Cannot call {method_type} method on {'async' if self.is_async else 'sync'} session")
