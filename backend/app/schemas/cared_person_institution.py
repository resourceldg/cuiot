from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

class CaredPersonInstitutionBase(BaseModel):
    """Base schema for cared person institution relationship"""
    cared_person_id: UUID
    institution_id: int
    service_type_id: int = Field(..., description="Service type ID")
    start_date: date
    end_date: Optional[date] = None
    schedule: Optional[str] = None
    frequency: Optional[str] = None
    duration_hours: Optional[float] = None
    cost_per_session: Optional[int] = None
    payment_frequency: Optional[str] = None
    insurance_coverage: bool = False
    insurance_provider: Optional[str] = None
    primary_doctor: Optional[str] = None
    medical_notes: Optional[str] = None
    treatment_plan: Optional[str] = None
    status_type_id: Optional[int] = None
    is_primary: bool = False
    notes: Optional[str] = None

class CaredPersonInstitutionCreate(CaredPersonInstitutionBase):
    """Schema for creating a cared person institution relationship"""
    cared_person_id: UUID = Field(..., description="ID of the cared person")
    institution_id: int = Field(..., description="ID of the institution")
    cost_per_session: Optional[int] = Field(None, ge=0, description="Cost per session in cents")
    payment_frequency: Optional[str] = Field(None, description="Payment frequency")
    insurance_coverage: bool = Field(False, description="Whether service is covered by insurance")
    insurance_provider: Optional[str] = Field(None, description="Insurance provider name")
    primary_doctor: Optional[str] = Field(None, description="Primary doctor name")
    medical_notes: Optional[str] = Field(None, description="Medical notes")
    treatment_plan: Optional[str] = Field(None, description="Treatment plan")
    is_primary: bool = Field(False, description="Whether this is the primary institution")
    notes: Optional[str] = Field(None, description="Additional notes")

class CaredPersonInstitutionUpdate(BaseModel):
    """Schema for updating a cared person institution relationship"""
    service_type_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    schedule: Optional[str] = None
    frequency: Optional[str] = None
    duration_hours: Optional[float] = None
    cost_per_session: Optional[int] = None
    payment_frequency: Optional[str] = None
    insurance_coverage: Optional[bool] = None
    insurance_provider: Optional[str] = None
    primary_doctor: Optional[str] = None
    medical_notes: Optional[str] = None
    treatment_plan: Optional[str] = None
    status_type_id: Optional[int] = None
    is_primary: Optional[bool] = None
    notes: Optional[str] = None

class CaredPersonInstitution(CaredPersonInstitutionBase):
    """Schema for cared person institution relationship response"""
    id: UUID
    cared_person_id: UUID
    institution_id: int
    cost_per_session: Optional[int] = None
    payment_frequency: Optional[str] = None
    insurance_coverage: bool = False
    insurance_provider: Optional[str] = None
    primary_doctor: Optional[str] = None
    medical_notes: Optional[str] = None
    treatment_plan: Optional[str] = None
    status_type_id: Optional[int] = None
    is_primary: bool = False
    registered_by: Optional[UUID] = None
    registered_at: datetime
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CaredPersonInstitutionWithDetails(CaredPersonInstitution):
    """Schema for cared person institution with additional details"""
    cared_person_name: Optional[str] = Field(None, description="Name of the cared person")
    institution_name: Optional[str] = Field(None, description="Name of the institution")
    registered_by_name: Optional[str] = Field(None, description="Name of the user who registered")
    total_cost: float = Field(..., description="Total cost of service")
    
    class Config:
        from_attributes = True

class CaredPersonInstitutionSummary(BaseModel):
    """Schema for cared person institution summary"""
    total_services: int = Field(..., description="Total number of services")
    active_services: int = Field(..., description="Number of active services")
    total_cost: float = Field(..., description="Total cost of all services")
    primary_institution: Optional[str] = Field(None, description="Primary institution name")
    service_types: list = Field(..., description="List of service types")
    
    class Config:
        from_attributes = True
