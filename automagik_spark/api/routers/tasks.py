"""Tasks router for the AutoMagik API."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from ..models import TaskResponse, ErrorResponse, PaginatedResponse
from ..dependencies import verify_api_key
from ..dependencies import get_session
from ...core.workflows.manager import WorkflowManager
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tasks", tags=["tasks"], responses={401: {"model": ErrorResponse}})


async def get_flow_manager(
    session: AsyncSession = Depends(get_session),
) -> WorkflowManager:
    """Get flow manager instance."""
    return WorkflowManager(session)


@router.get("", response_model=PaginatedResponse[TaskResponse], dependencies=[Depends(verify_api_key)])
async def list_tasks(
    workflow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    flow_manager: WorkflowManager = Depends(get_flow_manager),
):
    """List all tasks with pagination support."""
    try:
        tasks = await flow_manager.list_tasks(workflow_id, status, limit, offset)
        total = await flow_manager.count_tasks(workflow_id, status)

        return PaginatedResponse[TaskResponse](
            items=[TaskResponse.model_validate(task) for task in tasks],
            total=total,
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def get_task(task_id: str, flow_manager: WorkflowManager = Depends(get_flow_manager)):
    """Get a specific task by ID."""
    try:
        task = await flow_manager.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def delete_task(task_id: str, flow_manager: WorkflowManager = Depends(get_flow_manager)):
    """Delete a task by ID."""
    try:
        deleted_task = await flow_manager.task.delete_task(task_id)
        if not deleted_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.model_validate(deleted_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
