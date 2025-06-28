from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class DeviceConfig(Base):
    """Modelo de configuración de dispositivos"""
    __tablename__ = "device_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)
    config_key = Column(String(100), nullable=False)
    config_value = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    device = relationship("Device", back_populates="configs")
    
    def __repr__(self):
        return f"<DeviceConfig(id={self.id}, key='{self.config_key}', device_id={self.device_id})>" 