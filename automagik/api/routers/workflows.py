
"""
Workflow router.

Provides endpoints for managing workflows.
"""

from typing import List, Dict, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_session
from ..middleware import verify_api_key
from ..models import WorkflowResponse, WorkflowListResponse, ErrorResponse, TaskResponse
from ...core.workflows.manager import WorkflowManager

router = APIRouter(
    prefix="/workflows",
    tags=["workflows"],
    responses={404: {"model": ErrorResponse}},
)


@router.get("", response_model=List[WorkflowListResponse], dependencies=[Depends(verify_api_key)])
async def list_workflows(
    session: AsyncSession = Depends(get_session)
) -> List[WorkflowListResponse]:
    """List all workflows."""
    async with WorkflowManager(session) as manager:
        workflows = await manager.list_workflows()
        return [WorkflowListResponse.model_validate(w) for w in workflows]


@router.get("/remote", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_api_key)])
async def list_remote_flows(
    simplified: bool = False,
    source_url: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
) -> List[Dict[str, Any]]:
    """List remote flows from LangFlow API.
    
    Args:
        simplified: If True, returns only essential flow information
        source_url: Optional URL or instance name to filter flows by source
        session: Database session
    """
    async with WorkflowManager(session) as manager:
        flows = await manager.list_remote_flows(source_url=source_url)
        
        if not flows:
            return []
        
        if simplified:
            simplified_flows = []
            for flow in flows:
                # Extract essential flow information
                simplified_flow = {
                    "id": flow.get("id"),
                    "name": flow.get("name"),
                    "description": flow.get("description"),
                    "origin": {
                        "instance": flow.get("instance"),
                        "source_url": flow.get("source_url")
                    },
                    "components": []
                }
                
                # Extract essential component information
                if "data" in flow and "nodes" in flow["data"]:
                    for node in flow["data"]["nodes"]:
                        component = {
                            "id": node.get("id"),
                            "name": node.get("data", {}).get("name") or node.get("data", {}).get("type"),
                            "description": node.get("data", {}).get("description", "")
                        }
                        simplified_flow["components"].append(component)
                
                simplified_flows.append(simplified_flow)
            
            return simplified_flows
        
        return flows


@router.get("/remote/{flow_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_api_key)])
async def get_remote_flow(
    flow_id: str,
    source_url: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """Get full details of a remote flow.
    
    Args:
        flow_id: ID of the flow to get
        source_url: Optional URL of the source to get the flow from
        session: Database session
        
    Raises:
        HTTPException: If the flow is not found
    """
    async with WorkflowManager(session) as manager:
        flow = await manager.get_remote_flow(flow_id, source_url)
        if not flow:
            raise HTTPException(
                status_code=404,
                detail=f"Flow {flow_id} not found{' in source ' + source_url if source_url else ''}"
            )
        return flow


@router.get("/{workflow_id}", response_model=WorkflowResponse, dependencies=[Depends(verify_api_key)])
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


@router.delete("/{workflow_id}", dependencies=[Depends(verify_api_key)])
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


@router.post("/sync/{flow_id}", dependencies=[Depends(verify_api_key)])
async def sync_flow(
    flow_id: str,
    input_component: str,
    output_component: str,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """Sync a flow from LangFlow API into a local workflow."""
    async with WorkflowManager(session) as manager:
        workflow_data = await manager.sync_flow(flow_id, input_component, output_component)
        if not workflow_data:
            raise HTTPException(status_code=404, detail="Flow not found in LangFlow")
        return workflow_data


@router.post("/{workflow_id}/run", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def run_workflow(
    workflow_id: str,
    input_data: str = Body(..., description="Input string to be passed to the workflow's input component"),
    session: AsyncSession = Depends(get_session)
) -> TaskResponse:
    """Run a workflow with input data.
    
    Args:
        workflow_id: ID of the workflow to run
        input_data: Input string to be passed to the workflow's input component
        session: Database session
    
    Returns:
        TaskResponse: The created task
        
    Raises:
        HTTPException: If the workflow is not found or if there's an error running it
    """
    try:
        async with WorkflowManager(session) as manager:
            task = await manager.run_workflow(workflow_id, input_data)
            if not task:
                raise HTTPException(status_code=404, detail="Workflow not found")
            return TaskResponse.model_validate(task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


