from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ServiceSubscription(BaseModel):
    """ServiceSubscription model for service plans and subscriptions"""
    __tablename__ = "service_subscriptions"
    
    # Subscription identification
    subscription_type = Column(String(50), nullable=False, index=True)  # basic, premium, enterprise, etc.
    service_name = Column(String(100), nullable=False, index=True)
    
    # Subscription details
    description = Column(Text, nullable=True)
    features = Column(Text, nullable=True)  # JSON string with service features
    limitations = Column(Text, nullable=True)  # JSON string with service limitations
    
    # Billing and pricing
    price_per_month = Column(Integer, nullable=True)  # Price in cents
    price_per_year = Column(Integer, nullable=True)  # Price in cents
    currency = Column(String(3), default="USD", nullable=False)
    
    # Subscription period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # None for ongoing subscriptions
    auto_renew = Column(Boolean, default=True, nullable=False)
    
    # Status
    status = Column(String(20), default="active", nullable=False)  # active, suspended, cancelled, expired
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="service_subscriptions")
    institution = relationship("Institution", back_populates="service_subscriptions")
    billing_records = relationship("BillingRecord", back_populates="service_subscription")
    
    def __repr__(self):
        return f"<ServiceSubscription(type='{self.subscription_type}', service='{self.service_name}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is currently active"""
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
    def get_subscription_types(cls) -> list:
        """Returns available subscription types"""
        return ["basic", "premium", "enterprise", "custom", "trial", "free"]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "suspended", "cancelled", "expired", "pending", "trial"]
