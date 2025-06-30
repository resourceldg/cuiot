from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.sql import func
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import get_db
from app.models.user_role import UserRole

class User(BaseModel):
    """User model with roles, institution, and freelance support"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # Authentication
    email = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    
    # Professional info
    professional_license = Column(String(50), nullable=True)
    specialization = Column(String(100), nullable=True)
    experience_years = Column(Integer, nullable=True)
    
    # Freelance info
    is_freelance = Column(Boolean, default=False, nullable=False)
    hourly_rate = Column(Integer, nullable=True)  # Rate in cents
    availability = Column(Text, nullable=True)  # JSON string
    
    # Status
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="users")
    user_roles = relationship("UserRole", foreign_keys="[UserRole.user_id]", back_populates="user", cascade="all, delete-orphan")
    cared_persons = relationship("CaredPerson", back_populates="user")
    caregiver_assignments = relationship("CaregiverAssignment", foreign_keys="[CaregiverAssignment.caregiver_id]", back_populates="caregiver")
    caregiver_institutions = relationship("CaregiverInstitution", foreign_keys="[CaregiverInstitution.caregiver_id]", back_populates="caregiver")
    devices = relationship("Device", back_populates="user")
    events = relationship("Event", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    reminders = relationship("Reminder", foreign_keys="[Reminder.user_id]", back_populates="user")
    service_subscriptions = relationship("ServiceSubscription", back_populates="user")
    billing_records = relationship("BillingRecord", back_populates="user")
    location_tracking = relationship("LocationTracking", back_populates="user")
    geofences = relationship("Geofence", back_populates="user")
    debug_events = relationship("DebugEvent", back_populates="user")
    
    # Scoring relationships
    caregiver_score = relationship("CaregiverScore", back_populates="caregiver", uselist=False)
    received_reviews = relationship("CaregiverReview", foreign_keys="[CaregiverReview.caregiver_id]", back_populates="caregiver")
    given_reviews = relationship("CaregiverReview", foreign_keys="[CaregiverReview.reviewer_id]", back_populates="reviewer")
    institution_reviews = relationship("InstitutionReview", foreign_keys="[InstitutionReview.reviewer_id]", back_populates="reviewer")
    
    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.first_name} {self.last_name}')>"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name or ''}"
    
    @property
    def roles(self) -> list:
        """Get user roles"""
        return [user_role.role for user_role in self.user_roles if user_role.is_active]
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        # Use a more efficient query to avoid lazy loading deadlocks
        db = next(get_db())
        
        # Query user roles with permissions in a single query
        user_with_roles = db.query(User).options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        ).filter(User.id == self.id).first()
        
        if not user_with_roles or not user_with_roles.user_roles:
            return False
        
        for user_role in user_with_roles.user_roles:
            if user_role.is_active and user_role.role and user_role.role.has_permission(permission):
                return True
        
        return False
    
    @property
    def is_caregiver(self) -> bool:
        """Check if user is a caregiver"""
        return self.has_role("caregiver") or self.is_freelance
    
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
