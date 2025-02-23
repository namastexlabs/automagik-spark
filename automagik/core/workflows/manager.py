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
from sqlalchemy import select, delete, and_, cast, String, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func  # Add this line

from ..database.models import Workflow, Schedule, Task, WorkflowComponent, TaskLog, WorkflowSource
from ..schemas.source import SourceType
from .remote import LangFlowManager
from .task import TaskManager
from .source import WorkflowSource
from .agents import AutoMagikAgentManager

import os

LANGFLOW_API_URL = os.environ.get('LANGFLOW_API_URL')
LANGFLOW_API_KEY = os.environ.get('LANGFLOW_API_KEY')

logger = logging.getLogger(__name__)


class WorkflowManager:
    """Workflow management class."""

    def __init__(self, session: AsyncSession):
        """Initialize workflow manager."""
        self.session = session
        self.source_manager = None  # Initialize lazily based on workflow source
        self.task = TaskManager(session)

    async def __aenter__(self):
        """Enter context manager."""
        if self.source_manager:
            await self.source_manager.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self.source_manager:
            await self.source_manager.__aexit__(exc_type, exc_val, exc_tb)

    async def _get_workflow_source(self, workflow_id: str) -> Optional[WorkflowSource]:
        """Get the workflow source for a given workflow ID."""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
        
        # Return the associated workflow source
        return workflow.workflow_source

    async def _get_source_manager(self, source_url: Optional[str] = None, source: Optional[WorkflowSource] = None) -> Any:
        """Get the appropriate source manager based on source type."""
        if not source and source_url:
            # Try to find source by URL
            source = (await self.session.execute(
                select(WorkflowSource).where(WorkflowSource.url == source_url)
            )).scalar_one_or_none()
            if not source:
                raise ValueError(f"No source found with URL {source_url}")

        if not source:
            raise ValueError("Either source or source_url must be provided")

        # Get decrypted API key
        api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)

        # Initialize appropriate manager based on source type
        if source.source_type == SourceType.LANGFLOW:
            # Don't pass session to avoid async/sync issues
            return LangFlowManager(api_url=source.url, api_key=api_key)
        elif source.source_type == SourceType.AUTOMAGIK_AGENTS:
            return AutoMagikAgentManager(source.url, api_key, source_id=source.id)
        else:
            raise ValueError(f"Unsupported source type: {source.source_type}")

    async def list_remote_flows(self, workflow_id: Optional[str] = None, source_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """List remote flows from all sources, or a specific source if provided.
        
        Args:
            workflow_id: Optional workflow ID to filter by
            source_url: Optional source URL or instance name to filter by
            
        Returns:
            List[Dict[str, Any]]: List of flows matching the criteria
        """
        if source_url:
            # Try to find source by URL or instance name
            sources_query = select(WorkflowSource).where(
                or_(
                    WorkflowSource.url == source_url,
                    # Extract instance name from URL and compare
                    func.split_part(func.split_part(WorkflowSource.url, '://', 2), '/', 1).ilike(f"{source_url}%")
                )
            )
            sources = (await self.session.execute(sources_query)).scalars().all()
            
            if not sources:
                logger.warning(f"No sources found matching {source_url}")
                return []
                
            all_flows = []
            for source in sources:
                try:
                    api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
                    if source.source_type == SourceType.LANGFLOW:
                        manager = LangFlowManager(api_url=source.url, api_key=api_key)
                        with manager:  # Use context manager for proper cleanup
                            flows = manager.list_flows_sync()
                    elif source.source_type == SourceType.AUTOMAGIK_AGENTS:
                        manager = AutoMagikAgentManager(source.url, api_key, source_id=source.id)
                        flows = manager.list_flows_sync()
                    else:
                        logger.warning(f"Unsupported source type: {source.source_type}")
                        continue

                    # Add source info to each flow
                    for flow in flows:
                        flow["source_url"] = source.url
                        instance = source.url.split('://')[-1].split('/')[0]
                        instance = instance.split('.')[0]
                        flow["instance"] = instance
                    all_flows.extend(flows)
                except Exception as e:
                    logger.error(f"Failed to list flows from source {source.url}: {str(e)}")
                    continue

            return all_flows
        else:
            # Get all sources
            sources = (await self.session.execute(select(WorkflowSource))).scalars().all()
            return await self.list_remote_flows(workflow_id=workflow_id, source_url=sources[0].url if sources else None)

    async def get_remote_flow(self, flow_id: str, source_url: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a remote flow by ID from any source or a specific source.
        
        Args:
            flow_id: ID of the flow to get
            source_url: Optional URL of the source to get the flow from
            
        Returns:
            Optional[Dict[str, Any]]: The flow data if found, None otherwise
        """
        if source_url:
            # Try specific source
            try:
                self.source_manager = await self._get_source_manager(source_url=source_url)
                async with self.source_manager:
                    if isinstance(self.source_manager, LangFlowManager):
                        flow = await self.source_manager.get_flow(flow_id)
                    elif isinstance(self.source_manager, AutoMagikAgentManager):
                        flow = await self.source_manager.get_agent(flow_id)
                    else:
                        logger.warning(f"Unsupported source type")
                        return None

                    if flow:
                        flow["source_url"] = self.source_manager.api_url
                        instance = self.source_manager.api_url.split('://')[-1].split('/')[0]
                        instance = instance.split('.')[0]
                        flow["instance"] = instance
                        return flow
            except Exception as e:
                logger.error(f"Failed to get flow {flow_id} from source {source_url}: {str(e)}")
                return None
        else:
            # Try all sources
            sources = (await self.session.execute(select(WorkflowSource))).scalars().all()
            for source in sources:
                flow = await self.get_remote_flow(flow_id, source.url)
                if flow:
                    return flow
            return None

    async def get_flow_components(self, flow_id: str) -> Dict[str, Any]:
        """Get flow components from LangFlow API."""
        if not self.source_manager:
            raise ValueError("Source manager not initialized")
        return await self.source_manager.get_flow_components(flow_id)

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
        if source_url:
            # If source URL is provided, use that source
            source = (await self.session.execute(
                select(WorkflowSource).where(WorkflowSource.url == source_url)
            )).scalar_one_or_none()
            if not source:
                raise ValueError(f"No source found with URL {source_url}")
            sources = [source]
        else:
            # Get all sources
            sources = (await self.session.execute(select(WorkflowSource))).scalars().all()

        # Try each source until we find the flow
        for source in sources:
            api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
            self.source_manager = await self._get_source_manager(source=source)
            
            # Use sync methods since we're in a sync context
            flows = self.source_manager.list_flows_sync()
            if flows:
                # Check if the flow exists in this source
                flow_exists = any(flow.get('id') == flow_id for flow in flows)
                if flow_exists:
                    # Found the flow, get its data
                    flow_data = self.source_manager.get_flow_sync(flow_id)
                    if flow_data:
                        # Update with input and output components
                        flow_data['input_component'] = input_component
                        flow_data['output_component'] = output_component
                        return await self._create_or_update_workflow(flow_data)

        raise ValueError(f"No source found containing flow {flow_id}")

    async def list_workflows(self, options: dict = None) -> List[Dict[str, Any]]:
        """List all workflows from the local database."""
        query = select(Workflow)
        options = options or {}
        
        # Always load schedules and tasks by default
        if 'joinedload' not in options:
            options['joinedload'] = []
        if isinstance(options['joinedload'], list):
            options['joinedload'].extend(['schedules', 'tasks'])
        
        # Add other relationships if requested
        if options.get('with_source'):
            if isinstance(options['joinedload'], list):
                options['joinedload'].append('workflow_source')
            else:
                options['joinedload'] = ['workflow_source']
        
        # Apply joinedload options
        if options.get('joinedload'):
            for relationship in options['joinedload']:
                query = query.options(joinedload(getattr(Workflow, relationship)))
        
        result = await self.session.execute(query)
        # Call unique() to handle collection relationships
        workflows = result.unique().scalars().all()
        return [workflow.to_dict() for workflow in workflows]

    async def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID.
        
        Args:
            workflow_id: Can be either the local workflow ID or the remote flow ID
            
        Returns:
            Optional[Workflow]: The workflow if found, None otherwise
        """
        # Try to find by local ID first
        query = select(Workflow).options(joinedload(Workflow.workflow_source)).where(
            or_(
                cast(Workflow.id, String) == workflow_id,
                Workflow.remote_flow_id == workflow_id
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow and all its related objects."""
        # Check if workflow exists first
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return False

        try:
            # Delete related tasks first
            await self.session.execute(
                delete(Task).where(cast(Task.workflow_id, String) == workflow_id)
            )
            
            # Delete workflow
            await self.session.execute(
                delete(Workflow).where(cast(Workflow.id, String) == workflow_id)
            )
            
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        query = select(Task).where(cast(Task.id, String) == task_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_tasks(
        self,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List tasks from database."""
        query = select(Task).order_by(Task.created_at.desc()).limit(limit)
        
        if workflow_id:
            query = query.where(cast(Task.workflow_id, String) == workflow_id)
        if status:
            query = query.where(Task.status == status)
            
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return [task.to_dict() for task in tasks]

    async def retry_task(self, task_id: str) -> Optional[Task]:
        """Retry a failed task."""
        task = await self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.status != 'failed':
            raise ValueError(f"Task {task_id} is not in failed state")
        
        # Reset task status and error
        task.status = 'pending'
        task.error = None
        task.tries += 1
        task.started_at = datetime.now(timezone.utc)
        task.finished_at = None
        
        await self.session.commit()
        
        # Run the workflow again
        return await self.run_workflow(
            workflow_id=task.workflow_id,
            input_data=task.input_data,
            existing_task=task
        )

    async def run_workflow(
        self,
        workflow_id: str | UUID,
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
            workflow_id=workflow.id,  # Use the local workflow ID
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
            
            self.source_manager = await self._get_source_manager(source=source)
            
            # Execute workflow
            async with self.source_manager:
                try:
                    result = await self.source_manager.run_flow(workflow.remote_flow_id, input_data)
                    # For automagik-agents, extract just the message from the response
                    if isinstance(self.source_manager, AutoMagikAgentManager) and isinstance(result, dict):
                        result = result.get('result', result)
                except Exception as e:
                    logger.error(f"Error executing flow: {str(e)}")
                    if isinstance(e, httpx.HTTPStatusError):
                        logger.error(f"HTTP Status: {e.response.status_code}")
                        logger.error(f"Response text: {e.response.text}")
                    raise
            
            if result:
                logger.info(f"Task {task.id} completed successfully")
                # Store the result appropriately based on its type
                if isinstance(result, (dict, list)):
                    task.output_data = json.dumps(result)
                else:
                    task.output_data = str(result)
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

    async def create_task(self, workflow_id: str, input_data: Optional[str] = None, max_retries: int = 3) -> Optional[Task]:
        """Create a new task for a workflow.
        
        Args:
            workflow_id: ID of the workflow to create a task for
            input_data: Optional input data for the task
            max_retries: Maximum number of retries for the task
            
        Returns:
            Optional[Task]: The created task if successful
        """
        task_data = {
            "workflow_id": workflow_id,
            "input_data": input_data if input_data else "",
            "max_retries": max_retries,
            "status": "pending",
            "tries": 0
        }
        return await self.task.create_task(task_data)

    async def _create_or_update_workflow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a workflow from flow data."""
        # Get existing workflow by remote flow ID
        query = select(Workflow).where(
            Workflow.remote_flow_id == flow_data['id']
        )
        result = await self.session.execute(query)
        workflow = result.scalar_one_or_none()

        # Get the source
        source = (await self.session.execute(
            select(WorkflowSource).where(WorkflowSource.url == self.source_manager.api_url)
        )).scalar_one_or_none()
        
        if not source:
            raise ValueError(f"Source not found for URL: {self.source_manager.api_url}")

        # Extract workflow fields from flow data
        workflow_fields = {
            'name': flow_data.get('name'),
            'description': flow_data.get('description'),
            'source': self.source_manager.api_url,
            'remote_flow_id': flow_data['id'],
            'data': flow_data.get('data'),
            'flow_raw_data': flow_data,  # Store the complete flow data
            'input_component': flow_data.get('input_component'),
            'output_component': flow_data.get('output_component'),
            'is_component': self.to_bool(flow_data.get('is_component', False)),
            'folder_id': flow_data.get('folder_id'),
            'folder_name': flow_data.get('folder_name'),
            'icon': flow_data.get('icon'),
            'icon_bg_color': flow_data.get('icon_bg_color'),
            'gradient': self.to_bool(flow_data.get('gradient', False)),
            'liked': self.to_bool(flow_data.get('liked', False)),
            'tags': flow_data.get('tags', []),
            'workflow_source_id': source.id,  # Use the actual source ID
        }

        if workflow:
            # Update existing workflow
            for key, value in workflow_fields.items():
                setattr(workflow, key, value)
        else:
            # Create new workflow
            workflow = Workflow(**workflow_fields)
            self.session.add(workflow)

        # Delete existing components if any
        await self.session.execute(
            delete(WorkflowComponent).where(WorkflowComponent.workflow_id == workflow.id)
        )

        # Create components from flow data
        if 'data' in flow_data and 'nodes' in flow_data['data']:
            for node in flow_data['data']['nodes']:
                component = WorkflowComponent(
                    id=uuid4(),
                    workflow_id=workflow.id,
                    component_id=node['id'],
                    type=node.get('data', {}).get('type', 'genericNode'),
                    template=node.get('data', {}),
                    tweakable_params=node.get('data', {}).get('template', {}),
                    is_input=workflow.input_component == node['id'],
                    is_output=workflow.output_component == node['id']
                )
                self.session.add(component)

        await self.session.commit()
        # Detach the workflow from the session to avoid greenlet errors
        self.session.expunge(workflow)
        return {
            'id': str(workflow.id),
            'name': workflow.name,
            'description': workflow.description,
            'data': workflow.data,
            'flow_raw_data': workflow.flow_raw_data,
            'source': workflow.source,
            'remote_flow_id': workflow.remote_flow_id,
            'flow_version': workflow.flow_version,
            'input_component': workflow.input_component,
            'output_component': workflow.output_component,
            'is_component': workflow.is_component,
            'folder_id': workflow.folder_id,
            'folder_name': workflow.folder_name,
            'icon': workflow.icon,
            'icon_bg_color': workflow.icon_bg_color,
            'gradient': workflow.gradient,
            'liked': workflow.liked,
            'tags': workflow.tags,
            'workflow_source_id': str(workflow.workflow_source_id) if workflow.workflow_source_id else None,
            'created_at': workflow.created_at.isoformat() if workflow.created_at else None,
            'updated_at': workflow.updated_at.isoformat() if workflow.updated_at else None,
            'schedules': []  # Don't load schedules in async context
        }

    @staticmethod
    def to_bool(value):
        """Convert a value to boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 't', 'y', 'yes')
        return bool(value)


class SyncWorkflowManager:
    """Synchronous workflow management class."""

    def __init__(self, session: Session):
        """Initialize workflow manager."""
        self.session = session
        self.source_manager = None  # Initialize lazily based on workflow source

    def _get_workflow_source(self, workflow_id: str) -> Optional[WorkflowSource]:
        """Get the workflow source for a given workflow ID."""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return None
        
        # Return the associated workflow source
        return workflow.workflow_source

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID."""
        query = select(Workflow).where(cast(Workflow.id, String) == workflow_id)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def run_workflow_sync(
        self,
        workflow: Workflow,
        task: Task,
        session: Session
    ) -> Optional[Task]:
        """Run a workflow synchronously."""
        try:
            # Get the workflow source
            source = self._get_workflow_source(str(workflow.id))
            if not source:
                raise ValueError(f"No source found for workflow {workflow.id}")

            logger.info(f"Using workflow source: {source.url}")
            logger.info(f"Remote flow ID: {workflow.remote_flow_id}")

            # Initialize appropriate manager with the correct source settings
            api_key = WorkflowSource.decrypt_api_key(source.encrypted_api_key)
            logger.info(f"Decrypted API key length: {len(api_key) if api_key else 0}")
            
            # Initialize appropriate manager based on source type
            if source.source_type == SourceType.LANGFLOW:
                self.source_manager = LangFlowManager(
                    session,
                    api_url=source.url,
                    api_key=api_key
                )
                result = self.source_manager.run_workflow_sync(workflow.remote_flow_id, task.input_data)
            elif source.source_type == SourceType.AUTOMAGIK_AGENTS:
                self.source_manager = AutoMagikAgentManager(
                    source.url,
                    api_key,
                    source_id=source.id
                )
                with self.source_manager:
                    result = self.source_manager.run_flow_sync(workflow.remote_flow_id, task.input_data)
                    # For automagik-agents, extract just the message from the response
                    if isinstance(result, dict):
                        result = result.get('result', result)
            else:
                raise ValueError(f"Unsupported source type: {source.source_type}")
            
            if result:
                logger.info(f"Task {task.id} completed successfully")
                # Store the result appropriately based on its type
                if isinstance(result, (dict, list)):
                    task.output_data = json.dumps(result)
                else:
                    task.output_data = str(result)
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
        
        session.commit()
        return task
