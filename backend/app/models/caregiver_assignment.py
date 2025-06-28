from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel

class CaregiverAssignment(BaseModel):
    """CaregiverAssignment model for assigning caregivers to cared persons"""
    __tablename__ = "caregiver_assignments"
    
    # Assignment info
    caregiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    cared_person_id = Column(Integer, ForeignKey("cared_persons.id"), nullable=False, index=True)
    
    # Schedule
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # None for ongoing assignments
    schedule = Column(Text, nullable=True)  # JSON string with schedule details
    
    # Assignment details
    assignment_type = Column(String(50), nullable=False)  # full_time, part_time, on_call, emergency
    responsibilities = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Status
    status = Column(String(50), default="active", nullable=False)  # active, paused, completed, terminated
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    caregiver = relationship("User", foreign_keys=[caregiver_id], back_populates="caregiver_assignments")
    cared_person = relationship("CaredPerson", back_populates="caregiver_assignments")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    
    def __repr__(self):
        return f"<CaregiverAssignment(caregiver_id={self.caregiver_id}, cared_person_id={self.cared_person_id})>"
    
    @property
    def is_active(self) -> bool:
        """Check if assignment is currently active"""
        from datetime import date
        today = date.today()
        
        if self.status != "active":
            return False
        
        if self.start_date > today:
            return False
        
        if self.end_date and self.end_date < today:
            return False
        
        return True
    
    @classmethod
    def get_assignment_types(cls) -> list:
        """Returns available assignment types"""
        return ["full_time", "part_time", "on_call", "emergency", "temporary", "permanent"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "paused", "completed", "terminated", "pending"]
