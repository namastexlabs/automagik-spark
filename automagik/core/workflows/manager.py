"""
Workflow management.

Provides the main interface for managing workflows and remote flows
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

import httpx
from sqlalchemy import select, delete, and_, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models import Workflow, Schedule, Task, WorkflowComponent, TaskLog, WorkflowSource
from .remote import LangFlowManager
from .task import TaskManager
from .source import WorkflowSource

import os

LANGFLOW_API_URL = os.environ.get('LANGFLOW_API_URL')
LANGFLOW_API_KEY = os.environ.get('LANGFLOW_API_KEY')

logger = logging.getLogger(__name__)


class WorkflowManager:
    """Workflow management class."""

    def __init__(self, session: AsyncSession):
        """Initialize workflow manager."""
        self.session = session
        self.langflow = None  # Initialize lazily based on workflow source
        self.task = TaskManager(session)

    async def __aenter__(self):
        """Enter context manager."""
        if self.langflow:
            await self.langflow.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self.langflow:
            await self.langflow.__aexit__(exc_type, exc_val, exc_tb)

    async def _get_workflow_source(self, workflow_id: str) -> Optional[WorkflowSource]:
        """Get the workflow source for a given workflow ID."""
        try:
            uuid_obj = UUID(workflow_id)
            workflow = await self.session.execute(
                select(Workflow)
                .options(joinedload(Workflow.workflow_source))
                .where(Workflow.id == uuid_obj)
            )
            workflow = workflow.scalar_one_or_none()
            if workflow:
                return workflow.workflow_source
        except ValueError:
            pass
        return None

    async def _get_langflow_manager(self, workflow_id: Optional[str] = None, source_url: Optional[str] = None) -> LangFlowManager:
        """Get a LangFlow manager for a workflow."""
        logger.info(f"Getting LangFlow manager for workflow_id={workflow_id}, source_url={source_url}")

        source = None

        # If source_url is provided, try to find source by URL first
        if source_url:
            result = await self.session.execute(
                select(WorkflowSource).where(
                    and_(
                        WorkflowSource.source_type == "langflow",
                        WorkflowSource.url == source_url
                    )
                )
            )
            source = result.scalar_one_or_none()

            # If not found by URL, try instance name
            if not source:
                result = await self.session.execute(
                    select(WorkflowSource).where(WorkflowSource.source_type == "langflow")
                )
                sources = result.scalars().all()
                for src in sources:
                    instance = src.url.split('://')[-1].split('/')[0].split('.')[0]
                    if instance == source_url:
                        source = src
                        break

        # If no source found by URL, try workflow ID
        if not source and workflow_id:
            source = await self._get_workflow_source(workflow_id)

        # If still no source, try environment variables
        if not source and (LANGFLOW_API_URL or LANGFLOW_API_KEY):
            logger.info("Using environment variables for LangFlow configuration")
            return LangFlowManager(
                self.session,
                api_url=LANGFLOW_API_URL,
                api_key=LANGFLOW_API_KEY
            )

        # If no source found at all, try to get first available source
        if not source:
            result = await self.session.execute(
                select(WorkflowSource).where(WorkflowSource.source_type == "langflow")
            )
            sources = result.scalars().all()
            if sources:
                source = sources[0]
            else:
                raise ValueError("No LangFlow sources found in DB and LANGFLOW_API_URL not set in environment")

        logger.info(f"Found source: {source}")
        if not source:
            raise ValueError(f"No source configuration found for URL: {source_url}")

        # Create manager with source configuration
        return LangFlowManager(
            self.session,
            api_url=source.url,
            api_key=WorkflowSource.decrypt_api_key(source.encrypted_api_key)
        )

    # Remote flow operations
    async def list_remote_flows(self, workflow_id: Optional[str] = None, source_url: Optional[str] = None) -> Dict[str, List[Dict]]:
        """List remote flows from all LangFlow sources, or a specific source if provided."""
        if workflow_id or source_url:
            # If specific source requested, use that one
            self.langflow = await self._get_langflow_manager(workflow_id, source_url)
            flows = await self.langflow.list_remote_flows()
            return {"flows": flows}
        else:
            # Get all langflow sources
            result = await self.session.execute(
                select(WorkflowSource).where(WorkflowSource.source_type == "langflow")
            )
            sources = result.scalars().all()
            
            all_flows = []
            for source in sources:
                try:
                    self.langflow = LangFlowManager(
                        self.session,
                        api_url=source.url,
                        api_key=WorkflowSource.decrypt_api_key(source.encrypted_api_key)
                    )
                    async with self.langflow:
                        flows = await self.langflow.list_remote_flows()
                        # Add source information to each flow
                        for flow in flows:
                            flow["source"] = source.url
                        all_flows.extend(flows)
                except Exception as e:
                    logger.error(f"Failed to list flows from source {source.url}: {str(e)}")
                    continue
            
            return {"flows": all_flows}

    async def get_flow_components(self, flow_id: str) -> List[Dict[str, Any]]:
        """Get flow components from LangFlow API."""
        self.langflow = await self._get_langflow_manager(flow_id)
        flow = await self.langflow.sync_flow(flow_id)
        if not flow:
            return []
        
        # First try to get components directly
        if "components" in flow:
            return flow["components"]
        
        # If no direct components, try to extract from flow data nodes
        flow_data = flow.get("flow", {}).get("data", {})
        nodes = flow_data.get("nodes", [])
        components = []
        
        for node in nodes:
            node_data = node.get("data", {}).get("node", {})
            if node_data:
                components.append({
                    "id": node_data.get("id"),
                    "type": node_data.get("type"),
                    "name": node_data.get("name"),
                    "description": node_data.get("description")
                })
        
        return components

    async def sync_flow(
        self, 
        flow_id: str, 
        input_component: Optional[str] = None, 
        output_component: Optional[str] = None,
        source_url: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Sync a flow from a remote source.
        
        Args:
            flow_id: ID of the flow to sync
            input_component: ID of the input component
            output_component: ID of the output component
            source_url: Optional URL of the source to sync from
            
        Returns:
            Optional[Dict[str, Any]]: The synced workflow data if successful
        """
        logger.info(f"Syncing flow {flow_id}")

        # If source_url is provided, try that source first
        if source_url:
            logger.info(f"Using specified source: {source_url}")
            async with await self._get_langflow_manager(source_url=source_url) as lf:
                flow_data = await lf.sync_flow(flow_id)
                if flow_data:
                    flow_data["source"] = source_url
                    flow_data["input_component"] = input_component
                    flow_data["output_component"] = output_component
                    workflow = await self._create_or_update_workflow(flow_data)
                    return workflow
                logger.warning(f"Flow {flow_id} not found in specified source {source_url}")

        # If no source_url or flow not found in specified source, search all sources
        logger.info("Searching for flow across all sources")
        result = await self.session.execute(
            select(WorkflowSource).where(WorkflowSource.source_type == "langflow")
        )
        sources = result.scalars().all()

        for source in sources:
            try:
                logger.info(f"Checking source: {source.url}")
                async with await self._get_langflow_manager(source_url=source.url) as lf:
                    flow_data = await lf.sync_flow(flow_id)
                    if flow_data:
                        flow_data["source"] = source.url
                        flow_data["input_component"] = input_component
                        flow_data["output_component"] = output_component
                        workflow = await self._create_or_update_workflow(flow_data)
                        return workflow
            except Exception as e:
                logger.error(f"Error syncing flow from source {source.url}: {str(e)}")
                continue

        logger.warning(f"Flow {flow_id} not found in any source")
        return None

    # Local workflow operations
    async def list_workflows(self, options: dict = None) -> List[Workflow]:
        """List all workflows from the local database."""
        stmt = select(Workflow)

        # Apply eager loading options
        if options and options.get("joinedload"):
            for relationship in options["joinedload"]:
                stmt = stmt.options(joinedload(getattr(Workflow, relationship)))

        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID."""
        if not workflow_id:
            return None

        if len(workflow_id) < 32:
            # Handle truncated UUID by querying all workflows and matching prefix
            result = await self.session.execute(select(Workflow))
            workflows = result.scalars().all()
            for workflow in workflows:
                if str(workflow.id).startswith(workflow_id):
                    return workflow
            return None
        try:
            uuid_obj = UUID(workflow_id)
            return await self.session.get(Workflow, uuid_obj)
        except ValueError:
            return None

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow and all its related objects."""
        # Validate UUID format
        if not workflow_id:
            raise ValueError("Invalid UUID format")
        
        # Try exact match first (for full UUID)
        try:
            if len(workflow_id) == 36:  # Full UUID
                uuid_obj = UUID(workflow_id)
                exact_match = True
            elif len(workflow_id) >= 8 and all(c in '0123456789abcdefABCDEF' for c in workflow_id):
                exact_match = False
            else:
                raise ValueError("Invalid UUID format")
        except ValueError:
            raise ValueError("Invalid UUID format")
        
        try:
            # Build query based on match type
            query = select(Workflow).options(
                joinedload(Workflow.components),
                joinedload(Workflow.schedules),
                joinedload(Workflow.tasks).joinedload(Task.logs)
            )
            
            if exact_match:
                query = query.where(Workflow.id == uuid_obj)
            else:
                query = query.where(cast(Workflow.id, String).like(f"{workflow_id}%"))
            
            # Execute query
            result = await self.session.execute(query)
            workflow = result.unique().scalar_one_or_none()
            
            if not workflow:
                return False
            
            # Delete related objects first
            for task in workflow.tasks:
                # Delete task logs
                if task.logs:
                    for log in task.logs:
                        await self.session.delete(log)
                # Delete task
                await self.session.delete(task)
            
            # Delete schedules
            for schedule in workflow.schedules:
                await self.session.delete(schedule)
            
            # Delete components
            for component in workflow.components:
                await self.session.delete(component)
            
            # Finally delete the workflow
            await self.session.delete(workflow)
            await self.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete workflow: {str(e)}")
            await self.session.rollback()
            return False

    # Task operations
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return await self.task.get_task(task_id)

    async def list_tasks(
        self,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks from database."""
        return await self.task.list_tasks(workflow_id, status, limit)

    async def retry_task(self, task_id: str) -> Optional[Task]:
        """Retry a failed task."""
        return await self.task.retry_task(task_id)

    async def run_workflow(
        self,
        workflow_id: UUID,
        input_data: str,
        existing_task: Optional[Task] = None
    ) -> Optional[Task]:
        """Run a workflow with input data."""
        workflow = await self.get_workflow(str(workflow_id))
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Use existing task or create a new one
        task = existing_task or Task(
            id=uuid4(),
            workflow_id=workflow_id,
            input_data=input_data,
            status="running",
            started_at=datetime.now(timezone.utc)
        )
        
        if not existing_task:
            self.session.add(task)
            await self.session.commit()
        
        try:
            # Get the workflow source
            source = await self._get_workflow_source(str(workflow_id))
            if not source:
                raise ValueError(f"No source found for workflow {workflow_id}")

            logger.info(f"Using workflow source: {source.url}")
            logger.info(f"Remote flow ID: {workflow.remote_flow_id}")

            # Initialize LangFlow manager with the correct source settings
            api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
            logger.info(f"Decrypted API key length: {len(api_key) if api_key else 0}")
            
            self.langflow = LangFlowManager(
                self.session,
                api_url=source.url,
                api_key=api_key
            )
            
            # Execute workflow
            async with self.langflow:
                try:
                    result = await self.langflow.run_flow(workflow.remote_flow_id, input_data)
                except Exception as e:
                    logger.error(f"Error executing flow: {str(e)}")
                    if isinstance(e, httpx.HTTPStatusError):
                        logger.error(f"HTTP Status: {e.response.status_code}")
                        logger.error(f"Response text: {e.response.text}")
                    raise
            
            if result:
                logger.info(f"Task {task.id} completed successfully")
                logger.info(f"Output data: {result}")
                task.output_data = result
                task.status = 'completed'
                task.finished_at = datetime.now(timezone.utc)
            else:
                logger.error(f"Task {task.id} failed - no result returned")
                task.status = 'failed'
                task.error = "No result returned from workflow execution"
                task.finished_at = datetime.now(timezone.utc)
                
        except Exception as e:
            logger.error(f"Failed to run workflow: {str(e)}")
            if isinstance(e, httpx.HTTPStatusError):
                logger.error(f"HTTP Status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            task.status = 'failed'
            task.error = str(e)
            task.finished_at = datetime.now(timezone.utc)
        
        await self.session.commit()
        return task

    async def _create_or_update_workflow(self, flow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create or update a workflow from flow data."""
        # Get source URL from flow data
        source_url = flow_data.get("source")
        if not source_url:
            logger.error("No source URL provided in flow data")
            return None

        # Get the workflow source by URL
        result = await self.session.execute(
            select(WorkflowSource).where(WorkflowSource.url == source_url)
        )
        source = result.scalar_one_or_none()
        if not source:
            logger.error(f"No workflow source found for URL: {source_url}")
            return None

        # Extract flow ID and data
        flow_id = flow_data.get("id")
        if not flow_id:
            logger.error("No flow ID provided in flow data")
            return None

        # Find existing workflow by remote flow ID and source
        result = await self.session.execute(
            select(Workflow).where(
                and_(
                    Workflow.remote_flow_id == flow_id,
                    Workflow.source == source.source_type
                )
            )
        )
        workflow = result.scalar_one_or_none()

        # Helper function to convert string to boolean
        def to_bool(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ("true", "1", "t", "y", "yes")
            return bool(value)

        # Prepare workflow data
        workflow_data = {
            "name": flow_data.get("name", "Untitled Workflow"),
            "description": flow_data.get("description"),
            "data": flow_data.get("data", {}),
            "source": source.source_type,
            "remote_flow_id": flow_id,
            "flow_version": flow_data.get("flow_version", 1),
            "input_component": flow_data.get("input_component"),
            "output_component": flow_data.get("output_component"),
            "is_component": to_bool(flow_data.get("is_component", False)),
            "folder_id": flow_data.get("folder_id"),
            "folder_name": flow_data.get("folder_name"),
            "icon": flow_data.get("icon"),
            "icon_bg_color": flow_data.get("icon_bg_color"),
            "gradient": to_bool(flow_data.get("gradient", False))
        }

        if workflow:
            # Update existing workflow
            for key, value in workflow_data.items():
                setattr(workflow, key, value)
        else:
            # Create new workflow
            workflow = Workflow(**workflow_data)
            self.session.add(workflow)

        await self.session.commit()
        await self.session.refresh(workflow)
        return workflow
