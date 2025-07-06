from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class AttachmentMeta(BaseModel):
    filename: str
    url: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class DiagnosisBase(BaseModel):
    diagnosis_name: str = Field(..., description="Nombre estandarizado del diagnóstico")
    description: Optional[str] = Field(None, description="Descripción clínica detallada")
    severity_level: Optional[str] = Field(None, description="Gravedad: leve, moderada, severa")
    diagnosis_date: Optional[datetime] = Field(None, description="Fecha del diagnóstico")
    doctor_name: Optional[str] = Field(None, description="Nombre del profesional que emite el diagnóstico")
    medical_notes: Optional[str] = Field(None, description="Notas adicionales")
    cie10_code: Optional[str] = Field(None, description="Código CIE-10 para interoperabilidad clínica")
    attachments: Optional[List[AttachmentMeta]] = Field(default_factory=list, description="Lista de metadatos de archivos adjuntos")
    is_active: bool = True

class DiagnosisCreate(DiagnosisBase):
    cared_person_id: UUID

class DiagnosisUpdate(DiagnosisBase):
    pass

class Diagnosis(DiagnosisBase):
    id: UUID
    cared_person_id: UUID
    created_by_id: UUID
    created_at: datetime
    updated_by_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True) 