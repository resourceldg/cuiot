from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class BillingRecord(BaseModel):
    """BillingRecord model for billing and payment records"""
    __tablename__ = "billing_records"
    
    # Billing identification
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    billing_type = Column(String(50), nullable=False, index=True)  # subscription, service, usage, etc.
    
    # Billing details
    description = Column(Text, nullable=True)
    amount = Column(Integer, nullable=False)  # Amount in cents
    currency = Column(String(3), default="USD", nullable=False)
    tax_amount = Column(Integer, default=0, nullable=False)
    total_amount = Column(Integer, nullable=False)  # Total including tax
    
    # Billing period
    billing_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    paid_date = Column(Date, nullable=True)
    
    # Payment status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    payment_method = Column(String(50), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True)
    service_subscription_id = Column(Integer, ForeignKey("service_subscriptions.id"), nullable=True)
    user_package_id = Column(UUID(as_uuid=True), ForeignKey("user_packages.id", ondelete="CASCADE"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="billing_records")
    institution = relationship("Institution", back_populates="billing_records")
    service_subscription = relationship("ServiceSubscription", back_populates="billing_records")
    user_package = relationship("UserPackage", back_populates="billing_records")
    status_type = relationship("StatusType")
    
    def __repr__(self):
        return f"<BillingRecord(invoice='{self.invoice_number}', amount={self.total_amount}, status='{self.status}')>"
    
    @property
    def is_paid(self) -> bool:
        """Check if billing record is paid"""
        return self.status_type and self.status_type.name == "paid"
    
    @property
    def is_overdue(self) -> bool:
        """Check if billing record is overdue"""
        from datetime import date
        today = date.today()
        return self.status_type and self.status_type.name == "pending" and self.due_date and self.due_date < today
    
    @classmethod
    def get_billing_types(cls) -> list:
        """Returns available billing types"""
        return ["subscription", "service", "usage", "setup", "maintenance", "consultation"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["pending", "paid", "overdue", "cancelled", "refunded", "disputed"]
