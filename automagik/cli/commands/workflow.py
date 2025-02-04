"""
Workflow management commands.
"""

import asyncio
import json
from typing import Optional
from uuid import UUID

import click
from tabulate import tabulate

from ...core.workflows import WorkflowManager
from ...core.database.session import get_session

workflow_group = click.Group(name="workflow", help="Workflow management commands")


@workflow_group.command("list")
@click.option("--folder", help="Filter by folder name")
def list_workflows(folder: Optional[str]):
    """List all workflows."""
    async def _list():
        async with get_session() as session:
            async with WorkflowManager(session) as manager:
                workflows = await manager.list_workflows()
                
                # Filter by folder if specified
                if folder:
                    workflows = [w for w in workflows if w.folder_name == folder]
                
                # Format for display
                rows = []
                for w in workflows:
                    rows.append([
                        str(w.id),
                        w.name,
                        w.folder_name or "",
                        w.source,
                        w.remote_flow_id,
                        len(w.tasks) if w.tasks else 0,
                        len(w.schedules) if w.schedules else 0
                    ])
                
                if not rows:
                    click.echo("No workflows found")
                    return
                
                headers = ["ID", "Name", "Folder", "Source", "Remote Flow ID", "Tasks", "Schedules"]
                click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
    
    asyncio.run(_list())


@workflow_group.command("sync")
@click.argument("flow_id")
@click.option("--input", "input_component", help="Input component ID")
@click.option("--output", "output_component", help="Output component ID")
def sync_flow(flow_id: str, input_component: Optional[str], output_component: Optional[str]):
    """Sync a flow from LangFlow API into a local workflow."""
    async def _sync():
        async with get_session() as session:
            async with WorkflowManager(session) as manager:
                workflow_id = await manager.sync_flow(
                    flow_id=flow_id,
                    input_component=input_component,
                    output_component=output_component
                )
                if workflow_id:
                    click.echo(f"Successfully synced workflow {workflow_id}")
                else:
                    click.echo("Failed to sync workflow", err=True)
    
    asyncio.run(_sync())


@workflow_group.command("delete")
@click.argument("workflow_id")
def delete_workflow(workflow_id: str):
    """Delete a workflow."""
    async def _delete():
        async with get_session() as session:
            async with WorkflowManager(session) as manager:
                success = await manager.delete_workflow(workflow_id)
                if success:
                    click.echo(f"Successfully deleted workflow {workflow_id}")
                else:
                    click.echo(f"Failed to delete workflow {workflow_id}", err=True)
    
    asyncio.run(_delete())
