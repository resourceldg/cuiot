from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class MedicalProfileBase(BaseModel):
    blood_type: Optional[str] = Field(None, max_length=10)
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    emergency_info: Optional[Dict[str, Any]] = None
    medical_preferences: Optional[Dict[str, Any]] = None
    insurance_info: Optional[Dict[str, Any]] = None
    is_active: str = 'active'
    cared_person_id: UUID

class MedicalProfileCreate(MedicalProfileBase):
    pass

class MedicalProfileUpdate(MedicalProfileBase):
    pass

class MedicalProfileResponse(MedicalProfileBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 