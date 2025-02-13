
"""Add default values for task timestamps

Revision ID: add_task_timestamp_defaults
Revises: 
Create Date: 2024-02-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = 'add_task_timestamp_defaults'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add default values for created_at and updated_at
    op.alter_column('tasks', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_nullable=True)
    
    op.alter_column('tasks', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_nullable=True)


def downgrade():
    # Remove default values for created_at and updated_at
    op.alter_column('tasks', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=None,
               existing_nullable=True)
    
    op.alter_column('tasks', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=None,
               existing_nullable=True)


