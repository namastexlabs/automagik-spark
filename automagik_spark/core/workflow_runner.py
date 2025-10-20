"""
Core workflow execution functionality.
"""

import logging

from ..core.workflows.remote import LangFlowManager


def get_logger(name):
    logger = logging.getLogger(name)
    return logger


async def run_workflow(workflow, task):
    """Run a workflow."""
    logger = get_logger(__name__)
    logger.info(f"Running workflow {workflow.id} for task {task.id}")

    try:
        # Get the workflow manager based on the workflow type
        workflow_type = workflow.type
        if workflow_type == "langflow":
            manager = LangFlowManager()
            result = await manager.run_flow(workflow, task)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")

        return {
            "workflow_id": str(workflow.id),
            "task_id": str(task.id),
            "result": result,
        }

    except Exception as e:
        logger.error(f"Error running workflow: {e}")
        raise
