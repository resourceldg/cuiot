from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid

class Diagnosis(BaseModel):
    __tablename__ = 'diagnoses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey('cared_persons.id'), nullable=False)
    diagnosis_text = Column(Text, nullable=False)
    diagnosis_type = Column(String(50), nullable=False, default='inicial')
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    attachments = Column(JSONB, default=list)  # List of file metadata dicts
    is_active = Column(String(10), default='active')

    cared_person = relationship('CaredPerson', back_populates='diagnoses')
    created_by = relationship('User') 