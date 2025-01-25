"""
Flow CLI Commands

Provides commands for:
- List flows
- View flow details
- Sync flows from LangFlow
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

@click.group(name='flow')
def flow_group():
    """Manage flows."""
    pass

@flow_group.command()
@click.option('--all', 'show_all', is_flag=True, help='Include example flows')
def list(show_all: bool):
    """List available flows from LangFlow."""
    async def _list_flows():
        async with get_session() as session:
            flow_manager = FlowManager(session)
            flows = await flow_manager.list_remote_flows(include_examples=show_all)
            
            if not flows:
                click.echo("No flows available")
                return
                
            click.echo("\nAvailable Flows:")
            for i, flow in enumerate(flows, 1):
                click.echo(f"\n{i}. {flow['name']}")
                if flow.get('description'):
                    click.echo(f"   Description: {flow['description']}")
                
    asyncio.run(_list_flows())

@flow_group.command()
@click.argument('flow-id', required=False)
def sync(flow_id: Optional[str]):
    """Sync a flow from LangFlow to local database."""
    async def _sync_flow(flow_id: Optional[str]):
        async with get_session() as session:
            flow_manager = FlowManager(session)
            
            # If no flow ID provided, show list and get selection
            if not flow_id:
                flows = await flow_manager.list_remote_flows()
                if not flows:
                    click.echo("No flows available to sync")
                    return
                
                click.echo("\nAvailable Flows:")
                for i, flow in enumerate(flows, 1):
                    click.echo(f"{i}. {flow['name']}")
                    if flow.get('description'):
                        click.echo(f"   Description: {flow['description']}")
                
                flow_num = click.prompt(
                    "\nSelect flow number to sync",
                    type=int,
                    default=1,
                    show_default=True
                )
                
                if not 1 <= flow_num <= len(flows):
                    click.echo("Invalid flow number")
                    return
                    
                flow_id = flows[flow_num - 1]['id']
            
            # Get flow components
            components = await flow_manager.get_flow_components(flow_id)
            if not components:
                click.echo("Failed to get flow components")
                return
                
            # Show components
            click.echo("\nFlow Components:")
            for i, comp in enumerate(components, 1):
                click.echo(f"{i}. {comp['name']} ({comp['type']})")
                click.echo(f"   ID: {comp['id']}")
                if comp.get('tweakable_params'):
                    click.echo(f"   Parameters: {', '.join(comp['tweakable_params'])}")
                
            # Select input component
            input_num = click.prompt(
                "\nSelect input component number",
                type=int,
                default=1,
                show_default=True
            )
            
            if not 1 <= input_num <= len(components):
                click.echo("Invalid input component number")
                return
                
            # Select output component
            output_num = click.prompt(
                "\nSelect output component number",
                type=int,
                default=len(components),
                show_default=True
            )
            
            if not 1 <= output_num <= len(components):
                click.echo("Invalid output component number")
                return
                
            # Get component IDs
            input_component = components[input_num - 1]['id']
            output_component = components[output_num - 1]['id']
            
            # Sync flow
            flow_uuid = await flow_manager.sync_flow(
                flow_id,
                input_component,
                output_component
            )
            
            if flow_uuid:
                click.echo(f"\nFlow synced successfully! Flow ID: {flow_uuid}")
            else:
                click.echo("Failed to sync flow")
    
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
