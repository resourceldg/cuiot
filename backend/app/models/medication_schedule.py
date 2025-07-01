from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid

class MedicationSchedule(BaseModel):
    __tablename__ = 'medication_schedules'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey('cared_persons.id'), nullable=False)
    medication_name = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)  # ej: "1 vez/día", "cada 8h"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    instructions = Column(Text, nullable=True)
    prescribed_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    schedule_details = Column(JSONB, nullable=True)  # Horarios específicos, días de la semana, etc.
    side_effects = Column(Text, nullable=True)

    cared_person = relationship('CaredPerson', back_populates='medication_schedules')
    prescribed_by_user = relationship('User')
    medication_logs = relationship('MedicationLog', back_populates='medication_schedule', cascade='all, delete-orphan') 