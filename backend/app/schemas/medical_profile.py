from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class MedicalProfileBase(BaseModel):
    blood_type: Optional[str] = Field(None, description="Blood type (e.g., A+, B-, O+, AB+)")
    allergies: Optional[str] = Field(None, description="List of allergies")
    chronic_conditions: Optional[str] = Field(None, description="Chronic medical conditions")
    emergency_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Emergency contact information")
    medical_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Medical preferences and restrictions")
    insurance_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Insurance information")
    is_active: bool = True
    cared_person_id: UUID

class MedicalProfileCreate(MedicalProfileBase):
    cared_person_id: UUID = Field(..., description="ID of the cared person")

class MedicalProfileUpdate(BaseModel):
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    emergency_info: Optional[Dict[str, Any]] = None
    medical_preferences: Optional[Dict[str, Any]] = None
    insurance_info: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class MedicalProfileResponse(MedicalProfileBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 