import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_functions import get_remote_flows, get_flow_details, sync_flow

def main():
    # Load environment variables
    load_dotenv()
    langflow_api_url = os.getenv("LANGFLOW_API_URL")
    langflow_api_key = os.getenv("LANGFLOW_API_KEY")
    database_url = os.getenv("DATABASE_URL")
    
    # Create database engine and session
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    
    try:
        # Get list of flows
        flows = get_remote_flows(langflow_api_url, langflow_api_key)
        
        # Display available flows
        print("\nAvailable flows:")
        for i, flow in enumerate(flows):
            print(f"{i}: {flow['name']} (ID: {flow['id']})")
        
        # Get user selection
        while True:
            try:
                selection = input("\nSelect a flow by index: ")
                index = int(selection)
                if 0 <= index < len(flows):
                    selected_flow = flows[index]
                    break
                else:
                    print("Please select a valid index.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get detailed flow information
        flow_details = get_flow_details(langflow_api_url, langflow_api_key, selected_flow['id'])
        
        # Sync the flow to the database
        flow = sync_flow(db_session, flow_details, langflow_api_url, langflow_api_key)
        
        print("\nFlow synced successfully!")
        print(f"Name: {flow.name}")
        print(f"Version: {flow.flow_version}")
        print(f"Source ID: {flow.source_id}")
        if flow.folder_name:
            print(f"Folder Name: {flow.folder_name}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        db_session.close()

if __name__ == "__main__":
    main()
