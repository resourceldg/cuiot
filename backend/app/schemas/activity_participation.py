from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

class ActivityParticipationBase(BaseModel):
    participation_date: datetime
    duration_minutes: Optional[int] = None
    performance_level: Optional[str] = None
    notes: Optional[str] = None

class ActivityParticipationCreate(ActivityParticipationBase):
    cared_person_id: UUID4
    activity_id: UUID4

class ActivityParticipationUpdate(BaseModel):
    participation_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    performance_level: Optional[str] = None
    notes: Optional[str] = None

class ActivityParticipation(ActivityParticipationBase):
    id: UUID4
    cared_person_id: UUID4
    activity_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
