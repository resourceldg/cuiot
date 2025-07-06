from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class Allergy(BaseModel):
    __tablename__ = "allergies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    allergen_name = Column(String(255), nullable=False)
    allergy_type = Column(String(100), nullable=True)
    severity = Column(String(50), nullable=True)  # mild, moderate, severe, life-threatening
    reaction_description = Column(Text, nullable=True)
    diagnosis_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    cared_person = relationship("CaredPerson", back_populates="allergies")
    
    def __repr__(self):
        return f"<Allergy(id={self.id}, allergy_name='{self.allergy_name}', severity='{self.severity}')>" 