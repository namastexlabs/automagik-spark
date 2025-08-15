
"""merge workflow_components and schedules changes

Revision ID: 1e9250ec4418
Revises: 9adb44ec69a7, f7173038c3b4
Create Date: 2025-02-18 00:16:36.943121+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e9250ec4418'
down_revision: Union[str, None] = ('9adb44ec69a7', 'f7173038c3b4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass


