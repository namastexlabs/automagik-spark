#!/usr/bin/env python3

import os
import uuid
from typing import Dict, List, Optional, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import Base, FlowDB, AgentDB
from main_functions import get_flows, get_flow_details

def list_flows(db_session) -> List[FlowDB]:
    """List all available flows."""
    flows = db_session.query(FlowDB).all()
    print("\nAvailable flows:")
    for i, flow in enumerate(flows):
        print(f"{i}: {flow.name} (ID: {flow.id})")
    return flows

def select_flow(flows: List[FlowDB]) -> Optional[FlowDB]:
    """Let user select a flow."""
    try:
        idx = int(input("\nSelect a flow by index: "))
        return flows[idx]
    except (ValueError, IndexError):
        print("Invalid selection")
        return None

def get_component_type(component: Dict) -> str:
    """Determine if a component is an input or output type."""
    # Check component type based on its template
    template = component.get("data", {}).get("node", {}).get("template", {})
    
    # Input components typically have input fields
    input_indicators = ["input", "query", "message"]
    output_indicators = ["output", "response", "result"]
    
    # Check template keys and values for indicators
    for key, value in template.items():
        key_lower = key.lower()
        # Check if it's an input component
        if any(ind in key_lower for ind in input_indicators):
            return "input"
        # Check if it's an output component
        if any(ind in key_lower for ind in output_indicators):
            return "output"
    
    return "unknown"

def identify_components(flow_data: Dict) -> Tuple[List[Dict], List[Dict]]:
    """Identify input and output components in the flow."""
    input_components = []
    output_components = []
    
    nodes = flow_data.get("data", {}).get("nodes", [])
    for node in nodes:
        component_type = get_component_type(node)
        if component_type == "input":
            input_components.append(node)
        elif component_type == "output":
            output_components.append(node)
    
    return input_components, output_components

def select_component(components: List[Dict], component_type: str) -> Optional[str]:
    """Let user select a component."""
    if not components:
        print(f"No {component_type} components found")
        return None
        
    print(f"\nAvailable {component_type} components:")
    for i, comp in enumerate(components):
        print(f"{i}: {comp.get('id')} - {comp.get('type')}")
        
    try:
        idx = int(input(f"Select {component_type} component by index: "))
        return components[idx].get("id")
    except (ValueError, IndexError):
        print("Invalid selection")
        return None

def create_agent(db_session, flow: FlowDB, input_component: str, output_component: str) -> Optional[AgentDB]:
    """Create a new agent in the database."""
    name = input("\nEnter agent name: ")
    description = input("Enter agent description (optional): ")
    
    agent = AgentDB(
        id=uuid.uuid4(),
        name=name,
        description=description,
        flow_id=flow.id,
        input_component=input_component,
        output_component=output_component
    )
    
    try:
        db_session.add(agent)
        db_session.commit()
        print(f"\nAgent '{name}' created successfully!")
        return agent
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        db_session.rollback()
        return None

def main():
    load_dotenv()
    
    # Initialize database
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    
    try:
        # List and select flow
        flows = list_flows(db_session)
        if not flows:
            print("No flows available. Please sync flows first.")
            return
            
        flow = select_flow(flows)
        if not flow:
            return
            
        # Get flow details
        flow_data = flow.data
        
        # Identify and select components
        input_components, output_components = identify_components(flow_data)
        
        input_component = select_component(input_components, "input")
        if not input_component:
            return
            
        output_component = select_component(output_components, "output")
        if not output_component:
            return
            
        # Create agent
        agent = create_agent(db_session, flow, input_component, output_component)
        if agent:
            print(f"Agent ID: {agent.id}")
            
    finally:
        db_session.close()

if __name__ == "__main__":
    main()
