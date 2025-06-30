from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.models.base import Base
import uuid

class Report(Base):
    __tablename__ = 'reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    report_type = Column(String(50), nullable=False, default='general')
    attached_files = Column(JSONB, default=list)  # List of file metadata dicts
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey('cared_persons.id'), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    is_autocuidado = Column(Boolean, default=False)

    cared_person = relationship('CaredPerson', back_populates='reports')
    created_by = relationship('User') 