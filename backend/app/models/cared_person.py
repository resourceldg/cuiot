from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.diagnosis import Diagnosis
import uuid

class CaredPerson(BaseModel):
    """CaredPerson model for people under care (replaces elderly_person)"""
    __tablename__ = "cared_persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
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
    care_type = Column(String(20), nullable=False, default="delegated")  # "self_care" or "delegated"
    care_level = Column(String(50), nullable=True)  # low, medium, high, critical
    special_needs = Column(Text, nullable=True)
    mobility_level = Column(String(50), nullable=True)  # independent, assisted, wheelchair, bedridden
    
    # Location
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Family member or guardian (for delegated care)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)  # Primary institution (legacy)
    
    # Relationships
    user = relationship("User", back_populates="cared_persons")
    institution = relationship("Institution", back_populates="cared_persons")  # Primary institution (legacy)
    caregiver_assignments = relationship("CaregiverAssignment", back_populates="cared_person")
    cared_person_institutions = relationship("CaredPersonInstitution", back_populates="cared_person")
    devices = relationship("Device", back_populates="cared_person")
    events = relationship("Event", back_populates="cared_person")
    alerts = relationship("Alert", back_populates="cared_person")
    reminders = relationship("Reminder", back_populates="cared_person")
    location_tracking = relationship("LocationTracking", back_populates="cared_person")
    geofences = relationship("Geofence", back_populates="cared_person")
    debug_events = relationship("DebugEvent", back_populates="cared_person")
    reports = relationship('Report', back_populates='cared_person', cascade='all, delete-orphan')
    diagnoses = relationship('Diagnosis', back_populates='cared_person', cascade='all, delete-orphan')
    medical_profile = relationship('MedicalProfile', back_populates='cared_person', uselist=False, cascade='all, delete-orphan')
    medication_schedules = relationship('MedicationSchedule', back_populates='cared_person', cascade='all, delete-orphan')
    
    # Scoring relationships
    caregiver_reviews = relationship("CaregiverReview", foreign_keys="[CaregiverReview.cared_person_id]", back_populates="cared_person")
    institution_reviews = relationship("InstitutionReview", foreign_keys="[InstitutionReview.cared_person_id]", back_populates="cared_person")
    
    # New fields
    medical_contact_name = Column(String(100), nullable=True)
    medical_contact_phone = Column(String(20), nullable=True)
    family_contact_name = Column(String(100), nullable=True)
    family_contact_phone = Column(String(20), nullable=True)
    medical_notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<CaredPerson(name='{self.first_name} {self.last_name}', care_type='{self.care_type}')>"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int | None:
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    @property
    def is_self_care(self) -> bool:
        """Check if person is in self-care mode"""
        return self.care_type == "self_care"
    
    @property
    def is_delegated_care(self) -> bool:
        """Check if person is in delegated care mode"""
        return self.care_type == "delegated"
    
    @property
    def can_make_purchases(self) -> bool:
        """Check if person can make purchases (self-care or has legal capacity)"""
        return self.is_self_care or (self.is_delegated_care and self.user_id is not None)
    
    @property
    def legal_representative(self):
        """Get legal representative (user) for delegated care"""
        if self.is_delegated_care:
            return self.user
        return None
    
    @property
    def active_caregivers(self) -> list:
        """Get active caregivers for this person"""
        return [assignment.caregiver for assignment in self.caregiver_assignments if assignment.is_active]
    
    @property
    def primary_caregiver(self):
        """Get primary caregiver for this person"""
        for assignment in self.caregiver_assignments:
            if assignment.is_active and assignment.is_primary:
                return assignment.caregiver
        return None
    
    @property
    def active_institutions(self) -> list:
        """Get active institutions for this person"""
        return [cpi.institution for cpi in self.cared_person_institutions if cpi.is_active]
    
    @property
    def primary_institution(self):
        """Get primary institution for this person"""
        for cpi in self.cared_person_institutions:
            if cpi.is_active and cpi.is_primary:
                return cpi.institution
        return self.institution  # Fallback to legacy field
    
    @property
    def total_care_cost(self) -> float:
        """Calculate total cost of care from all active assignments"""
        total = 0.0
        
        # Add caregiver costs
        for assignment in self.caregiver_assignments:
            if assignment.is_active:
                total += assignment.estimated_total_cost
        
        # Add institution costs
        for cpi in self.cared_person_institutions:
            if cpi.is_active:
                total += cpi.total_cost
        
        return total
    
    @property
    def care_coverage_hours(self) -> float:
        """Calculate total hours of care coverage per week"""
        total_hours = 0.0
        
        for assignment in self.caregiver_assignments:
            if assignment.is_active and assignment.schedule:
                # This would parse the schedule JSON to calculate actual hours
                # For now, we'll use a simplified calculation
                if assignment.assignment_type == "full_time":
                    total_hours += 40
                elif assignment.assignment_type == "part_time":
                    total_hours += 20
                elif assignment.assignment_type == "on_call":
                    total_hours += 10
        
        return total_hours
    
    @property
    def care_team_size(self) -> int:
        """Get number of active caregivers"""
        return len(self.active_caregivers)
    
    @property
    def institution_count(self) -> int:
        """Get number of active institutions"""
        return len(self.active_institutions)
    
    @property
    def has_24h_coverage(self) -> bool:
        """Check if person has 24-hour care coverage"""
        # This would check if there are caregivers covering all hours
        # For now, we'll use a simplified check
        return self.care_coverage_hours >= 168  # 24 * 7 hours per week
    
    @property
    def can_receive_referrals(self) -> bool:
        """Check if person can receive referral commissions"""
        return self.is_self_care or (self.is_delegated_care and self.user_id is not None)
    
    @property
    def referral_code(self) -> str:
        """Generate unique referral code for this person"""
        return f"CP{self.id.hex[:8].upper()}"
