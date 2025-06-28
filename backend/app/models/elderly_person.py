from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates
from app.core.database import Base
import uuid
import json

class ElderlyPerson(Base):
    """Modelo de adulto mayor"""
    __tablename__ = "elderly_persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer)
    address = Column(Text)
    emergency_contacts = Column(JSONB)  # Array de contactos de emergencia
    medical_conditions = Column(JSONB)  # Array de condiciones médicas
    medications = Column(JSONB)  # Array de medicamentos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="elderly_persons")
    devices = relationship("Device", back_populates="elderly_person", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="elderly_person", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="elderly_person", cascade="all, delete-orphan")
    
    @validates('emergency_contacts', 'medical_conditions', 'medications')
    def validate_jsonb_fields(self, key, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return []
        return value
    
    def __repr__(self):
        return f"<ElderlyPerson(id={self.id}, name='{self.first_name} {self.last_name}')>" 