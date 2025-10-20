"""API endpoints for managing workflow sources."""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from ..dependencies import verify_api_key
from ...core.database.session import get_async_session
from ...core.database.models import WorkflowSource
from ...core.schemas.source import (
    WorkflowSourceCreate,
    WorkflowSourceUpdate,
    WorkflowSourceResponse,
    SourceType
)
router = APIRouter(prefix="/sources", tags=["sources"])
async def _validate_source(url: str, api_key: str, source_type: SourceType) -> dict:
    """Validate a source by checking health and fetching version info."""
    try:
        async with httpx.AsyncClient(verify=False) as client:
            headers = {"accept": "application/json"}
            if api_key:
                headers["x-api-key"] = api_key
            # Check health first - different endpoints for different source types
            if source_type == SourceType.AUTOMAGIK_HIVE:
                health_response = await client.get(f"{url}/api/v1/health", headers=headers)
            else:
                health_response = await client.get(f"{url}/health", headers=headers)
            health_response.raise_for_status()
            health_data = health_response.json()
            
            # Different expected statuses for different source types
            if source_type == SourceType.AUTOMAGIK_AGENTS:
                expected_status = 'healthy'
            elif source_type == SourceType.AUTOMAGIK_HIVE:
                expected_status = 'success'
            else:  # LANGFLOW
                expected_status = 'ok'
                
            if health_data.get('status') != expected_status:
                raise HTTPException(
                    status_code=400,
                    detail=f"Source health check failed: {health_data}"
                )
            # Get version info based on source type
            if source_type == SourceType.AUTOMAGIK_AGENTS:
                # Get root info which contains version and service info
                root_response = await client.get(f"{url}/", headers=headers)
                root_response.raise_for_status()
                root_data = root_response.json()
                version_data = {
                    'version': root_data.get('version', health_data.get('version', 'unknown')),
                    'name': root_data.get('name', 'AutoMagik Agents'),
                    'description': root_data.get('description', ''),
                    'status': health_data.get('status', 'unknown'),
                    'timestamp': health_data.get('timestamp'),
                    'environment': health_data.get('environment', 'unknown')
                }
            elif source_type == SourceType.AUTOMAGIK_HIVE:
                # For AutoMagik Hive, get status info for additional details
                try:
                    status_response = await client.get(f"{url}/playground/status", headers=headers)
                    status_response.raise_for_status()
                    status_data = status_response.json()
                    version_data = {
                        'version': health_data.get('utc', 'unknown'),
                        'name': health_data.get('service', 'Automagik Hive Multi-Agent System'),
                        'description': 'AutoMagik Hive Multi-Agent System with agents, teams, and workflows',
                        'status': health_data.get('status', 'unknown'),
                        'timestamp': health_data.get('utc'),
                        'environment': 'production',
                        'agents_loaded': status_data.get('agents_loaded', 0),
                        'teams_loaded': status_data.get('teams_loaded', 0),
                        'workflows_loaded': status_data.get('workflows_loaded', 0)
                    }
                except:
                    # Fallback if status endpoint fails
                    version_data = {
                        'version': health_data.get('utc', 'unknown'),
                        'name': health_data.get('service', 'Automagik Hive Multi-Agent System'),
                        'description': 'AutoMagik Hive Multi-Agent System',
                        'status': health_data.get('status', 'unknown'),
                        'timestamp': health_data.get('utc'),
                        'environment': 'production'
                    }
            else:
                # For langflow, use /api/v1/version endpoint
                version_response = await client.get(f"{url}/api/v1/version", headers=headers)
                version_response.raise_for_status()
                version_data = version_response.json()
            return {
                **version_data,
                'status': health_data.get('status', 'unknown')
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to validate source: {str(e)}"
        )
@router.post("/", response_model=WorkflowSourceResponse, status_code=201, dependencies=[Depends(verify_api_key)])
async def create_source(
    source: WorkflowSourceCreate,
    session: AsyncSession = Depends(get_async_session)
) -> WorkflowSourceResponse:
    """Create a new workflow source."""
    # Convert HttpUrl to string for database operations
    url_str = str(source.url).rstrip('/')
    
    # Check if source with URL already exists
    result = await session.execute(
        select(WorkflowSource).where(WorkflowSource.url == url_str)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Source with URL {url_str} already exists"
        )
    
    # Validate source and get version info
    version_info = await _validate_source(url_str, source.api_key, source.source_type)
    
    # Create source with status from health check
    # Determine expected status based on source type
    if source.source_type == SourceType.AUTOMAGIK_AGENTS:
        expected_status = 'healthy'
    elif source.source_type == SourceType.AUTOMAGIK_HIVE:
        expected_status = 'success'
    else:  # LANGFLOW
        expected_status = 'ok'
    db_source = WorkflowSource(
        name=source.name,
        source_type=source.source_type,
        url=url_str,
        encrypted_api_key=WorkflowSource.encrypt_api_key(source.api_key),
        version_info=version_info,
        status='active' if version_info.get('status') == expected_status else 'inactive'
    )
    session.add(db_source)
    await session.commit()
    await session.refresh(db_source)
    
    return WorkflowSourceResponse.from_orm(db_source)
@router.get("/", response_model=List[WorkflowSourceResponse], dependencies=[Depends(verify_api_key)])
async def list_sources(
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
) -> List[WorkflowSourceResponse]:
    """List all workflow sources."""
    query = select(WorkflowSource)
    if status:
        query = query.where(WorkflowSource.status == status)
    
    result = await session.execute(query)
    sources = result.scalars().all()
    return [WorkflowSourceResponse.from_orm(source) for source in sources]
@router.get("/{source_id}", response_model=WorkflowSourceResponse, dependencies=[Depends(verify_api_key)])
async def get_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_async_session)
) -> WorkflowSourceResponse:
    """Get a specific workflow source."""
    source = await session.get(WorkflowSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return WorkflowSourceResponse.from_orm(source)
@router.patch("/{source_id}", response_model=WorkflowSourceResponse, dependencies=[Depends(verify_api_key)])
async def update_source(
    source_id: UUID,
    update_data: WorkflowSourceUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> WorkflowSourceResponse:
    """Update a workflow source."""
    source = await session.get(WorkflowSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    # Update fields
    if update_data.name is not None:
        source.name = update_data.name
    if update_data.source_type is not None:
        source.source_type = update_data.source_type
    if update_data.url is not None:
        # Convert HttpUrl to string for database operations
        url_str = str(update_data.url).rstrip('/')
        # Check if new URL conflicts with existing source
        if url_str != source.url:
            result = await session.execute(
                select(WorkflowSource).where(WorkflowSource.url == url_str)
            )
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=400,
                    detail=f"Source with URL {url_str} already exists"
                )
        source.url = url_str
    if update_data.api_key is not None:
        source.encrypted_api_key = WorkflowSource.encrypt_api_key(update_data.api_key)
        # Validate new API key and update version info
        version_info = await _validate_source(source.url, update_data.api_key, source.source_type)
        source.version_info = version_info
    if update_data.status is not None:
        source.status = update_data.status
    
    await session.commit()
    await session.refresh(source)
    return WorkflowSourceResponse.from_orm(source)
@router.delete("/{source_id}", dependencies=[Depends(verify_api_key)])
async def delete_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    """Delete a workflow source."""
    try:
        source = await session.get(WorkflowSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        await session.delete(source)
        await session.commit()
        return {"message": "Source deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting source: {str(e)}")