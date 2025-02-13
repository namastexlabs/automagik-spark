
"""allow null input_data in tasks

Revision ID: f4e43ba0207f
Revises: e07d97b4efea
Create Date: 2025-02-09 19:42:40.583445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4e43ba0207f'
down_revision: Union[str, None] = 'e07d97b4efea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Allow null input_data in tasks table
    op.alter_column('tasks', 'input_data',
                    existing_type=sa.String(),
                    nullable=True)


def downgrade() -> None:
    # Revert back to non-null input_data
    op.alter_column('tasks', 'input_data',
                    existing_type=sa.String(),
                    nullable=False)


