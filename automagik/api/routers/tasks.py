
"""Tasks router for the AutoMagik API."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from ..models import TaskCreate, TaskResponse, ErrorResponse
from ..middleware import verify_api_key
from ..dependencies import get_session
from ...core.workflows.manager import WorkflowManager
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={401: {"model": ErrorResponse}}
)

async def get_flow_manager(session: AsyncSession = Depends(get_session)) -> WorkflowManager:
    """Get flow manager instance."""
    return WorkflowManager(session)

@router.post("", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def create_task(
    task: TaskCreate,
    flow_manager: WorkflowManager = Depends(get_flow_manager)
):
    """Create a new task."""
    try:
        async with flow_manager as fm:
            created_task = await fm.task.create_task(task)
            return TaskResponse.model_validate(created_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[TaskResponse], dependencies=[Depends(verify_api_key)])
async def list_tasks(
    flow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    flow_manager: WorkflowManager = Depends(get_flow_manager)
):
    """List all tasks."""
    try:
        async with flow_manager as fm:
            tasks = await fm.list_tasks(flow_id, status, limit)
            return [TaskResponse.model_validate(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def get_task(
    task_id: str,
    flow_manager: WorkflowManager = Depends(get_flow_manager)
):
    """Get a specific task by ID."""
    try:
        async with flow_manager as fm:
            task = await fm.get_task(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def delete_task(
    task_id: str,
    flow_manager: WorkflowManager = Depends(get_flow_manager)
):
    """Delete a task by ID."""
    try:
        async with flow_manager as fm:
            deleted_task = await fm.task.delete_task(task_id)
            if not deleted_task:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskResponse.model_validate(deleted_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{task_id}/run", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def run_task(
    task_id: str,
    flow_manager: WorkflowManager = Depends(get_flow_manager)
):
    """Run a task by ID."""
    try:
        async with flow_manager as fm:
            task = await fm.task.retry_task(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


