from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CaregiverScoreBase(BaseModel):
    """Base schema for caregiver score"""
    overall_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Overall score from 0.0 to 5.0")
    experience_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Experience score from 0.0 to 5.0")
    quality_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Quality score from 0.0 to 5.0")
    reliability_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Reliability score from 0.0 to 5.0")
    availability_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Availability score from 0.0 to 5.0")

class CaregiverScoreCreate(CaregiverScoreBase):
    """Schema for creating a caregiver score"""
    caregiver_id: UUID = Field(..., description="ID of the caregiver")

class CaregiverScoreUpdate(CaregiverScoreBase):
    """Schema for updating a caregiver score"""
    total_reviews: Optional[int] = Field(None, ge=0, description="Total number of reviews")
    total_recommendations: Optional[int] = Field(None, ge=0, description="Total number of recommendations")
    total_services: Optional[int] = Field(None, ge=0, description="Total number of services provided")
    total_hours: Optional[int] = Field(None, ge=0, description="Total hours worked")
    avg_response_time: Optional[int] = Field(None, ge=0, description="Average response time in minutes")
    punctuality_rate: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentage of on-time arrivals")
    completion_rate: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentage of completed services")
    is_identity_verified: Optional[bool] = Field(None, description="Identity verification status")
    is_background_checked: Optional[bool] = Field(None, description="Background check status")
    is_references_verified: Optional[bool] = Field(None, description="References verification status")

class CaregiverScore(CaregiverScoreBase):
    """Schema for caregiver score response"""
    id: UUID
    caregiver_id: UUID
    total_reviews: int = 0
    total_recommendations: int = 0
    total_services: int = 0
    total_hours: int = 0
    avg_response_time: Optional[int] = None
    punctuality_rate: Optional[float] = None
    completion_rate: Optional[float] = None
    is_identity_verified: bool = False
    is_background_checked: bool = False
    is_references_verified: bool = False
    last_calculated: Optional[datetime] = None
    last_review: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CaregiverScoreWithLevel(CaregiverScore):
    """Schema for caregiver score with level information"""
    score_level: str = Field(..., description="Score level: excellent, very_good, good, fair, poor, unrated")
    is_verified: bool = Field(..., description="Whether caregiver is fully verified")
    
    class Config:
        from_attributes = True
