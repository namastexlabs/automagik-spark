"""Router package for the AutoMagik API."""

from .flows import router as flows_router
from .schedules import router as schedules_router
from .tasks import router as tasks_router
from .status import router as status_router

__all__ = [
    'flows_router',
    'schedules_router',
    'tasks_router',
    'status_router',
]
