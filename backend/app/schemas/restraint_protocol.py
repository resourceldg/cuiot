from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from .base import BaseResponse

class FileMeta(BaseModel):
    """Metadata for attached files"""
    filename: str
    url: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None

class RestraintProtocolBase(BaseModel):
    """
    Base para protocolos de sujeción y prevención de incidentes.
    Tipos de protocolo recomendados:
      - physical: Sujeción física (cinturones, chalecos, etc.)
      - chemical: Sujeción química (medicamentos)
      - environmental: Sujeción ambiental (cerraduras, alarmas)
      - behavioral: Protocolos conductuales
      - mechanical: Dispositivos mecánicos
      - electronic: Dispositivos electrónicos
      - social: Protocolos sociales
      - other: Otros tipos
    """
    protocol_type: str = Field(..., description="Tipo de protocolo de sujeción")
    title: str = Field(..., max_length=200, description="Título del protocolo")
    description: Optional[str] = Field(None, description="Descripción detallada del protocolo")
    justification: str = Field(..., description="Justificación clínica requerida")
    risk_assessment: Optional[str] = Field(None, description="Evaluación de riesgos")
    
    # Implementation details
    start_date: datetime = Field(..., description="Fecha de inicio del protocolo")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin (None para protocolos continuos)")
    review_frequency: Optional[str] = Field(None, description="Frecuencia de revisión")
    next_review_date: Optional[datetime] = Field(None, description="Próxima fecha de revisión")
    
    # Professional oversight
    responsible_professional: str = Field(..., max_length=200, description="Profesional responsable")
    professional_license: Optional[str] = Field(None, max_length=100, description="Licencia profesional")
    supervising_doctor: Optional[str] = Field(None, max_length=200, description="Médico supervisor")
    
    # Status and compliance (normalized)
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    compliance_status: str = Field(default="compliant", description="Estado de cumplimiento")
    
    # Documentation
    attached_files: List[FileMeta] = Field(default_factory=list, description="Lista de metadatos de archivos adjuntos")
    notes: Optional[str] = Field(None, description="Notas adicionales")
    
    # Relationships
    cared_person_id: UUID = Field(..., description="ID de la persona bajo cuidado")
    institution_id: Optional[int] = Field(None, description="ID de la institución (opcional)")

    @field_validator('protocol_type')
    def validate_protocol_type(cls, v):
        allowed_types = [
            "physical", "chemical", "environmental", "behavioral", 
            "mechanical", "electronic", "social", "other"
        ]
        if v not in allowed_types:
            raise ValueError(f"protocol_type debe ser uno de: {allowed_types}")
        return v

    @field_validator('status_type_id')
    def validate_status_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID del tipo de estado debe ser un entero positivo")
        return v

    @field_validator('compliance_status')
    def validate_compliance_status(cls, v):
        allowed_compliance = ["compliant", "non_compliant", "under_review", "pending_assessment"]
        if v not in allowed_compliance:
            raise ValueError(f"compliance_status debe ser uno de: {allowed_compliance}")
        return v

    @field_validator('review_frequency')
    def validate_review_frequency(cls, v):
        if v is not None:
            allowed_frequencies = ["daily", "weekly", "biweekly", "monthly", "quarterly", "as_needed"]
            if v not in allowed_frequencies:
                raise ValueError(f"review_frequency debe ser uno de: {allowed_frequencies}")
        return v

class RestraintProtocolCreate(RestraintProtocolBase):
    pass

class RestraintProtocolUpdate(BaseModel):
    """Schema for updating restraint protocols"""
    protocol_type: Optional[str] = None
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    justification: Optional[str] = None
    risk_assessment: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    review_frequency: Optional[str] = None
    next_review_date: Optional[datetime] = None
    responsible_professional: Optional[str] = Field(None, max_length=200)
    professional_license: Optional[str] = Field(None, max_length=100)
    supervising_doctor: Optional[str] = Field(None, max_length=200)
    status_type_id: Optional[int] = None
    compliance_status: Optional[str] = None
    attached_files: Optional[List[FileMeta]] = None
    notes: Optional[str] = None
    institution_id: Optional[int] = None

    @field_validator('protocol_type')
    def validate_protocol_type(cls, v):
        if v is not None:
            allowed_types = [
                "physical", "chemical", "environmental", "behavioral", 
                "mechanical", "electronic", "social", "other"
            ]
            if v not in allowed_types:
                raise ValueError(f"protocol_type debe ser uno de: {allowed_types}")
        return v

    @field_validator('status_type_id')
    def validate_status_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID del tipo de estado debe ser un entero positivo")
        return v

    @field_validator('compliance_status')
    def validate_compliance_status(cls, v):
        if v is not None:
            allowed_compliance = ["compliant", "non_compliant", "under_review", "pending_assessment"]
            if v not in allowed_compliance:
                raise ValueError(f"compliance_status debe ser uno de: {allowed_compliance}")
        return v

    @field_validator('review_frequency')
    def validate_review_frequency(cls, v):
        if v is not None:
            allowed_frequencies = ["daily", "weekly", "biweekly", "monthly", "quarterly", "as_needed"]
            if v not in allowed_frequencies:
                raise ValueError(f"review_frequency debe ser uno de: {allowed_frequencies}")
        return v

class RestraintProtocolResponse(RestraintProtocolBase, BaseResponse):
    """Schema for restraint protocol response"""
    id: UUID
    created_by_id: UUID
    updated_by_id: Optional[UUID] = None
    last_compliance_check: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RestraintProtocolSummary(BaseModel):
    """Schema for restraint protocol summary"""
    total_protocols: int
    active_protocols: int
    protocols_by_type: Dict[str, int]
    protocols_by_status: Dict[str, int]
    protocols_requiring_review: int
    
    class Config:
        from_attributes = True 