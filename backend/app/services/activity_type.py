from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.activity_type import ActivityType
from app.schemas.activity_type import ActivityTypeCreate, ActivityTypeUpdate

class ActivityTypeService:
    @staticmethod
    def create(db: Session, activity_type: ActivityTypeCreate) -> ActivityType:
        db_activity_type = ActivityType(**activity_type.model_dump())
        db.add(db_activity_type)
        db.commit()
        db.refresh(db_activity_type)
        return db_activity_type

    @staticmethod
    def get_by_id(db: Session, activity_type_id: UUID) -> Optional[ActivityType]:
        return db.query(ActivityType).filter(
            ActivityType.id == activity_type_id,
            ActivityType.is_active == True
        ).first()

    @staticmethod
    def get_all(db: Session) -> List[ActivityType]:
        return db.query(ActivityType).filter(ActivityType.is_active == True).all()

    @staticmethod
    def update(db: Session, activity_type_id: UUID, activity_type: ActivityTypeUpdate) -> Optional[ActivityType]:
        db_activity_type = ActivityTypeService.get_by_id(db, activity_type_id)
        if db_activity_type:
            for field, value in activity_type.model_dump(exclude_unset=True).items():
                setattr(db_activity_type, field, value)
            db.commit()
            db.refresh(db_activity_type)
        return db_activity_type

    @staticmethod
    def delete(db: Session, activity_type_id: UUID) -> bool:
        db_activity_type = ActivityTypeService.get_by_id(db, activity_type_id)
        if db_activity_type:
            db_activity_type.is_active = False
            db.commit()
            return True
        return False
