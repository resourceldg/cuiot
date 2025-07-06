from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Date, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.referral_type import ReferralType
import uuid
from datetime import datetime

class Referral(BaseModel):
    """Referral model for tracking referrals and commissions"""
    __tablename__ = "referrals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Referral info
    referral_code = Column(String(20), nullable=False, unique=True, index=True)
    referrer_type = Column(String(20), nullable=False)  # "caregiver", "institution", "family", "cared_person"
    referrer_id = Column(UUID(as_uuid=True), nullable=False)  # ID of the referrer
    
    # Referred person info
    referred_email = Column(String(100), nullable=False)
    referred_name = Column(String(100), nullable=True)
    referred_phone = Column(String(20), nullable=True)
    
    # Nuevo campo normalizado
    referral_type_id = Column(Integer, ForeignKey('referral_types.id'), nullable=False, index=True)
    
    # Status and tracking (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    registered_at = Column(DateTime, nullable=True)
    converted_at = Column(DateTime, nullable=True)
    expired_at = Column(DateTime, nullable=True)
    
    # Commission tracking
    commission_amount = Column(Float, nullable=True)
    commission_paid = Column(Boolean, default=False)
    commission_paid_at = Column(DateTime, nullable=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    source = Column(String(50), nullable=True)  # "email", "whatsapp", "phone", "in_person"
    
    # Relationships
    commissions = relationship("ReferralCommission", back_populates="referral")
    status_type = relationship("StatusType")
    referral_type = relationship("ReferralType")
    
    def __repr__(self):
        return f"<Referral(code='{self.referral_code}', referrer='{self.referrer_type}:{self.referrer_id}', status='{self.status}')>"
    
    @property
    def is_pending(self) -> bool:
        return self.status_type and self.status_type.name == "pending"
    
    @property
    def is_registered(self) -> bool:
        return self.status_type and self.status_type.name == "registered"
    
    @property
    def is_converted(self) -> bool:
        return self.status_type and self.status_type.name == "converted"
    
    @property
    def is_expired(self) -> bool:
        return self.status_type and self.status_type.name == "expired"
    
    @property
    def days_since_created(self) -> int:
        """Calculate days since referral was created"""
        now = datetime.now()
        created = self.created_at.replace(tzinfo=None) if self.created_at.tzinfo else self.created_at
        return (now - created).days
    
    @property
    def is_expirable(self) -> bool:
        """Check if referral can expire (30 days)"""
        return self.days_since_created >= 30 and self.status == "pending"
    
    def mark_as_registered(self):
        """Mark referral as registered"""
        # Note: status_type_id should be set via service layer
        self.registered_at = datetime.now()
    
    def mark_as_converted(self, commission_amount: float):
        """Mark referral as converted with commission"""
        # Note: status_type_id should be set via service layer
        self.converted_at = datetime.now()
        self.commission_amount = commission_amount
    
    def mark_as_expired(self):
        """Mark referral as expired"""
        # Note: status_type_id should be set via service layer
        self.expired_at = datetime.now()
    
    def pay_commission(self):
        """Mark commission as paid"""
        self.commission_paid = True
        self.commission_paid_at = datetime.now()

class ReferralCommission(BaseModel):
    """Commission tracking for referrals"""
    __tablename__ = "referral_commissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Commission info
    referral_id = Column(UUID(as_uuid=True), ForeignKey("referrals.id"), nullable=False)
    recipient_type = Column(String(20), nullable=False)  # "caregiver", "institution", "family"
    recipient_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Amount and type
    amount = Column(Float, nullable=False)
    commission_type = Column(String(20), nullable=False)  # "first_month", "recurring", "bonus"
    percentage = Column(Float, nullable=False)  # Commission percentage
    
    # Status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Relationships
    referral = relationship("Referral", back_populates="commissions")
    status_type = relationship("StatusType")
    
    def __repr__(self):
        return f"<ReferralCommission(recipient='{self.recipient_type}:{self.recipient_id}', amount={self.amount}, type='{self.commission_type}')>"
    
    @property
    def is_pending(self) -> bool:
        return self.status_type and self.status_type.name == "pending"
    
    @property
    def is_paid(self) -> bool:
        return self.status_type and self.status_type.name == "paid"
    
    @property
    def is_cancelled(self) -> bool:
        return self.status_type and self.status_type.name == "cancelled"
    
    def mark_as_paid(self):
        """Mark commission as paid"""
        # Note: status_type_id should be set via service layer
        self.paid_at = datetime.now()
    
    def cancel(self):
        """Cancel commission"""
        # Note: status_type_id should be set via service layer 