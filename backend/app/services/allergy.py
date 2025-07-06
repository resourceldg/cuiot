from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.allergy import Allergy
from app.schemas.allergy import AllergyCreate, AllergyUpdate

class AllergyService:
    @staticmethod
    def create(db: Session, allergy: AllergyCreate) -> Allergy:
        db_allergy = Allergy(**allergy.model_dump())
        db.add(db_allergy)
        db.commit()
        db.refresh(db_allergy)
        return db_allergy

    @staticmethod
    def get_by_id(db: Session, allergy_id: UUID) -> Optional[Allergy]:
        return db.query(Allergy).filter(
            Allergy.id == allergy_id,
            Allergy.is_active == True
        ).first()

    @staticmethod
    def get_by_cared_person(db: Session, cared_person_id: UUID) -> List[Allergy]:
        return db.query(Allergy).filter(
            Allergy.cared_person_id == cared_person_id,
            Allergy.is_active == True
        ).all()

    @staticmethod
    def update(db: Session, allergy_id: UUID, allergy: AllergyUpdate) -> Optional[Allergy]:
        db_allergy = AllergyService.get_by_id(db, allergy_id)
        if db_allergy:
            for field, value in allergy.model_dump(exclude_unset=True).items():
                setattr(db_allergy, field, value)
            db.commit()
            db.refresh(db_allergy)
        return db_allergy

    @staticmethod
    def delete(db: Session, allergy_id: UUID) -> bool:
        db_allergy = AllergyService.get_by_id(db, allergy_id)
        if db_allergy:
            db_allergy.is_active = False
            db.commit()
            return True
        return False
