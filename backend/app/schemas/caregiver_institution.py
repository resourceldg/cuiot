from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any
from datetime import datetime
from uuid import UUID


class CaregiverInstitutionBase(BaseModel):
    """Esquema base para relaciones cuidador-institución."""
    caregiver_id: UUID = Field(..., description="ID del cuidador")
    institution_id: Optional[UUID] = Field(None, description="ID de la institución (None para freelance)")
    relationship_type: str = Field(..., description="Tipo de relación")
    role_in_institution: Optional[str] = Field(None, description="Rol en la institución")
    start_date: datetime = Field(..., description="Fecha de inicio de la relación")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin de la relación")
    status: str = Field(default="active", description="Estado de la relación")
    is_primary_institution: bool = Field(default=False, description="Si es la institución principal")
    working_hours: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Horarios de trabajo")
    responsibilities: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Responsabilidades específicas")
    compensation_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Información de compensación")
    contract_details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detalles del contrato")
    notes: Optional[str] = Field(None, description="Notas adicionales")

    @validator('relationship_type')
    def validate_relationship_type(cls, v):
        valid_types = [
            "employee", "contractor", "volunteer", "freelance", 
            "consultant", "temporary", "part_time"
        ]
        if v not in valid_types:
            raise ValueError(f"Tipo de relación inválido. Debe ser uno de: {valid_types}")
        return v

    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["active", "inactive", "suspended", "terminated", "pending"]
        if v not in valid_statuses:
            raise ValueError(f"Estado inválido. Debe ser uno de: {valid_statuses}")
        return v

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and v <= values['start_date']:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return v


class CaregiverInstitutionCreate(CaregiverInstitutionBase):
    """Esquema para crear una nueva relación cuidador-institución."""
    pass


class CaregiverInstitutionUpdate(BaseModel):
    """Esquema para actualizar una relación cuidador-institución."""
    institution_id: Optional[UUID] = None
    relationship_type: Optional[str] = None
    role_in_institution: Optional[str] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    is_primary_institution: Optional[bool] = None
    working_hours: Optional[Dict[str, Any]] = None
    responsibilities: Optional[Dict[str, Any]] = None
    compensation_info: Optional[Dict[str, Any]] = None
    contract_details: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class CaregiverInstitutionResponse(CaregiverInstitutionBase):
    """Esquema de respuesta para relaciones cuidador-institución."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CaregiverInstitutionSummary(BaseModel):
    """Esquema resumido para relaciones cuidador-institución."""
    id: UUID
    caregiver_id: UUID
    institution_id: Optional[UUID]
    relationship_type: str
    role_in_institution: Optional[str]
    status: str
    is_primary_institution: bool
    start_date: datetime
    end_date: Optional[datetime]
    is_freelance: bool = Field(False, description="Si es una relación freelance")
    
    class Config:
        from_attributes = True


class FreelanceCaregiverInfo(BaseModel):
    """Esquema para información de cuidadores freelance."""
    caregiver_id: UUID
    caregiver_name: str
    caregiver_email: str
    relationship_type: str
    start_date: datetime
    status: str
    working_hours: Optional[Dict[str, Any]]
    responsibilities: Optional[Dict[str, Any]]
    compensation_info: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class InstitutionCaregiverInfo(BaseModel):
    """Esquema para información de cuidadores de una institución."""
    caregiver_id: UUID
    caregiver_name: str
    caregiver_email: str
    relationship_type: str
    role_in_institution: Optional[str]
    start_date: datetime
    status: str
    is_primary_institution: bool
    working_hours: Optional[Dict[str, Any]]
    responsibilities: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class CaregiverInstitutionStats(BaseModel):
    """Esquema para estadísticas de relaciones cuidador-institución."""
    total_relationships: int
    active_relationships: int
    freelance_caregivers: int
    institution_caregivers: int
    primary_institutions: int
    relationship_types: Dict[str, int]
    status_distribution: Dict[str, int] 