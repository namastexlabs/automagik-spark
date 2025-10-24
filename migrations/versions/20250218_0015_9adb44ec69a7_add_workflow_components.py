"""add_workflow_components

Revision ID: 9adb44ec69a7
Revises: d2f7d449b382
Create Date: 2025-02-18 00:15:00.000000+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9adb44ec69a7"
down_revision: Union[str, None] = "d2f7d449b382"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workflow_components table
    op.create_table(
        "workflow_components",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("workflow_id", sa.UUID(), nullable=False),
        sa.Column("component_id", sa.String(255), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("template", sa.JSON(), nullable=True),
        sa.Column("tweakable_params", sa.JSON(), nullable=True),
        sa.Column("is_input", sa.Boolean(), server_default="false"),
        sa.Column("is_output", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflows.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("workflow_components")
