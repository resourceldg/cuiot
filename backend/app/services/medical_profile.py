from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.medical_profile import MedicalProfile
from app.schemas.medical_profile import MedicalProfileCreate, MedicalProfileUpdate
from app.core.exceptions import NotFoundException, ValidationException

class MedicalProfileService:
    @staticmethod
    def create(db: Session, medical_profile: MedicalProfileCreate) -> MedicalProfile:
        """Create a new medical profile"""
        db_medical_profile = MedicalProfile(**medical_profile.dict())
        db.add(db_medical_profile)
        db.commit()
        db.refresh(db_medical_profile)
        return db_medical_profile

    @staticmethod
    def get_by_id(db: Session, medical_profile_id: UUID) -> Optional[MedicalProfile]:
        """Get medical profile by ID"""
        return db.query(MedicalProfile).filter(
            and_(
                MedicalProfile.id == medical_profile_id,
                MedicalProfile.is_active == 'active'
            )
        ).first()

    @staticmethod
    def get_by_cared_person_id(db: Session, cared_person_id: UUID) -> Optional[MedicalProfile]:
        """Get medical profile by cared person ID"""
        return db.query(MedicalProfile).filter(
            and_(
                MedicalProfile.cared_person_id == cared_person_id,
                MedicalProfile.is_active == 'active'
            )
        ).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[MedicalProfile]:
        """Get all active medical profiles"""
        return db.query(MedicalProfile).filter(
            MedicalProfile.is_active == 'active'
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, medical_profile_id: UUID, medical_profile: MedicalProfileUpdate) -> MedicalProfile:
        """Update medical profile"""
        db_medical_profile = MedicalProfileService.get_by_id(db, medical_profile_id)
        if not db_medical_profile:
            raise NotFoundException(f"Medical profile with id {medical_profile_id} not found")
        
        update_data = medical_profile.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_medical_profile, field, value)
        
        db.commit()
        db.refresh(db_medical_profile)
        return db_medical_profile

    @staticmethod
    def delete(db: Session, medical_profile_id: UUID) -> bool:
        """Soft delete medical profile"""
        db_medical_profile = MedicalProfileService.get_by_id(db, medical_profile_id)
        if not db_medical_profile:
            raise NotFoundException(f"Medical profile with id {medical_profile_id} not found")
        
        db_medical_profile.is_active = 'inactive'
        db.commit()
        return True 