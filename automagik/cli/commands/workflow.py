"""
Workflow management commands.
"""

from typing import Optional, List, Dict, Any
import asyncio
import click
from sqlalchemy import select

from ...core.database.session import get_session
from ...core.database.models import WorkflowSource
from ...core.workflows.manager import WorkflowManager
from ..utils.table_styles import (
    create_rich_table,
    format_timestamp,
    get_status_style,
    print_table
)

from rich.console import Console
from uuid import UUID

workflow_group = click.Group(name="workflows", help="Workflow management commands")


@workflow_group.command("list")
@click.option("--folder", help="Filter by folder name")
def list_workflows(folder: Optional[str]):
    """List all workflows."""
    async def _list():
        async with get_session() as session:
            # Get all workflow sources first
            query = select(WorkflowSource)
            result = await session.execute(query)
            sources = {str(s.id): s for s in result.scalars().all()}

            # Get workflows with eager loading of tasks and schedules
            async with WorkflowManager(session) as manager:
                workflows = await manager.list_workflows(options={"joinedload": ["tasks", "schedules"]})
                
                if not workflows:
                    click.secho("\n No workflows found", fg="yellow")
                    return
                
                # Filter by folder if specified
                if folder:
                    workflows = [w for w in workflows if w.folder == folder]
                
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
                        {"name": "Instance", "justify": "left", "style": "magenta"},
                        {"name": "Type", "justify": "left", "style": "dim magenta"},
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
                    
                    # Get source display name from workflow source
                    instance_name = "unknown"
                    source_type = w.source if w.source else "unknown"
                    if w.workflow_source_id and str(w.workflow_source_id) in sources:
                        source = sources[str(w.workflow_source_id)]
                        url = source.url
                        instance = url.split('://')[-1].split('/')[0]
                        instance = instance.split('.')[0]
                        instance_name = instance
                    
                    # Format the row
                    table.add_row(
                        str(w.id),  # ID
                        w.name,  # Name
                        status,  # Latest run status
                        tasks_display,  # Tasks count with failed count
                        f"[bold]{len(schedules)}[/bold]",  # Schedules count
                        f"[italic]{instance_name}[/italic]",  # Instance name
                        f"[dim]{source_type}[/dim]",  # Source type
                        format_timestamp(w.updated_at)  # Last Updated
                    )
                
                print_table(table)

    asyncio.run(_list())


@workflow_group.command("sync")
@click.argument("flow_id", required=False)
@click.option("--source", help="Source URL or ID to sync from")
@click.option("--page", default=1, help="Page number (default: 1)")
@click.option("--page-size", default=20, help="Number of items per page (default: 20)")
def sync_flow(flow_id: Optional[str], source: Optional[str], page: int, page_size: int):
    """Sync a flow from LangFlow API into a local workflow."""
    async def _sync():
        source_url = None
        async with get_session() as session:
            sources_to_check = []

            # If source is provided and looks like a UUID, try to get the source URL
            if source:
                if len(source) == 36:  # Simple UUID length check
                    try:
                        source_id = UUID(source)
                        result = await session.execute(
                            select(WorkflowSource).where(WorkflowSource.id == source_id)
                        )
                        source_obj = result.scalar_one_or_none()
                        if source_obj:
                            sources_to_check = [source_obj]
                            source_url = source_obj.url
                    except ValueError:
                        source_url = source  # Not a valid UUID, use as URL
                        sources_to_check = [{"url": source_url}]
                else:
                    source_url = source  # Use as URL
                    sources_to_check = [{"url": source_url}]
            else:
                # If no source specified, get all sources
                result = await session.execute(select(WorkflowSource))
                sources_to_check = result.scalars().all()

            async with WorkflowManager(session) as manager:
                if flow_id:
                    # Sync specific flow
                    flow = await manager.sync_flow(flow_id, source_url=source_url)
                    if flow:
                        click.echo(f"Successfully synced flow {flow_id}")
                    else:
                        click.echo(f"Failed to sync flow {flow_id}")
                else:
                    all_flows = []
                    
                    # Collect flows from all sources
                    for src in sources_to_check:
                        try:
                            if isinstance(src, dict):
                                src_url = src["url"]
                            else:
                                src_url = src.url
                                
                            flows = await manager.list_remote_flows(source_url=src_url)
                            if flows and flows.get("flows"):
                                # Add source info to each flow
                                for flow in flows["flows"]:
                                    flow["source_url"] = src_url
                                    # Get instance name from URL
                                    instance = src_url.split('://')[-1].split('/')[0]
                                    instance = instance.split('.')[0]
                                    flow["instance"] = instance
                                all_flows.extend(flows["flows"])
                        except Exception as e:
                            click.secho(f"\nError fetching flows from {src_url}: {str(e)}", fg="red")
                            continue
                    
                    if not all_flows:
                        click.secho("\nNo flows found", fg="yellow")
                        return
                    
                    total_flows = len(all_flows)
                    total_pages = (total_flows + page_size - 1) // page_size
                    
                    # Create table with consistent styling
                    table = create_rich_table(
                        title="Available Flows",
                        caption=f"Page {page}/{total_pages} (Total: {total_flows} flow(s))",
                        columns=[
                            {"name": "ID", "justify": "left", "style": "bright_blue", "no_wrap": True},
                            {"name": "Name", "justify": "left", "style": "green"},
                            {"name": "Description", "justify": "left", "style": "yellow"},
                            {"name": "Source", "justify": "left", "style": "magenta"}
                        ]
                    )
                    
                    # Paginate flows
                    start_idx = (page - 1) * page_size
                    end_idx = start_idx + page_size
                    page_flows = all_flows[start_idx:end_idx]
                    
                    for flow in page_flows:
                        description = flow.get("description") or ""
                        description = description.strip()
                        table.add_row(
                            flow["id"],
                            flow["name"],
                            description,
                            f"[italic]{flow['instance']}[/italic]"
                        )
                    
                    print_table(table)
                    
                    from rich.panel import Panel
                    from rich.console import Console
                    from rich.text import Text
                    
                    # Create footer text
                    footer = Text()
                    
                    # Add sync command
                    footer.append("Command: ", style="bold")
                    footer.append("sync ", style="cyan")
                    footer.append("<flow_id>")
                    
                    # Add source info
                    footer.append(" • ", style="dim")
                    footer.append("Sources: ", style="bold")
                    if len(sources_to_check) == 1:
                        src = sources_to_check[0]
                        src_url = src.url if hasattr(src, 'url') else src['url']
                        instance = src_url.split('://')[-1].split('/')[0].split('.')[0]
                        footer.append(instance, style="green")
                    else:
                        sources = [s.url.split('://')[-1].split('/')[0].split('.')[0] if hasattr(s, 'url') else s['url'].split('://')[-1].split('/')[0].split('.')[0] for s in sources_to_check]
                        footer.append(", ".join(sources), style="green")
                    
                    # Create and print panel
                    console = Console()
                    panel = Panel(footer, expand=True)
                    console.print(panel)

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
                    click.echo(f"Output: {task.output_data}")
                else:
                    click.echo("Workflow execution failed")
                    
        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
    
    asyncio.run(_run())


if __name__ == "__main__":
    workflow_group()
