from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class EventBase(BaseModel):
    event_type_id: int = Field(..., description="ID del tipo de evento")
    event_subtype: Optional[str] = Field(None, max_length=50)
    severity: str = Field(default="info", max_length=20)
    event_data: Optional[str] = None  # JSON string
    message: Optional[str] = None
    source: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    event_time: datetime
    processed_at: Optional[datetime] = None
    user_id: Optional[UUID] = None
    cared_person_id: Optional[UUID] = None
    device_id: Optional[UUID] = None

class EventCreate(EventBase, BaseCreate):
    pass

class EventUpdate(EventBase, BaseUpdate):
    event_type_id: Optional[int] = Field(None, description="ID del tipo de evento")
    event_subtype: Optional[str] = Field(None, max_length=50)
    severity: Optional[str] = Field(None, max_length=20)
    event_time: Optional[datetime] = None

class EventResponse(EventBase, BaseResponse):
    pass

class EventInDB(EventBase, BaseResponse):
    pass
