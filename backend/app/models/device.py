from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Device(Base):
    """Modelo de dispositivo IoT"""
    __tablename__ = "devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elderly_person_id = Column(UUID(as_uuid=True), ForeignKey("elderly_persons.id"), nullable=False)
    device_id = Column(String(100), unique=True, nullable=False, index=True)  # ID único del ESP32
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
    last_heartbeat = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(String(20), default="ready")  # ready, offline, error, off
    type = Column(String(50), default="unknown")  # smart_watch, panic_button, motion_sensor, etc.
    
    # Relaciones
    elderly_person = relationship("ElderlyPerson", back_populates="devices")
    events = relationship("Event", back_populates="device", cascade="all, delete-orphan")
    configs = relationship("DeviceConfig", back_populates="device", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Device(id={self.id}, device_id='{self.device_id}', name='{self.name}')>" 