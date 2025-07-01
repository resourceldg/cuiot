from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID

class MedicationScheduleBase(BaseModel):
    medication_name: str = Field(..., max_length=200)
    dosage: str = Field(..., max_length=100)
    frequency: str = Field(..., max_length=100)
    start_date: date
    end_date: Optional[date] = None
    instructions: Optional[str] = None
    prescribed_by: Optional[UUID] = None
    is_active: str = 'active'
    schedule_details: Optional[Dict[str, Any]] = None
    cared_person_id: UUID

class MedicationScheduleCreate(MedicationScheduleBase):
    pass

class MedicationScheduleUpdate(MedicationScheduleBase):
    pass

class MedicationScheduleResponse(MedicationScheduleBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 