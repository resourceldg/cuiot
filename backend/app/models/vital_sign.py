from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class VitalSign(BaseModel):
    __tablename__ = "vital_signs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shift_observation_id = Column(UUID(as_uuid=True), ForeignKey("shift_observations.id"), nullable=False)
    blood_pressure_systolic = Column(Integer, nullable=True)  # mmHg
    blood_pressure_diastolic = Column(Integer, nullable=True)  # mmHg
    heart_rate = Column(Integer, nullable=True)  # bpm
    temperature = Column(Float, nullable=True)  # Celsius
    oxygen_saturation = Column(Integer, nullable=True)  # percentage
    respiratory_rate = Column(Integer, nullable=True)  # breaths per minute
    weight = Column(Float, nullable=True)  # kg
    height = Column(Float, nullable=True)  # cm
    bmi = Column(Float, nullable=True)  # Body Mass Index
    notes = Column(Text, nullable=True)
    measured_at = Column(DateTime, nullable=False)
    
    # Relationships
    shift_observation = relationship("ShiftObservation")
    
    def __repr__(self):
        return f"<VitalSign(id={self.id}, cared_person_id={self.cared_person_id}, recorded_at={self.recorded_at})>" 