from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

class VitalSignBase(BaseModel):
    temperature: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    oxygen_saturation: Optional[int] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    notes: Optional[str] = None
    measured_at: Optional[datetime] = None

class VitalSignCreate(VitalSignBase):
    shift_observation_id: UUID4

class VitalSignUpdate(BaseModel):
    temperature: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    oxygen_saturation: Optional[int] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    notes: Optional[str] = None
    measured_at: Optional[datetime] = None

class VitalSign(VitalSignBase):
    id: UUID4
    shift_observation_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
