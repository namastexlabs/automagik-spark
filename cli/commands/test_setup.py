import click
from datetime import datetime
from ..models import Task
from ..db import engine
from sqlalchemy.orm import Session

@click.command()
def setup_test_tasks():
    """Create some test tasks in the database"""
    session = Session(engine)
    
    # Create a few test tasks
    tasks = [
        Task(
            agent_id=1,
            status='pending',
            input_data={'action': 'test1'},
            output_data={},
            tries=0,
            max_retries=3,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Task(
            agent_id=2,
            status='pending',
            input_data={'action': 'test2'},
            output_data={},
            tries=0,
            max_retries=3,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    session.add_all(tasks)
    session.commit()
    click.echo(f"Created {len(tasks)} test tasks") 