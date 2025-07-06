from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.vital_sign import VitalSign
from app.schemas.vital_sign import VitalSignCreate, VitalSignUpdate

class VitalSignService:
    @staticmethod
    def create(db: Session, vital_sign: VitalSignCreate) -> VitalSign:
        db_vital_sign = VitalSign(**vital_sign.model_dump())
        db.add(db_vital_sign)
        db.commit()
        db.refresh(db_vital_sign)
        return db_vital_sign

    @staticmethod
    def get_by_id(db: Session, vital_sign_id: UUID) -> Optional[VitalSign]:
        return db.query(VitalSign).filter(
            VitalSign.id == vital_sign_id,
            VitalSign.is_active == True
        ).first()

    @staticmethod
    def get_by_shift_observation(db: Session, shift_observation_id: UUID) -> List[VitalSign]:
        return db.query(VitalSign).filter(
            VitalSign.shift_observation_id == shift_observation_id,
            VitalSign.is_active == True
        ).all()

    @staticmethod
    def update(db: Session, vital_sign_id: UUID, vital_sign: VitalSignUpdate) -> Optional[VitalSign]:
        db_vital_sign = VitalSignService.get_by_id(db, vital_sign_id)
        if db_vital_sign:
            for field, value in vital_sign.model_dump(exclude_unset=True).items():
                setattr(db_vital_sign, field, value)
            db.commit()
            db.refresh(db_vital_sign)
        return db_vital_sign

    @staticmethod
    def delete(db: Session, vital_sign_id: UUID) -> bool:
        db_vital_sign = VitalSignService.get_by_id(db, vital_sign_id)
        if db_vital_sign:
            db_vital_sign.is_active = False
            db.commit()
            return True
        return False
