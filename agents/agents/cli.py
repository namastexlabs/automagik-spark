#!/usr/bin/env python3

import os
import sys
import uuid
import click
from typing import Dict, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from tabulate import tabulate

# Add parent directory to Python path to find sync_flows
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents.models import Base, Agent
from shared.base import Base
from sqlalchemy import Column, String, JSON, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class FlowDB(Base):
    __tablename__ = "flows"
    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    # ... add other fields as needed

def init_db():
    """Initialize database connection."""
    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"))
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

def format_uuid(id):
    """Format UUID for display."""
    return str(id) if id else "N/A"

@click.group()
def cli():
    """Agent CLI - Manage agents"""
    pass

@cli.command()
def list():
    """List all agents"""
    db = init_db()
    agents = db.query(Agent).all()
    
    if not agents:
        click.echo("No agents found")
        return

    headers = ["ID", "Name", "Flow ID", "Input Component", "Output Component", "Status"]
    rows = []
    
    for agent in agents:
        rows.append([
            format_uuid(agent.id),
            agent.name,
            format_uuid(agent.flow_id),
            agent.input_component,
            agent.output_component,
            "Active" if agent.is_active else "Inactive"
        ])
    
    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))

@cli.command()
def create():
    """Create a new agent."""
    # List flows
    db = init_db()
    flows = db.query(FlowDB).all()
    if not flows:
        click.echo("No flows found. Please sync flows first.")
        return
    
    # Select flow
    flow_choices = [
        {"name": f"{flow.name} (ID: {flow.id})", "value": flow}
        for flow in flows
    ]
    
    flow = click.Choice(
        "Select a flow:",
        choices=[choice["name"] for choice in flow_choices],
        show_default=True
    )
    
    if not flow:
        return
    
    # Get all components
    components = identify_components(flow.data)
    if not components:
        click.echo("\nError: No components found in flow.")
        return
    
    # Show available components
    click.echo("\nAvailable components:")
    for comp in components:
        click.echo(f"- {comp['id']} ({comp['type']}) - {comp['display_name']}")
    
    # Select input component
    input_choices = [
        {"name": f"{comp['id']} ({comp['type']}) - {comp['display_name']}", "value": comp['id']}
        for comp in components
    ]
    
    input_component = click.Choice(
        "Select input component:",
        choices=[choice["name"] for choice in input_choices],
        show_default=True
    )
    
    if not input_component:
        return
    
    # Select output component
    output_choices = [
        {"name": f"{comp['id']} ({comp['type']}) - {comp['display_name']}", "value": comp['id']}
        for comp in components if comp['id'] != input_component  # Exclude the input component
    ]
    
    output_component = click.Choice(
        "Select output component:",
        choices=[choice["name"] for choice in output_choices],
        show_default=True
    )
    
    if not output_component:
        return
    
    # Get agent details
    name = click.Text("Enter agent name:")
    description = click.Text("Enter agent description (optional):")
    
    # Create agent
    agent = Agent(
        id=uuid.uuid4(),
        name=name,
        description=description,
        flow_id=flow.id,
        input_component=input_component,
        output_component=output_component
    )
    
    try:
        db.add(agent)
        db.commit()
        click.echo(f"\nAgent '{name}' created successfully!")
    except Exception as e:
        click.echo(f"\nError creating agent: {str(e)}")
        db.rollback()

@cli.command()
def update():
    """Update an existing agent."""
    # List agents
    db = init_db()
    agents = db.query(Agent).all()
    if not agents:
        click.echo("\nNo agents found to update.")
        return
    
    # Select agent
    agent_choices = [
        {"name": f"{agent.name} (ID: {agent.id})", "value": agent}
        for agent in agents
    ]
    
    agent = click.Choice(
        "Select agent to update:",
        choices=[choice["name"] for choice in agent_choices],
        show_default=True
    )
    
    if not agent:
        return
    
    # Update fields
    name = click.Text("Enter new name (or press enter to keep current):", default=agent.name)
    description = click.Text("Enter new description (or press enter to keep current):", default=agent.description or "")
    is_active = click.Boolean("Should the agent be active?", default=agent.is_active)
    
    # Update agent
    try:
        agent.name = name
        agent.description = description
        agent.is_active = is_active
        db.commit()
        click.echo(f"\nAgent '{name}' updated successfully!")
    except Exception as e:
        click.echo(f"\nError updating agent: {str(e)}")
        db.rollback()

@cli.command()
def delete():
    """Delete an existing agent."""
    # List agents
    db = init_db()
    agents = db.query(Agent).all()
    if not agents:
        click.echo("\nNo agents found to delete.")
        return
    
    # Select agent
    agent_choices = [
        {"name": f"{agent.name} (ID: {agent.id})", "value": agent}
        for agent in agents
    ]
    
    agent = click.Choice(
        "Select agent to delete:",
        choices=[choice["name"] for choice in agent_choices],
        show_default=True
    )
    
    if not agent:
        return
    
    # Confirm deletion
    confirm = click.Boolean(f"Are you sure you want to delete agent '{agent.name}'?")
    if not confirm:
        return
    
    # Delete agent
    try:
        db.delete(agent)
        db.commit()
        click.echo(f"\nAgent '{agent.name}' deleted successfully!")
    except Exception as e:
        click.echo(f"\nError deleting agent: {str(e)}")
        db.rollback()

def identify_components(flow_data: Dict) -> List[Dict]:
    """Get all components from the flow."""
    components = []
    nodes = flow_data.get("nodes", [])  # Get nodes directly from flow_data
    for node in nodes:
        # Get component info
        node_data = node.get("data", {}).get("node", {})
        components.append({
            "id": node.get("id"),
            "type": node.get("type"),
            "display_name": node_data.get("display_name", "Unknown")
        })
    return components

if __name__ == "__main__":
    cli()
