"""Update schedules to use input_data instead of workflow_params

Revision ID: f7173038c3b4
Revises: 4b7033ec9033
Create Date: 2025-02-14 04:13:16.000000+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f7173038c3b4"
down_revision: Union[str, None] = "4b7033ec9033"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Copy data from workflow_params to input_data if it exists
    op.execute("""
        UPDATE schedules 
        SET input_data = workflow_params
        WHERE workflow_params IS NOT NULL
          AND input_data IS NULL
    """)

    # Drop workflow_params and params columns
    op.drop_column("schedules", "workflow_params")
    op.drop_column("schedules", "params")


def downgrade() -> None:
    # Add back workflow_params and params columns
    op.add_column("schedules", sa.Column("workflow_params", sa.String(), nullable=True))
    op.add_column("schedules", sa.Column("params", postgresql.JSON(astext_type=sa.Text()), nullable=True))

    # Copy data back from input_data to workflow_params
    op.execute("""
        UPDATE schedules 
        SET workflow_params = input_data
        WHERE input_data IS NOT NULL
    """)

    # Drop input_data column
    op.drop_column("schedules", "input_data")
