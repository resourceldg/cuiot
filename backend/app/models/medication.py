from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class Medication(BaseModel):
    __tablename__ = "medications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    medication_name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=True)
    frequency = Column(String(100), nullable=True)  # daily, twice daily, as needed, etc.
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    prescribed_by = Column(String(255), nullable=True)
    instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="medications")
    
    def __repr__(self):
        return f"<Medication(id={self.id}, medication_name='{self.medication_name}', dosage='{self.dosage}')>" 