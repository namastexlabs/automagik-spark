
"""merge timestamp migrations

Revision ID: merge_timestamp_migrations
Revises: d7e242592870, add_task_timestamp_defaults
Create Date: 2024-02-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_timestamp_migrations'
down_revision = ('d7e242592870', 'add_task_timestamp_defaults')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass


