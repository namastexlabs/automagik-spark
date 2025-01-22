"""
Flow Manager Module

This module provides the main interface for managing flows, combining functionality
from flow_analyzer and flow_sync.
"""

from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
import uuid
import logging

from automagik.core.database.models import FlowDB, FlowComponent
from .flow_analyzer import FlowAnalyzer
from .flow_sync import FlowSync

logger = logging.getLogger(__name__)

class FlowManager:
    def __init__(self, db_session: Session, langflow_api_url: str = None, langflow_api_key: str = None):
        """
        Initialize FlowManager with database session and optional API credentials.
        
        Args:
            db_session: SQLAlchemy database session
            langflow_api_url: Optional URL for LangFlow API
            langflow_api_key: Optional API key for authentication
        """
        self.db_session = db_session
        self.flow_sync = None
        if langflow_api_url and langflow_api_key:
            self.flow_sync = FlowSync(langflow_api_url, langflow_api_key)
        self.flow_analyzer = FlowAnalyzer()

    def sync_flow(self, flow_data: Dict[str, Any]) -> Optional[str]:
        """
        Sync a flow to the local database and analyze its components.
        
        Args:
            flow_data: Flow data from LangFlow
            
        Returns:
            ID of the synced flow if successful, None otherwise
        """
        try:
            # Generate a new UUID for the flow
            flow_id = str(uuid.uuid4())
            
            # Extract basic flow information
            name = flow_data.get("name", "Unnamed Flow")
            description = flow_data.get("description", "")
            folder_id = flow_data.get("folder_id")
            
            # Get folder name if available
            folder_name = None
            if self.flow_sync and folder_id:
                folder_name = self.flow_sync.get_folder_name(folder_id)
            
            # Analyze flow components
            components = []
            for node in flow_data.get("data", {}).get("nodes", []):
                is_input, is_output, tweakable_params = self.flow_analyzer.analyze_component(node)
                
                component_info = self.flow_analyzer.get_component_info(node)
                components.append({
                    "node_id": component_info["id"],
                    "name": component_info["name"],
                    "type": component_info["type"],
                    "is_input": is_input,
                    "is_output": is_output,
                    "tweakable_params": tweakable_params
                })
            
            # Store flow data in database
            # Note: Actual database operations would go here
            # This is a placeholder for the database schema
            
            return flow_id
            
        except Exception as e:
            logger.error(f"Error syncing flow: {str(e)}")
            return None

    def get_available_flows(self) -> List[Dict[str, Any]]:
        """
        Get list of available flows from LangFlow server.
        
        Returns:
            List of flow dictionaries
        """
        if not self.flow_sync:
            logger.error("LangFlow API credentials not configured")
            return []
        
        return self.flow_sync.get_remote_flows()

    def get_flow_details(self, flow_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific flow.
        
        Args:
            flow_id: ID of the flow
            
        Returns:
            Flow details dictionary
        """
        if not self.flow_sync:
            logger.error("LangFlow API credentials not configured")
            return {}
        
        return self.flow_sync.get_flow_details(flow_id)

    def analyze_flow_components(self, flow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze all components in a flow.
        
        Args:
            flow_data: Flow data from LangFlow
            
        Returns:
            List of component information dictionaries
        """
        components = []
        for node in flow_data.get("data", {}).get("nodes", []):
            is_input, is_output, tweakable_params = self.flow_analyzer.analyze_component(node)
            component_info = self.flow_analyzer.get_component_info(node)
            components.append({
                "id": component_info["id"],
                "name": component_info["name"],
                "type": component_info["type"],
                "is_input": is_input,
                "is_output": is_output,
                "tweakable_params": tweakable_params
            })
        return components
