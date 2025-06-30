from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class CaregiverInstitution(BaseModel):
    """CaregiverInstitution model for freelance caregivers with multiple institutions"""
    __tablename__ = "caregiver_institutions"
    
    # Relationship info
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    
    # Contract details
    contract_type = Column(String(50), nullable=False)  # employee, contractor, volunteer, intern
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # None for ongoing contracts
    
    # Work details
    position = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    work_schedule = Column(Text, nullable=True)  # JSON string with schedule
    
    # Compensation
    hourly_rate = Column(Integer, nullable=True)  # Rate in cents
    salary = Column(Integer, nullable=True)  # Monthly salary in cents
    benefits = Column(Text, nullable=True)  # JSON string with benefits
    
    # Status
    status = Column(String(50), default="active", nullable=False)  # active, inactive, suspended, terminated
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary institution for the caregiver
    
    # Admin info
    hired_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    hired_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    caregiver = relationship("User", foreign_keys=[caregiver_id], back_populates="caregiver_institutions")
    institution = relationship("Institution", back_populates="caregiver_institutions")
    hired_by_user = relationship("User", foreign_keys=[hired_by])
    
    def __repr__(self):
        return f"<CaregiverInstitution(caregiver_id={self.caregiver_id}, institution_id={self.institution_id})>"
    
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
    
    @classmethod
    def get_contract_types(cls) -> list:
        """Returns available contract types"""
        return ["employee", "contractor", "volunteer", "intern", "consultant", "temporary"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "inactive", "suspended", "terminated", "pending", "on_leave"]
