from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate

class ActivityService:
    @staticmethod
    def create(db: Session, activity: ActivityCreate) -> Activity:
        print(f"🔍 Debug: activity.cared_person_id = {getattr(activity, 'cared_person_id', None)} (type: {type(getattr(activity, 'cared_person_id', None))})")
        print(f"🔍 Debug: activity.model_dump() = {activity.model_dump()}")
        db_activity = Activity(**activity.model_dump())
        print(f"🔍 Debug: db_activity.cared_person_id = {db_activity.cared_person_id}")
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

    @staticmethod
    def get_by_id(db: Session, activity_id: UUID) -> Optional[Activity]:
        return db.query(Activity).filter(Activity.id == activity_id, Activity.is_active == True).first()

    @staticmethod
    def get_all(db: Session) -> List[Activity]:
        return db.query(Activity).filter(Activity.is_active == True).all()

    @staticmethod
    def update(db: Session, activity_id: UUID, activity: ActivityUpdate) -> Optional[Activity]:
        db_activity = ActivityService.get_by_id(db, activity_id)
        if db_activity:
            for field, value in activity.model_dump(exclude_unset=True).items():
                setattr(db_activity, field, value)
            db.commit()
            db.refresh(db_activity)
        return db_activity

    @staticmethod
    def delete(db: Session, activity_id: UUID) -> bool:
        db_activity = ActivityService.get_by_id(db, activity_id)
        if db_activity:
            db_activity.is_active = False
            db.commit()
            return True
        return False 