from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.event_type import EventType
import uuid

class Event(BaseModel):
    """Event model for sensor events, system events, and user activities"""
    __tablename__ = "events"
    
    # Override id to use UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Event identification
    event_type_id = Column(Integer, ForeignKey('event_types.id'), nullable=False, index=True)
    event_subtype = Column(String(50), nullable=True, index=True)  # motion_detected, temperature_alert, etc.
    severity = Column(String(20), default="info", nullable=False)  # info, warning, error, critical
    
    # Event data
    event_data = Column(Text, nullable=True)  # JSON string with event details
    message = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)  # device_id, system, user, etc.
    
    # Location and context
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    
    # Timestamps
    event_time = Column(DateTime(timezone=True), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="events")
    cared_person = relationship("CaredPerson", back_populates="events")
    device = relationship("Device", back_populates="events")
    alerts = relationship("Alert", back_populates="event")
    event_type = relationship("EventType")
    
    def __repr__(self):
        return f"<Event(type='{self.event_type}', subtype='{self.event_subtype}', severity='{self.severity}')>"
    
    @classmethod
    def get_event_types(cls) -> list:
        """Returns available event types - DEPRECATED: Use EventType model instead"""
        return [
            "sensor_event", "system_event", "user_action", "alert_event",
            "device_event", "location_event", "health_event", "environmental_event",
            "security_event", "maintenance_event", "error_event"
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """Returns available severity levels"""
        return ["info", "warning", "error", "critical", "debug"]
