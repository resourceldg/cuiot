from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.medication import Medication
from app.schemas.medication import MedicationCreate, MedicationUpdate

class MedicationService:
    @staticmethod
    def create(db: Session, medication: MedicationCreate) -> Medication:
        db_medication = Medication(**medication.model_dump())
        db.add(db_medication)
        db.commit()
        db.refresh(db_medication)
        return db_medication

    @staticmethod
    def get_by_id(db: Session, medication_id: UUID) -> Optional[Medication]:
        return db.query(Medication).filter(
            Medication.id == medication_id,
            Medication.is_active == True
        ).first()

    @staticmethod
    def get_by_cared_person(db: Session, cared_person_id: UUID) -> List[Medication]:
        return db.query(Medication).filter(
            Medication.cared_person_id == cared_person_id,
            Medication.is_active == True
        ).all()

    @staticmethod
    def update(db: Session, medication_id: UUID, medication: MedicationUpdate) -> Optional[Medication]:
        db_medication = MedicationService.get_by_id(db, medication_id)
        if db_medication:
            for field, value in medication.model_dump(exclude_unset=True).items():
                setattr(db_medication, field, value)
            db.commit()
            db.refresh(db_medication)
        return db_medication

    @staticmethod
    def delete(db: Session, medication_id: UUID) -> bool:
        db_medication = MedicationService.get_by_id(db, medication_id)
        if db_medication:
            db_medication.is_active = False
            db.commit()
            return True
        return False
