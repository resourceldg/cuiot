"""add_missing_columns

Revision ID: add_missing_columns
Revises: fix_normalization_issues
Create Date: 2025-07-03 23:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_missing_columns'
down_revision: Union[str, None] = 'fix_normalization_issues'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add requirements column to activity_types
    op.add_column('activity_types', sa.Column('requirements', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # Add value_name column to enumeration_values (if it doesn't exist)
    # First check if the column exists
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns('enumeration_values')]
    
    if 'value_name' not in columns:
        # Add column as nullable first
        op.add_column('enumeration_values', sa.Column('value_name', sa.String(100), nullable=True))
        
        # Update existing records with a default value
        op.execute("UPDATE enumeration_values SET value_name = 'default_value' WHERE value_name IS NULL")
        
        # Make column not nullable
        op.alter_column('enumeration_values', 'value_name', nullable=False)


def downgrade() -> None:
    # Remove requirements column from activity_types
    op.drop_column('activity_types', 'requirements')
    
    # Remove value_name column from enumeration_values
    op.drop_column('enumeration_values', 'value_name') 