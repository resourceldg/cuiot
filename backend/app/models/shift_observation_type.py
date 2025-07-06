from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.models.base import Base

class ShiftObservationType(Base):
    __tablename__ = 'shift_observation_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<ShiftObservationType(id={self.id}, name='{self.name}', category='{self.category}')>" 