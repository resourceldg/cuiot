from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Time, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Reminder(Base):
    """Modelo de recordatorios"""
    __tablename__ = "reminders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elderly_person_id = Column(UUID(as_uuid=True), ForeignKey("elderly_persons.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    reminder_type = Column(String(50), nullable=False)  # 'medication', 'appointment', 'activity'
    scheduled_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    days_of_week = Column(ARRAY(Integer))  # [1,2,3,4,5,6,7] para días de la semana
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    received_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    elderly_person = relationship("ElderlyPerson", back_populates="reminders")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="reminders_created")
    received_by = relationship("User", foreign_keys=[received_by_id], back_populates="reminders_received")
    
    def __repr__(self):
        return f"<Reminder(id={self.id}, title='{self.title}', type='{self.reminder_type}')>" 