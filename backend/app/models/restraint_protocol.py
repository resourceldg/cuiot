from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Date, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import BaseModel
import uuid

class RestraintProtocol(BaseModel):
    """RestraintProtocol model for safety protocols and incident prevention"""
    __tablename__ = "restraint_protocols"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relationships
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True, index=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Protocol details
    protocol_type = Column(String(50), nullable=False, index=True)  # physical, chemical, environmental, behavioral, other
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    justification = Column(Text, nullable=False)  # Clinical justification required
    risk_assessment = Column(Text, nullable=True)  # Risk assessment details
    
    # Implementation details
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)  # None for ongoing protocols
    review_frequency = Column(String(50), nullable=True)  # daily, weekly, monthly
    next_review_date = Column(DateTime, nullable=True)
    
    # Professional oversight
    responsible_professional = Column(String(200), nullable=False)
    professional_license = Column(String(100), nullable=True)
    supervising_doctor = Column(String(200), nullable=True)
    
    # Status and compliance (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    compliance_status = Column(String(50), default="compliant", nullable=False)  # compliant, non_compliant, under_review
    last_compliance_check = Column(DateTime, nullable=True)
    
    # Documentation
    attached_files = Column(JSONB, default=list, doc="Lista de metadatos de archivos adjuntos")
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="restraint_protocols")
    institution = relationship("Institution", back_populates="restraint_protocols")
    created_by = relationship("User", foreign_keys=[created_by_id])
    updated_by = relationship("User", foreign_keys=[updated_by_id])
    status_type = relationship("StatusType")
    
    def __repr__(self):
        return f"<RestraintProtocol(id={self.id}, type='{self.protocol_type}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if protocol is currently active"""
        from datetime import datetime
        now = datetime.now()
        
        if not self.status_type or self.status_type.name != "active":
            return False
        
        if self.start_date > now:
            return False
        
        if self.end_date and self.end_date < now:
            return False
        
        return True
    
    @property
    def days_active(self) -> int:
        """Calculate days since protocol started"""
        from datetime import datetime
        now = datetime.now()
        if self.start_date > now:
            return 0
        
        end_date = self.end_date or now
        return (end_date - self.start_date).days
    
    @property
    def requires_review(self) -> bool:
        """Check if protocol requires review"""
        if not self.next_review_date:
            return False
        
        from datetime import datetime
        now = datetime.now()
        return now >= self.next_review_date
    
    @classmethod
    def get_protocol_types(cls) -> list:
        """Returns available protocol types"""
        return [
            "physical", "chemical", "environmental", "behavioral", 
            "mechanical", "electronic", "social", "other"
        ]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "suspended", "completed", "terminated", "pending", "under_review"]
    
    @classmethod
    def get_compliance_status_types(cls) -> list:
        """Returns available compliance status types"""
        return ["compliant", "non_compliant", "under_review", "pending_assessment"]
    
    @classmethod
    def get_review_frequency_types(cls) -> list:
        """Returns available review frequency types"""
        return ["daily", "weekly", "biweekly", "monthly", "quarterly", "as_needed"] 