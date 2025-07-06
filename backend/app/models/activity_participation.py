from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class ActivityParticipation(BaseModel):
    __tablename__ = "activity_participation"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    participation_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    performance_level = Column(String(50), nullable=True)  # excellent, good, fair, poor
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="activity_participations")
    activity = relationship("Activity", back_populates="participations")
    
    def __repr__(self):
        return f"<ActivityParticipation(id={self.id}, cared_person_id={self.cared_person_id}, activity_id={self.activity_id})>" 