from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.caregiver_score import CaregiverScoreService
from app.services.caregiver_review import CaregiverReviewService
from app.schemas.caregiver_score import (
    CaregiverScore, CaregiverScoreWithLevel, CaregiverScoreCreate, CaregiverScoreUpdate
)
from app.schemas.caregiver_review import (
    CaregiverReview, CaregiverReviewWithDetails, CaregiverReviewCreate, 
    CaregiverReviewUpdate, CaregiverReviewSummary
)
from uuid import UUID

router = APIRouter()

@router.get("/caregivers/{caregiver_id}/score", response_model=CaregiverScoreWithLevel)
def get_caregiver_score(
    caregiver_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get caregiver score by caregiver ID"""
    score = CaregiverScoreService.get_score_by_caregiver_id(db, caregiver_id)
    if not score:
        raise HTTPException(status_code=404, detail="Caregiver score not found")
    
    return score

@router.post("/caregivers/{caregiver_id}/score", response_model=CaregiverScore)
def create_caregiver_score(
    caregiver_id: UUID,
    score_data: CaregiverScoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new caregiver score (admin only)"""
    if not current_user.has_permission("admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if score already exists
    existing_score = CaregiverScoreService.get_score_by_caregiver_id(db, caregiver_id)
    if existing_score:
        raise HTTPException(status_code=400, detail="Caregiver score already exists")
    
    score_data.caregiver_id = caregiver_id
    return CaregiverScoreService.create_score(db, score_data)

@router.put("/caregivers/{caregiver_id}/score", response_model=CaregiverScore)
def update_caregiver_score(
    caregiver_id: UUID,
    score_data: CaregiverScoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update caregiver score (admin only)"""
    if not current_user.has_permission("admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    score = CaregiverScoreService.update_score(db, caregiver_id, score_data)
    if not score:
        raise HTTPException(status_code=404, detail="Caregiver score not found")
    
    return score

@router.post("/caregivers/{caregiver_id}/calculate-score", response_model=CaregiverScore)
def calculate_caregiver_score(
    caregiver_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate caregiver score from reviews"""
    score = CaregiverScoreService.calculate_score_from_reviews(db, caregiver_id)
    if not score:
        raise HTTPException(status_code=404, detail="No reviews found for caregiver")
    
    return score

@router.get("/caregivers/{caregiver_id}/reviews", response_model=List[CaregiverReview])
def get_caregiver_reviews(
    caregiver_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all reviews for a caregiver"""
    reviews = CaregiverReviewService.get_reviews_by_caregiver(db, caregiver_id, skip, limit)
    return reviews

@router.post("/caregivers/{caregiver_id}/reviews", response_model=CaregiverReview)
def create_caregiver_review(
    caregiver_id: UUID,
    review_data: CaregiverReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new review for a caregiver"""
    # Ensure the review is for the specified caregiver
    review_data.caregiver_id = caregiver_id
    
    # Check if user already reviewed this caregiver
    existing_reviews = CaregiverReviewService.get_reviews_by_reviewer(db, current_user.id)
    for review in existing_reviews:
        if review.caregiver_id == caregiver_id:
            raise HTTPException(status_code=400, detail="You have already reviewed this caregiver")
    
    return CaregiverReviewService.create_review(db, review_data, current_user.id)

@router.get("/caregivers/{caregiver_id}/reviews/summary", response_model=CaregiverReviewSummary)
def get_caregiver_review_summary(
    caregiver_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get summary of reviews for a caregiver"""
    summary = CaregiverScoreService.get_review_summary(db, caregiver_id)
    if not summary:
        raise HTTPException(status_code=404, detail="No reviews found for caregiver")
    
    return summary

@router.get("/reviews/{review_id}", response_model=CaregiverReviewWithDetails)
def get_review_details(
    review_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed review information"""
    review_details = CaregiverReviewService.get_review_with_details(db, review_id)
    if not review_details:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review_details

@router.put("/reviews/{review_id}", response_model=CaregiverReview)
def update_review(
    review_id: UUID,
    review_data: CaregiverReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a review (only by the original reviewer or admin)"""
    db_review = CaregiverReviewService.get_review_by_id(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check permissions
    if not (current_user.id == db_review.reviewer_id or current_user.has_permission("admin")):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return CaregiverReviewService.update_review(db, review_id, review_data)

@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a review (only by the original reviewer or admin)"""
    db_review = CaregiverReviewService.get_review_by_id(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check permissions
    if not (current_user.id == db_review.reviewer_id or current_user.has_permission("admin")):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = CaregiverReviewService.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete review")
    
    return {"message": "Review deleted successfully"}

@router.post("/reviews/{review_id}/verify", response_model=CaregiverReview)
def verify_review(
    review_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify a review (admin only)"""
    if not current_user.has_permission("admin"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    review = CaregiverReviewService.verify_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review

@router.get("/reviews/recent", response_model=List[dict])
def get_recent_reviews(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent reviews"""
    return CaregiverReviewService.get_recent_reviews(db, limit)

@router.get("/caregivers/top", response_model=List[dict])
def get_top_caregivers(
    limit: int = Query(10, ge=1, le=100),
    min_reviews: int = Query(3, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get top rated caregivers"""
    return CaregiverScoreService.get_top_caregivers(db, limit, min_reviews)

@router.get("/reviews/search", response_model=List[CaregiverReview])
def search_reviews(
    caregiver_id: Optional[UUID] = Query(None),
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    is_recommended: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search reviews with filters"""
    return CaregiverReviewService.search_reviews(
        db, caregiver_id, min_rating, max_rating, is_recommended, skip, limit
    )
