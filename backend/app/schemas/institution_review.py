from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID

class InstitutionReviewBase(BaseModel):
    """Base schema for institution review"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: Optional[str] = Field(None, max_length=1000, description="Review comment")
    categories: Optional[Dict[str, int]] = Field(None, description="Category ratings")
    is_recommended: bool = Field(..., description="Whether the institution is recommended")

class InstitutionReviewCreate(InstitutionReviewBase):
    """Schema for creating an institution review"""
    institution_id: int = Field(..., description="ID of the institution being reviewed")
    cared_person_id: Optional[UUID] = Field(None, description="ID of the cared person if applicable")
    service_date: Optional[date] = Field(None, description="Date of the service")
    service_type: Optional[str] = Field(None, description="Type of service provided")
    length_of_stay: Optional[int] = Field(None, ge=0, description="Length of stay in days if applicable")

class InstitutionReviewUpdate(BaseModel):
    """Schema for updating an institution review"""
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: Optional[str] = Field(None, max_length=1000, description="Review comment")
    categories: Optional[Dict[str, int]] = Field(None, description="Category ratings")
    is_recommended: Optional[bool] = Field(None, description="Whether the institution is recommended")
    is_public: Optional[bool] = Field(None, description="Whether the review is public")

class InstitutionReview(InstitutionReviewBase):
    """Schema for institution review response"""
    id: UUID
    institution_id: int
    reviewer_id: UUID
    cared_person_id: Optional[UUID] = None
    institution_score_id: Optional[UUID] = None
    service_date: Optional[date] = None
    service_type: Optional[str] = None
    length_of_stay: Optional[int] = None
    is_verified: bool = False
    is_public: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class InstitutionReviewWithDetails(InstitutionReview):
    """Schema for institution review with additional details"""
    rating_text: str = Field(..., description="Rating as text")
    categories_average: float = Field(..., description="Average of category ratings")
    reviewer_name: Optional[str] = Field(None, description="Name of the reviewer")
    institution_name: Optional[str] = Field(None, description="Name of the institution")
    
    class Config:
        from_attributes = True

class InstitutionReviewSummary(BaseModel):
    """Schema for institution review summary"""
    total_reviews: int = Field(..., description="Total number of reviews")
    average_rating: float = Field(..., description="Average rating")
    recommendation_rate: float = Field(..., description="Percentage of recommendations")
    rating_distribution: Dict[str, int] = Field(..., description="Distribution of ratings")
    category_averages: Dict[str, float] = Field(..., description="Average ratings by category")
    
    class Config:
        from_attributes = True
