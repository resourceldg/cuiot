# Database models
from app.core.database import Base

# Core models
from .user import User
from .role import Role
from .user_role import UserRole
from .institution import Institution

# Care models
from .cared_person import CaredPerson
from .caregiver_assignment import CaregiverAssignment

# Service models
from .emergency_protocol import EmergencyProtocol
from .service_subscription import ServiceSubscription
from .billing_record import BillingRecord

# Device models
from .device import Device
from .device_config import DeviceConfig

# Event and monitoring models
from .event import Event
from .alert import Alert
from .reminder import Reminder

# Legacy models (to be deprecated)
from .elderly_person import ElderlyPerson

__all__ = [
    "Base",
    # Core models
    "User",
    "Role", 
    "UserRole",
    "Institution",
    # Care models
    "CaredPerson",
    "CaregiverAssignment",
    # Service models
    "EmergencyProtocol",
    "ServiceSubscription",
    "BillingRecord",
    # Device models
    "Device",
    "DeviceConfig",
    # Event and monitoring models
    "Event",
    "Alert", 
    "Reminder",
    # Legacy models
    "ElderlyPerson"
] 