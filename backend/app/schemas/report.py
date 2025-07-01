from pydantic import BaseModel, Field
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
    report_type: str = Field('general', description="Tipo de reporte clínico o de cuidado. Valores sugeridos: higiene, alimentacion, evacuacion, conducta, estado_animo, incidente, turno, clinico, general, otro.")
    attached_files: List[FileMeta] = Field(default_factory=list, description="Lista de metadatos de archivos adjuntos (filename, url, content_type, size)")
    is_autocuidado: bool = False
    cared_person_id: Optional[int] = None

    @classmethod
    def allowed_report_types(cls) -> list:
        return [
            'higiene', 'alimentacion', 'evacuacion', 'conducta', 'estado_animo',
            'incidente', 'turno', 'clinico', 'general', 'otro'
        ]

    @classmethod
    def validate_report_type(cls, v):
        allowed = cls.allowed_report_types()
        if v not in allowed:
            raise ValueError(f"report_type debe ser uno de: {allowed}")
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

    class Config:
        from_attributes = True 