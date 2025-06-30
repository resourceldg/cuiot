from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid

class Alert(BaseModel):
    """Alert model for notifications and alerts"""
    __tablename__ = "alerts"
    
    # Override id to use UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Alert identification
    alert_type = Column(String(50), nullable=False, index=True)  # health_alert, security_alert, etc.
    alert_subtype = Column(String(50), nullable=True, index=True)  # fall_detected, temperature_high, etc.
    severity = Column(String(20), default="medium", nullable=False)  # low, medium, high, critical
    
    # Alert content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=True)
    alert_data = Column(Text, nullable=True)  # JSON string with alert details
    
    # Alert status
    status = Column(String(20), default="active", nullable=False)  # active, acknowledged, resolved, dismissed
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Priority and escalation
    priority = Column(Integer, default=5, nullable=False)  # 1-10, higher is more important
    escalation_level = Column(Integer, default=0, nullable=False)  # 0-5, escalation steps
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="alerts")
    cared_person = relationship("CaredPerson", back_populates="alerts")
    device = relationship("Device", back_populates="alerts")
    event = relationship("Event", back_populates="alerts")
    
    def __repr__(self):
        return f"<Alert(type='{self.alert_type}', severity='{self.severity}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if alert is currently active"""
        return self.status == "active"
    
    @property
    def is_critical(self) -> bool:
        """Check if alert is critical severity"""
        return self.severity == "critical"
    
    @classmethod
    def get_alert_types(cls) -> list:
        """Returns available alert types"""
        return [
            "health_alert", "security_alert", "environmental_alert", "device_alert",
            "location_alert", "medication_alert", "appointment_alert", "system_alert",
            "emergency_alert", "maintenance_alert"
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """Returns available severity levels"""
        return ["low", "medium", "high", "critical"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "acknowledged", "resolved", "dismissed", "escalated"]
