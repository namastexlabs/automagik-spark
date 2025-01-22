"""
Scheduler Exception Classes

This module defines custom exceptions for the scheduler package.
"""

class SchedulerError(Exception):
    """Base exception for scheduler-related errors."""
    pass

class TaskExecutionError(SchedulerError):
    """Raised when there's an error executing a task."""
    def __init__(self, message: str, task_id: str = None, response: dict = None):
        super().__init__(message)
        self.task_id = task_id
        self.response = response

class InvalidScheduleError(SchedulerError):
    """Raised when a schedule configuration is invalid."""
    pass

class ComponentNotConfiguredError(SchedulerError):
    """Raised when required flow components are not configured."""
    pass

class ScheduleNotFoundError(SchedulerError):
    """Raised when a requested schedule is not found."""
    pass

class FlowNotFoundError(SchedulerError):
    """Raised when a requested flow is not found."""
    pass
