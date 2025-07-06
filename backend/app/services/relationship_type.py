from sqlalchemy.orm import Session
from app.models.relationship_type import RelationshipType
from app.schemas.relationship_type import RelationshipTypeCreate, RelationshipTypeUpdate
from typing import List, Optional

class RelationshipTypeService:
    @staticmethod
    def create_relationship_type(db: Session, relationship_type: RelationshipTypeCreate) -> RelationshipType:
        db_relationship_type = RelationshipType(**relationship_type.model_dump())
        db.add(db_relationship_type)
        db.commit()
        db.refresh(db_relationship_type)
        return db_relationship_type

    @staticmethod
    def get_relationship_type(db: Session, relationship_type_id: int) -> Optional[RelationshipType]:
        return db.query(RelationshipType).filter(RelationshipType.id == relationship_type_id).first()

    @staticmethod
    def get_relationship_types(db: Session, skip: int = 0, limit: int = 100) -> List[RelationshipType]:
        return db.query(RelationshipType).offset(skip).limit(limit).all()

    @staticmethod
    def update_relationship_type(db: Session, relationship_type_id: int, relationship_type: RelationshipTypeUpdate) -> Optional[RelationshipType]:
        db_relationship_type = db.query(RelationshipType).filter(RelationshipType.id == relationship_type_id).first()
        if db_relationship_type:
            update_data = relationship_type.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_relationship_type, field, value)
            db.commit()
            db.refresh(db_relationship_type)
        return db_relationship_type

    @staticmethod
    def delete_relationship_type(db: Session, relationship_type_id: int) -> bool:
        db_relationship_type = db.query(RelationshipType).filter(RelationshipType.id == relationship_type_id).first()
        if db_relationship_type:
            db.delete(db_relationship_type)
            db.commit()
            return True
        return False 