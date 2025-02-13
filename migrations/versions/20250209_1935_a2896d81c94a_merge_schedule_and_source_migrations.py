
"""merge schedule and source migrations

Revision ID: a2896d81c94a
Revises: 1ffd9d6e9df7, a198131eb48e
Create Date: 2025-02-09 19:35:22.890017+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2896d81c94a'
down_revision: Union[str, None] = ('1ffd9d6e9df7', 'a198131eb48e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass


