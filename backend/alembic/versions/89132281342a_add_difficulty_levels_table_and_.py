"""add_difficulty_levels_table_and_normalize_difficulty_level_in_activity

Revision ID: 89132281342a
Revises: dfb5939c5d29
Create Date: 2025-07-06 00:39:27.397398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89132281342a'
down_revision: Union[str, None] = 'dfb5939c5d29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
