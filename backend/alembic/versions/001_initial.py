"""initial

Revision ID: 001
Revises: 
Create Date: 2024-06-27 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Tabla users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('phone', sa.String(20)),
        sa.Column('user_type', sa.String(20), default='family'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    # Tabla elderly_persons
    op.create_table(
        'elderly_persons',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('age', sa.Integer),
        sa.Column('address', sa.Text),
        sa.Column('emergency_contacts', postgresql.JSONB),
        sa.Column('medical_conditions', postgresql.JSONB, server_default=sa.text("'[]'::jsonb")),
        sa.Column('medications', postgresql.JSONB, server_default=sa.text("'[]'::jsonb")),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('is_deleted', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    # Tabla devices
    op.create_table(
        'devices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('elderly_person_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elderly_persons.id', ondelete='CASCADE')),
        sa.Column('device_id', sa.String(100), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('location', sa.String(100)),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
        sa.Column('last_heartbeat', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('status', sa.String(20), default='ready'),
        sa.Column('type', sa.String(50), default='unknown'),
    )
    # Tabla device_configs
    op.create_table(
        'device_configs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('device_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('devices.id', ondelete='CASCADE')),
        sa.Column('config_key', sa.String(100), nullable=False),
        sa.Column('config_value', postgresql.JSONB, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    # Tabla events
    op.create_table(
        'events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('elderly_person_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elderly_persons.id', ondelete='CASCADE')),
        sa.Column('device_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('devices.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(120)),
        sa.Column('description', sa.Text),
        sa.Column('event_type', sa.String(50), nullable=False, index=True),
        sa.Column('value', postgresql.JSONB),
        sa.Column('location', sa.String(100)),
        sa.Column('start_datetime', sa.DateTime(timezone=True)),
        sa.Column('end_datetime', sa.DateTime(timezone=True)),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('received_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    # Tabla alerts
    op.create_table(
        'alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('elderly_person_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elderly_persons.id', ondelete='CASCADE')),
        sa.Column('alert_type', sa.String(50), nullable=False, index=True),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('severity', sa.String(20), default='medium'),
        sa.Column('is_resolved', sa.Boolean, default=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True)),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('received_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    # Tabla reminders
    op.create_table(
        'reminders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('elderly_person_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elderly_persons.id', ondelete='CASCADE')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('reminder_type', sa.String(50), nullable=False),
        sa.Column('scheduled_time', sa.Time, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('days_of_week', postgresql.ARRAY(sa.Integer)),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('received_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade() -> None:
    op.drop_table('reminders')
    op.drop_table('alerts')
    op.drop_table('events')
    op.drop_table('device_configs')
    op.drop_table('devices')
    op.drop_table('elderly_persons')
    op.drop_table('users') 