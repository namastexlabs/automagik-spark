import click
from alembic.config import Config
from alembic import command
import os
import sys

@click.group()
def db():
    """Database management commands"""
    pass

@db.command()
def init():
    """Initialize the database with all tables"""
    try:
        # Get the absolute path to alembic.ini
        alembic_ini = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'alembic.ini')
        
        if not os.path.exists(alembic_ini):
            click.echo(f"Error: Could not find alembic.ini at {alembic_ini}")
            sys.exit(1)
            
        # Create Alembic configuration
        alembic_cfg = Config(alembic_ini)
        
        # Run all migrations
        command.upgrade(alembic_cfg, "head")
        
        click.echo("Database initialized successfully!")
    except Exception as e:
        click.echo(f"Error initializing database: {str(e)}")
        sys.exit(1)
