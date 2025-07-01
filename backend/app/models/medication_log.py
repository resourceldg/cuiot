from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid

class MedicationLog(BaseModel):
    __tablename__ = 'medication_logs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    medication_schedule_id = Column(UUID(as_uuid=True), ForeignKey('medication_schedules.id'), nullable=False)
    taken_at = Column(DateTime(timezone=True), nullable=False)
    confirmed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    confirmation_method = Column(String(50), nullable=True)  # app, caregiver, auto, etc.
    notes = Column(Text, nullable=True)
    attachment = Column(JSONB, nullable=True)  # Evidencia de la toma
    is_missed = Column(Boolean, default=False)
    side_effects = Column(Text, nullable=True)
    effectiveness_rating = Column(String(20), nullable=True)  # excelente, bueno, regular, malo

    medication_schedule = relationship('MedicationSchedule', back_populates='medication_logs')
    confirmed_by_user = relationship('User') 