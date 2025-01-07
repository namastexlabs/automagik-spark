import click
import json
from tabulate import tabulate
from sqlalchemy import select
from ..models import FlowDB
from ..db import get_db_session
from ..flow_sync import get_remote_flows, get_flow_details, sync_flow
import os
from dotenv import load_dotenv

@click.group()
def flows():
    """Manage flows"""
    pass

@flows.command()
def sync():
    """Sync flows from Langflow server"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get environment variables
        api_url = os.getenv('LANGFLOW_API_URL')
        api_key = os.getenv('LANGFLOW_API_KEY')
        
        click.echo("\nEnvironment Configuration:")
        click.echo(f"LANGFLOW_API_URL: {api_url}")
        click.echo(f"LANGFLOW_API_KEY: {api_key[:8]}... (truncated)")
        
        if not api_url or not api_key:
            click.echo("\nError: LANGFLOW_API_URL and LANGFLOW_API_KEY must be set", err=True)
            click.echo("Please check your .env file or environment variables")
            return
        
        # Get remote flows
        click.echo("\nFetching flows from Langflow server...")
        remote_flows = get_remote_flows(api_url, api_key)
        
        if not remote_flows:
            click.echo("\nNo flows found on the server or error occurred")
            return
            
        # Display available flows
        click.echo("\nAvailable flows:")
        for i, flow in enumerate(remote_flows):
            click.echo(f"{i}: {flow['name']} (ID: {flow['id']})")
        
        # Get user selection
        while True:
            try:
                selection = click.prompt("\nSelect a flow by index", type=int)
                if 0 <= selection < len(remote_flows):
                    selected_flow = remote_flows[selection]
                    break
                else:
                    click.echo("Please select a valid index.")
            except ValueError:
                click.echo("Please enter a valid number.")
        
        # Get detailed flow information
        click.echo(f"\nFetching details for flow {selected_flow['name']}...")
        flow_details = get_flow_details(api_url, api_key, selected_flow['id'])
        
        if not flow_details:
            click.echo("Could not get flow details")
            return
            
        # Sync the flow to the database
        db = get_db_session()
        flow = sync_flow(db, flow_details, api_url, api_key)
        
        click.echo("\nFlow synced successfully!")
        click.echo(f"Name: {flow.name}")
        click.echo(f"Version: {flow.flow_version}")
        click.echo(f"Source ID: {flow.source_id}")
        if flow.folder_name:
            click.echo(f"Folder Name: {flow.folder_name}")
        if flow.input_component:
            click.echo(f"Input Component: {flow.input_component}")
        if flow.output_component:
            click.echo(f"Output Component: {flow.output_component}")
    
    except Exception as e:
        click.echo(f"\nError during sync: {str(e)}", err=True)
        click.echo(f"Error type: {type(e)}")

@flows.command()
def list():
    """List all flows"""
    db = get_db_session()
    flows = db.execute(select(FlowDB)).scalars()
    
    rows = []
    for flow in flows:
        rows.append([
            str(flow.id),
            flow.name,
            flow.description or "",
            flow.folder_name or "No Folder",
            "Yes" if flow.input_component else "No",
            "Yes" if flow.output_component else "No",
            flow.flow_version
        ])
    
    if not rows:
        click.echo("\nNo flows found in the database")
        return
        
    headers = ['ID', 'Name', 'Description', 'Folder', 'Has Input', 'Has Output', 'Version']
    click.echo("\nSynced Flows:")
    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
