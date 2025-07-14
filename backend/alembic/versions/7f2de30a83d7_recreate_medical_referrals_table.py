"""recreate_medical_referrals_table

Revision ID: 7f2de30a83d7
Revises: b270ee7261b2
Create Date: 2025-07-14 01:30:02.465442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f2de30a83d7'
down_revision: Union[str, None] = 'b270ee7261b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
