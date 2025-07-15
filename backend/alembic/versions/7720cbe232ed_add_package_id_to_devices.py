"""add_package_id_to_devices

Revision ID: 7720cbe232ed
Revises: 0d2cb7578830
Create Date: 2025-07-15 14:03:13.627445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7720cbe232ed'
down_revision: Union[str, None] = '0d2cb7578830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
