from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import logging
import json

from .models import Task, Log
from .db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self):
        self.session = Session(engine)

    def get_pending_tasks(self) -> list[Task]:
        """Fetch tasks that are pending execution"""
        query = select(Task).where(
            Task.status == 'pending'
        ).order_by(Task.created_at)
        return list(self.session.execute(query).scalars())

    def execute_task(self, task: Task) -> bool:
        """Execute a single task and handle its outcome"""
        try:
            # Update task status to running
            task.status = 'running'
            task.updated_at = datetime.utcnow()
            self.session.commit()

            # Log task start
            self._log_task(task, 'info', f'Starting task execution. Attempt {task.tries + 1}/{task.max_retries}')

            # TODO: Implement actual task execution logic here
            # This is where you'll add the specific agent execution code
            success = self._run_agent_task(task)

            if success:
                task.status = 'completed'
                self._log_task(task, 'info', 'Task completed successfully')
            else:
                self._handle_failure(task)

            task.updated_at = datetime.utcnow()
            self.session.commit()
            return success

        except Exception as e:
            logger.exception(f"Error executing task {task.id}")
            self._log_task(task, 'error', f'Task execution failed: {str(e)}')
            self._handle_failure(task)
            return False

    def _handle_failure(self, task: Task):
        """Handle task failure and manage retries"""
        task.tries += 1
        if task.tries >= task.max_retries:
            task.status = 'failed'
            self._log_task(task, 'error', 'Task failed: Max retries exceeded')
        else:
            task.status = 'pending'
            self._log_task(task, 'warning', f'Task failed: Will retry. Attempts remaining: {task.max_retries - task.tries}')

    def _log_task(self, task: Task, level: str, message: str):
        """Create a log entry for the task"""
        log = Log(
            task_id=task.id,
            level=level,
            message=message,
            created_at=datetime.utcnow()
        )
        self.session.add(log)
        self.session.commit()

    def _run_agent_task(self, task: Task) -> bool:
        """Execute the specific agent task"""
        # TODO: Implement the actual agent execution logic
        # This is a placeholder that should be replaced with real implementation
        logger.info(f"Executing agent task {task.id} for agent {task.agent_id}")
        
        # Simulate task execution
        # In reality, this would interact with your agent system
        return True

    def run(self):
        """Main loop to continuously process tasks"""
        logger.info("Starting task runner")
        while True:
            try:
                tasks = self.get_pending_tasks()
                if not tasks:
                    logger.debug("No pending tasks found")
                    continue

                for task in tasks:
                    self.execute_task(task)

            except Exception as e:
                logger.exception("Error in task runner main loop")

            # TODO: Add appropriate sleep/delay here 