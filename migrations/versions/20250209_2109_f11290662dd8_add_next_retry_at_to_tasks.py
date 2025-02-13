
"""add next_retry_at to tasks

Revision ID: f11290662dd8
Revises: f4e43ba0207f
Create Date: 2025-02-09 21:09:18.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f11290662dd8'
down_revision = 'f4e43ba0207f'
branch_labels = None
depends_on = None


def upgrade():
    # Convert input_data to JSON using a safe conversion
    op.execute('ALTER TABLE tasks ALTER COLUMN input_data TYPE JSON USING CASE WHEN input_data IS NULL THEN \'{}\' ELSE input_data::json END')
    
    # Update other columns
    op.alter_column('tasks', 'tries',
                    existing_type=sa.INTEGER(),
                    nullable=False,
                    server_default='0')
    op.alter_column('tasks', 'max_retries',
                    existing_type=sa.INTEGER(),
                    nullable=False,
                    server_default='3')


def downgrade():
    op.execute('ALTER TABLE tasks ALTER COLUMN input_data TYPE VARCHAR')
    op.alter_column('tasks', 'tries',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.alter_column('tasks', 'max_retries',
                    existing_type=sa.INTEGER(),
                    nullable=True)


