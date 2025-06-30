from sqlalchemy import Column, String, Text, Boolean, Integer, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CaregiverScore(BaseModel):
    """CaregiverScore model for tracking caregiver ratings and scores"""
    __tablename__ = "caregiver_scores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Overall scores
    overall_score = Column(Float, nullable=True)  # 0.0 to 5.0
    experience_score = Column(Float, nullable=True)  # 0.0 to 5.0
    quality_score = Column(Float, nullable=True)  # 0.0 to 5.0
    reliability_score = Column(Float, nullable=True)  # 0.0 to 5.0
    availability_score = Column(Float, nullable=True)  # 0.0 to 5.0
    
    # Statistics
    total_reviews = Column(Integer, default=0, nullable=False)
    total_recommendations = Column(Integer, default=0, nullable=False)
    total_services = Column(Integer, default=0, nullable=False)
    total_hours = Column(Integer, default=0, nullable=False)  # Total hours worked
    
    # Response metrics
    avg_response_time = Column(Integer, nullable=True)  # Average response time in minutes
    punctuality_rate = Column(Float, nullable=True)  # Percentage of on-time arrivals
    completion_rate = Column(Float, nullable=True)  # Percentage of completed services
    
    # Verification status
    is_identity_verified = Column(Boolean, default=False, nullable=False)
    is_background_checked = Column(Boolean, default=False, nullable=False)
    is_references_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    last_calculated = Column(DateTime(timezone=True), nullable=True)
    last_review = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    caregiver = relationship("User", back_populates="caregiver_score")
    reviews = relationship("CaregiverReview", back_populates="caregiver_score")
    
    def __repr__(self):
        return f"<CaregiverScore(caregiver_id={self.caregiver_id}, overall_score={self.overall_score})>"
    
    @property
    def score_level(self) -> str:
        """Get score level based on overall score"""
        if not self.overall_score:
            return "unrated"
        
        if self.overall_score >= 4.5:
            return "excellent"
        elif self.overall_score >= 3.5:
            return "very_good"
        elif self.overall_score >= 2.5:
            return "good"
        elif self.overall_score >= 1.5:
            return "fair"
        else:
            return "poor"
    
    @property
    def is_verified(self) -> bool:
        """Check if caregiver is fully verified"""
        return (self.is_identity_verified and 
                self.is_background_checked and 
                self.is_references_verified)
    
    def calculate_overall_score(self) -> float:
        """Calculate overall score based on weighted factors"""
        if not all([self.experience_score, self.quality_score, 
                   self.reliability_score, self.availability_score]):
            return 0.0
        
        # Weighted calculation
        overall = (
            self.experience_score * 0.4 +
            self.quality_score * 0.35 +
            self.reliability_score * 0.15 +
            self.availability_score * 0.1
        )
        
        # Apply verification bonus
        if self.is_verified:
            overall = min(5.0, overall + 0.2)
        
        return round(overall, 2)
    
    def update_scores(self):
        """Update all scores based on reviews and metrics"""
        # This would be implemented with actual review data
        # For now, this is a placeholder
        pass
