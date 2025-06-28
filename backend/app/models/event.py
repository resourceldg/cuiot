from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Event(BaseModel):
    """Event model for sensor events, system events, and user activities"""
    __tablename__ = "events"
    
    # Event identification
    event_type = Column(String(50), nullable=False, index=True)  # sensor_event, system_event, user_action, etc.
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cared_person_id = Column(Integer, ForeignKey("cared_persons.id"), nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="events")
    cared_person = relationship("CaredPerson", back_populates="events")
    device = relationship("Device", back_populates="events")
    alerts = relationship("Alert", back_populates="event")
    
    def __repr__(self):
        return f"<Event(type='{self.event_type}', subtype='{self.event_subtype}', severity='{self.severity}')>"
    
    @classmethod
    def get_event_types(cls) -> list:
        """Returns available event types"""
        return [
            "sensor_event", "system_event", "user_action", "alert_event",
            "device_event", "location_event", "health_event", "environmental_event",
            "security_event", "maintenance_event", "error_event"
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """Returns available severity levels"""
        return ["info", "warning", "error", "critical", "debug"]
