from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid


class EnumerationValue(BaseModel):
    __tablename__ = "enumeration_values"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enumeration_type_id = Column(UUID(as_uuid=True), ForeignKey("enumeration_types.id"), nullable=False)
    value_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    enumeration_type = relationship("EnumerationType", back_populates="values")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('enumeration_type_id', 'value_name', name='enumeration_values_type_value_unique'),
    )
    
    def __repr__(self):
        return f"<EnumerationValue(id={self.id}, value_name='{self.value_name}', type_id={self.enumeration_type_id})>" 