"""Normalization Phase 2: Activities and Detailed Events

Revision ID: normalization_phase_2
Revises: normalization_phase_1
Create Date: 2024-01-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'normalization_phase_2'
down_revision = 'normalization_phase_1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create activity types table
    op.create_table('activity_types',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create activities table
    op.create_table('activities',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cared_person_id', sa.UUID(), nullable=False),
        sa.Column('activity_type_id', sa.UUID(), nullable=False),
        sa.Column('activity_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('difficulty_level', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cared_person_id'], ['cared_persons.id'], ),
        sa.ForeignKeyConstraint(['activity_type_id'], ['activity_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create activity participation table
    op.create_table('activity_participation',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('shift_observation_id', sa.UUID(), nullable=False),
        sa.Column('activity_id', sa.UUID(), nullable=False),
        sa.Column('participation_level', sa.String(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('enjoyment_rating', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['shift_observation_id'], ['shift_observations.id'], ),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create medication administration table
    op.create_table('medication_administrations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('medication_schedule_id', sa.UUID(), nullable=False),
        sa.Column('shift_observation_id', sa.UUID(), nullable=True),
        sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('administered_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('confirmed_by', sa.UUID(), nullable=True),
        sa.Column('confirmation_method', sa.String(), nullable=True),
        sa.Column('dosage_given', sa.String(), nullable=True),
        sa.Column('is_missed', sa.Boolean(), nullable=False, default=False),
        sa.Column('side_effects', sa.Text(), nullable=True),
        sa.Column('effectiveness_rating', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, default='scheduled'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['medication_schedule_id'], ['medication_schedules.id'], ),
        sa.ForeignKeyConstraint(['shift_observation_id'], ['shift_observations.id'], ),
        sa.ForeignKeyConstraint(['confirmed_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create assignment details table
    op.create_table('assignment_details',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('caregiver_assignment_id', sa.Integer(), nullable=False),
        sa.Column('schedule', sa.Text(), nullable=True),
        sa.Column('responsibilities', sa.Text(), nullable=True),
        sa.Column('special_requirements', sa.Text(), nullable=True),
        sa.Column('hourly_rate', sa.Integer(), nullable=True),
        sa.Column('payment_frequency', sa.String(), nullable=True),
        sa.Column('is_insured', sa.Boolean(), nullable=False, default=False),
        sa.Column('insurance_provider', sa.String(), nullable=True),
        sa.Column('primary_doctor', sa.String(), nullable=True),
        sa.Column('medical_contact', sa.String(), nullable=True),
        sa.Column('emergency_protocol', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['caregiver_assignment_id'], ['caregiver_assignments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create vital signs table
    op.create_table('vital_signs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('shift_observation_id', sa.UUID(), nullable=False),
        sa.Column('blood_pressure_systolic', sa.Integer(), nullable=True),
        sa.Column('blood_pressure_diastolic', sa.Integer(), nullable=True),
        sa.Column('heart_rate', sa.Integer(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('oxygen_saturation', sa.Integer(), nullable=True),
        sa.Column('respiratory_rate', sa.Integer(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.Column('bmi', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('measured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['shift_observation_id'], ['shift_observations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('vital_signs')
    op.drop_table('assignment_details')
    op.drop_table('medication_administrations')
    op.drop_table('activity_participation')
    op.drop_table('activities')
    op.drop_table('activity_types') 