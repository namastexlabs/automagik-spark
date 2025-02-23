"""API endpoints for managing workflow sources."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from ..middleware import verify_api_key
from ...core.database.session import get_session
from ...core.workflows.source import WorkflowSource
from ...core.schemas.source import (
    WorkflowSourceCreate,
    WorkflowSourceUpdate,
    WorkflowSourceResponse
)
from ...core.schemas.source import SourceType

router = APIRouter(prefix="/sources", tags=["sources"])

async def _validate_source(url: str, api_key: str, source_type: SourceType) -> dict:
    """Validate a source by checking health and fetching version info."""
    try:
        async with httpx.AsyncClient(verify=False) as client:
            headers = {"accept": "application/json"}
            if api_key:
                headers["x-api-key"] = api_key

            # Check health first
            health_response = await client.get(f"{url}/health", headers=headers)
            health_response.raise_for_status()
            health_data = health_response.json()
            
            # For automagik-agents, status should be 'healthy'
            # For langflow, status should be 'ok'
            expected_status = 'healthy' if source_type == SourceType.AUTOMAGIK_AGENTS else 'ok'
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
                    'version': root_data.get('version', 'unknown'),
                    'name': root_data.get('name', 'AutoMagik Agents'),
                    'description': root_data.get('description', ''),
                    'status': health_data.get('status', 'unknown'),
                    'timestamp': health_data.get('timestamp'),
                    'environment': health_data.get('environment', 'unknown')
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

@router.post("/", response_model=WorkflowSourceResponse, dependencies=[Depends(verify_api_key)])
async def create_source(
    source: WorkflowSourceCreate,
    session_factory: AsyncSession = Depends(get_session)
) -> WorkflowSourceResponse:
    """Create a new workflow source."""
    async with session_factory as session:
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
        db_source = WorkflowSource(
            source_type=source.source_type,
            url=url_str,
            encrypted_api_key=WorkflowSource.encrypt_api_key(source.api_key),
            version_info=version_info,
            status='active' if version_info.get('status') == 'ok' else 'inactive'
        )
        session.add(db_source)
        await session.commit()
        await session.refresh(db_source)
        
        return WorkflowSourceResponse.from_orm(db_source)

@router.get("/", response_model=List[WorkflowSourceResponse], dependencies=[Depends(verify_api_key)])
async def list_sources(
    status: Optional[str] = None,
    session_factory: AsyncSession = Depends(get_session)
) -> List[WorkflowSourceResponse]:
    """List all workflow sources."""
    async with session_factory as session:
        query = select(WorkflowSource)
        if status:
            query = query.where(WorkflowSource.status == status)
        
        result = await session.execute(query)
        sources = result.scalars().all()
        return [WorkflowSourceResponse.from_orm(source) for source in sources]

@router.get("/{source_id}", response_model=WorkflowSourceResponse, dependencies=[Depends(verify_api_key)])
async def get_source(
    source_id: UUID,
    session_factory: AsyncSession = Depends(get_session)
) -> WorkflowSourceResponse:
    """Get a specific workflow source."""
    async with session_factory as session:
        source = await session.get(WorkflowSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        return WorkflowSourceResponse.from_orm(source)

@router.patch("/{source_id}", response_model=WorkflowSourceResponse, dependencies=[Depends(verify_api_key)])
async def update_source(
    source_id: UUID,
    update_data: WorkflowSourceUpdate,
    session_factory: AsyncSession = Depends(get_session)
) -> WorkflowSourceResponse:
    """Update a workflow source."""
    async with session_factory as session:
        source = await session.get(WorkflowSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        # Update fields
        if update_data.source_type is not None:
            source.source_type = update_data.source_type
        if update_data.url is not None:
            # Check if new URL conflicts with existing source
            if update_data.url != source.url:
                result = await session.execute(
                    select(WorkflowSource).where(WorkflowSource.url == update_data.url)
                )
                if result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Source with URL {update_data.url} already exists"
                    )
            source.url = update_data.url
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
    session_factory: AsyncSession = Depends(get_session)
) -> dict:
    """Delete a workflow source."""
    async with session_factory as session:
        source = await session.get(WorkflowSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        await session.delete(source)
        await session.commit()
        return {"message": "Source deleted successfully"}
