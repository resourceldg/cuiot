from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.caregiver_score import CaregiverScore
from app.models.caregiver_review import CaregiverReview
from app.models.user import User
from app.schemas.caregiver_score import CaregiverScoreCreate, CaregiverScoreUpdate
from app.schemas.caregiver_review import CaregiverReviewSummary
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class CaregiverScoreService:
    """Service for managing caregiver scores"""
    
    @staticmethod
    def create_score(db: Session, score_data: CaregiverScoreCreate) -> CaregiverScore:
        """Create a new caregiver score"""
        db_score = CaregiverScore(**score_data.dict())
        db.add(db_score)
        db.commit()
        db.refresh(db_score)
        return db_score
    
    @staticmethod
    def get_score_by_caregiver_id(db: Session, caregiver_id: UUID) -> Optional[CaregiverScore]:
        """Get caregiver score by caregiver ID"""
        return db.query(CaregiverScore).filter(CaregiverScore.caregiver_id == caregiver_id).first()
    
    @staticmethod
    def update_score(db: Session, caregiver_id: UUID, score_data: CaregiverScoreUpdate) -> Optional[CaregiverScore]:
        """Update caregiver score"""
        db_score = CaregiverScoreService.get_score_by_caregiver_id(db, caregiver_id)
        if not db_score:
            return None
        
        for field, value in score_data.dict(exclude_unset=True).items():
            setattr(db_score, field, value)
        
        db.commit()
        db.refresh(db_score)
        return db_score
    
    @staticmethod
    def calculate_score_from_reviews(db: Session, caregiver_id: UUID) -> Optional[CaregiverScore]:
        """Calculate caregiver score based on reviews"""
        # Get all reviews for the caregiver
        reviews = db.query(CaregiverReview).filter(
            CaregiverReview.caregiver_id == caregiver_id,
            CaregiverReview.is_verified == True
        ).all()
        
        if not reviews:
            return None
        
        # Calculate statistics
        total_reviews = len(reviews)
        total_recommendations = sum(1 for review in reviews if review.is_recommended)
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / total_reviews
        
        # Calculate category averages
        category_totals = {}
        category_counts = {}
        
        for review in reviews:
            if review.categories:
                for category, rating in review.categories.items():
                    if category not in category_totals:
                        category_totals[category] = 0
                        category_counts[category] = 0
                    category_totals[category] += rating
                    category_counts[category] += 1
        
        category_averages = {}
        for category in category_totals:
            category_averages[category] = category_totals[category] / category_counts[category]
        
        # Calculate component scores
        experience_score = CaregiverScoreService._calculate_experience_score(db, caregiver_id)
        quality_score = average_rating
        reliability_score = CaregiverScoreService._calculate_reliability_score(db, caregiver_id)
        availability_score = CaregiverScoreService._calculate_availability_score(db, caregiver_id)
        
        # Get or create score record
        db_score = CaregiverScoreService.get_score_by_caregiver_id(db, caregiver_id)
        if not db_score:
            db_score = CaregiverScore(caregiver_id=caregiver_id)
            db.add(db_score)
        
        # Update score data
        db_score.overall_score = CaregiverScoreService._calculate_overall_score(
            experience_score, quality_score, reliability_score, availability_score
        )
        db_score.experience_score = experience_score
        db_score.quality_score = quality_score
        db_score.reliability_score = reliability_score
        db_score.availability_score = availability_score
        db_score.total_reviews = total_reviews
        db_score.total_recommendations = total_recommendations
        
        db.commit()
        db.refresh(db_score)
        return db_score
    
    @staticmethod
    def _calculate_experience_score(db: Session, caregiver_id: UUID) -> float:
        """Calculate experience score based on years of experience and certifications"""
        caregiver = db.query(User).filter(User.id == caregiver_id).first()
        if not caregiver:
            return 0.0
        
        score = 0.0
        
        # Years of experience (max 4 points)
        if caregiver.experience_years:
            if caregiver.experience_years >= 10:
                score += 4.0
            elif caregiver.experience_years >= 6:
                score += 3.0
            elif caregiver.experience_years >= 3:
                score += 2.0
            else:
                score += 1.0
        
        # Professional license (+0.5)
        if caregiver.professional_license:
            score += 0.5
        
        # Specialization (+0.3)
        if caregiver.specialization:
            score += 0.3
        
        return min(5.0, score)
    
    @staticmethod
    def _calculate_reliability_score(db: Session, caregiver_id: UUID) -> float:
        """Calculate reliability score based on verification status and consistency"""
        db_score = CaregiverScoreService.get_score_by_caregiver_id(db, caregiver_id)
        if not db_score:
            return 0.0
        
        score = 0.0
        
        # Verification status
        if db_score.is_identity_verified:
            score += 1.0
        if db_score.is_background_checked:
            score += 1.0
        if db_score.is_references_verified:
            score += 1.0
        
        # Completion rate
        if db_score.completion_rate:
            score += (db_score.completion_rate / 100) * 2.0
        
        return min(5.0, score)
    
    @staticmethod
    def _calculate_availability_score(db: Session, caregiver_id: UUID) -> float:
        """Calculate availability score based on response time and punctuality"""
        db_score = CaregiverScoreService.get_score_by_caregiver_id(db, caregiver_id)
        if not db_score:
            return 0.0
        
        score = 0.0
        
        # Response time (max 2.5 points)
        if db_score.avg_response_time:
            if db_score.avg_response_time <= 30:  # 30 minutes
                score += 2.5
            elif db_score.avg_response_time <= 60:  # 1 hour
                score += 2.0
            elif db_score.avg_response_time <= 120:  # 2 hours
                score += 1.5
            else:
                score += 1.0
        
        # Punctuality rate (max 2.5 points)
        if db_score.punctuality_rate:
            score += (db_score.punctuality_rate / 100) * 2.5
        
        return min(5.0, score)
    
    @staticmethod
    def _calculate_overall_score(experience: float, quality: float, reliability: float, availability: float) -> float:
        """Calculate overall score using weighted formula"""
        overall = (
            experience * 0.4 +
            quality * 0.35 +
            reliability * 0.15 +
            availability * 0.1
        )
        return round(overall, 2)
    
    @staticmethod
    def get_review_summary(db: Session, caregiver_id: UUID) -> Optional[CaregiverReviewSummary]:
        """Get summary of reviews for a caregiver"""
        reviews = db.query(CaregiverReview).filter(
            CaregiverReview.caregiver_id == caregiver_id,
            CaregiverReview.is_verified == True
        ).all()
        
        if not reviews:
            return None
        
        total_reviews = len(reviews)
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / total_reviews
        recommendation_count = sum(1 for review in reviews if review.is_recommended)
        recommendation_rate = (recommendation_count / total_reviews) * 100
        
        # Rating distribution
        rating_distribution = {str(i): 0 for i in range(1, 6)}
        for review in reviews:
            rating_distribution[str(review.rating)] += 1
        
        # Category averages
        category_totals = {}
        category_counts = {}
        
        for review in reviews:
            if review.categories:
                for category, rating in review.categories.items():
                    if category not in category_totals:
                        category_totals[category] = 0
                        category_counts[category] = 0
                    category_totals[category] += rating
                    category_counts[category] += 1
        
        category_averages = {}
        for category in category_totals:
            category_averages[category] = round(category_totals[category] / category_counts[category], 2)
        
        return CaregiverReviewSummary(
            total_reviews=total_reviews,
            average_rating=round(average_rating, 2),
            recommendation_rate=round(recommendation_rate, 1),
            rating_distribution=rating_distribution,
            category_averages=category_averages
        )
    
    @staticmethod
    def get_top_caregivers(db: Session, limit: int = 10, min_reviews: int = 3) -> List[Dict[str, Any]]:
        """Get top rated caregivers"""
        # Get caregivers with minimum reviews and good scores
        top_caregivers = db.query(
            CaregiverScore, User
        ).join(
            User, CaregiverScore.caregiver_id == User.id
        ).filter(
            CaregiverScore.total_reviews >= min_reviews,
            CaregiverScore.overall_score >= 3.5,
            User.is_active == True
        ).order_by(
            CaregiverScore.overall_score.desc()
        ).limit(limit).all()
        
        result = []
        for score, user in top_caregivers:
            result.append({
                "caregiver_id": str(user.id),
                "name": user.full_name,
                "overall_score": score.overall_score,
                "total_reviews": score.total_reviews,
                "recommendation_rate": score.total_recommendations / score.total_reviews * 100 if score.total_reviews > 0 else 0,
                "is_verified": score.is_verified,
                "specialization": user.specialization,
                "experience_years": user.experience_years
            })
        
        return result
