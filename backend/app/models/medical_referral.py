from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Date, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid
from datetime import datetime

class MedicalReferral(BaseModel):
    """Medical referral model for healthcare referrals"""
    __tablename__ = "medical_referrals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Patient info
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    
    # Referral details
    referral_type = Column(String(50), nullable=False)  # "medical", "specialist", "therapy", "diagnostic"
    referred_by = Column(String(100), nullable=False)  # Doctor name
    referred_to = Column(String(200), nullable=False)  # Hospital/Clinic/Specialist
    reason = Column(Text, nullable=False)  # Reason for referral
    
    # Status and dates
    status = Column(String(20), nullable=False, default="pending")  # pending, scheduled, completed, cancelled
    referral_date = Column(Date, nullable=False, default=datetime.utcnow().date)
    appointment_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    
    # Additional info
    priority = Column(String(20), nullable=True)  # "low", "medium", "high", "urgent"
    notes = Column(Text, nullable=True)
    insurance_info = Column(String(200), nullable=True)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="medical_referrals")
    
    def __repr__(self):
        return f"<MedicalReferral(type='{self.referral_type}', status='{self.status}', patient='{self.cared_person_id}')>"
    
    @property
    def is_pending(self) -> bool:
        return self.status == "pending"
    
    @property
    def is_scheduled(self) -> bool:
        return self.status == "scheduled"
    
    @property
    def is_completed(self) -> bool:
        return self.status == "completed"
    
    @property
    def is_cancelled(self) -> bool:
        return self.status == "cancelled"
    
    @property
    def is_urgent(self) -> bool:
        return self.priority == "urgent"
    
    def schedule_appointment(self, appointment_date: datetime):
        """Schedule the referral appointment"""
        self.status = "scheduled"
        self.appointment_date = appointment_date
    
    def mark_completed(self):
        """Mark referral as completed"""
        self.status = "completed"
        self.completed_date = datetime.utcnow()
    
    def cancel(self):
        """Cancel the referral"""
        self.status = "cancelled" 