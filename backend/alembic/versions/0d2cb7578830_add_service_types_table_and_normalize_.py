"""add_service_types_table_and_normalize_service_type

Revision ID: 0d2cb7578830
Revises: 7f59716bedbb
Create Date: 2025-07-06 01:08:12.000422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d2cb7578830'
down_revision: Union[str, None] = '7f59716bedbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_subscriptions', sa.Column('service_type_id', sa.Integer(), nullable=False))
    op.drop_index('ix_service_subscriptions_subscription_type', table_name='service_subscriptions')
    op.create_index(op.f('ix_service_subscriptions_service_type_id'), 'service_subscriptions', ['service_type_id'], unique=False)
    op.create_foreign_key(None, 'service_subscriptions', 'service_types', ['service_type_id'], ['id'])
    op.drop_column('service_subscriptions', 'subscription_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_subscriptions', sa.Column('subscription_type', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'service_subscriptions', type_='foreignkey')
    op.drop_index(op.f('ix_service_subscriptions_service_type_id'), table_name='service_subscriptions')
    op.create_index('ix_service_subscriptions_subscription_type', 'service_subscriptions', ['subscription_type'], unique=False)
    op.drop_column('service_subscriptions', 'service_type_id')
    # ### end Alembic commands ###
