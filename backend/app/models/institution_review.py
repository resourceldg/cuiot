from sqlalchemy import Column, String, Text, Boolean, Integer, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

class InstitutionReview(BaseModel):
    """InstitutionReview model for institution ratings and reviews"""
    __tablename__ = "institution_reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relationships
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True, index=True)
    institution_score_id = Column(UUID(as_uuid=True), ForeignKey("institution_scores.id"), nullable=True, index=True)
    
    # Review details
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    categories = Column(JSONB, nullable=True)  # {"atencion": 5, "limpieza": 4, "personal": 5}
    is_recommended = Column(Boolean, nullable=False)
    
    # Service details
    service_date = Column(Date, nullable=True)
    service_type = Column(String(50), nullable=True)  # inpatient, outpatient, emergency, etc.
    length_of_stay = Column(Integer, nullable=True)  # Days if applicable
    
    # Status
    is_verified = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="received_reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="institution_reviews")
    cared_person = relationship("CaredPerson", back_populates="institution_reviews")
    institution_score = relationship("InstitutionScore", back_populates="reviews")
    
    def __repr__(self):
        return f"<InstitutionReview(institution_id={self.institution_id}, rating={self.rating})>"
    
    @property
    def rating_text(self) -> str:
        """Get rating as text"""
        rating_texts = {
            1: "Muy malo",
            2: "Malo", 
            3: "Regular",
            4: "Bueno",
            5: "Excelente"
        }
        return rating_texts.get(self.rating, "Sin calificar")
    
    @property
    def categories_average(self) -> float:
        """Calculate average of category ratings"""
        if not self.categories:
            return 0.0
        
        values = list(self.categories.values())
        return sum(values) / len(values) if values else 0.0
    
    def get_category_rating(self, category: str) -> int:
        """Get rating for specific category"""
        if not self.categories:
            return 0
        return self.categories.get(category, 0)
    
    @classmethod
    def get_available_categories(cls) -> list:
        """Returns available review categories"""
        return [
            "atencion_medica",
            "limpieza",
            "personal",
            "instalaciones",
            "seguridad",
            "comunicacion",
            "puntualidad",
            "costo_beneficio"
        ]
