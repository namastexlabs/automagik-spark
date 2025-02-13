
"""add workflow source model and relationships

Revision ID: 1ffd9d6e9df7
Revises: 8ce2957b5216
Create Date: 2025-02-06 06:23:57.744115+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1ffd9d6e9df7'
down_revision: Union[str, None] = '8ce2957b5216'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workflow_sources table
    op.create_table(
        'workflow_sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_type', sa.String(50), nullable=False),
        sa.Column('url', sa.String(255), nullable=False, unique=True),
        sa.Column('encrypted_api_key', sa.String(), nullable=False),
        sa.Column('version_info', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    # Add workflow_source_id to workflows table
    op.add_column(
        'workflows',
        sa.Column('workflow_source_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_workflows_workflow_source_id',
        'workflows',
        'workflow_sources',
        ['workflow_source_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('fk_workflows_workflow_source_id', 'workflows', type_='foreignkey')

    # Drop workflow_source_id column
    op.drop_column('workflows', 'workflow_source_id')

    # Drop workflow_sources table
    op.drop_table('workflow_sources')


