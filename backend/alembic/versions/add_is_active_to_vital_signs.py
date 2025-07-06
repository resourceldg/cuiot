"""add_is_active_to_vital_signs

Revision ID: add_is_active_to_vital_signs
Revises: add_audit_logs_table
Create Date: 2025-07-03 23:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_is_active_to_vital_signs'
down_revision: Union[str, None] = 'add_audit_logs_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_active column to vital_signs table
    op.add_column('vital_signs', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    # Remove is_active column from vital_signs table
    op.drop_column('vital_signs', 'is_active') 