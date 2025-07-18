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
    cared_persons = relationship("CaredPerson", back_populates="institution")  # Legacy - primary cared persons
    cared_person_institutions = relationship("CaredPersonInstitution", back_populates="institution")
    devices = relationship("Device", back_populates="institution")
    caregiver_institutions = relationship("CaregiverInstitution", back_populates="institution")
    protocols = relationship("EmergencyProtocol", back_populates="institution")
    service_subscriptions = relationship("ServiceSubscription", back_populates="institution")
    billing_records = relationship("BillingRecord", back_populates="institution")
    geofences = relationship("Geofence", back_populates="institution")
    restraint_protocols = relationship("RestraintProtocol", back_populates="institution")
    shift_observations = relationship("ShiftObservation", back_populates="institution")
    institution_packages = relationship("InstitutionPackage", back_populates="institution")
    
    # Scoring relationships
    institution_score = relationship("InstitutionScore", back_populates="institution", uselist=False)
    received_reviews = relationship("InstitutionReview", foreign_keys="[InstitutionReview.institution_id]", back_populates="institution")
    reviews = relationship("InstitutionReview", back_populates="institution")
    
    def __repr__(self):
        return f"<Institution(name='{self.name}', type='{self.institution_type}')>"
    
    @classmethod
    def get_institution_types(cls) -> list:
        return ["hospital", "clinic", "nursing_home", "assisted_living", "home_care", "rehabilitation_center", "hospice", "day_care", "other"]
    
    @property
    def active_cared_persons(self) -> list:
        """Get all active cared persons (both legacy and new relationships)"""
        active_persons = []
        
        # Add from legacy relationship
        for person in self.cared_persons:
            if person.is_active:
                active_persons.append(person)
        
        # Add from new relationship
        for cpi in self.cared_person_institutions:
            if cpi.is_active:
                active_persons.append(cpi.cared_person)
        
        return active_persons
    
    @property
    def active_caregivers(self) -> list:
        """Get active caregivers working with this institution"""
        return [ci.caregiver for ci in self.caregiver_institutions if ci.is_active]
    
    @property
    def total_caredpersons(self) -> int:
        """Get total number of active caredpersons"""
        active_persons = []
        
        # Add from legacy relationship
        for person in self.cared_persons:
            if person.is_active:
                active_persons.append(person)
        
        # Add from new relationship
        for cpi in self.cared_person_institutions:
            if cpi.is_active:
                active_persons.append(cpi.cared_person)
        
        return len(active_persons)
    
    @property
    def total_caregivers(self) -> int:
        """Get total number of active caregivers"""
        return len(self.active_caregivers)
    
    @property
    def average_rating(self) -> float:
        """Get average rating from received reviews"""
        if not self.received_reviews:
            return 0.0
        
        total_rating = sum(review.rating for review in self.received_reviews)
        return round(total_rating / len(self.received_reviews), 2)
    
    @property
    def total_reviews(self) -> int:
        """Get total number of received reviews"""
        return len(self.received_reviews)
    
    @property
    def recommendation_rate(self) -> float:
        """Get percentage of reviews that recommend"""
        if not self.received_reviews:
            return 0.0
        
        recommended = sum(1 for review in self.received_reviews if review.is_recommended)
        return round((recommended / len(self.received_reviews)) * 100, 1)
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy rate based on capacity and active caredpersons"""
        if not self.capacity or self.capacity == 0:
            return 0.0
        
        return round((self.total_caredpersons() / self.capacity) * 100, 1)
