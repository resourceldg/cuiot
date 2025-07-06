from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.reminder_type import ReminderType
from app.schemas.reminder_type import ReminderTypeCreate, ReminderTypeUpdate

class ReminderTypeService:
    def __init__(self, db: Session):
        self.db = db

    def get_reminder_types(self, skip: int = 0, limit: int = 100) -> List[ReminderType]:
        """Get all reminder types with pagination"""
        return self.db.query(ReminderType).offset(skip).limit(limit).all()

    def get_reminder_type(self, reminder_type_id: int) -> Optional[ReminderType]:
        """Get a specific reminder type by ID"""
        return self.db.query(ReminderType).filter(ReminderType.id == reminder_type_id).first()

    def create_reminder_type(self, reminder_type: ReminderTypeCreate) -> ReminderType:
        """Create a new reminder type"""
        db_reminder_type = ReminderType(**reminder_type.dict())
        self.db.add(db_reminder_type)
        self.db.commit()
        self.db.refresh(db_reminder_type)
        return db_reminder_type

    def update_reminder_type(self, reminder_type_id: int, reminder_type: ReminderTypeUpdate) -> Optional[ReminderType]:
        """Update a reminder type"""
        db_reminder_type = self.get_reminder_type(reminder_type_id)
        if not db_reminder_type:
            return None
        
        update_data = reminder_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reminder_type, field, value)
        
        self.db.commit()
        self.db.refresh(db_reminder_type)
        return db_reminder_type

    def delete_reminder_type(self, reminder_type_id: int) -> bool:
        """Delete a reminder type"""
        db_reminder_type = self.get_reminder_type(reminder_type_id)
        if not db_reminder_type:
            return False
        
        self.db.delete(db_reminder_type)
        self.db.commit()
        return True

    def get_active_reminder_types(self) -> List[ReminderType]:
        """Get all active reminder types"""
        return self.db.query(ReminderType).filter(ReminderType.is_active == True).all()

    def get_reminder_types_by_category(self, category: str) -> List[ReminderType]:
        """Get reminder types by category"""
        return self.db.query(ReminderType).filter(ReminderType.category == category).all()

    @staticmethod
    def create_default_reminder_types(db: Session) -> List[ReminderType]:
        defaults = [
            {"name": "medication", "description": "Medication reminder"},
            {"name": "appointment", "description": "Appointment reminder"},
            {"name": "task", "description": "Task reminder"},
            {"name": "exercise", "description": "Exercise reminder"},
            {"name": "meal", "description": "Meal reminder"},
            {"name": "hygiene", "description": "Hygiene reminder"},
            {"name": "social", "description": "Social reminder"},
            {"name": "medical_checkup", "description": "Medical checkup reminder"},
            {"name": "therapy", "description": "Therapy reminder"},
            {"name": "maintenance", "description": "Maintenance reminder"}
        ]
        created = []
        for data in defaults:
            obj = db.query(ReminderType).filter_by(name=data["name"]).first()
            if not obj:
                obj = ReminderType(**data)
                db.add(obj)
                db.flush()
            created.append(obj)
        db.commit()
        return created 