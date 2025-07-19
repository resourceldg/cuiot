from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from app.models.service_type import ServiceType

class CaredPersonInstitution(BaseModel):
    """CaredPersonInstitution model for multiple institutions per cared person"""
    __tablename__ = "cared_person_institutions"
    
    # Relationship info
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=False, index=True)
    
    # Service details
    service_type_id = Column(Integer, ForeignKey('service_types.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # None for ongoing services
    
    # Schedule and frequency
    schedule = Column(Text, nullable=True)  # JSON string with schedule details
    frequency = Column(String(50), nullable=True)  # daily, weekly, monthly, on_demand
    duration_hours = Column(Float, nullable=True)  # Hours per session
    
    # Financial info
    cost_per_session = Column(Integer, nullable=True)  # Cost in cents
    payment_frequency = Column(String(50), nullable=True)  # per_session, weekly, monthly
    insurance_coverage = Column(Boolean, default=False, nullable=False)
    insurance_provider = Column(String(100), nullable=True)
    
    # Medical info
    primary_doctor = Column(String(100), nullable=True)
    medical_notes = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    
    # Status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary institution for this person
    
    # Admin info
    registered_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="cared_person_institutions")
    institution = relationship("Institution", back_populates="cared_person_institutions")
    registered_by_user = relationship("User", foreign_keys=[registered_by])
    service_type = relationship("ServiceType")
    status_type = relationship("StatusType")
    
    def __repr__(self):
        return f"<CaredPersonInstitution(cared_person_id={self.cared_person_id}, institution_id={self.institution_id})>"
    
    @property
    def is_active(self) -> bool:
        """Check if relationship is currently active"""
        from datetime import date
        today = date.today()
        
        if self.status != "active":
            return False
        
        if self.start_date > today:
            return False
        
        if self.end_date and self.end_date < today:
            return False
        
        return True
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost for this service"""
        if not self.cost_per_session or not self.duration_hours:
            return 0.0
        
        # This is a simplified calculation - in reality you'd need to consider frequency and duration
        return self.cost_per_session / 100  # Convert from cents
    
    @classmethod
    def get_service_types(cls) -> list:
        """Returns available service types - DEPRECATED: Use ServiceType model instead"""
        return [
            "inpatient", "outpatient", "day_care", "emergency", "consultation",
            "rehabilitation", "therapy", "nursing", "social_work", "nutrition",
            "pharmacy", "laboratory", "imaging", "surgery", "preventive_care"
        ]
    
    @classmethod
    def get_frequency_types(cls) -> list:
        """Returns available frequency types"""
        return ["daily", "weekly", "biweekly", "monthly", "quarterly", "on_demand", "emergency"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "paused", "completed", "terminated", "pending", "suspended"]
