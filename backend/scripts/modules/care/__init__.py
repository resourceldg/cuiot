"""
Care Module - Handles all care-related data population
"""

from .cared_persons import populate_cared_persons
from .caregivers import populate_caregivers
from .medical_data import populate_medical_data
from .care_assignments import populate_care_assignments

__all__ = [
    'populate_cared_persons',
    'populate_caregivers', 
    'populate_medical_data',
    'populate_care_assignments'
] 