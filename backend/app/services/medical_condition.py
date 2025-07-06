from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.medical_condition import MedicalCondition
from app.schemas.medical_condition import MedicalConditionCreate, MedicalConditionUpdate

class MedicalConditionService:
    @staticmethod
    def create(db: Session, medical_condition: MedicalConditionCreate) -> MedicalCondition:
        db_medical_condition = MedicalCondition(**medical_condition.model_dump())
        db.add(db_medical_condition)
        db.commit()
        db.refresh(db_medical_condition)
        return db_medical_condition

    @staticmethod
    def get_by_id(db: Session, medical_condition_id: UUID) -> Optional[MedicalCondition]:
        return db.query(MedicalCondition).filter(
            MedicalCondition.id == medical_condition_id,
            MedicalCondition.is_active == True
        ).first()

    @staticmethod
    def get_by_cared_person(db: Session, cared_person_id: UUID) -> List[MedicalCondition]:
        return db.query(MedicalCondition).filter(
            MedicalCondition.cared_person_id == cared_person_id,
            MedicalCondition.is_active == True
        ).all()

    @staticmethod
    def update(db: Session, medical_condition_id: UUID, medical_condition: MedicalConditionUpdate) -> Optional[MedicalCondition]:
        db_medical_condition = MedicalConditionService.get_by_id(db, medical_condition_id)
        if db_medical_condition:
            for field, value in medical_condition.model_dump(exclude_unset=True).items():
                setattr(db_medical_condition, field, value)
            db.commit()
            db.refresh(db_medical_condition)
        return db_medical_condition

    @staticmethod
    def delete(db: Session, medical_condition_id: UUID) -> bool:
        db_medical_condition = MedicalConditionService.get_by_id(db, medical_condition_id)
        if db_medical_condition:
            db_medical_condition.is_active = False
            db.commit()
            return True
        return False 