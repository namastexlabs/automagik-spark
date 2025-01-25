"""Schedules router for the AutoMagik API."""
from typing import List
from fastapi import APIRouter, HTTPException, Security, Depends
from ..models import ScheduleCreate, ScheduleResponse, ErrorResponse
from ..dependencies import verify_api_key, get_session
from ...core.flows.manager import FlowManager
from ...core.scheduler.manager import SchedulerManager
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={401: {"model": ErrorResponse}}
)

async def get_scheduler_manager(session: AsyncSession = Depends(get_session)) -> SchedulerManager:
    """Get scheduler manager instance."""
    flow_manager = FlowManager(session)
    return SchedulerManager(session, flow_manager)

@router.post("", response_model=ScheduleResponse)
async def create_schedule(
    schedule: ScheduleCreate,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Create a new schedule."""
    try:
        async with scheduler_manager as sm:
            created_schedule = await sm.create_schedule(schedule)
            return ScheduleResponse.model_validate(created_schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ScheduleResponse])
async def list_schedules(
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """List all schedules."""
    try:
        async with scheduler_manager as sm:
            schedules = await sm.list_schedules()
            return [ScheduleResponse.model_validate(schedule) for schedule in schedules]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Get a specific schedule by ID."""
    try:
        async with scheduler_manager as sm:
            schedule = await sm.get_schedule(schedule_id)
            if not schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            return ScheduleResponse.model_validate(schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: str,
    schedule: ScheduleCreate,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Update a schedule by ID."""
    try:
        async with scheduler_manager as sm:
            updated_schedule = await sm.update_schedule(schedule_id, schedule)
            if not updated_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            return ScheduleResponse.model_validate(updated_schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{schedule_id}", response_model=ScheduleResponse)
async def delete_schedule(
    schedule_id: str,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Delete a schedule by ID."""
    try:
        async with scheduler_manager as sm:
            deleted_schedule = await sm.delete_schedule(schedule_id)
            if not deleted_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            return ScheduleResponse.model_validate(deleted_schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{schedule_id}/enable", response_model=ScheduleResponse)
async def enable_schedule(
    schedule_id: str,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Enable a schedule."""
    try:
        async with scheduler_manager as sm:
            enabled_schedule = await sm.enable_schedule(schedule_id)
            if not enabled_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            return ScheduleResponse.model_validate(enabled_schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{schedule_id}/disable", response_model=ScheduleResponse)
async def disable_schedule(
    schedule_id: str,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Disable a schedule."""
    try:
        async with scheduler_manager as sm:
            disabled_schedule = await sm.disable_schedule(schedule_id)
            if not disabled_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            return ScheduleResponse.model_validate(disabled_schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
