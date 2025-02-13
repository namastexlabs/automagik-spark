
"""
Workflow router.

Provides endpoints for managing workflows.
"""

from typing import List, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_session
from ..models import WorkflowResponse, ErrorResponse
from ...core.workflows.manager import WorkflowManager

router = APIRouter(
    prefix="/workflows",
    tags=["workflows"],
    responses={404: {"model": ErrorResponse}},
)


@router.get("", response_model=List[WorkflowResponse])
async def list_workflows(
    session: AsyncSession = Depends(get_session)
) -> List[WorkflowResponse]:
    """List all workflows."""
    async with WorkflowManager(session) as manager:
        workflows = await manager.list_workflows()
        return [WorkflowResponse.model_validate(w) for w in workflows]


@router.get("/remote", response_model=Dict[str, List[Dict[str, Any]]])
async def list_remote_flows(
    session: AsyncSession = Depends(get_session)
) -> Dict[str, List[Dict[str, Any]]]:
    """List remote flows from LangFlow API."""
    async with WorkflowManager(session) as manager:
        return await manager.list_remote_flows()


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    session: AsyncSession = Depends(get_session)
) -> WorkflowResponse:
    """Get a workflow by ID."""
    async with WorkflowManager(session) as manager:
        workflow = await manager.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return WorkflowResponse.model_validate(workflow)


@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: str,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, bool]:
    """Delete a workflow."""
    async with WorkflowManager(session) as manager:
        success = await manager.delete_workflow(workflow_id)
        if not success:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return {"success": True}


@router.post("/sync/{flow_id}")
async def sync_flow(
    flow_id: str,
    input_component: str,
    output_component: str,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, str]:
    """Sync a flow from LangFlow API into a local workflow."""
    async with WorkflowManager(session) as manager:
        workflow_id = await manager.sync_flow(flow_id, input_component, output_component)
        if not workflow_id:
            raise HTTPException(status_code=404, detail="Flow not found in LangFlow")
        return {"workflow_id": str(workflow_id)}


