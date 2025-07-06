from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime
from app.schemas.cared_person import CaredPersonResponse
from uuid import UUID
from .base import BaseResponse

class FileMeta(BaseModel):
    filename: str
    url: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None

class ReportBase(BaseModel):
    """
    Base para reportes clínicos y de cuidado.
    Tipos recomendados para report_type:
      - higiene
      - alimentacion
      - evacuacion
      - conducta
      - estado_animo
      - incidente
      - turno
      - clinico
      - general
      - otro
    attached_files debe ser una lista de metadatos de archivos (nombre, url, tipo, tamaño).
    """
    title: str
    description: Optional[str] = None
    report_type_id: Optional[int] = Field(None, description="ID del tipo de reporte (normalizado)")
    attached_files: List[FileMeta] = Field(default_factory=list, description="Lista de metadatos de archivos adjuntos (filename, url, content_type, size)")
    is_autocuidado: bool = False
    cared_person_id: Optional[int] = None

    @field_validator('report_type_id')
    def validate_report_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID del tipo de reporte debe ser un entero positivo")
        return v

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class ReportResponse(BaseResponse):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_id: UUID
    cared_person: Optional[CaredPersonResponse] = None
    report_type: Optional[str] = None  # Nombre del tipo de reporte (opcional, para respuesta)

    class Config:
        from_attributes = True 