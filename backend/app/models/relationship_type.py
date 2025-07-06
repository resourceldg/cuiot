from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class RelationshipType(Base):
    __tablename__ = 'relationship_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # caregiver_institutions = relationship('CaregiverInstitution', back_populates='relationship_type')

    def __repr__(self):
        return f"<RelationshipType(id={self.id}, name='{self.name}')>" 