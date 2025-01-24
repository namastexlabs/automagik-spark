"""
Flow Manager Module

This module provides the main interface for managing flows, combining functionality
from flow_analyzer and flow_sync.
"""

import logging
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from ..database.models import FlowDB as Flow, FlowComponent, Task, Schedule, TaskLog as Log, Base
from .flow_sync import FlowSync
from .flow_analyzer import FlowAnalyzer

logger = logging.getLogger(__name__)

class FlowManager:
    """Flow manager class."""

    def __init__(
        self,
        langflow_api_url: Optional[str] = None,
        langflow_api_key: Optional[str] = None,
        db_url: Optional[str] = None,
    ):
        """Initialize FlowManager."""
        self.flow_sync = FlowSync(langflow_api_url, langflow_api_key)
        self.flow_analyzer = FlowAnalyzer()
        self.db_url = db_url or os.getenv("DATABASE_URL")
        
        if not self.db_url:
            logger.error("No database URL provided")
            self.engine = None
            self.session_maker = None
            return
            
        try:
            logger.debug(f"Raw DATABASE_URL from environment: {self.db_url}")
            
            # Convert SQLite URL to async format if needed
            if self.db_url.startswith("sqlite"):
                self.db_url = self.db_url.replace("sqlite", "sqlite+aiosqlite", 1)
            
            # Convert PostgreSQL URL to async format if needed
            elif self.db_url.startswith("postgresql"):
                self.db_url = self.db_url.replace("postgresql", "postgresql+asyncpg", 1)
            
            logger.info(f"Using {self.db_url.split('://')[0]} database at {self.db_url}")
            
            # Create engine and session maker
            self.engine = create_async_engine(self.db_url)
            self.session_maker = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            
        except Exception as e:
            logger.error(f"Error initializing database connection: {e}")
            self.engine = None
            self.session_maker = None

    async def __aenter__(self):
        """Enter async context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        if self.engine:
            await self.engine.dispose()

    async def sync_flow(self, flow_details: Dict[str, Any]) -> bool:
        """Sync a flow to the database."""
        try:
            # Create flow record
            flow = Flow(
                id=flow_details["id"],
                name=flow_details["name"],
                data=flow_details.get("data", {}),
                input_component=flow_details.get("input_component"),
                output_component=flow_details.get("output_component")
            )

            async with self.session_maker() as session:
                # Check if flow exists
                existing_flow = await session.get(Flow, flow.id)
                if existing_flow:
                    # Update existing flow
                    existing_flow.name = flow.name
                    existing_flow.data = flow.data
                    existing_flow.input_component = flow.input_component
                    existing_flow.output_component = flow.output_component
                    existing_flow.updated_at = datetime.now()
                else:
                    session.add(flow)
                
                await session.commit()
                logger.info(f"Successfully synced flow: {flow.name}")
                return True

        except Exception as e:
            logger.error(f"Error syncing flow: {e}")
            return False

    async def get_available_flows(self) -> List[Dict[str, Any]]:
        """Get available flows from the server.

        Returns:
            List[Dict[str, Any]]: List of available flows.
        """
        try:
            remote_flows = await self.flow_sync.get_remote_flows()
            if not remote_flows:
                return []

            # Filter out example flows based on their names and descriptions
            example_names = {
                "Blog Writer", "Sequential Tasks Agents", "Memory Chatbot",
                "Custom Component Generator", "Document Q&A", "SaaS Pricing",
                "SEO Keyword Generator", "Travel Planning Agents", "Simple Agent",
                "Basic Prompting", "Prompt Chaining", "Research Agent",
                "Image Sentiment Analysis", "Vector Store RAG",
                "Instagram Copywriter", "Market Research", "Twitter Thread Generator"
            }
            
            available_flows = []
            for flow in remote_flows:
                # Skip flows without required fields
                if not all(field in flow for field in ["id", "name", "folder_id"]):
                    continue
                    
                # Skip example flows
                if flow["name"] in example_names:
                    continue
                    
                available_flows.append(flow)

            return available_flows
        except Exception as e:
            logger.error(f"Error getting available flows: {e}")
            return []

    async def get_flow_details(self, flow_id: str) -> Dict[str, Any]:
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
        
        flow_details = await self.flow_sync.get_flow_details(flow_id)
        logger.debug(f"Flow details response: {json.dumps(flow_details, indent=2)}")
        return flow_details

    async def analyze_flow_components(self, flow_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Analyze flow components and return a list of components with their IDs."""
        try:
            components = []
            nodes = flow_data.get("data", {}).get("nodes", [])
            
            for node in nodes:
                component = {
                    "component_id": node.get("id"),
                    "name": node.get("data", {}).get("node", {}).get("display_name", "Unknown")
                }
                components.append(component)
            
            return components
            
        except Exception as e:
            logger.error(f"Error analyzing flow components: {e}")
            return []

    async def init_db(self) -> bool:
        """Initialize the database."""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Successfully created database tables")
            return True
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            return False

    async def clear_database(self) -> bool:
        """
        Clear all data from the database.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.flow_sync:
            logger.error("FlowSync not initialized")
            return False
            
        return await self.flow_sync.clear_database()
