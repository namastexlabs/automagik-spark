"""add_missing_workflow_columns

Revision ID: 4b7033ec9033
Revises: d2f7d449b382
Create Date: 2025-02-13 19:29:24.013417+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4b7033ec9033"
down_revision: Union[str, None] = "d2f7d449b382"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to workflows table
    op.add_column("workflows", sa.Column("gradient", sa.String(255), nullable=True))
    op.add_column("workflows", sa.Column("liked", sa.Boolean(), server_default="false", nullable=False))
    op.add_column("workflows", sa.Column("tags", sa.JSON(), nullable=True))
    op.add_column(
        "workflows",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "workflows",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    # Remove added columns from workflows table
    op.drop_column("workflows", "updated_at")
    op.drop_column("workflows", "created_at")
    op.drop_column("workflows", "tags")
    op.drop_column("workflows", "liked")
    op.drop_column("workflows", "gradient")
