from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseResponse, BaseCreate, BaseUpdate

class DeviceBase(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=100)
    device_type: str = Field(..., max_length=50)
    model: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="active", max_length=50)
    battery_level: Optional[int] = Field(None, ge=0, le=100)
    signal_strength: Optional[int] = Field(None, ge=0, le=100)
    last_seen: Optional[datetime] = None
    location_description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    settings: Optional[str] = None  # JSON string
    firmware_version: Optional[str] = Field(None, max_length=50)
    hardware_version: Optional[str] = Field(None, max_length=50)
    user_id: Optional[int] = None
    cared_person_id: Optional[int] = None
    institution_id: Optional[int] = None

class DeviceCreate(DeviceBase, BaseCreate):
    pass

class DeviceUpdate(DeviceBase, BaseUpdate):
    device_id: Optional[str] = Field(None, min_length=1, max_length=100)
    device_type: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=50)

class DeviceResponse(DeviceBase, BaseResponse):
    is_online: bool

class DeviceInDB(DeviceBase, BaseResponse):
    pass
