"""change_tweakable_params_to_json

Revision ID: e6dd44e1aa45
Revises: 14d1c29e0c79
Create Date: 2025-01-24 17:07:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6dd44e1aa45'
down_revision: Union[str, None] = '14d1c29e0c79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a temporary column
    op.add_column('flow_components', sa.Column('tweakable_params_json', sa.JSON(), nullable=True))
    
    # Copy data from old column to new column, converting array to JSON array
    op.execute("""
        UPDATE flow_components 
        SET tweakable_params_json = to_json(tweakable_params)
        WHERE tweakable_params IS NOT NULL
    """)
    
    # Drop old column
    op.drop_column('flow_components', 'tweakable_params')
    
    # Rename new column to old name
    op.alter_column('flow_components', 'tweakable_params_json', new_column_name='tweakable_params')


def downgrade() -> None:
    # Create a temporary column
    op.add_column('flow_components', sa.Column('tweakable_params_array', sa.ARRAY(sa.String()), nullable=True))
    
    # Copy data from JSON column to array column
    op.execute("""
        UPDATE flow_components 
        SET tweakable_params_array = ARRAY(
            SELECT json_array_elements_text(tweakable_params)
        )
        WHERE tweakable_params IS NOT NULL
    """)
    
    # Drop JSON column
    op.drop_column('flow_components', 'tweakable_params')
    
    # Rename array column to original name
    op.alter_column('flow_components', 'tweakable_params_array', new_column_name='tweakable_params')
