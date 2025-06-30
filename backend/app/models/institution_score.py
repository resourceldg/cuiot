from sqlalchemy import Column, String, Text, Boolean, Integer, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class InstitutionScore(BaseModel):
    """InstitutionScore model for tracking institution ratings and scores"""
    __tablename__ = "institution_scores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    
    # Overall scores
    overall_score = Column(Float, nullable=True)  # 0.0 to 5.0
    service_score = Column(Float, nullable=True)  # 0.0 to 5.0
    infrastructure_score = Column(Float, nullable=True)  # 0.0 to 5.0
    compliance_score = Column(Float, nullable=True)  # 0.0 to 5.0
    reputation_score = Column(Float, nullable=True)  # 0.0 to 5.0
    
    # Statistics
    total_reviews = Column(Integer, default=0, nullable=False)
    total_recommendations = Column(Integer, default=0, nullable=False)
    total_patients = Column(Integer, default=0, nullable=False)
    years_operating = Column(Integer, nullable=True)
    
    # Quality metrics
    staff_ratio = Column(Float, nullable=True)  # Staff per patient
    response_time = Column(Integer, nullable=True)  # Average response time in minutes
    safety_incidents = Column(Integer, default=0, nullable=False)
    satisfaction_rate = Column(Float, nullable=True)  # Percentage of satisfied patients
    
    # Certifications
    has_medical_license = Column(Boolean, default=False, nullable=False)
    has_safety_certification = Column(Boolean, default=False, nullable=False)
    has_quality_certification = Column(Boolean, default=False, nullable=False)
    last_inspection_date = Column(Date, nullable=True)
    inspection_score = Column(Float, nullable=True)
    
    # Timestamps
    last_calculated = Column(DateTime(timezone=True), nullable=True)
    last_review = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="institution_score")
    reviews = relationship("InstitutionReview", back_populates="institution_score")
    
    def __repr__(self):
        return f"<InstitutionScore(institution_id={self.institution_id}, overall_score={self.overall_score})>"
    
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
    def is_certified(self) -> bool:
        """Check if institution has all required certifications"""
        return (self.has_medical_license and 
                self.has_safety_certification and 
                self.has_quality_certification)
    
    def calculate_overall_score(self) -> float:
        """Calculate overall score based on weighted factors"""
        if not all([self.service_score, self.infrastructure_score, 
                   self.compliance_score, self.reputation_score]):
            return 0.0
        
        # Weighted calculation
        overall = (
            self.service_score * 0.45 +
            self.infrastructure_score * 0.25 +
            self.compliance_score * 0.20 +
            self.reputation_score * 0.10
        )
        
        # Apply certification bonus
        if self.is_certified:
            overall = min(5.0, overall + 0.3)
        
        # Apply inspection bonus
        if self.inspection_score and self.inspection_score >= 4.0:
            overall = min(5.0, overall + 0.2)
        
        return round(overall, 2)
    
    def update_scores(self):
        """Update all scores based on reviews and metrics"""
        # This would be implemented with actual review data
        # For now, this is a placeholder
        pass
