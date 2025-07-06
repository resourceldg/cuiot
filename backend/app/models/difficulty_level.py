from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class DifficultyLevel(Base):
    __tablename__ = 'difficulty_levels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    color_code = Column(String(7), nullable=True)  # Hex color for UI (e.g., "#FF0000")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # activities = relationship('Activity', back_populates='difficulty_level')

    def __repr__(self):
        return f"<DifficultyLevel(id={self.id}, name='{self.name}')>" 