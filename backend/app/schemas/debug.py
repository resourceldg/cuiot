from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseResponse, BaseCreate, BaseUpdate

class DebugEventBase(BaseModel):
    event_type: str = Field(..., max_length=50)
    event_subtype: Optional[str] = Field(None, max_length=50)
    severity: str = Field(default="info", max_length=20)
    event_data: Optional[str] = None  # JSON string
    message: Optional[str] = None
    stack_trace: Optional[str] = None
    source: Optional[str] = Field(None, max_length=100)
    test_session: Optional[str] = Field(None, max_length=100)
    environment: Optional[str] = Field(None, max_length=50)
    event_time: datetime
    processed_at: Optional[datetime] = None
    user_id: Optional[int] = None
    cared_person_id: Optional[int] = None
    device_id: Optional[int] = None

class DebugEventCreate(DebugEventBase, BaseCreate):
    pass

class DebugEventUpdate(DebugEventBase, BaseUpdate):
    event_type: Optional[str] = Field(None, max_length=50)
    event_subtype: Optional[str] = Field(None, max_length=50)
    severity: Optional[str] = Field(None, max_length=20)
    event_time: Optional[datetime] = None

class DebugEventResponse(DebugEventBase, BaseResponse):
    pass

class DebugEventInDB(DebugEventBase, BaseResponse):
    pass

class DebugSummary(BaseModel):
    total_events: int
    events_by_type: dict
    events_by_severity: dict
    recent_events: list
    test_sessions: list
