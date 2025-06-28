# Import all models for SQLAlchemy to recognize them
from app.models.base import Base, BaseModel
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.institution import Institution
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.caregiver_assignment import CaregiverAssignment
from app.models.caregiver_institution import CaregiverInstitution
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
]
