from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class DeviceBase(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., max_length=100)
    device_type_id: Optional[int] = Field(None, description="ID del tipo de dispositivo")
    model: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
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
    user_id: Optional[UUID] = None
    cared_person_id: Optional[UUID] = None
    institution_id: Optional[UUID] = None

class DeviceCreate(DeviceBase, BaseCreate):
    pass

class DeviceUpdate(BaseUpdate):
    device_id: Optional[str] = Field(None, min_length=1, max_length=100)
    name: Optional[str] = Field(None, max_length=100)
    device_type_id: Optional[int] = Field(None, description="ID del tipo de dispositivo")
    model: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
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
    user_id: Optional[UUID] = None
    cared_person_id: Optional[UUID] = None
    institution_id: Optional[UUID] = None

class DeviceResponse(DeviceBase, BaseResponse):
    is_online: bool

class DeviceInDB(DeviceBase, BaseResponse):
    pass
