from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from uuid import UUID

class CaredPerson(BaseModel):
    """CaredPerson model for people under care (replaces elderly_person)"""
    __tablename__ = "cared_persons"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    identification_number = Column(String(50), nullable=True, unique=True)
    
    # Contact info
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    emergency_contact = Column(String(100), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    
    # Medical info
    medical_conditions = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    blood_type = Column(String(10), nullable=True)
    
    # Care info
    care_level = Column(String(50), nullable=True)  # low, medium, high, critical
    special_needs = Column(Text, nullable=True)
    mobility_level = Column(String(50), nullable=True)  # independent, assisted, wheelchair, bedridden
    
    # Location
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Relationships
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # Family member or guardian
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="cared_persons")
    institution = relationship("Institution", back_populates="cared_persons")
    caregiver_assignments = relationship("CaregiverAssignment", back_populates="cared_person")
    devices = relationship("Device", back_populates="cared_person")
    events = relationship("Event", back_populates="cared_person")
    alerts = relationship("Alert", back_populates="cared_person")
    reminders = relationship("Reminder", back_populates="cared_person")
    location_tracking = relationship("LocationTracking", back_populates="cared_person")
    geofences = relationship("Geofence", back_populates="cared_person")
    debug_events = relationship("DebugEvent", back_populates="cared_person")
    reports = relationship('Report', back_populates='cared_person')
    
    # New fields
    medical_contact_name = Column(String(100), nullable=True)
    medical_contact_phone = Column(String(20), nullable=True)
    family_contact_name = Column(String(100), nullable=True)
    family_contact_phone = Column(String(20), nullable=True)
    medical_notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<CaredPerson(name='{self.first_name} {self.last_name}')>"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
