from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid
from datetime import datetime

class MedicalProfile(BaseModel):
    __tablename__ = 'medical_profiles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey('cared_persons.id'), nullable=False, unique=True)
    blood_type = Column(String(10), nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    emergency_info = Column(JSONB, nullable=True)  # Información adicional de emergencia
    medical_preferences = Column(JSONB, nullable=True)  # Preferencias médicas
    insurance_info = Column(JSONB, nullable=True)  # Información de seguro médico
    is_active = Column(Boolean, default=True, nullable=False)

    cared_person = relationship('CaredPerson', back_populates='medical_profile')

    def __repr__(self):
        return f"<MedicalProfile(id={self.id}, cared_person_id={self.cared_person_id})>" 