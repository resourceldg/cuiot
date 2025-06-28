# Pydantic schemas for data validation 

# User schemas
from .user import (
    UserBase, UserCreate, UserUpdate, User, 
    UserLogin, Token, TokenData
)

# Elderly person schemas
from .elderly_person import (
    EmergencyContact, ElderlyPersonBase, ElderlyPersonCreate, ElderlyPersonUpdate, 
    ElderlyPerson, ElderlyPersonWithDevices
)

# Device schemas
from .device import (
    DeviceBase, DeviceCreate, DeviceUpdate, 
    Device
)

# Event schemas
from .event import (
    EventBase, EventCreate, 
    Event
)

# Alert schemas
from .alert import (
    AlertType, AlertSeverity, AlertBase, AlertCreate, 
    AlertUpdate, AlertResponse, AlertListResponse
)

# Reminder schemas
from .reminder import (
    ReminderType, ReminderBase, ReminderCreate, 
    ReminderUpdate, ReminderResponse, ReminderListResponse
) 