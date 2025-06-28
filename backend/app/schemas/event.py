from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class EventBase(BaseModel):
    """Esquema base para eventos (sensores y calendario)"""
    event_type: str = Field(..., description="Tipo de evento: medical, family, medication, sensor, etc.")
    title: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = None
    value: Optional[Dict[str, Any]] = Field(None, description="Datos del evento")
    location: Optional[str] = Field(None, max_length=100)
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

class EventCreate(EventBase):
    """Esquema para crear evento"""
    elderly_person_id: Optional[UUID] = None
    device_id: Optional[UUID] = None
    created_by_id: UUID = Field(..., description="ID del usuario que crea el evento")
    received_by_id: Optional[UUID] = Field(None, description="ID del usuario que recibe el evento")

class EventUpdate(BaseModel):
    """Esquema para actualizar evento"""
    event_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    received_by_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class EventInDB(EventBase):
    """Esquema para evento en base de datos"""
    id: UUID
    elderly_person_id: Optional[UUID] = None
    device_id: Optional[UUID] = None
    created_by_id: UUID
    received_by_id: Optional[UUID] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Event(EventInDB):
    """Esquema para respuesta de evento"""
    pass 