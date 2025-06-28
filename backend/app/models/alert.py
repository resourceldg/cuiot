from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Alert(Base):
    """Modelo de alertas del sistema"""
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elderly_person_id = Column(UUID(as_uuid=True), ForeignKey("elderly_persons.id"), nullable=False)
    alert_type = Column(String(50), nullable=False, index=True)  # 'no_movement', 'sos', 'temperature', 'medication'
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")  # 'low', 'medium', 'high', 'critical'
    is_resolved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    resolved_at = Column(DateTime(timezone=True))
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    received_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    elderly_person = relationship("ElderlyPerson", back_populates="alerts")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="alerts_created")
    received_by = relationship("User", foreign_keys=[received_by_id], back_populates="alerts_received")
    
    def __repr__(self):
        return f"<Alert(id={self.id}, type='{self.alert_type}', severity='{self.severity}')>" 