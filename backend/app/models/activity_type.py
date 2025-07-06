from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class ActivityType(BaseModel):
    __tablename__ = "activity_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    requirements = Column(JSONB, nullable=True)  # Equipment, skills, etc.
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    activities = relationship("Activity", back_populates="activity_type", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ActivityType(id={self.id}, type_name='{self.type_name}')>" 