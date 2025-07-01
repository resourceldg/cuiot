from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid
from datetime import datetime

class Diagnosis(BaseModel):
    __tablename__ = 'diagnoses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey('cared_persons.id'), nullable=False)
    diagnosis_name = Column(String(255), nullable=False, doc="Nombre estandarizado del diagnóstico")
    description = Column(Text, nullable=True, doc="Descripción clínica detallada")
    severity_level = Column(String(50), nullable=True, doc="Gravedad: leve, moderada, severa")
    diagnosis_date = Column(DateTime, nullable=True, doc="Fecha del diagnóstico")
    doctor_name = Column(String(255), nullable=True, doc="Nombre del profesional que emite el diagnóstico")
    medical_notes = Column(Text, nullable=True, doc="Notas adicionales")
    cie10_code = Column(String(20), nullable=True, doc="Código CIE-10 para interoperabilidad clínica")
    attachments = Column(JSONB, default=list, doc="Lista de metadatos de archivos adjuntos")
    is_active = Column(Boolean, default=True, nullable=False)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    cared_person = relationship('CaredPerson', back_populates='diagnoses')
    created_by = relationship('User', foreign_keys=[created_by_id])
    updated_by = relationship('User', foreign_keys=[updated_by_id])

    def __repr__(self):
        return f"<Diagnosis(id={self.id}, diagnosis_name='{self.diagnosis_name}', cared_person_id={self.cared_person_id})>" 