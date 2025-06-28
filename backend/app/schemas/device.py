from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class DeviceBase(BaseModel):
    """Esquema base para dispositivos IoT"""
    device_id: str = Field(..., min_length=1, max_length=100, description="ID único del dispositivo ESP32")
    name: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    is_active: bool = True

class DeviceCreate(DeviceBase):
    """Esquema para crear dispositivo"""
    elderly_person_id: UUID

class DeviceUpdate(BaseModel):
    """Esquema para actualizar dispositivo"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class DeviceInDB(DeviceBase):
    """Esquema para dispositivo en base de datos"""
    id: UUID
    elderly_person_id: UUID
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Device(DeviceInDB):
    """Esquema para respuesta de dispositivo"""
    pass 