"""Normalization Phase 3: Data Migration and Cleanup

Revision ID: normalization_phase_3
Revises: normalization_phase_2
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'normalization_phase_3'
down_revision = 'normalization_phase_2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert default enumeration types
    op.execute("""
        INSERT INTO enumeration_types (id, name, description, is_system, is_active) VALUES
        ('550e8400-e29b-41d4-a716-446655440001', 'care_type', 'Types of care provided', true, true),
        ('550e8400-e29b-41d4-a716-446655440002', 'care_level', 'Levels of care intensity', true, true),
        ('550e8400-e29b-41d4-a716-446655440003', 'mobility_level', 'Mobility assessment levels', true, true),
        ('550e8400-e29b-41d4-a716-446655440004', 'severity_level', 'Severity assessment levels', true, true),
        ('550e8400-e29b-41d4-a716-446655440005', 'status', 'General status values', true, true),
        ('550e8400-e29b-41d4-a716-446655440006', 'gender', 'Gender options', true, true),
        ('550e8400-e29b-41d4-a716-446655440007', 'blood_type', 'Blood type options', true, true),
        ('550e8400-e29b-41d4-a716-446655440008', 'allergy_type', 'Types of allergies', true, true),
        ('550e8400-e29b-41d4-a716-446655440009', 'activity_category', 'Activity categories', true, true),
        ('550e8400-e29b-41d4-a716-446655440010', 'contact_type', 'Types of contact information', true, true)
    """)
    
    # Insert default enumeration values
    op.execute("""
        INSERT INTO enumeration_values (id, enumeration_type_id, value, label, sort_order, is_default, is_active) VALUES
        -- Care types
        ('550e8400-e29b-41d4-a716-446655440101', '550e8400-e29b-41d4-a716-446655440001', 'home_care', 'Home Care', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440102', '550e8400-e29b-41d4-a716-446655440001', 'institutional', 'Institutional Care', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440103', '550e8400-e29b-41d4-a716-446655440001', 'respite', 'Respite Care', 3, false, true),
        ('550e8400-e29b-41d4-a716-446655440104', '550e8400-e29b-41d4-a716-446655440001', 'palliative', 'Palliative Care', 4, false, true),
        
        -- Care levels
        ('550e8400-e29b-41d4-a716-446655440201', '550e8400-e29b-41d4-a716-446655440002', 'basic', 'Basic Care', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440202', '550e8400-e29b-41d4-a716-446655440002', 'intermediate', 'Intermediate Care', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440203', '550e8400-e29b-41d4-a716-446655440002', 'advanced', 'Advanced Care', 3, false, true),
        ('550e8400-e29b-41d4-a716-446655440204', '550e8400-e29b-41d4-a716-446655440002', 'specialized', 'Specialized Care', 4, false, true),
        
        -- Mobility levels
        ('550e8400-e29b-41d4-a716-446655440301', '550e8400-e29b-41d4-a716-446655440003', 'independent', 'Independent', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440302', '550e8400-e29b-41d4-a716-446655440003', 'assisted', 'Assisted', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440303', '550e8400-e29b-41d4-a716-446655440003', 'wheelchair', 'Wheelchair', 3, false, true),
        ('550e8400-e29b-41d4-a716-446655440304', '550e8400-e29b-41d4-a716-446655440003', 'bedridden', 'Bedridden', 4, false, true),
        
        -- Severity levels
        ('550e8400-e29b-41d4-a716-446655440401', '550e8400-e29b-41d4-a716-446655440004', 'mild', 'Mild', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440402', '550e8400-e29b-41d4-a716-446655440004', 'moderate', 'Moderate', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440403', '550e8400-e29b-41d4-a716-446655440004', 'severe', 'Severe', 3, false, true),
        ('550e8400-e29b-41d4-a716-446655440404', '550e8400-e29b-41d4-a716-446655440004', 'critical', 'Critical', 4, false, true),
        
        -- Status values
        ('550e8400-e29b-41d4-a716-446655440501', '550e8400-e29b-41d4-a716-446655440005', 'active', 'Active', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440502', '550e8400-e29b-41d4-a716-446655440005', 'inactive', 'Inactive', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440503', '550e8400-e29b-41d4-a716-446655440005', 'pending', 'Pending', 3, false, true),
        ('550e8400-e29b-41d4-a716-446655440504', '550e8400-e29b-41d4-a716-446655440005', 'completed', 'Completed', 4, false, true),
        
        -- Gender options
        ('550e8400-e29b-41d4-a716-446655440601', '550e8400-e29b-41d4-a716-446655440006', 'male', 'Male', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440602', '550e8400-e29b-41d4-a716-446655440006', 'female', 'Female', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440603', '550e8400-e29b-41d4-a716-446655440006', 'other', 'Other', 3, false, true),
        
        -- Blood types
        ('550e8400-e29b-41d4-a716-446655440701', '550e8400-e29b-41d4-a716-446655440007', 'A+', 'A+', 1, false, true),
        ('550e8400-e29b-41d4-a716-446655440702', '550e8400-e29b-41d4-a716-446655440007', 'A-', 'A-', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440703', '550e8400-e29b-41d4-a716-446655440007', 'B+', 'B+', 3, false, true),
        ('550e8400-e29b-41d4-a716-446655440704', '550e8400-e29b-41d4-a716-446655440007', 'B-', 'B-', 4, false, true),
        ('550e8400-e29b-41d4-a716-446655440705', '550e8400-e29b-41d4-a716-446655440007', 'AB+', 'AB+', 5, false, true),
        ('550e8400-e29b-41d4-a716-446655440706', '550e8400-e29b-41d4-a716-446655440007', 'AB-', 'AB-', 6, false, true),
        ('550e8400-e29b-41d4-a716-446655440707', '550e8400-e29b-41d4-a716-446655440007', 'O+', 'O+', 7, false, true),
        ('550e8400-e29b-41d4-a716-446655440708', '550e8400-e29b-41d4-a716-446655440007', 'O-', 'O-', 8, false, true),
        
        -- Contact types
        ('550e8400-e29b-41d4-a716-446655440801', '550e8400-e29b-41d4-a716-446655440010', 'emergency', 'Emergency Contact', 1, true, true),
        ('550e8400-e29b-41d4-a716-446655440802', '550e8400-e29b-41d4-a716-446655440010', 'family', 'Family Contact', 2, false, true),
        ('550e8400-e29b-41d4-a716-446655440803', '550e8400-e29b-41d4-a716-446655440010', 'medical', 'Medical Contact', 3, false, true)
    """)
    
    # Insert default activity types
    op.execute("""
        INSERT INTO activity_types (id, name, description, category, is_active) VALUES
        ('550e8400-e29b-41d4-a716-446655440901', 'Physical Exercise', 'Physical activities and exercises', 'physical', true),
        ('550e8400-e29b-41d4-a716-446655440902', 'Cognitive Games', 'Mental exercises and brain games', 'cognitive', true),
        ('550e8400-e29b-41d4-a716-446655440903', 'Social Activities', 'Group activities and social interaction', 'social', true),
        ('550e8400-e29b-41d4-a716-446655440904', 'Creative Arts', 'Art, music, and creative activities', 'creative', true),
        ('550e8400-e29b-41d4-a716-446655440905', 'Daily Living Skills', 'Activities of daily living', 'daily_living', true),
        ('550e8400-e29b-41d4-a716-446655440906', 'Recreation', 'Leisure and recreational activities', 'recreation', true)
    """)


def downgrade() -> None:
    # Remove default data
    op.execute("DELETE FROM activity_types")
    op.execute("DELETE FROM enumeration_values")
    op.execute("DELETE FROM enumeration_types") 