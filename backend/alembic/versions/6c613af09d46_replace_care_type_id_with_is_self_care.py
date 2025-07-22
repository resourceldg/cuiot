"""replace_care_type_id_with_is_self_care

Revision ID: 6c613af09d46
Revises: 0ab56ac02384
Create Date: 2025-07-22 04:52:08.695427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c613af09d46'
down_revision: Union[str, None] = '0ab56ac02384'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
