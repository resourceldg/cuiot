from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from app.models.caregiver_assignment_type import CaregiverAssignmentType
from sqlalchemy.dialects.postgresql import UUID

class CaregiverAssignment(BaseModel):
    """CaregiverAssignment model for assigning caregivers to cared persons"""
    __tablename__ = "caregiver_assignments"
    
    # Assignment info
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False, index=True)
    
    # Schedule
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # None for ongoing assignments
    schedule = Column(Text, nullable=True)  # JSON string with schedule details
    
    # Assignment details
    caregiver_assignment_type_id = Column(Integer, ForeignKey('caregiver_assignment_types.id'), nullable=False, index=True)
    responsibilities = Column(Text, nullable=True)
    special_requirements = Column(Text, nullable=True)  # Specific care requirements
    
    # Financial info
    hourly_rate = Column(Integer, nullable=True)  # Rate in cents
    payment_frequency = Column(String(50), nullable=True)  # hourly, daily, weekly, monthly
    is_insured = Column(Boolean, default=False, nullable=False)
    insurance_provider = Column(String(100), nullable=True)
    
    # Performance tracking
    client_rating = Column(Integer, nullable=True)  # Rating given by client/family (1-5)
    client_feedback = Column(Text, nullable=True)
    caregiver_self_rating = Column(Integer, nullable=True)  # Self-assessment (1-5)
    caregiver_notes = Column(Text, nullable=True)
    
    # Medical coordination
    primary_doctor = Column(String(100), nullable=True)
    medical_contact = Column(String(100), nullable=True)
    emergency_protocol = Column(Text, nullable=True)  # Specific emergency procedures
    
    # Status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary caregiver for this person
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    caregiver = relationship("User", foreign_keys=[caregiver_id], back_populates="caregiver_assignments")
    cared_person = relationship("CaredPerson", back_populates="caregiver_assignments")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    status_type = relationship("StatusType")
    caregiver_assignment_type = relationship("CaregiverAssignmentType")
    
    def __repr__(self):
        return f"<CaregiverAssignment(caregiver_id={self.caregiver_id}, cared_person_id={self.cared_person_id})>"
    
    @property
    def is_active(self) -> bool:
        """Check if assignment is currently active"""
        from datetime import date
        today = date.today()
        
        if not self.status_type or self.status_type.name != "active":
            return False
        
        if self.start_date > today:
            return False
        
        if self.end_date and self.end_date < today:
            return False
        
        return True
    
    @property
    def duration_days(self) -> int:
        """Calculate duration of assignment in days"""
        from datetime import date
        if not self.end_date:
            return (date.today() - self.start_date).days
        return (self.end_date - self.start_date).days
    
    @property
    def hourly_rate_decimal(self) -> float:
        """Get hourly rate as decimal"""
        return self.hourly_rate / 100 if self.hourly_rate else 0.0
    
    @property
    def estimated_total_cost(self) -> float:
        """Estimate total cost based on schedule and rate"""
        if not self.hourly_rate or not self.schedule:
            return 0.0
        
        # This is a simplified calculation - in reality you'd parse the schedule JSON
        # and calculate based on actual hours worked
        hours_per_week = 40  # Default assumption
        weeks = self.duration_days / 7 if self.duration_days > 0 else 1
        
        return (self.hourly_rate_decimal * hours_per_week * weeks)
    
    @classmethod
    def get_assignment_types(cls) -> list:
        """Returns available assignment types - DEPRECATED: Use CaregiverAssignmentType model instead"""
        return [
            "full_time", "part_time", "on_call", "emergency", "temporary", 
            "permanent", "weekend_only", "night_shift", "day_shift", "flexible"
        ]
    
    @classmethod
    def get_payment_frequencies(cls) -> list:
        """Returns available payment frequencies"""
        return ["hourly", "daily", "weekly", "biweekly", "monthly", "per_service"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "paused", "completed", "terminated", "pending", "suspended", "on_leave"]
