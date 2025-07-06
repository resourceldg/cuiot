from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List, Any
from datetime import datetime
from uuid import UUID


class CaregiverInstitutionBase(BaseModel):
    """Esquema base para relaciones cuidador-institución."""
    caregiver_id: UUID = Field(..., description="ID del cuidador")
    institution_id: Optional[UUID] = Field(None, description="ID de la institución (None para freelance)")
    relationship_type_id: Optional[int] = Field(None, description="ID del tipo de relación (normalizado)")
    role_in_institution: Optional[str] = Field(None, description="Rol en la institución")
    start_date: datetime = Field(..., description="Fecha de inicio de la relación")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin de la relación")
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    is_primary_institution: bool = Field(default=False, description="Si es la institución principal")
    working_hours: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Horarios de trabajo")
    responsibilities: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Responsabilidades específicas")
    compensation_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Información de compensación")
    contract_details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detalles del contrato")
    notes: Optional[str] = Field(None, description="Notas adicionales")

    @field_validator('relationship_type_id')
    def validate_relationship_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID del tipo de relación debe ser un entero positivo")
        return v

    @field_validator('status_type_id')
    def validate_status_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID del tipo de estado debe ser un entero positivo")
        return v

    @field_validator('end_date')
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
    relationship_type_id: Optional[int] = None
    role_in_institution: Optional[str] = None
    end_date: Optional[datetime] = None
    status_type_id: Optional[int] = None
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
    relationship_type: Optional[str] = None  # Nombre del tipo de relación (opcional, para respuesta)
    
    class Config:
        from_attributes = True


class CaregiverInstitutionSummary(BaseModel):
    """Esquema resumido para relaciones cuidador-institución."""
    id: UUID
    caregiver_id: UUID
    institution_id: Optional[UUID]
    relationship_type: str
    role_in_institution: Optional[str]
    status_type_id: Optional[int]
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
    status_type_id: Optional[int]
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
    status_type_id: Optional[int]
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