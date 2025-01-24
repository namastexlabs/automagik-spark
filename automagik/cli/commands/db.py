import click
import os
import sys
from sqlalchemy import inspect
from automagik.core.database.session import engine
import asyncio
from automagik.core.services.flow_manager import FlowManager

@click.group()
def db():
    """Database management commands"""
    pass

@db.command()
@click.option('--force', is_flag=True, help='Force reinitialization even if tables exist')
def init_alembic(force):
    """Initialize the database with all tables"""
    try:
        # Get the absolute path to alembic.ini in root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        alembic_ini = os.path.join(root_dir, 'alembic.ini')
        
        if not os.path.exists(alembic_ini):
            click.echo("Error: alembic.ini not found in project root")
            sys.exit(1)
            
        # Check if tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables and not force:
            click.echo("Tables already exist. Use --force to reinitialize")
            sys.exit(1)
            
        # Run alembic upgrade
        os.environ['PYTHONPATH'] = root_dir
        result = os.system(f'cd {root_dir} && alembic upgrade head')
        
        if result == 0:
            click.echo("Successfully initialized database")
        else:
            click.echo("Error running alembic migrations")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error initializing database: {str(e)}")
        sys.exit(1)

@db.command()
def init():
    """Initialize the database."""
    try:
        # Get event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Initialize FlowManager
        flow_manager = FlowManager()
        
        # Initialize database
        if loop.run_until_complete(flow_manager.init_db()):
            print("Successfully initialized database")
        else:
            print("Failed to initialize database")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
