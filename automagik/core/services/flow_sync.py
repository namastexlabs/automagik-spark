"""
Flow Sync Module

This module handles synchronization with the LangFlow server, including fetching flows
and their details.
"""

import logging
import re
import json
from typing import Dict, List, Any, Optional
import httpx
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..models import Flow, Base
from sqlalchemy import text
import uuid
import os

logger = logging.getLogger(__name__)

class FlowSync:
    """Class for syncing flows between LangFlow and the database."""
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize FlowSync with API credentials.
        
        Args:
            api_url: Base URL for the LangFlow API
            api_key: API key for authentication
        """
        self.api_url = api_url or os.getenv("LANGFLOW_API_URL")
        self.api_key = api_key or os.getenv("LANGFLOW_API_KEY")

        if not self.api_url or not self.api_key:
            logger.error("Missing required environment variables")
            return

        # Set up headers for API requests
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key,
        }

        logger.debug(f"Initialized FlowSync with API URL: {self.api_url}")

    async def get_remote_flows(self) -> List[Dict[str, Any]]:
        """
        Fetch flows from LangFlow server.
        
        Returns:
            List of flow dictionaries
        """
        url = f"{self.api_url}/api/v1/flows/"
        logger.debug(f"Fetching flows from: {url}")
        
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return []
                
                data = response.json()
                if not isinstance(data, list):
                    logger.error(f"Expected list of flows, got {type(data)}")
                    return []
                
                # Filter out template flows
                filtered_data = [
                    flow for flow in data 
                    if not flow.get("is_template", False)
                ]
                
                return filtered_data
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error fetching flows: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching flows: {str(e)}")
            return []

    async def get_flow_details(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get details of a flow from the server.

        Args:
            flow_id (str): ID of the flow to get details for.

        Returns:
            Optional[Dict[str, Any]]: Flow details if successful, None otherwise.
        """
        try:
            # Get flow details
            url = f"{self.api_url}/api/v1/flows/{flow_id}"
            logger.debug(f"Fetching flow details from: {url}")
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                flow_details = response.json()

                # Handle string data by attempting to parse it
                if isinstance(flow_details, str):
                    try:
                        flow_details = json.loads(flow_details)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to parse flow details as JSON: {flow_details}")
                        return None

                # Ensure data is a dictionary
                if not isinstance(flow_details, dict):
                    logger.error(f"Expected dictionary for flow details, got {type(flow_details)}")
                    return None

                # Skip template flows
                if flow_details.get("is_template", False):
                    logger.info(f"Skipping template flow: {flow_details.get('name')}")
                    return None

                # Ensure required fields are present
                required_fields = ["id", "name", "data"]
                if not all(field in flow_details for field in required_fields):
                    logger.error(f"Flow {flow_id} missing required fields")
                    return None

                # Log successful flow details retrieval
                logger.info(f"Successfully retrieved details for flow: {flow_details.get('name', 'Unknown flow')}")
                return flow_details

        except httpx.HTTPError as e:
            logger.error(f"HTTP Error fetching flow details: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching flow details: {e}")
            return None

    async def create_flow(self, name: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Create a new flow on the LangFlow server.
        
        Args:
            name: Name of the flow
            data: Flow configuration data
            
        Returns:
            Flow ID if successful, None otherwise
        """
        url = f"{self.api_url}/api/v1/flows/"
        logger.debug(f"Creating flow '{name}' at: {url}")
        
        try:
            payload = {
                "name": name,
                "data": data
            }
            
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(url, headers=self.headers, json=payload)
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return None
                
                response.raise_for_status()
                result = response.json()
                return result.get("id")
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error creating flow: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error creating flow: {str(e)}")
            return None

    async def update_flow(self, flow_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a flow with new data.
        
        Args:
            flow_id: ID of the flow to update
            data: New data for the flow
            
        Returns:
            True if successful, False otherwise
        """
        # Update flow with echo flow data
        flow_data = data.get("data", {})
        updated_data = {
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "data": {
                "nodes": flow_data.get("nodes", []),
                "edges": flow_data.get("edges", [])
            },
            "last_tested_version": data.get("last_tested_version", "1.0.0")
        }
        
        url = f"{self.api_url}/api/v1/flows/{flow_id}"
        logger.debug(f"Updating flow {flow_id} at: {url}")
        
        logger.debug(f"Flow update data: {json.dumps(updated_data, indent=2)}")
        
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.patch(url, headers=self.headers, json=updated_data)
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return False
                elif response.status_code == 404:
                    logger.error(f"Flow {flow_id} not found")
                    return False
                elif response.status_code == 500:
                    logger.error(f"Server error updating flow. Response: {response.text}")
                    logger.debug(f"Server error updating flow. Request data: {json.dumps(updated_data, indent=2)}")
                    return False
                
                response.raise_for_status()
                return True
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error updating flow: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error updating flow: {str(e)}")
            return False

    async def get_folder_name(self, flow_name: str) -> str:
        """
        Get a sanitized folder name from a flow name.
        
        Args:
            flow_name: Name of the flow
            
        Returns:
            Sanitized folder name
        """
        # Replace spaces and special characters with underscores
        folder_name = "".join(c if c.isalnum() else "_" for c in flow_name)
        # Remove consecutive underscores
        while "__" in folder_name:
            folder_name = folder_name.replace("__", "_")
        # Remove leading/trailing underscores
        folder_name = folder_name.strip("_")
        # Convert to lowercase for consistency
        return folder_name.lower()

    async def run_flow(self, flow_id: str, inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Run a flow with the given inputs.
        
        Args:
            flow_id: ID of the flow to run
            inputs: Input data for the flow
            
        Returns:
            Flow execution results if successful, None otherwise
        """
        url = f"{self.api_url}/api/v1/run/advanced/{flow_id}"
        logger.debug(f"Running flow {flow_id} at: {url}")
        
        # Format inputs according to advanced API schema
        request_data = {
            "inputs": {
                "ChatInput-PBSQV": {
                    "input_value": inputs.get("input_value", ""),
                    "should_store_message": True,
                    "sender": "user",
                    "sender_name": "User",
                    "session_id": "",
                    "files": [],
                    "background_color": "",
                    "chat_icon": "",
                    "text_color": ""
                }
            },
            "stream": False
        }
        
        logger.debug(f"Flow inputs: {json.dumps(request_data, indent=2)}")
        
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(url, headers=self.headers, json=request_data)
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return None
                elif response.status_code == 404:
                    logger.error(f"Flow {flow_id} not found")
                    return None
                elif response.status_code == 500:
                    logger.error(f"Server error running flow. Response: {response.text}")
                    return None
                
                response.raise_for_status()
                result = response.json()
                
                # Extract the output from the response
                if result.get("outputs"):
                    # Return the first output's value
                    return {"result": result["outputs"][0].get("value", "")}
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error running flow: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error running flow: {str(e)}")
            return None

    async def sync_flow(self, flow_id: str) -> bool:
        """
        Sync a specific flow with the database.
        
        Args:
            flow_id: ID of the flow to sync
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get flow details from LangFlow
            flow_data = await self.get_flow_details(flow_id)
            if not flow_data:
                logger.error(f"Could not get details for flow {flow_id}")
                return False
            
            async with self.async_session() as session:
                # Create flow object
                flow = Flow(
                    id=uuid.UUID(flow_id),
                    name=flow_data.get("name", "Unnamed Flow"),
                    description=flow_data.get("description", ""),
                    data=flow_data.get("data", {}),
                    folder_id=flow_data.get("folder_id"),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Add flow to database
                session.add(flow)
                await session.commit()
                
                logger.info(f"Successfully synced flow {flow.name} ({flow.id})")
                return True
            
        except Exception as e:
            logger.error(f"Error syncing flow {flow_id}: {e}")
            return False
