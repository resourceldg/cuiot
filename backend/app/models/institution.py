from sqlalchemy import Column, String, Text, Boolean, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Institution(BaseModel):
    """Institution model for care centers, clinics, homes, etc."""
    __tablename__ = "institutions"
    
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    institution_type = Column(String(50), nullable=False, index=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    tax_id = Column(String(50), nullable=True)
    license_number = Column(String(50), nullable=True)
    capacity = Column(Integer, nullable=True)
    
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="institution")
    cared_persons = relationship("CaredPerson", back_populates="institution")
    devices = relationship("Device", back_populates="institution")
    caregiver_institutions = relationship("CaregiverInstitution", back_populates="institution")
    protocols = relationship("EmergencyProtocol", back_populates="institution")
    service_subscriptions = relationship("ServiceSubscription", back_populates="institution")
    billing_records = relationship("BillingRecord", back_populates="institution")
    geofences = relationship("Geofence", back_populates="institution")
    
    def __repr__(self):
        return f"<Institution(name='{self.name}', type='{self.institution_type}')>"
    
    @classmethod
    def get_institution_types(cls) -> list:
        return ["hospital", "clinic", "nursing_home", "assisted_living", "home_care", "rehabilitation_center", "hospice", "day_care", "other"]
