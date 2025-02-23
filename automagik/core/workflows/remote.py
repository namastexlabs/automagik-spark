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
from pydantic import BaseModel, Field, validator
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

    class Config:
        extra = "allow"  # Allow extra fields from the API

    @validator('gradient')
    def validate_gradient(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v == '1' or v.lower() == 'true'
        return bool(v)

    @validator('instance', always=True)
    def set_instance_from_source(cls, v, values):
        if not v and 'source_url' in values:
            src_url = values['source_url']
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
        self.client = None
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
            with httpx.Client() as sync_client:
                response = sync_client.request(
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

    async def _make_request_async(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make an async request to the API."""
        self._check_session_type(True)
        response = await self._request_with_retry(
            self.client,
            method,
            self._get_endpoint(endpoint),
            **kwargs
        )
        return self._process_response(response)

    def _make_request_sync(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a sync request to the API."""
        self._check_session_type(False)
        response = self._request_with_retry_sync(
            self.client,
            method,
            self._get_endpoint(endpoint),
            **kwargs
        )
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
        return await self._make_request_async(
            "POST",
            f"run/{flow_id}",
            params={"stream": "false"},
            json=request_data.dict()
        )

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
            client = httpx.Client(headers=self.headers, timeout=60.0)
            url = f"{self.api_url}/api/v1/run/{flow_id}"
            
            # Ensure input_data is a string
            if not isinstance(input_data, str):
                input_data = str(input_data)
            
            # Prepare payload
            request_data = FlowExecuteRequest(
                input_value=input_data,
                tweaks={}  # No tweaks needed for basic execution
            )
            
            # Execute workflow
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
            self.client = httpx.AsyncClient(verify=False, follow_redirects=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager."""
        if self.is_async and self.client:
            await self.client.aclose()

    def __enter__(self):
        """Enter sync context manager."""
        if not self.is_async:
            self.client = httpx.Client(verify=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sync context manager."""
        if not self.is_async and self.client:
            self.client.close()

    def _check_session_type(self, expected_async: bool):
        """Check if the session type matches the method type."""
        if self.is_async != expected_async:
            method_type = "async" if expected_async else "sync"
            raise ValueError(f"Cannot call {method_type} method on {'async' if self.is_async else 'sync'} session")
