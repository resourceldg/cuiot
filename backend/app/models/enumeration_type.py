from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class EnumerationType(BaseModel):
    __tablename__ = "enumeration_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)  # System vs user-defined
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    values = relationship("EnumerationValue", back_populates="enumeration_type", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<EnumerationType(id={self.id}, type_name='{self.type_name}')>" 