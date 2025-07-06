from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.difficulty_level import DifficultyLevel
import uuid


class Activity(BaseModel):
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    activity_type_id = Column(UUID(as_uuid=True), ForeignKey("activity_types.id"), nullable=False)
    activity_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    difficulty_level_id = Column(Integer, ForeignKey('difficulty_levels.id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="activities")
    activity_type = relationship("ActivityType", back_populates="activities")
    difficulty_level = relationship("DifficultyLevel")
    participations = relationship("ActivityParticipation", back_populates="activity", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, activity_name='{self.activity_name}')>" 