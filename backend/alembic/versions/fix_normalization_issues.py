"""fix_normalization_issues

Revision ID: fix_normalization_issues
Revises: add_is_active_to_vital_signs
Create Date: 2025-07-03 23:47:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fix_normalization_issues'
down_revision: Union[str, None] = 'add_is_active_to_vital_signs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Fix activity_types table
    op.alter_column('activity_types', 'name', new_column_name='type_name')
    
    # Fix enumeration_types table  
    op.alter_column('enumeration_types', 'name', new_column_name='type_name')
    
    # Remove old medical fields from cared_persons (these are now in separate tables)
    op.drop_column('cared_persons', 'medical_conditions')
    op.drop_column('cared_persons', 'medications') 
    op.drop_column('cared_persons', 'allergies')


def downgrade() -> None:
    # Restore activity_types table
    op.alter_column('activity_types', 'type_name', new_column_name='name')
    
    # Restore enumeration_types table
    op.alter_column('enumeration_types', 'type_name', new_column_name='name')
    
    # Restore old medical fields in cared_persons
    op.add_column('cared_persons', sa.Column('medical_conditions', sa.Text(), nullable=True))
    op.add_column('cared_persons', sa.Column('medications', sa.Text(), nullable=True))
    op.add_column('cared_persons', sa.Column('allergies', sa.Text(), nullable=True)) 