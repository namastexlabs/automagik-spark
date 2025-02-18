
"""merge workflow_components and schedules changes

Revision ID: 1e9250ec4418
Revises: 20250218_0015, update_schedules_input_data
Create Date: 2025-02-18 00:16:36.943121+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e9250ec4418'
down_revision: Union[str, None] = ('20250218_0015', 'update_schedules_input_data')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass


