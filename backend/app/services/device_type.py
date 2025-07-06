from sqlalchemy.orm import Session
from app.models.device_type import DeviceType
from app.schemas.device_type import DeviceTypeCreate, DeviceTypeUpdate
from typing import List

class DeviceTypeService:
    @staticmethod
    def create_device_type(db: Session, device_type: DeviceTypeCreate) -> DeviceType:
        """Crear un nuevo tipo de dispositivo"""
        db_device_type = DeviceType(**device_type.model_dump())
        db.add(db_device_type)
        db.commit()
        db.refresh(db_device_type)
        return db_device_type

    @staticmethod
    def get_device_types(db: Session, skip: int = 0, limit: int = 100) -> List[DeviceType]:
        """Obtener lista de tipos de dispositivo"""
        return db.query(DeviceType).offset(skip).limit(limit).all()

    @staticmethod
    def get_device_type(db: Session, device_type_id: int) -> DeviceType:
        """Obtener un tipo de dispositivo específico"""
        return db.query(DeviceType).filter(DeviceType.id == device_type_id).first()

    @staticmethod
    def update_device_type(db: Session, device_type_id: int, device_type: DeviceTypeUpdate) -> DeviceType:
        """Actualizar un tipo de dispositivo"""
        db_device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
        if not db_device_type:
            return None
        
        for field, value in device_type.model_dump(exclude_unset=True).items():
            setattr(db_device_type, field, value)
        
        db.commit()
        db.refresh(db_device_type)
        return db_device_type

    @staticmethod
    def delete_device_type(db: Session, device_type_id: int) -> bool:
        """Eliminar un tipo de dispositivo"""
        db_device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
        if not db_device_type:
            return False
        
        db.delete(db_device_type)
        db.commit()
        return True

    @staticmethod
    def create_default_device_types(db: Session) -> List[DeviceType]:
        defaults = [
            {"name": "sensor", "description": "Sensor device"},
            {"name": "tracker", "description": "Tracker device"},
            {"name": "camera", "description": "Camera device"},
            {"name": "smartphone", "description": "Smartphone device"},
            {"name": "tablet", "description": "Tablet device"},
            {"name": "wearable", "description": "Wearable device"},
            {"name": "medical_device", "description": "Medical device"},
            {"name": "environmental_sensor", "description": "Environmental sensor"},
            {"name": "door_sensor", "description": "Door sensor"},
            {"name": "motion_sensor", "description": "Motion sensor"},
            {"name": "temperature_sensor", "description": "Temperature sensor"},
            {"name": "heart_rate_monitor", "description": "Heart rate monitor"},
            {"name": "fall_detector", "description": "Fall detector"},
            {"name": "gps_tracker", "description": "GPS tracker"}
        ]
        created = []
        for data in defaults:
            obj = db.query(DeviceType).filter_by(name=data["name"]).first()
            if not obj:
                obj = DeviceType(**data)
                db.add(obj)
                db.flush()
            created.append(obj)
        db.commit()
        return created 