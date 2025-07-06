from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.enumeration_type import EnumerationType
from app.schemas.enumeration_type import EnumerationTypeCreate, EnumerationTypeUpdate

class EnumerationTypeService:
    @staticmethod
    def create(db: Session, enumeration_type: EnumerationTypeCreate) -> EnumerationType:
        db_enumeration_type = EnumerationType(**enumeration_type.model_dump())
        db.add(db_enumeration_type)
        db.commit()
        db.refresh(db_enumeration_type)
        return db_enumeration_type

    @staticmethod
    def get_by_id(db: Session, enumeration_type_id: UUID) -> Optional[EnumerationType]:
        return db.query(EnumerationType).filter(
            EnumerationType.id == enumeration_type_id,
            EnumerationType.is_active == True
        ).first()

    @staticmethod
    def get_all(db: Session) -> List[EnumerationType]:
        return db.query(EnumerationType).filter(EnumerationType.is_active == True).all()

    @staticmethod
    def update(db: Session, enumeration_type_id: UUID, enumeration_type: EnumerationTypeUpdate) -> Optional[EnumerationType]:
        db_enumeration_type = EnumerationTypeService.get_by_id(db, enumeration_type_id)
        if db_enumeration_type:
            for field, value in enumeration_type.model_dump(exclude_unset=True).items():
                setattr(db_enumeration_type, field, value)
            db.commit()
            db.refresh(db_enumeration_type)
        return db_enumeration_type

    @staticmethod
    def delete(db: Session, enumeration_type_id: UUID) -> bool:
        db_enumeration_type = EnumerationTypeService.get_by_id(db, enumeration_type_id)
        if db_enumeration_type:
            db_enumeration_type.is_active = False
            db.commit()
            return True
        return False
