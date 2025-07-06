from sqlalchemy.orm import Session
from app.models.care_type import CareType
from app.schemas.care_type import CareTypeCreate, CareTypeUpdate
from typing import List, Optional

class CareTypeService:
    @staticmethod
    def create_care_type(db: Session, care_type: CareTypeCreate) -> CareType:
        db_care_type = CareType(**care_type.model_dump())
        db.add(db_care_type)
        db.commit()
        db.refresh(db_care_type)
        return db_care_type

    @staticmethod
    def get_care_type(db: Session, care_type_id: int) -> Optional[CareType]:
        return db.query(CareType).filter(CareType.id == care_type_id).first()

    @staticmethod
    def get_care_types(db: Session, skip: int = 0, limit: int = 100) -> List[CareType]:
        return db.query(CareType).offset(skip).limit(limit).all()

    @staticmethod
    def update_care_type(db: Session, care_type_id: int, care_type: CareTypeUpdate) -> Optional[CareType]:
        db_care_type = db.query(CareType).filter(CareType.id == care_type_id).first()
        if db_care_type:
            update_data = care_type.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_care_type, field, value)
            db.commit()
            db.refresh(db_care_type)
        return db_care_type

    @staticmethod
    def delete_care_type(db: Session, care_type_id: int) -> bool:
        db_care_type = db.query(CareType).filter(CareType.id == care_type_id).first()
        if db_care_type:
            db.delete(db_care_type)
            db.commit()
            return True
        return False 