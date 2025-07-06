from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class MedicalCondition(BaseModel):
    __tablename__ = "medical_conditions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    condition_name = Column(String(255), nullable=False)
    severity_level = Column(String(50), nullable=True)  # mild, moderate, severe, critical
    diagnosis_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    doctor_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="medical_conditions")
    
    def __repr__(self):
        return f"<MedicalCondition(id={self.id}, condition_name='{self.condition_name}', severity='{self.severity}')>" 