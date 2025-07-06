from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class ServiceType(Base):
    __tablename__ = 'service_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True, index=True)  # healthcare, caregiving, emergency, etc.
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # cared_person_institutions = relationship('CaredPersonInstitution', back_populates='service_type')
    # caregiver_reviews = relationship('CaregiverReview', back_populates='service_type')
    # institution_reviews = relationship('InstitutionReview', back_populates='service_type')

    def __repr__(self):
        return f"<ServiceType(id={self.id}, name='{self.name}', category='{self.category}')>" 