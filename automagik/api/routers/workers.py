"""Workers router for the AutoMagik API."""
from typing import List
from fastapi import APIRouter, HTTPException, Security, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import WorkerStatus, ErrorResponse
from ..dependencies import verify_api_key, get_session
from ...core.database.models import Worker

router = APIRouter(
    prefix="/workers",
    tags=["workers"],
    responses={401: {"model": ErrorResponse}}
)

@router.get("", response_model=List[WorkerStatus])
async def list_workers(
    api_key: str = Security(verify_api_key),
    session: AsyncSession = Depends(get_session)
):
    """List all active workers."""
    try:
        result = await session.execute(select(Worker))
        workers = result.scalars().all()
        return [
            WorkerStatus(
                id=str(worker.id),
                status=worker.status,
                last_heartbeat=worker.last_heartbeat,
                current_task=str(worker.current_task_id) if worker.current_task_id else None,
                stats=worker.stats or {}
            )
            for worker in workers
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{worker_id}", response_model=WorkerStatus)
async def get_worker(
    worker_id: str,
    api_key: str = Security(verify_api_key),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific worker by ID."""
    try:
        result = await session.execute(select(Worker).filter(Worker.id == worker_id))
        worker = result.scalar_one_or_none()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        return WorkerStatus(
            id=str(worker.id),
            status=worker.status,
            last_heartbeat=worker.last_heartbeat,
            current_task=str(worker.current_task_id) if worker.current_task_id else None,
            stats=worker.stats or {}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{worker_id}/pause", response_model=WorkerStatus)
async def pause_worker(
    worker_id: str,
    api_key: str = Security(verify_api_key),
    session: AsyncSession = Depends(get_session)
):
    """Pause a worker."""
    try:
        result = await session.execute(select(Worker).filter(Worker.id == worker_id))
        worker = result.scalar_one_or_none()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        
        worker.status = "paused"
        await session.commit()
        
        return WorkerStatus(
            id=str(worker.id),
            status=worker.status,
            last_heartbeat=worker.last_heartbeat,
            current_task=str(worker.current_task_id) if worker.current_task_id else None,
            stats=worker.stats or {}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{worker_id}/resume", response_model=WorkerStatus)
async def resume_worker(
    worker_id: str,
    api_key: str = Security(verify_api_key),
    session: AsyncSession = Depends(get_session)
):
    """Resume a worker."""
    try:
        result = await session.execute(select(Worker).filter(Worker.id == worker_id))
        worker = result.scalar_one_or_none()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        
        worker.status = "active"
        await session.commit()
        
        return WorkerStatus(
            id=str(worker.id),
            status=worker.status,
            last_heartbeat=worker.last_heartbeat,
            current_task=str(worker.current_task_id) if worker.current_task_id else None,
            stats=worker.stats or {}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{worker_id}/stop", response_model=WorkerStatus)
async def stop_worker(
    worker_id: str,
    api_key: str = Security(verify_api_key),
    session: AsyncSession = Depends(get_session)
):
    """Stop a worker."""
    try:
        result = await session.execute(select(Worker).filter(Worker.id == worker_id))
        worker = result.scalar_one_or_none()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        
        worker.status = "stopped"
        await session.commit()
        
        return WorkerStatus(
            id=str(worker.id),
            status=worker.status,
            last_heartbeat=worker.last_heartbeat,
            current_task=str(worker.current_task_id) if worker.current_task_id else None,
            stats=worker.stats or {}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
