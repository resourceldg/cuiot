from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4

class MedicationBase(BaseModel):
    medication_name: str
    dosage: str
    frequency: str
    start_date: Optional[date] = None
    prescribed_by: Optional[str] = None
    instructions: Optional[str] = None

class MedicationCreate(MedicationBase):
    cared_person_id: UUID4

class MedicationUpdate(BaseModel):
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    prescribed_by: Optional[str] = None
    instructions: Optional[str] = None

class Medication(MedicationBase):
    id: UUID4
    cared_person_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
