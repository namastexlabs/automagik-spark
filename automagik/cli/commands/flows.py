import click
import json
from tabulate import tabulate
from dotenv import load_dotenv
import os
import logging
import asyncio

from automagik.core.services.flow_manager import FlowManager
from automagik.core.database.session import get_db_session
from automagik.core.database.models import FlowDB

logger = logging.getLogger(__name__)

@click.group()
def flows():
    """Manage LangFlow flows."""
    pass

@flows.command()
def clear():
    """Clear all flows from the database."""
    try:
        flow_manager = FlowManager(
            langflow_api_url=os.getenv("LANGFLOW_API_URL"),
            langflow_api_key=os.getenv("LANGFLOW_API_KEY"),
            db_url=os.getenv("DATABASE_URL")
        )
        
        asyncio.run(flow_manager.clear_database())
        click.echo("Successfully cleared database")
        
    except Exception as e:
        click.echo(f"Error clearing database: {e}")

@flows.command()
def sync():
    """Sync flows from the Langflow server."""
    try:
        # Initialize FlowManager
        flow_manager = FlowManager()

        # Get the event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Initialize database first
        loop.run_until_complete(flow_manager.init_db())

        # Run the async function
        loop.run_until_complete(_sync_flow(flow_manager))

    except Exception as e:
        print(f"Error syncing flows: {str(e)}")

async def _sync_flow(flow_manager: FlowManager):
    """Internal async function to sync flows."""
    try:
        print("\nFetching flows from Langflow server...")
        flows = await flow_manager.get_available_flows()
        if not flows:
            print("No flows found on the server or error occurred")
            return

        # Display available flows
        print("\nAvailable flows:")
        for i, flow in enumerate(flows):
            print(f"{i}: {flow['name']} (ID: {flow['id']})")

        # Get flow selection
        while True:
            try:
                selection = input("\nEnter the number of the flow to sync (or 'q' to quit): ")
                if selection.lower() == 'q':
                    return
                    
                index = int(selection)
                if 0 <= index < len(flows):
                    selected_flow = flows[index]
                    break
                else:
                    print(f"Please enter a number between 0 and {len(flows)-1}")
            except ValueError:
                print("Please enter a valid number")

        # Get flow details
        print(f"\nFetching details for flow: {selected_flow['name']}")
        flow_details = await flow_manager.get_flow_details(selected_flow['id'])
        if not flow_details:
            print(f"Failed to get details for flow: {selected_flow['name']}")
            return

        # Get components
        components = await flow_manager.analyze_flow_components(flow_details)
        if not components:
            print("No components found in flow")
            return

        # Display flow components for selection
        print("\nFlow Components:")
        for i, comp in enumerate(components):
            print(f"{i}: {comp['name']} (ID: {comp['component_id']})")
            
        # Get input component selection
        while True:
            try:
                input_selection = input("\nEnter the number of the input component (or 'q' to quit): ")
                if input_selection.lower() == 'q':
                    return
                    
                input_index = int(input_selection)
                if 0 <= input_index < len(components):
                    input_component = components[input_index]
                    break
                else:
                    print(f"Please enter a number between 0 and {len(components)-1}")
            except ValueError:
                print("Please enter a valid number")
        
        # Get output component selection
        while True:
            try:
                output_selection = input("\nEnter the number of the output component (or 'q' to quit): ")
                if output_selection.lower() == 'q':
                    return
                    
                output_index = int(output_selection)
                if 0 <= output_index < len(components):
                    output_component = components[output_index]
                    break
                else:
                    print(f"Please enter a number between 0 and {len(components)-1}")
            except ValueError:
                print("Please enter a valid number")
        
        # Update flow details with selected components
        flow_details['input_component'] = input_component['component_id']
        flow_details['output_component'] = output_component['component_id']

        # Sync the flow
        try:
            async with flow_manager:
                success = await flow_manager.sync_flow(flow_details)
                if success:
                    print(f"\nSuccessfully synced flow: {flow_details['name']}")
                else:
                    print(f"\nFailed to sync flow: {flow_details['name']}")
        except Exception as e:
            print(f"Error syncing flow: {str(e)}")
        
    except Exception as e:
        print(f"Error syncing flows: {str(e)}")

@flows.command()
def list():
    """List all flows"""
    try:
        db_session = get_db_session()
        flow_manager = FlowManager(db_session)
        
        flows = db_session.query(FlowDB).all()
        
        if not flows:
            print("No flows found")
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
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        print(f"Error listing flows: {str(e)}")
