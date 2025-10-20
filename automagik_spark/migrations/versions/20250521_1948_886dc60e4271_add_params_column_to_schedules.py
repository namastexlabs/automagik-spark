# Remove gradient column if present
# op.drop_column('workflows', 'gradient')
# op.add_column('workflows', sa.Column('gradient', sa.Boolean(), nullable=True, server_default=sa.text('false')))
# op.add_column('workflows', sa.Column('gradient', sa.VARCHAR(length=255), nullable=True))
