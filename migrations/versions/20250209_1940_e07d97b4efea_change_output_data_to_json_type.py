
"""change output_data to json type

Revision ID: e07d97b4efea
Revises: a2896d81c94a
Create Date: 2025-02-09 19:40:16.583445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e07d97b4efea'
down_revision: Union[str, None] = 'a2896d81c94a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convert output_data column to JSON type
    op.alter_column('tasks', 'output_data',
                    type_=postgresql.JSON(),
                    postgresql_using='output_data::json',
                    nullable=True)


def downgrade() -> None:
    # Convert output_data column back to String type
    op.alter_column('tasks', 'output_data',
                    type_=sa.String(),
                    postgresql_using='output_data::text',
                    nullable=True)


