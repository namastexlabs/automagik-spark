"""
Flow Sync Module

This module handles synchronization with the LangFlow server, including fetching flows
and their details.
"""

import httpx
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FlowSync:
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize FlowSync with API credentials.
        
        Args:
            api_url: Base URL for the LangFlow API
            api_key: API key for authentication
        """
        self.api_url = self._normalize_api_url(api_url)
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "accept": "application/json"
        }

    def _normalize_api_url(self, url: str) -> str:
        """Ensure URL has the correct API version prefix."""
        url = url.rstrip('/')
        if not url.endswith('/api/v1'):
            url = f"{url}/api/v1"
        return url

    def get_remote_flows(self) -> List[Dict[str, Any]]:
        """
        Fetch flows from LangFlow server.
        
        Returns:
            List of flow dictionaries
        """
        params = {
            "remove_example_flows": "false",
            "components_only": "false",
            "get_all": "true",
            "header_flows": "false",
            "page": "1",
            "size": "50"
        }
        
        try:
            with httpx.Client(verify=False) as client:
                url = f"{self.api_url}/flows/"
                response = client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return []
                elif response.status_code == 404:
                    logger.error("API endpoint not found. Please check the API URL")
                    return []
                    
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    logger.info("No flows found on the server")
                    return []
                    
                return data
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Status code: {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"Error fetching flows: {str(e)}")
            return []

    def get_flow_details(self, flow_id: str) -> Dict[str, Any]:
        """
        Fetch detailed information about a specific flow.
        
        Args:
            flow_id: ID of the flow to fetch
            
        Returns:
            Flow details dictionary
        """
        try:
            with httpx.Client(verify=False) as client:
                url = f"{self.api_url}/flows/{flow_id}"
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching flow details: {str(e)}")
            return {}

    def get_folder_name(self, folder_id: str) -> Optional[str]:
        """
        Fetch folder name from the API.
        
        Args:
            folder_id: ID of the folder
            
        Returns:
            Folder name if found, None otherwise
        """
        if not folder_id:
            return None
            
        url = f"{self.api_url}/folders/{folder_id}"
        
        try:
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                folder_data = response.json()
                return folder_data.get('name')
        except Exception as e:
            logger.error(f"Error fetching folder name: {str(e)}")
            return None
