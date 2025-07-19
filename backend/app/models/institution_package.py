from sqlalchemy import Column, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import BaseModel

class InstitutionPackage(BaseModel):
    __tablename__ = "institution_packages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=False)
    package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True)

    institution = relationship("Institution", back_populates="institution_packages")
    package = relationship("Package", back_populates="institution_packages")
    status_type = relationship("StatusType") 