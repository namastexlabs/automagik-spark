import click
import json
from tabulate import tabulate
from dotenv import load_dotenv
import os

from automagik.core.services.flow_manager import FlowManager
from automagik.core.database.session import get_db_session
from automagik.core.database.models import FlowDB

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
        if api_key:
            click.echo(f"LANGFLOW_API_KEY: {api_key[:8]}... (truncated)")
        else:
            click.echo("LANGFLOW_API_KEY: Not set")
        
        if not api_url or not api_key:
            click.echo("\nError: LANGFLOW_API_URL and LANGFLOW_API_KEY must be set", err=True)
            click.echo("Please check your .env file or environment variables")
            return
        
        # Initialize flow manager
        db_session = get_db_session()
        flow_manager = FlowManager(db_session, api_url, api_key)
        
        # Get remote flows
        click.echo("\nFetching flows from Langflow server...")
        remote_flows = flow_manager.get_available_flows()
        
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
        flow_details = flow_manager.get_flow_details(selected_flow['id'])
        
        if not flow_details:
            click.echo("Could not get flow details")
            return
            
        # Sync the flow to the database
        flow_id = flow_manager.sync_flow(flow_details)
        if not flow_id:
            click.echo("Failed to sync flow")
            return
            
        click.echo("\nFlow synced successfully!")
        click.echo(f"Flow ID: {flow_id}")
        click.echo(f"Name: {flow_details.get('name', 'Unnamed')}")
        
        # Analyze components
        components = flow_manager.analyze_flow_components(flow_details)
        if components:
            click.echo("\nFlow Components:")
            for comp in components:
                role = []
                if comp['is_input']:
                    role.append("Input")
                if comp['is_output']:
                    role.append("Output")
                role_str = " & ".join(role) if role else "Processing"
                
                click.echo(f"- {comp['name']} ({role_str})")
                if comp['tweakable_params']:
                    click.echo(f"  Tweakable parameters: {', '.join(comp['tweakable_params'])}")
    
    except Exception as e:
        click.echo(f"\nError during sync: {str(e)}", err=True)

@flows.command()
def list():
    """List all flows"""
    try:
        db_session = get_db_session()
        flow_manager = FlowManager(db_session)
        
        flows = db_session.query(FlowDB).all()
        
        if not flows:
            click.echo("No flows found")
            return
            
        rows = []
        for flow in flows:
            rows.append([
                str(flow.id),
                flow.name,
                flow.folder_name or '',
                'Yes' if flow.input_component else 'No',
                'Yes' if flow.output_component else 'No',
                flow.flow_version
            ])
            
        headers = ['ID', 'Name', 'Folder', 'Has Input', 'Has Output', 'Version']
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        click.echo(f"Error listing flows: {str(e)}", err=True)
