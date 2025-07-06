from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class CaregiverAssignmentBase(BaseModel):
    caregiver_id: UUID
    cared_person_id: UUID
    start_date: date
    end_date: Optional[date] = None
    schedule: Optional[str] = None  # JSON string
    caregiver_assignment_type_id: int = Field(..., description="ID del tipo de asignación normalizado")
    responsibilities: Optional[str] = None
    special_requirements: Optional[str] = None
    hourly_rate: Optional[int] = Field(None, ge=0)  # Rate in cents
    payment_frequency: Optional[str] = Field(None, max_length=50)
    is_insured: bool = False
    insurance_provider: Optional[str] = Field(None, max_length=100)
    client_rating: Optional[int] = Field(None, ge=1, le=5)
    client_feedback: Optional[str] = None
    caregiver_self_rating: Optional[int] = Field(None, ge=1, le=5)
    caregiver_notes: Optional[str] = None
    primary_doctor: Optional[str] = Field(None, max_length=100)
    medical_contact: Optional[str] = Field(None, max_length=100)
    emergency_protocol: Optional[str] = None
    status_type_id: Optional[int] = Field(None, description="ID del tipo de status normalizado")
    is_primary: bool = False
    assigned_by: Optional[UUID] = None
    notes: Optional[str] = None

class CaregiverAssignmentCreate(CaregiverAssignmentBase, BaseCreate):
    pass

class CaregiverAssignmentUpdate(CaregiverAssignmentBase, BaseUpdate):
    caregiver_id: Optional[UUID] = None
    cared_person_id: Optional[UUID] = None
    start_date: Optional[date] = None
    caregiver_assignment_type_id: Optional[int] = Field(None, description="ID del tipo de asignación normalizado")
    hourly_rate: Optional[int] = Field(None, ge=0)
    payment_frequency: Optional[str] = Field(None, max_length=50)
    is_insured: Optional[bool] = None
    client_rating: Optional[int] = Field(None, ge=1, le=5)
    caregiver_self_rating: Optional[int] = Field(None, ge=1, le=5)
    status_type_id: Optional[int] = Field(None, description="ID del tipo de status normalizado")
    is_primary: Optional[bool] = None

class CaregiverAssignmentResponse(CaregiverAssignmentBase, BaseResponse):
    is_active: bool
    duration_days: int
    hourly_rate_decimal: float
    estimated_total_cost: float

class CaregiverAssignmentInDB(CaregiverAssignmentBase, BaseResponse):
    pass 