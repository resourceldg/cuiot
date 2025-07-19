from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class DebugEvent(BaseModel):
    """DebugEvent model for testing and debugging purposes"""
    __tablename__ = "debug_events"
    
    # Debug event identification
    event_type = Column(String(50), nullable=False, index=True)  # test_event, debug_event, simulation, etc.
    event_subtype = Column(String(50), nullable=True, index=True)
    severity = Column(String(20), default="info", nullable=False)  # info, warning, error, debug
    
    # Debug data
    event_data = Column(Text, nullable=True)  # JSON string with debug data
    message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    
    # Context
    source = Column(String(100), nullable=True)  # test_suite, manual_test, system_test, etc.
    test_session = Column(String(100), nullable=True)
    environment = Column(String(50), nullable=True)  # development, testing, staging, production
    
    # Timestamps
    event_time = Column(DateTime(timezone=True), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="debug_events")
    cared_person = relationship("CaredPerson", back_populates="debug_events")
    device = relationship("Device", back_populates="debug_events")
    
    def __repr__(self):
        return f"<DebugEvent(type='{self.event_type}', subtype='{self.event_subtype}', severity='{self.severity}')>"
    
    @classmethod
    def get_event_types(cls) -> list:
        """Returns available debug event types"""
        return [
            "test_event", "debug_event", "simulation", "mock_event",
            "system_test", "integration_test", "performance_test", "load_test"
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """Returns available severity levels"""
        return ["debug", "info", "warning", "error", "critical"]
    
    @classmethod
    def get_environments(cls) -> list:
        """Returns available environments"""
        return ["development", "testing", "staging", "production"]
