"""create_medical_referrals_table

Revision ID: create_medical_referrals_table
Revises: 881d292c26c8
Create Date: 2025-07-04 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'create_medical_referrals_table'
down_revision: Union[str, None] = '881d292c26c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create medical_referrals table
    op.create_table('medical_referrals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cared_person_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('referral_type', sa.String(length=50), nullable=False),
        sa.Column('referred_by', sa.String(length=100), nullable=False),
        sa.Column('referred_to', sa.String(length=200), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('status_type_id', sa.Integer(), nullable=True),
        sa.Column('referral_date', sa.Date(), nullable=False),
        sa.Column('appointment_date', sa.DateTime(), nullable=True),
        sa.Column('completed_date', sa.DateTime(), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('insurance_info', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.ForeignKeyConstraint(['status_type_id'], ['status_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medical_referrals_id'), 'medical_referrals', ['id'], unique=False)
    op.create_index(op.f('ix_medical_referrals_status_type_id'), 'medical_referrals', ['status_type_id'], unique=False)


def downgrade() -> None:
    # Drop medical_referrals table
    op.drop_index(op.f('ix_medical_referrals_status_type_id'), table_name='medical_referrals')
    op.drop_index(op.f('ix_medical_referrals_id'), table_name='medical_referrals')
    op.drop_table('medical_referrals') 