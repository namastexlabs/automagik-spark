
"""add input_data to schedules

Revision ID: a198131eb48e
Revises: 
Create Date: 2025-02-09 19:34:46.583445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a198131eb48e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add input_data column to schedules table
    op.add_column('schedules', sa.Column('input_data', sa.String(), nullable=True))
    
    # Add schedule_id column to tasks table
    op.add_column('tasks', sa.Column('schedule_id', postgresql.UUID(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'schedules', ['schedule_id'], ['id'])


def downgrade() -> None:
    # Remove schedule_id column from tasks table
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'schedule_id')
    
    # Remove input_data column from schedules table
    op.drop_column('schedules', 'input_data')


