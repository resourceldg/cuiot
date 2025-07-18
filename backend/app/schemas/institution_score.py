from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID

class InstitutionScoreBase(BaseModel):
    """Base schema for institution score"""
    overall_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Overall score from 0.0 to 5.0")
    service_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Service score from 0.0 to 5.0")
    infrastructure_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Infrastructure score from 0.0 to 5.0")
    compliance_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Compliance score from 0.0 to 5.0")
    reputation_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Reputation score from 0.0 to 5.0")

class InstitutionScoreCreate(InstitutionScoreBase):
    """Schema for creating an institution score"""
    institution_id: int = Field(..., description="ID of the institution")

class InstitutionScoreUpdate(InstitutionScoreBase):
    """Schema for updating an institution score"""
    total_reviews: Optional[int] = Field(None, ge=0, description="Total number of reviews")
    total_recommendations: Optional[int] = Field(None, ge=0, description="Total number of recommendations")
    total_caredpersons: Optional[int] = Field(None, ge=0, description="Total number of caredpersons")
    years_operating: Optional[int] = Field(None, ge=0, description="Years of operation")
    staff_ratio: Optional[float] = Field(None, ge=0.0, description="Staff per caredperson ratio")
    response_time: Optional[int] = Field(None, ge=0, description="Average response time in minutes")
    safety_incidents: Optional[int] = Field(None, ge=0, description="Number of safety incidents")
    satisfaction_rate: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentage of satisfied caredpersons")
    has_medical_license: Optional[bool] = Field(None, description="Medical license status")
    has_safety_certification: Optional[bool] = Field(None, description="Safety certification status")
    has_quality_certification: Optional[bool] = Field(None, description="Quality certification status")
    last_inspection_date: Optional[date] = Field(None, description="Date of last inspection")
    inspection_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Inspection score")

class InstitutionScore(InstitutionScoreBase):
    """Schema for institution score response"""
    id: UUID
    institution_id: int
    total_reviews: int = 0
    total_recommendations: int = 0
    total_caredpersons: int = 0
    years_operating: Optional[int] = None
    staff_ratio: Optional[float] = None
    response_time: Optional[int] = None
    safety_incidents: int = 0
    satisfaction_rate: Optional[float] = None
    has_medical_license: bool = False
    has_safety_certification: bool = False
    has_quality_certification: bool = False
    last_inspection_date: Optional[date] = None
    inspection_score: Optional[float] = None
    last_calculated: Optional[datetime] = None
    last_review: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class InstitutionScoreWithLevel(InstitutionScore):
    """Schema for institution score with level information"""
    score_level: str = Field(..., description="Score level: excellent, very_good, good, fair, poor, unrated")
    is_certified: bool = Field(..., description="Whether institution has all required certifications")
    
    class Config:
        from_attributes = True
