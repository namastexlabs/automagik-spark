"""
Flow CLI Commands

Provides commands for:
- List flows
- View flow details
- Sync flows from LangFlow
- Delete a flow by its ID
"""

import asyncio
import logging
import click
from tabulate import tabulate
from datetime import datetime
import json
from typing import Optional
from sqlalchemy import select

from ...core.flows import FlowManager
from ...core.database.session import get_session
from ...core.database.models import Flow

logger = logging.getLogger(__name__)

@click.group(name='flows')
def flow_group():
    """Manage flows."""
    pass

@flow_group.command()
@click.option('--remote', is_flag=True, help='List remote flows from LangFlow')
def list(remote: bool):
    """List flows. By default shows local flows, use --remote to show LangFlow flows."""
    async def _list_flows():
        async with get_session() as session:
            async with FlowManager(session) as flow_manager:
                if remote:
                    flows_by_folder = await flow_manager.list_remote_flows()
                    if not flows_by_folder:
                        click.echo("No remote flows available")
                        return
                        
                    # Get all synced flows to check which remote flows are synced
                    stmt = select(Flow)
                    result = await session.execute(stmt)
                    synced_flows = {flow.source_id: flow for flow in result.scalars().all()}
                        
                    click.echo("\nAvailable Remote Flows:")
                    total_count = 1
                    for folder_name, flows in flows_by_folder.items():
                        click.echo(f"\n {folder_name}:")
                        click.echo("-" * (len(folder_name) + 4))
                        
                        for flow in flows:
                            flow_id = flow['id']
                            synced_flow = synced_flows.get(flow_id)
                            sync_status = f"[Synced: {str(synced_flow.id)[:8]}]" if synced_flow else "[Not Synced]"
                            
                            click.echo(f"{total_count}. {flow['name']} (ID: {flow_id}) {sync_status}")
                            if flow.get('description'):
                                click.echo(f"   Description: {flow['description']}")
                            total_count += 1
                else:
                    # List flows from database
                    stmt = select(Flow)
                    result = await session.execute(stmt)
                    flows = result.scalars().all()
                    
                    if not flows:
                        click.echo("No flows synced")
                        return
                        
                    click.echo("\nSynced Flows:")
                    click.echo("-" * 12)
                    
                    table_data = []
                    for flow in flows:
                        folder = f"[{flow.folder_name}]" if flow.folder_name else ""
                        table_data.append([
                            str(flow.id)[:8],
                            f"{folder} {flow.name}",
                            flow.description or "",
                            flow.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        ])
                    
                    click.echo(tabulate(
                        table_data,
                        headers=["ID", "Name", "Description", "Created"],
                        tablefmt="simple"
                    ))

    asyncio.run(_list_flows())

@flow_group.command()
@click.argument('flow-id', required=False)
def sync(flow_id: Optional[str]):
    """Sync a flow from LangFlow to local database."""
    async def _sync_flow(flow_id: Optional[str]):
        async with get_session() as session:
            flow_manager = FlowManager(session)
            async with flow_manager:
                # If no flow ID provided, show list and get selection
                if not flow_id:
                    flows_by_folder = await flow_manager.list_remote_flows()
                    if not flows_by_folder:
                        click.echo("No flows available to sync")
                        return
                    
                    # Flatten flows for selection while keeping folder info
                    flat_flows = []
                    for folder_name, flows in flows_by_folder.items():
                        for flow in flows:
                            flow['folder_name'] = folder_name
                            flat_flows.append(flow)
                    
                    click.echo("\nAvailable Flows:")
                    for i, flow in enumerate(flat_flows, 1):
                        click.echo(f"{i}. [{flow['folder_name']}] {flow['name']}")
                        if flow.get('description'):
                            click.echo(f"   Description: {flow['description']}")
                    
                    flow_num = click.prompt(
                        "\nSelect flow number to sync",
                        type=int,
                        default=1,
                        show_default=True
                    )
                    
                    if not 1 <= flow_num <= len(flat_flows):
                        click.echo("Invalid flow number")
                        return
                        
                    flow_id = flat_flows[flow_num - 1]['id']
                
                # Get flow components
                components = await flow_manager.get_flow_components(flow_id)
                if not components:
                    click.echo("Failed to get flow components")
                    return
                    
                # Show components and get input/output selection
                click.echo("\nFlow Components:")
                for i, comp in enumerate(components, 1):
                    click.echo(f"{i}. {comp['id']} ({comp['type']})")
                    
                input_num = click.prompt(
                    "\nSelect input component number",
                    type=int,
                    default=1,
                    show_default=True
                )
                
                output_num = click.prompt(
                    "Select output component number", 
                    type=int,
                    default=len(components),
                    show_default=True
                )
                
                if not (1 <= input_num <= len(components) and 1 <= output_num <= len(components)):
                    click.echo("Invalid component numbers")
                    return
                    
                input_component = components[input_num - 1]['id']
                output_component = components[output_num - 1]['id']
                
                # Sync the flow
                flow_uuid = await flow_manager.sync_flow(flow_id, input_component, output_component)
                if flow_uuid:
                    click.echo(f"\nSuccessfully synced flow with ID: {flow_uuid}")
                else:
                    click.echo("\nFailed to sync flow")
                
    asyncio.run(_sync_flow(flow_id))

@flow_group.command()
@click.argument('flow-name')
def view(flow_name: str):
    """View flow details."""
    async def _view_flow():
        async with get_session() as session:
            result = await session.execute(
                select(Flow).where(Flow.name == flow_name)
            )
            flow = result.scalar_one_or_none()
            
            if not flow:
                click.echo(f"Flow {flow_name} not found")
                return
            
            click.echo("\nFlow Details:")
            click.echo(f"ID: {flow.id}")
            click.echo(f"Name: {flow.name}")
            click.echo(f"Created: {flow.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(f"Updated: {flow.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if flow.data and 'description' in flow.data:
                click.echo(f"Description: {flow.data['description']}")
            
    asyncio.run(_view_flow())

@flow_group.command()
@click.argument('flow_id')
def delete(flow_id: str):
    """Delete a flow by its ID."""
    async def _delete_flow():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            success = await flow_manager.delete_flow(flow_id)
            if success:
                click.echo(f"Successfully deleted flow {flow_id}")
            else:
                click.echo(f"Failed to delete flow {flow_id}")
                
    asyncio.run(_delete_flow())
