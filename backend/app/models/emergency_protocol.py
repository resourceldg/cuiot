from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class EmergencyProtocol(BaseModel):
    """EmergencyProtocol model for emergency procedures and protocols"""
    __tablename__ = "emergency_protocols"
    
    # Protocol identification
    name = Column(String(200), nullable=False, index=True)
    protocol_type = Column(String(50), nullable=False, index=True)  # medical, security, environmental, etc.
    crisis_type = Column(String(50), nullable=False, index=True)  # fall, heart_attack, fire, etc.
    
    # Protocol content
    description = Column(Text, nullable=True)
    steps = Column(Text, nullable=True)  # JSON string with protocol steps
    contacts = Column(Text, nullable=True)  # JSON string with emergency contacts
    
    # Activation criteria
    trigger_conditions = Column(Text, nullable=True)  # JSON string with trigger conditions
    severity_threshold = Column(String(20), default="medium", nullable=False)
    
    # Protocol status
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="protocols")
    
    def __repr__(self):
        return f"<EmergencyProtocol(name='{self.name}', type='{self.protocol_type}', crisis='{self.crisis_type}')>"
    
    @classmethod
    def get_protocol_types(cls) -> list:
        """Returns available protocol types"""
        return [
            "medical", "security", "environmental", "fire", "evacuation",
            "natural_disaster", "technical", "communication", "coordination"
        ]
    
    @classmethod
    def get_crisis_types(cls) -> list:
        """Returns available crisis types"""
        return [
            "fall", "heart_attack", "stroke", "choking", "bleeding",
            "fire", "flood", "earthquake", "power_outage", "intruder",
            "medical_emergency", "environmental_hazard"
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """Returns available severity levels"""
        return ["low", "medium", "high", "critical"]
