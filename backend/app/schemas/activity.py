from typing import Optional
from pydantic import BaseModel, UUID4

class ActivityBase(BaseModel):
    activity_name: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = None

class ActivityCreate(ActivityBase):
    activity_type_id: UUID4

class ActivityUpdate(BaseModel):
    activity_name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = None

class Activity(ActivityBase):
    id: UUID4
    activity_type_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
