"""Flows router for the AutoMagik API."""
from typing import List
from fastapi import APIRouter, HTTPException, Security, Depends
from ..models import FlowCreate, FlowResponse, ErrorResponse
from ..dependencies import verify_api_key, get_session
from ...core.flows.manager import FlowManager
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/flows",
    tags=["flows"],
    responses={401: {"model": ErrorResponse}}
)

async def get_flow_manager(session: AsyncSession = Depends(get_session)) -> FlowManager:
    """Get flow manager instance."""
    return FlowManager(session)

@router.post("", response_model=FlowResponse)
async def create_flow(
    flow: FlowCreate,
    api_key: str = Security(verify_api_key),
    flow_manager: FlowManager = Depends(get_flow_manager)
):
    """Create a new flow."""
    try:
        async with flow_manager as fm:
            created_flow = await fm.create_flow(flow)
            return FlowResponse.model_validate(created_flow)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[FlowResponse])
async def list_flows(
    api_key: str = Security(verify_api_key),
    flow_manager: FlowManager = Depends(get_flow_manager)
):
    """List all flows."""
    try:
        async with flow_manager as fm:
            flows = await fm.list_flows()
            return [FlowResponse.model_validate(flow) for flow in flows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{flow_id}", response_model=FlowResponse)
async def get_flow(
    flow_id: str,
    api_key: str = Security(verify_api_key),
    flow_manager: FlowManager = Depends(get_flow_manager)
):
    """Get a specific flow by ID."""
    try:
        async with flow_manager as fm:
            flow = await fm.get_flow(flow_id)
            if not flow:
                raise HTTPException(status_code=404, detail="Flow not found")
            return FlowResponse.model_validate(flow)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{flow_id}", response_model=FlowResponse)
async def update_flow(
    flow_id: str,
    flow: FlowCreate,
    api_key: str = Security(verify_api_key),
    flow_manager: FlowManager = Depends(get_flow_manager)
):
    """Update a flow by ID."""
    try:
        async with flow_manager as fm:
            updated_flow = await fm.update_flow(flow_id, flow)
            if not updated_flow:
                raise HTTPException(status_code=404, detail="Flow not found")
            return FlowResponse.model_validate(updated_flow)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{flow_id}", response_model=FlowResponse)
async def delete_flow(
    flow_id: str,
    api_key: str = Security(verify_api_key),
    flow_manager: FlowManager = Depends(get_flow_manager)
):
    """Delete a flow by ID."""
    try:
        async with flow_manager as fm:
            deleted_flow = await fm.delete_flow(flow_id)
            if not deleted_flow:
                raise HTTPException(status_code=404, detail="Flow not found")
            return FlowResponse.model_validate(deleted_flow)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
