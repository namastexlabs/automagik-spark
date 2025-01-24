"""
Flow Sync Module

This module handles synchronization with the LangFlow server, including fetching flows
and their details.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Set
import httpx
import time

logger = logging.getLogger(__name__)

class FlowSync:
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize FlowSync with API credentials.
        
        Args:
            api_url: Base URL for the LangFlow API
            api_key: API key for authentication
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "accept": "application/json"
        }
        self._template_names = None

    def _get_template_names(self) -> Set[str]:
        """
        Get a set of template names from the basic examples endpoint.
        These are the built-in templates that we want to ignore unless modified.
        """
        if self._template_names is not None:
            return self._template_names

        try:
            url = f"{self.api_url}/api/v1/flows/basic_examples/"
            logger.debug(f"Fetching template names from: {url}")
            
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                
                templates = response.json()
                self._template_names = {t['name'] for t in templates}
                logger.debug(f"Found {len(self._template_names)} templates")
                return self._template_names
                
        except Exception as e:
            logger.error(f"Error fetching template names: {str(e)}")
            return set()  # Return empty set on error

    def get_remote_flows(self) -> List[Dict[str, Any]]:
        """
        Fetch flows from LangFlow server.
        Ignores template flows unless they've been saved to a folder.
        
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
            # First get the template names
            template_names = self._get_template_names()
            logger.debug(f"Found {len(template_names)} template flows")
            
            # Then get all flows
            url = f"{self.api_url}/api/v1/flows/"
            logger.debug(f"Fetching flows from: {url}")
            
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 401:
                    logger.error("Invalid API key or unauthorized access")
                    return []
                elif response.status_code == 404:
                    logger.error("API endpoint not found. Please check the API URL")
                    return []
                    
                response.raise_for_status()
                
                # Verify content type
                content_type = response.headers.get('content-type', '')
                if 'application/json' not in content_type:
                    logger.error(f"Unexpected content type: {content_type}")
                    return []
                
                data = response.json()
                if not isinstance(data, list):
                    logger.error(f"Expected list of flows, got {type(data)}")
                    return []
                
                # Filter out unmodified templates
                filtered_flows = []
                for flow in data:
                    name = flow.get('name')
                    folder_id = flow.get('folder_id')
                    flow_id = flow.get('id')
                    
                    # Skip flows without folder_id (unmodified templates)
                    if not folder_id:
                        logger.debug(f"Skipping unmodified template: {name}")
                        continue
                        
                    # If we got a valid flow, add it
                    if name and flow_id:
                        filtered_flows.append(flow)
                    else:
                        logger.debug(f"Skipping invalid flow data: {flow}")
                
                logger.debug(f"Found {len(filtered_flows)} modified flows")
                return filtered_flows
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error: {str(e)}")
            if hasattr(e, 'response'):
                logger.error(f"Status code: {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"Error fetching flows: {str(e)}")
            return []

    def get_flow_details(self, flow_id: str) -> dict:
        """Get flow details from API."""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                url = f"{self.api_url}/api/v1/flows/{flow_id}"
                logger.debug(f"Fetching flow details from: {url} (attempt {retry_count + 1})")
                
                with httpx.Client(verify=False) as client:
                    response = client.get(url, headers=self.headers)
                    
                    if response.status_code == 401:
                        logger.error("Invalid API key or unauthorized access")
                        return None
                    elif response.status_code == 404:
                        logger.error(f"Flow {flow_id} not found")
                        return None
                    
                    response.raise_for_status()
                    
                    # Verify content type
                    content_type = response.headers.get('content-type', '')
                    if 'application/json' not in content_type:
                        logger.warning(f"Unexpected content type: {content_type}, response: {response.text[:500]}")
                        retry_count += 1
                        
                        # If we get HTML, try parsing it as JSON anyway
                        try:
                            data = response.json()
                            if isinstance(data, dict):
                                return data
                        except:
                            pass
                            
                        # Wait for 1 second before retrying
                        time.sleep(1)
                        continue
                    
                    data = response.json()
                    if not isinstance(data, dict):
                        logger.error(f"Expected flow details to be a dictionary, got {type(data)}")
                        return None
                    
                    return data
                    
            except httpx.HTTPError as e:
                logger.error(f"HTTP Error fetching flow details: {str(e)}")
                retry_count += 1
                if retry_count >= max_retries:
                    return None
            except Exception as e:
                logger.error(f"Error fetching flow details: {str(e)}")
                return None
        
        logger.error(f"Failed to get flow details after {max_retries} attempts")
        return None

    def get_folder_name(self, folder_id: str) -> Optional[str]:
        """
        Fetch folder name from the API.
        
        Args:
            folder_id: ID of the folder
            
        Returns:
            Folder name if found, None otherwise
        """
        if not folder_id:
            logger.debug("No folder ID provided")
            return None
        
        try:
            url = f"{self.api_url}/api/v1/folders/{folder_id}"
            logger.debug(f"Fetching folder name from: {url}")
            
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers)
                
                # Handle non-200 responses
                if response.status_code != 200:
                    logger.warning(f"Received status code {response.status_code} from folder API")
                    return None
                
                # Verify content type
                content_type = response.headers.get('content-type', '')
                if 'application/json' not in content_type:
                    logger.error(f"Unexpected content type: {content_type}")
                    return None
                
                # Handle empty response
                if not response.text.strip():
                    logger.warning("Received empty response from folder API")
                    return None
                    
                try:
                    folder_data = response.json()
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response from folder API")
                    return None
                    
                # Validate folder data structure
                if not isinstance(folder_data, dict):
                    logger.warning(f"Unexpected folder data format: {type(folder_data)}")
                    return None
                    
                folder_name = folder_data.get('name')
                if folder_name:
                    logger.debug(f"Successfully retrieved folder name: {folder_name}")
                    return folder_name
                else:
                    logger.warning("Folder data missing 'name' field")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching folder name: {str(e)}")
            return None
