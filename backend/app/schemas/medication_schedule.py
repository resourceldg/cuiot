from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID

class MedicationScheduleBase(BaseModel):
    medication_name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Dosage amount and unit")
    frequency: str = Field(..., description="How often to take the medication")
    start_date: date = Field(..., description="Start date for the medication")
    end_date: Optional[date] = Field(None, description="End date for the medication")
    instructions: Optional[str] = Field(None, description="Special instructions for taking the medication")
    side_effects: Optional[str] = Field(None, description="Known side effects")
    is_active: bool = True

class MedicationScheduleCreate(MedicationScheduleBase):
    cared_person_id: UUID = Field(..., description="ID of the cared person")

class MedicationScheduleUpdate(BaseModel):
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    instructions: Optional[str] = None
    side_effects: Optional[str] = None
    is_active: Optional[bool] = None

class MedicationSchedule(MedicationScheduleBase):
    id: UUID
    cared_person_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 