from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class AlertType(Base):
    __tablename__ = 'alert_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True, index=True)  # health, security, system, etc.
    icon_name = Column(String(50), nullable=True)  # Icon name for UI
    color_code = Column(String(7), nullable=True)  # Hex color for UI (e.g., "#FF0000")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # alerts = relationship('Alert', back_populates='alert_type')

    def __repr__(self):
        return f"<AlertType(id={self.id}, name='{self.name}', category='{self.category}')>" 