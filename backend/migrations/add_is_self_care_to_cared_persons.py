"""Add is_self_care to cared_persons and remove care_type_id

Revision ID: add_is_self_care_to_cared_persons
Revises: 1492e2d3f261
Create Date: 2025-07-20 05:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_is_self_care_to_cared_persons'
down_revision = '1492e2d3f261'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema"""
    
    # 1. Agregar campo is_self_care a cared_persons
    op.add_column('cared_persons', sa.Column('is_self_care', sa.Boolean(), nullable=False, server_default='false'))
    
    # 2. Actualizar is_self_care basado en roles de usuario
    # Los usuarios con rol 'cared_person_self' tendrán is_self_care = true
    op.execute("""
        UPDATE cared_persons 
        SET is_self_care = true 
        WHERE user_id IN (
            SELECT ur.user_id 
            FROM user_roles ur 
            JOIN roles r ON ur.role_id = r.id 
            WHERE r.name = 'cared_person_self' 
            AND ur.is_active = true
        )
    """)
    
    # 3. Eliminar campo care_type_id de cared_persons
    op.drop_column('cared_persons', 'care_type_id')
    
    # 4. Eliminar tabla care_types si existe
    op.execute("DROP TABLE IF EXISTS care_types CASCADE")


def downgrade():
    """Downgrade database schema"""
    
    # 1. Recrear tabla care_types
    op.create_table('care_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 2. Insertar datos básicos en care_types
    op.execute("""
        INSERT INTO care_types (id, name, description, created_at, updated_at) VALUES
        (1, 'self_care', 'Autocuidado', NOW(), NOW()),
        (2, 'delegated_care', 'Cuidado delegado', NOW(), NOW()),
        (3, 'family_care', 'Cuidado familiar', NOW(), NOW()),
        (4, 'professional_care', 'Cuidado profesional', NOW(), NOW()),
        (5, 'institutional_care', 'Cuidado institucional', NOW(), NOW()),
        (6, 'emergency_care', 'Cuidado de emergencia', NOW(), NOW())
    """)
    
    # 3. Agregar campo care_type_id de vuelta a cared_persons
    op.add_column('cared_persons', sa.Column('care_type_id', sa.Integer(), nullable=True))
    
    # 4. Actualizar care_type_id basado en is_self_care
    op.execute("""
        UPDATE cared_persons 
        SET care_type_id = CASE 
            WHEN is_self_care = true THEN 1  -- self_care
            ELSE 2  -- delegated_care
        END
    """)
    
    # 5. Agregar foreign key constraint
    op.create_foreign_key('fk_cared_persons_care_type_id', 'cared_persons', 'care_types', ['care_type_id'], ['id'])
    
    # 6. Eliminar campo is_self_care
    op.drop_column('cared_persons', 'is_self_care') 