from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class MedicationLogBase(BaseModel):
    medication_schedule_id: UUID
    taken_at: datetime
    confirmed_by: Optional[UUID] = None
    confirmation_method: Optional[str] = None
    notes: Optional[str] = None
    dosage_given: Optional[str] = Field(None, max_length=100)
    is_missed: bool = False
    side_effects: Optional[str] = None
    effectiveness_rating: Optional[str] = None
    attachment: Optional[Dict[str, Any]] = None
    additional_data: Optional[Dict[str, Any]] = None

class MedicationLogCreate(MedicationLogBase):
    pass

class MedicationLogUpdate(MedicationLogBase):
    pass

class MedicationLogResponse(MedicationLogBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 