from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4

class MedicalConditionBase(BaseModel):
    condition_name: str
    severity_level: str
    diagnosis_date: date
    description: Optional[str] = None
    treatment_plan: Optional[str] = None
    doctor_name: Optional[str] = None

class MedicalConditionCreate(MedicalConditionBase):
    cared_person_id: UUID4

class MedicalConditionUpdate(BaseModel):
    condition_name: Optional[str] = None
    severity_level: Optional[str] = None
    diagnosis_date: Optional[date] = None
    description: Optional[str] = None
    treatment_plan: Optional[str] = None
    doctor_name: Optional[str] = None

class MedicalCondition(MedicalConditionBase):
    id: UUID4
    cared_person_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True 