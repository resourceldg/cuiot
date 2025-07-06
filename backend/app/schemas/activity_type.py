from typing import Optional, Dict, Any
from pydantic import BaseModel, UUID4

class ActivityTypeBase(BaseModel):
    type_name: str
    description: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = None

class ActivityTypeCreate(ActivityTypeBase):
    pass

class ActivityTypeUpdate(BaseModel):
    type_name: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = None

class ActivityType(ActivityTypeBase):
    id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
