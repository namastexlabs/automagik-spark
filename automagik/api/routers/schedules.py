"""Schedules router for the AutoMagik API."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Security, Depends
from ..models import ScheduleCreate, ScheduleResponse, ErrorResponse
from ..dependencies import verify_api_key, get_session
from ...core.workflows.manager import WorkflowManager
from ...core.scheduler.manager import SchedulerManager
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={401: {"model": ErrorResponse}}
)

async def get_scheduler_manager(session: AsyncSession = Depends(get_session)) -> SchedulerManager:
    """Get scheduler manager instance."""
    workflow_manager = WorkflowManager(session)
    return SchedulerManager(session, workflow_manager)

@router.post("", response_model=ScheduleResponse)
async def create_schedule(
    schedule: ScheduleCreate,
    api_key: str = Security(verify_api_key),
    scheduler_manager: SchedulerManager = Depends(get_scheduler_manager)
):
    """Create a new schedule."""
    try:
        async with scheduler_manager as sm:
            # Convert flow_id to UUID
            flow_id = UUID(schedule.flow_id)
            created_schedule = await sm.create_schedule(
                flow_id=flow_id,
                schedule_type=schedule.schedule_type,
                schedule_expr=schedule.schedule_expr,
                flow_params=schedule.flow_params
            )
            if not created_schedule:
                raise HTTPException(status_code=400, detail="Failed to create schedule")
            return ScheduleResponse.model_validate(created_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
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
        schedule_uuid = UUID(schedule_id)
        async with scheduler_manager as sm:
            schedule = await sm.get_schedule(schedule_uuid)
            if not schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            return ScheduleResponse.model_validate(schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
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
        schedule_uuid = UUID(schedule_id)
        flow_uuid = UUID(schedule.flow_id)
        async with scheduler_manager as sm:
            # First check if schedule exists
            existing_schedule = await sm.get_schedule(schedule_uuid)
            if not existing_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            
            # Update schedule expression if changed
            if existing_schedule.schedule_expr != schedule.schedule_expr:
                success = await sm.update_schedule_expression(schedule_uuid, schedule.schedule_expr)
                if not success:
                    raise HTTPException(status_code=400, detail="Failed to update schedule expression")
            
            # Update schedule status if changed
            if existing_schedule.status != schedule.status:
                action = "resume" if schedule.status == "active" else "pause"
                success = await sm.update_schedule_status(str(schedule_uuid), action)
                if not success:
                    raise HTTPException(status_code=400, detail="Failed to update schedule status")
            
            # Get updated schedule
            updated_schedule = await sm.get_schedule(schedule_uuid)
            if not updated_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found after update")
            
            return ScheduleResponse.model_validate(updated_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
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
        schedule_uuid = UUID(schedule_id)
        async with scheduler_manager as sm:
            # First get the schedule
            schedule = await sm.get_schedule(schedule_uuid)
            if not schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            
            # Delete the schedule
            success = await sm.delete_schedule(schedule_uuid)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to delete schedule")
            
            return ScheduleResponse.model_validate(schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
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
        schedule_uuid = UUID(schedule_id)
        async with scheduler_manager as sm:
            # First check if schedule exists
            schedule = await sm.get_schedule(schedule_uuid)
            if not schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            
            # Enable the schedule
            success = await sm.update_schedule_status(str(schedule_uuid), "resume")
            if not success:
                raise HTTPException(status_code=400, detail="Failed to enable schedule")
            
            # Get updated schedule
            updated_schedule = await sm.get_schedule(schedule_uuid)
            if not updated_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found after update")
            
            return ScheduleResponse.model_validate(updated_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
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
        schedule_uuid = UUID(schedule_id)
        async with scheduler_manager as sm:
            # First check if schedule exists
            schedule = await sm.get_schedule(schedule_uuid)
            if not schedule:
                raise HTTPException(status_code=404, detail="Schedule not found")
            
            # Disable the schedule
            success = await sm.update_schedule_status(str(schedule_uuid), "pause")
            if not success:
                raise HTTPException(status_code=400, detail="Failed to disable schedule")
            
            # Get updated schedule
            updated_schedule = await sm.get_schedule(schedule_uuid)
            if not updated_schedule:
                raise HTTPException(status_code=404, detail="Schedule not found after update")
            
            return ScheduleResponse.model_validate(updated_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid UUID format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
