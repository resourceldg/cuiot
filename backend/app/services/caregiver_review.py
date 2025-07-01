from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.caregiver_review import CaregiverReview
from app.models.user import User
from app.schemas.caregiver_review import CaregiverReviewCreate, CaregiverReviewUpdate
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class CaregiverReviewService:
    """Service for managing caregiver reviews"""
    
    @staticmethod
    def create_review(db: Session, review_data: CaregiverReviewCreate, reviewer_id: UUID) -> CaregiverReview:
        """Create a new caregiver review"""
        db_review = CaregiverReview(
            **review_data.model_dump(),
            reviewer_id=reviewer_id
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        # Update caregiver score after new review
        from app.services.caregiver_score import CaregiverScoreService
        CaregiverScoreService.calculate_score_from_reviews(db, review_data.caregiver_id)
        
        return db_review
    
    @staticmethod
    def get_review_by_id(db: Session, review_id: UUID) -> Optional[CaregiverReview]:
        """Get review by ID"""
        return db.query(CaregiverReview).filter(CaregiverReview.id == review_id).first()
    
    @staticmethod
    def get_reviews_by_caregiver(db: Session, caregiver_id: UUID, skip: int = 0, limit: int = 100) -> List[CaregiverReview]:
        """Get all reviews for a caregiver"""
        return db.query(CaregiverReview).filter(
            CaregiverReview.caregiver_id == caregiver_id,
            CaregiverReview.is_public == True
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reviews_by_reviewer(db: Session, reviewer_id: UUID, skip: int = 0, limit: int = 100) -> List[CaregiverReview]:
        """Get all reviews by a specific reviewer"""
        return db.query(CaregiverReview).filter(
            CaregiverReview.reviewer_id == reviewer_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_review(db: Session, review_id: UUID, review_data: CaregiverReviewUpdate) -> Optional[CaregiverReview]:
        """Update a review"""
        db_review = CaregiverReviewService.get_review_by_id(db, review_id)
        if not db_review:
            return None
        
        for field, value in review_data.model_dump(exclude_unset=True).items():
            setattr(db_review, field, value)
        
        db.commit()
        db.refresh(db_review)
        
        # Update caregiver score after review update
        from app.services.caregiver_score import CaregiverScoreService
        CaregiverScoreService.calculate_score_from_reviews(db, db_review.caregiver_id)
        
        return db_review
    
    @staticmethod
    def delete_review(db: Session, review_id: UUID) -> bool:
        """Delete a review"""
        db_review = CaregiverReviewService.get_review_by_id(db, review_id)
        if not db_review:
            return False
        
        caregiver_id = db_review.caregiver_id
        db.delete(db_review)
        db.commit()
        
        # Update caregiver score after review deletion
        from app.services.caregiver_score import CaregiverScoreService
        CaregiverScoreService.calculate_score_from_reviews(db, caregiver_id)
        
        return True
    
    @staticmethod
    def verify_review(db: Session, review_id: UUID) -> Optional[CaregiverReview]:
        """Verify a review (admin function)"""
        db_review = CaregiverReviewService.get_review_by_id(db, review_id)
        if not db_review:
            return None
        
        db_review.is_verified = True
        db.commit()
        db.refresh(db_review)
        
        # Update caregiver score after verification
        from app.services.caregiver_score import CaregiverScoreService
        CaregiverScoreService.calculate_score_from_reviews(db, db_review.caregiver_id)
        
        return db_review
    
    @staticmethod
    def get_review_with_details(db: Session, review_id: UUID) -> Optional[Dict[str, Any]]:
        """Get review with additional details"""
        db_review = db.query(CaregiverReview).filter(CaregiverReview.id == review_id).first()
        if not db_review:
            return None
        
        # Get reviewer and caregiver names
        reviewer = db.query(User).filter(User.id == db_review.reviewer_id).first()
        caregiver = db.query(User).filter(User.id == db_review.caregiver_id).first()
        
        return {
            "id": str(db_review.id),
            "rating": db_review.rating,
            "rating_text": db_review.rating_text,
            "comment": db_review.comment,
            "categories": db_review.categories,
            "categories_average": db_review.categories_average,
            "is_recommended": db_review.is_recommended,
            "service_date": db_review.service_date,
            "service_hours": db_review.service_hours,
            "service_type": db_review.service_type,
            "is_verified": db_review.is_verified,
            "is_public": db_review.is_public,
            "created_at": db_review.created_at,
            "reviewer_name": reviewer.full_name if reviewer else None,
            "caregiver_name": caregiver.full_name if caregiver else None
        }
    
    @staticmethod
    def get_recent_reviews(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent reviews with details"""
        recent_reviews = db.query(CaregiverReview).filter(
            CaregiverReview.is_verified == True,
            CaregiverReview.is_public == True
        ).order_by(
            CaregiverReview.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for review in recent_reviews:
            reviewer = db.query(User).filter(User.id == review.reviewer_id).first()
            caregiver = db.query(User).filter(User.id == review.caregiver_id).first()
            
            result.append({
                "id": str(review.id),
                "rating": review.rating,
                "rating_text": review.rating_text,
                "comment": review.comment[:100] + "..." if review.comment and len(review.comment) > 100 else review.comment,
                "is_recommended": review.is_recommended,
                "created_at": review.created_at,
                "reviewer_name": reviewer.full_name if reviewer else None,
                "caregiver_name": caregiver.full_name if caregiver else None
            })
        
        return result
    
    @staticmethod
    def search_reviews(db: Session, 
                      caregiver_id: Optional[UUID] = None,
                      min_rating: Optional[int] = None,
                      max_rating: Optional[int] = None,
                      is_recommended: Optional[bool] = None,
                      skip: int = 0, 
                      limit: int = 100) -> List[CaregiverReview]:
        """Search reviews with filters"""
        query = db.query(CaregiverReview).filter(CaregiverReview.is_verified == True)
        
        if caregiver_id:
            query = query.filter(CaregiverReview.caregiver_id == caregiver_id)
        
        if min_rating:
            query = query.filter(CaregiverReview.rating >= min_rating)
        
        if max_rating:
            query = query.filter(CaregiverReview.rating <= max_rating)
        
        if is_recommended is not None:
            query = query.filter(CaregiverReview.is_recommended == is_recommended)
        
        return query.offset(skip).limit(limit).all()
