from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # create, update, delete
    changed_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    old_data = Column(Text, nullable=True)  # JSON string
    new_data = Column(Text, nullable=True)  # JSON string
    description = Column(Text, nullable=True)

    changed_by = relationship('User') 