"""add_flow_id_to_schedules

Revision ID: 6bf8b3bc2375
Revises: 3af7c6f910c2
Create Date: 2025-01-07 14:37:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6bf8b3bc2375'
down_revision: Union[str, None] = '3af7c6f910c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add flow_id column
    op.add_column('schedules', sa.Column('flow_id', sa.UUID(), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key(
        'schedules_flow_id_fkey',
        'schedules', 'flows',
        ['flow_id'], ['id']
    )
    
    # Make flow_id not nullable after adding the constraint
    op.alter_column('schedules', 'flow_id',
               existing_type=sa.UUID(),
               nullable=False)


def downgrade() -> None:
    # Drop the foreign key constraint first
    op.drop_constraint('schedules_flow_id_fkey', 'schedules', type_='foreignkey')
    
    # Drop the column
    op.drop_column('schedules', 'flow_id')
