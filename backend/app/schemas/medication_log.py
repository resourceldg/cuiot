from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class MedicationLogBase(BaseModel):
    medication_schedule_id: UUID
    administered_at: datetime
    administered_by: Optional[UUID] = None
    status: str = Field(..., max_length=50)  # 'administered', 'missed', 'refused', 'delayed'
    notes: Optional[str] = None
    dosage_given: Optional[str] = Field(None, max_length=100)
    side_effects: Optional[str] = None
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