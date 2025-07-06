from sqlalchemy.orm import Session
from app.models.alert_type import AlertType
from app.schemas.alert_type import AlertTypeCreate, AlertTypeUpdate
from typing import List

class AlertTypeService:
    @staticmethod
    def create_alert_type(db: Session, alert_type: AlertTypeCreate) -> AlertType:
        """Crear un nuevo tipo de alerta"""
        db_alert_type = AlertType(**alert_type.model_dump())
        db.add(db_alert_type)
        db.commit()
        db.refresh(db_alert_type)
        return db_alert_type

    @staticmethod
    def get_alert_types(db: Session, skip: int = 0, limit: int = 100) -> List[AlertType]:
        """Obtener lista de tipos de alerta"""
        return db.query(AlertType).offset(skip).limit(limit).all()

    @staticmethod
    def get_alert_type(db: Session, alert_type_id: int) -> AlertType:
        """Obtener un tipo de alerta por ID"""
        return db.query(AlertType).filter(AlertType.id == alert_type_id).first()

    @staticmethod
    def update_alert_type(db: Session, alert_type_id: int, alert_type: AlertTypeUpdate) -> AlertType:
        """Actualizar un tipo de alerta"""
        db_alert_type = db.query(AlertType).filter(AlertType.id == alert_type_id).first()
        if db_alert_type:
            for field, value in alert_type.model_dump(exclude_unset=True).items():
                setattr(db_alert_type, field, value)
            db.commit()
            db.refresh(db_alert_type)
        return db_alert_type

    @staticmethod
    def delete_alert_type(db: Session, alert_type_id: int) -> bool:
        """Eliminar un tipo de alerta (soft delete)"""
        db_alert_type = db.query(AlertType).filter(AlertType.id == alert_type_id).first()
        if db_alert_type:
            db_alert_type.is_active = False
            db.commit()
            return True
        return False

    @staticmethod
    def create_default_alert_types(db: Session) -> List[AlertType]:
        defaults = [
            {"name": "health_alert", "description": "Health alert"},
            {"name": "medication_alert", "description": "Medication alert"},
            {"name": "appointment_alert", "description": "Appointment alert"},
            {"name": "security_alert", "description": "Security alert"},
            {"name": "fall_detected", "description": "Fall detected"},
            {"name": "wandering_alert", "description": "Wandering alert"},
            {"name": "environmental_alert", "description": "Environmental alert"},
            {"name": "temperature_alert", "description": "Temperature alert"},
            {"name": "humidity_alert", "description": "Humidity alert"},
            {"name": "device_alert", "description": "Device alert"},
            {"name": "battery_low", "description": "Battery low"},
            {"name": "connection_lost", "description": "Connection lost"},
            {"name": "location_alert", "description": "Location alert"},
            {"name": "geofence_alert", "description": "Geofence alert"},
            {"name": "system_alert", "description": "System alert"},
            {"name": "maintenance_alert", "description": "Maintenance alert"},
            {"name": "emergency_alert", "description": "Emergency alert"},
            {"name": "panic_alert", "description": "Panic alert"},
            {"name": "no_movement", "description": "No movement detected"},
            {"name": "audit_test", "description": "Audit test alert"}
        ]
        created = []
        for data in defaults:
            obj = db.query(AlertType).filter_by(name=data["name"]).first()
            if not obj:
                obj = AlertType(**data)
                db.add(obj)
                db.flush()
            created.append(obj)
        db.commit()
        return created 