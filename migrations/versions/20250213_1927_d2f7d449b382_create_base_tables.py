"""create_base_tables

Revision ID: d2f7d449b382
Revises:
Create Date: 2025-02-13 19:27:58.513533+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d2f7d449b382"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workflow_sources first since workflows depend on it
    op.create_table(
        "workflow_sources",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("url", sa.String(255), nullable=False),
        sa.Column("encrypted_api_key", sa.String(), nullable=False),
        sa.Column("version_info", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )

    # Create workflows table
    op.create_table(
        "workflows",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column("flow_raw_data", sa.JSON(), nullable=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("remote_flow_id", sa.String(255), nullable=False),
        sa.Column("flow_version", sa.Integer(), server_default="1"),
        sa.Column("workflow_source_id", sa.UUID(), nullable=True),
        sa.Column("input_component", sa.String(255), nullable=True),
        sa.Column("output_component", sa.String(255), nullable=True),
        sa.Column("is_component", sa.Boolean(), server_default="false"),
        sa.Column("folder_id", sa.String(255), nullable=True),
        sa.Column("folder_name", sa.String(255), nullable=True),
        sa.Column("icon", sa.String(255), nullable=True),
        sa.Column("icon_bg_color", sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(["workflow_source_id"], ["workflow_sources.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create schedules table
    op.create_table(
        "schedules",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("workflow_id", sa.UUID(), nullable=False),
        sa.Column("schedule_type", sa.String(), nullable=False),
        sa.Column("schedule_expr", sa.String(), nullable=False),
        sa.Column("workflow_params", sa.String(), nullable=True),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("input_data", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflows.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create tasks table
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("workflow_id", sa.UUID(), nullable=False),
        sa.Column("schedule_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("input_data", sa.JSON(), nullable=False),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("error", sa.String(), nullable=True),
        sa.Column("tries", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_retries", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"]),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflows.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create task_logs table
    op.create_table(
        "task_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.Column("level", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("component_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create workers table
    op.create_table(
        "workers",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("hostname", sa.String(255), nullable=False),
        sa.Column("pid", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
        sa.Column("current_task_id", sa.UUID(), nullable=True),
        sa.Column("stats", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["current_task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Drop tables in reverse order of creation
    op.drop_table("workers")
    op.drop_table("task_logs")
    op.drop_table("tasks")
    op.drop_table("schedules")
    op.drop_table("workflows")
    op.drop_table("workflow_sources")
