
"""Add flow_raw_data column to workflows table

Revision ID: add_flow_raw_data
Revises: merge_timestamp_migrations
Create Date: 2025-02-10 00:44:56.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_flow_raw_data'
down_revision: Union[str, None] = 'merge_timestamp_migrations'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add flow_raw_data column to workflows table
    op.add_column('workflows', sa.Column('flow_raw_data', postgresql.JSON(), nullable=True))


def downgrade() -> None:
    # Remove flow_raw_data column from workflows table
    op.drop_column('workflows', 'flow_raw_data')


