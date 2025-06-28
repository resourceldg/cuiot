from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates
from app.core.database import Base
import uuid
import json

class Event(Base):
    """Modelo de eventos: sensores y calendario"""
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elderly_person_id = Column(UUID(as_uuid=True), ForeignKey("elderly_persons.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    title = Column(String(120), nullable=True)
    description = Column(Text, nullable=True)
    event_type = Column(String(50), nullable=False, index=True)  # 'medical', 'family', 'medication', 'sensor', etc.
    value = Column(JSONB, nullable=True)  # Datos del evento (temperatura, etc.)
    location = Column(String(100), nullable=True)
    start_datetime = Column(DateTime(timezone=True), nullable=True)
    end_datetime = Column(DateTime(timezone=True), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    received_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    device = relationship("Device", back_populates="events")
    elderly_person = relationship("ElderlyPerson", backref="events")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="events_created")
    received_by = relationship("User", foreign_keys=[received_by_id], back_populates="events_received")
    
    @validates('value')
    def validate_value_field(self, key, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return {}
        return value
    
    def __repr__(self):
        return f"<Event(id={self.id}, type='{self.event_type}', elderly_person_id={self.elderly_person_id}, device_id={self.device_id})>" 