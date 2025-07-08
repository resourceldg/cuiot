"""
Add unique constraint on (name, category) to status_types
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a5a24245d524'
down_revision = '881d292c26c8'
branch_labels = None
depends_on = None

def upgrade():
    # Eliminar el índice único existente en name si existe
    with op.batch_alter_table('status_types') as batch_op:
        batch_op.drop_index('ix_status_types_name')
        batch_op.create_unique_constraint('uq_status_types_name_category', ['name', 'category'])

def downgrade():
    # Revertir: eliminar la restricción única compuesta y restaurar la única en name
    with op.batch_alter_table('status_types') as batch_op:
        batch_op.drop_constraint('uq_status_types_name_category', type_='unique')
        batch_op.create_index('ix_status_types_name', ['name'], unique=True) 