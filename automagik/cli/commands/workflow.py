"""
Workflow management commands.
"""

import asyncio
import click
import json
from typing import Optional
from uuid import UUID

import click
from tabulate import tabulate

from ...core.workflows import WorkflowManager
from ...core.database.session import get_session
from ..utils.table_styles import (
    create_rich_table,
    format_timestamp,
    get_status_style,
    print_table
)

workflow_group = click.Group(name="workflows", help="Workflow management commands")

def run_async(coro):
    """Helper function to run coroutines. Can be overridden in tests."""
    return asyncio.run(coro)

@workflow_group.command("list")
@click.option("--folder", help="Filter by folder name")
def list_workflows(folder: Optional[str]):
    """List all workflows."""
    async def _list():
        async with get_session() as session:
            async with WorkflowManager(session) as manager:
                workflows = await manager.list_workflows(options={"joinedload": ["tasks", "schedules"]})
                
                # Filter by folder if specified
                if folder:
                    workflows = [w for w in workflows if w.folder_name == folder]
                
                if not workflows:
                    click.secho("\n No workflows found", fg="yellow")
                    return

                # Create table with consistent styling
                table = create_rich_table(
                    title="Workflows",
                    caption=f"Total: {len(workflows)} workflow(s)",
                    columns=[
                        {"name": "ID", "justify": "left", "style": "bright_blue", "no_wrap": True},
                        {"name": "Name", "justify": "left", "style": "green"},
                        {"name": "Latest Run", "justify": "center", "style": "bold"},
                        {"name": "Tasks (Failed)", "justify": "center", "style": "yellow"},
                        {"name": "Schedules", "justify": "center", "style": "yellow"},
                        {"name": "Source", "justify": "left", "style": "magenta"},
                        {"name": "Last Updated", "justify": "left", "style": "cyan"}
                    ]
                )

                # Add rows with proper styling
                for w in workflows:
                    tasks = getattr(w, 'tasks', [])
                    schedules = getattr(w, 'schedules', [])
                    latest_task = max(tasks, key=lambda t: t.created_at, default=None) if tasks else None
                    
                    # Count failed tasks
                    failed_tasks = sum(1 for t in tasks if t.status.lower() == 'failed')
                    
                    # Determine workflow status from latest run
                    if not latest_task:
                        status = "[bold yellow]NEW[/bold yellow]"
                    else:
                        status = get_status_style(latest_task.status)
                    
                    # Format task counts
                    if failed_tasks > 0:
                        tasks_display = f"[bold]{len(tasks)}[/bold] ([red]{failed_tasks}[/red])"
                    else:
                        tasks_display = f"[bold]{len(tasks)}[/bold] ([dim]0[/dim])"
                    
                    # Format the row
                    table.add_row(
                        str(w.id),  # ID
                        w.name,  # Name
                        status,  # Latest run status
                        tasks_display,  # Tasks count with failed count
                        f"[bold]{len(schedules)}[/bold]",  # Schedules count
                        f"[italic]{w.source}[/italic]",  # Source
                        format_timestamp(w.updated_at)  # Last Updated
                    )

                # Print the table
                print_table(table)

    return run_async(_list())


@workflow_group.command("sync")
@click.argument("flow_id", required=False)
def sync_flow(flow_id: Optional[str]):
    """Sync a flow from LangFlow API into a local workflow. If no flow ID is provided, shows an interactive selection."""
    run_async(_sync(flow_id))

async def _sync(flow_id: Optional[str]):
    async with get_session() as session:
        async with WorkflowManager(session) as manager:
            # If no flow ID provided, show list and get selection
            if not flow_id:
                # Get remote flows
                flows = await manager.list_remote_flows()
                if not flows:
                    click.echo("No flows available to sync")
                    return
                
                # Display flows
                click.echo("\nAvailable Remote Flows:")
                click.echo("-" * 20)
                flat_flows = []  # For selection tracking
                for i, flow in enumerate(flows, 1):
                    click.echo(f"{i}. {flow['name']}")
                    if flow.get('description'):
                        click.echo(f"   Description: {flow['description']}")
                    flat_flows.append(flow)
                
                if not flat_flows:
                    click.echo("No flows available to sync")
                    return
                
                # Get flow selection
                flow_num = click.prompt(
                    "\nSelect flow number to sync",
                    type=int,
                    default=1,
                    show_default=True
                )
                
                if not 1 <= flow_num <= len(flat_flows):
                    click.echo("Invalid flow number")
                    return
                
                selected_flow = flat_flows[flow_num - 1]
                flow_id = selected_flow['id']
            
            # Get flow components
            components = await manager.get_flow_components(flow_id)
            if not components:
                click.echo("Failed to get flow components")
                return
            
            # Show components and get input/output selection
            click.echo("\nFlow Components:")
            for i, comp in enumerate(components, 1):
                comp_name = comp.get("display_name", comp.get("name", "Unknown"))
                comp_type = comp.get("type", "Unknown")
                comp_id = comp.get("id", "unknown")
                click.echo(f"{i}. {comp_name} ({comp_type}) [ID: {comp_id}]")
            
            # Get component selections
            input_num = click.prompt(
                "\nSelect input component number",
                type=int,
                default=1,
            )
            output_num = click.prompt(
                "Select output component number",
                type=int,
                default=1,
            )

            if not (1 <= input_num <= len(components) and 1 <= output_num <= len(components)):
                click.echo("Invalid component number selected")
                return

            # Get component IDs
            input_component = components[input_num - 1].get("id")
            output_component = components[output_num - 1].get("id")

            if not input_component or not output_component:
                click.echo("Failed to get component IDs")
                return

            # Sync the flow
            workflow_id = await manager.sync_flow(
                flow_id=flow_id,
                input_component=input_component,
                output_component=output_component
            )
            
            if workflow_id:
                click.echo(f"Successfully synced workflow {workflow_id}")
            else:
                click.echo("Failed to sync workflow", err=True)


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
    
    run_async(_delete())


@workflow_group.command(name="run")
@click.argument("workflow_id")
@click.option("--input", "-i", help="Input string", default="")
def run_workflow(workflow_id: str, input: str):
    """Run a workflow directly."""
    async def _run():
        try:
            async with get_session() as session:
                workflow_manager = WorkflowManager(session)
                
                # Run workflow with string input
                task = await workflow_manager.run_workflow(UUID(workflow_id), input)
                
                if task:
                    click.echo(f"Task {task.id} completed successfully")
                    click.echo(f"Input: {task.input_data}")
                    click.echo(f"Output: {json.dumps(task.output_data, indent=2)}")
                else:
                    click.echo("Workflow execution failed")
                    
        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
    
    run_async(_run())


if __name__ == "__main__":
    workflow_group()
