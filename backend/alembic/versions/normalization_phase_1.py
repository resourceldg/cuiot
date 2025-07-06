"""Normalization Phase 1: Medical Information and Enumerations

Revision ID: normalization_phase_1
Revises: 562ffb9fcb30
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'normalization_phase_1'
down_revision = '562ffb9fcb30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enumeration tables for better data consistency
    op.create_table('enumeration_types',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_system', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('enumeration_values',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('enumeration_type_id', sa.UUID(), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['enumeration_type_id'], ['enumeration_types.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('enumeration_type_id', 'value')
    )
    
    # Create medical information tables
    op.create_table('medical_conditions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cared_person_id', sa.UUID(), nullable=False),
        sa.Column('condition_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity_level', sa.String(), nullable=True),
        sa.Column('diagnosis_date', sa.Date(), nullable=True),
        sa.Column('doctor_name', sa.String(), nullable=True),
        sa.Column('treatment_plan', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('medications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cared_person_id', sa.UUID(), nullable=False),
        sa.Column('medication_name', sa.String(), nullable=False),
        sa.Column('dosage', sa.String(), nullable=True),
        sa.Column('frequency', sa.String(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('prescribed_by', sa.String(), nullable=True),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('allergies',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cared_person_id', sa.UUID(), nullable=False),
        sa.Column('allergen_name', sa.String(), nullable=False),
        sa.Column('allergy_type', sa.String(), nullable=True),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('reaction_description', sa.Text(), nullable=True),
        sa.Column('diagnosis_date', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create contact information tables
    op.create_table('contact_information',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cared_person_id', sa.UUID(), nullable=False),
        sa.Column('contact_type', sa.String(), nullable=False),  # 'emergency', 'family', 'medical'
        sa.Column('contact_name', sa.String(), nullable=False),
        sa.Column('contact_phone', sa.String(), nullable=True),
        sa.Column('contact_email', sa.String(), nullable=True),
        sa.Column('relationship', sa.String(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create service relationship table
    op.create_table('service_relationships',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cared_person_id', sa.UUID(), nullable=False),
        sa.Column('institution_id', sa.Integer(), nullable=False),
        sa.Column('service_type', sa.String(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.ForeignKeyConstraint(['institution_id'], ['institutions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create service details table
    op.create_table('service_details',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('service_relationship_id', sa.UUID(), nullable=False),
        sa.Column('schedule', sa.Text(), nullable=True),
        sa.Column('frequency', sa.String(), nullable=True),
        sa.Column('duration_hours', sa.Float(), nullable=True),
        sa.Column('cost_per_session', sa.Integer(), nullable=True),
        sa.Column('payment_frequency', sa.String(), nullable=True),
        sa.Column('insurance_coverage', sa.Boolean(), nullable=False, default=False),
        sa.Column('insurance_provider', sa.String(), nullable=True),
        sa.Column('primary_doctor', sa.String(), nullable=True),
        sa.Column('medical_notes', sa.Text(), nullable=True),
        sa.Column('treatment_plan', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['service_relationship_id'], ['service_relationships.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('service_details')
    op.drop_table('service_relationships')
    op.drop_table('contact_information')
    op.drop_table('allergies')
    op.drop_table('medications')
    op.drop_table('medical_conditions')
    op.drop_table('enumeration_values')
    op.drop_table('enumeration_types') 