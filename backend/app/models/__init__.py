# Import all models for SQLAlchemy to recognize them
from app.models.base import Base, BaseModel
from app.models.status_type import StatusType
from app.models.relationship_type import RelationshipType
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.institution import Institution
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.caregiver_assignment import CaregiverAssignment
from app.models.caregiver_institution import CaregiverInstitution
from app.models.cared_person_institution import CaredPersonInstitution
from app.models.device import Device
from app.models.device_config import DeviceConfig
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.emergency_protocol import EmergencyProtocol
from app.models.service_subscription import ServiceSubscription
from app.models.billing_record import BillingRecord
from app.models.location_tracking import LocationTracking
from app.models.geofence import Geofence
from app.models.debug_event import DebugEvent
from app.models.report import Report
from .diagnosis import Diagnosis
from .medical_profile import MedicalProfile
from .medication_schedule import MedicationSchedule
from .medication_log import MedicationLog
from .restraint_protocol import RestraintProtocol
from .shift_observation import ShiftObservation
from .vital_sign import VitalSign

# Package models
from app.models.package import Package, UserPackage, PackageAddOn, UserPackageAddOn

# Scoring models
from app.models.caregiver_score import CaregiverScore
from app.models.caregiver_review import CaregiverReview
from app.models.institution_score import InstitutionScore
from app.models.institution_review import InstitutionReview

# Referral models
from app.models.referral import Referral, ReferralCommission

__all__ = [
    "Base",
    "BaseModel", 
    "Role",
    "UserRole",
    "Institution",
    "User",
    "CaredPerson",
    "CaregiverAssignment",
    "CaregiverInstitution",
    "CaredPersonInstitution",
    "Device",
    "DeviceConfig",
    "Event",
    "Alert",
    "Reminder",
    "EmergencyProtocol",
    "ServiceSubscription",
    "BillingRecord",
    "LocationTracking",
    "Geofence",
    "DebugEvent",
    "Report",
    "VitalSign",
    # Package models
    "Package",
    "UserPackage",
    "PackageAddOn",
    "UserPackageAddOn",
    # Scoring models
    "CaregiverScore",
    "CaregiverReview", 
    "InstitutionScore",
    "InstitutionReview",
    # Referral models
    "Referral",
    "ReferralCommission",
]
