"""
Módulos de población de datos para CUIOT
Organizados por dominio de negocio
"""

# Core modules
from .core.device_types import DeviceTypeManager

# IoT modules  
from .iot.device_manager import DeviceManager
from .iot.devices import populate_devices
from .iot.events import populate_events
from .iot.alerts import populate_alerts
from .iot.tracking import populate_tracking
from .iot.geofences import populate_geofences, populate_geofences_complete

# Care modules
# from .care.cared_persons import populate_cared_persons
# from .care.medical_data import populate_medical_data
# from .care.medications import populate_medications
from .care.referrals import (
    populate_referrals,
    populate_medical_referrals,
    populate_referrals_complete
)

# Business modules
# from .business.institutions import populate_institutions
# from .business.packages import populate_packages
# from .business.users import populate_users
from .business.addons import populate_package_add_ons, populate_user_packages, populate_user_package_add_ons, populate_addons_complete
from .business.billing import populate_billing_records, populate_billing_complete
from .business.scoring import (
    populate_caregiver_scores,
    populate_caregiver_reviews,
    populate_institution_scores,
    populate_institution_reviews,
    populate_scoring_complete
)

# Monitoring modules
# from .monitoring.reports import populate_reports
# from .monitoring.analytics import populate_analytics

__all__ = [
    # Core
    'DeviceTypeManager',
    
    # IoT
    'DeviceManager',
    'populate_devices',
    'populate_events', 
    'populate_alerts',
    'populate_tracking',
    'populate_geofences',
    'populate_geofences_complete',
    
    # Care (comentados hasta implementar)
    # 'populate_cared_persons',
    # 'populate_medical_data',
    # 'populate_medications',
    
    # Referrals
    'populate_referrals',
    'populate_medical_referrals',
    'populate_referrals_complete',
    
    # Business (comentados hasta implementar)
    # 'populate_institutions',
    # 'populate_packages',
    # 'populate_users',
    
    # Add-ons and subscriptions
    'populate_package_add_ons',
    'populate_user_packages',
    'populate_user_package_add_ons',
    'populate_addons_complete',
    
    # Billing
    'populate_billing_records',
    'populate_billing_complete',
    
    # Scoring and Reviews
    'populate_caregiver_scores',
    'populate_caregiver_reviews',
    'populate_institution_scores',
    'populate_institution_reviews',
    'populate_scoring_complete',
    
    # Monitoring (comentados hasta implementar)
    # 'populate_reports',
    # 'populate_analytics',
] 