from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class EventType(Base):
    __tablename__ = 'event_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True, index=True)  # sensor_event, system_event, user_action, etc.
    icon_name = Column(String(50), nullable=True)
    color_code = Column(String(7), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # events = relationship('Event', back_populates='event_type')

    def __repr__(self):
        return f"<EventType(id={self.id}, name='{self.name}', category='{self.category}')>" 