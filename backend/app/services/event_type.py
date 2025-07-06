from sqlalchemy.orm import Session
from app.models.event_type import EventType
from app.schemas.event_type import EventTypeCreate, EventTypeUpdate
from typing import List

class EventTypeService:
    @staticmethod
    def get_all_event_types(db: Session) -> List[EventType]:
        """Obtener todos los tipos de evento"""
        return db.query(EventType).all()

    # ... otros métodos ...

    @staticmethod
    def create_default_event_types(db: Session) -> List[EventType]:
        defaults = [
            {"name": "sensor_event", "description": "Sensor event"},
            {"name": "system_event", "description": "System event"},
            {"name": "user_action", "description": "User action event"},
            {"name": "alert_event", "description": "Alert event"},
            {"name": "device_event", "description": "Device event"},
            {"name": "location_event", "description": "Location event"},
            {"name": "health_event", "description": "Health event"},
            {"name": "environmental_event", "description": "Environmental event"},
            {"name": "security_event", "description": "Security event"},
            {"name": "maintenance_event", "description": "Maintenance event"},
            {"name": "error_event", "description": "Error event"}
        ]
        created = []
        for data in defaults:
            obj = db.query(EventType).filter_by(name=data["name"]).first()
            if not obj:
                obj = EventType(**data)
                db.add(obj)
                db.flush()
            created.append(obj)
        db.commit()
        return created 