from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate

def get_devices(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
    """Obtener lista de dispositivos IoT"""
    return db.query(Device).offset(skip).limit(limit).all()

def get_device_by_id(db: Session, device_id: UUID) -> Optional[Device]:
    """Obtener dispositivo por ID"""
    return db.query(Device).filter(Device.id == device_id).first()

def get_device_by_device_id(db: Session, device_id: str) -> Optional[Device]:
    """Obtener dispositivo por device_id (ID único del ESP32)"""
    return db.query(Device).filter(Device.device_id == device_id).first()

def get_devices_by_elderly_person(db: Session, elderly_person_id: UUID) -> List[Device]:
    """Obtener dispositivos por adulto mayor"""
    return db.query(Device).filter(Device.elderly_person_id == elderly_person_id).all()

def create_device(db: Session, device: DeviceCreate) -> Device:
    """Crear nuevo dispositivo IoT"""
    db_device = Device(
        elderly_person_id=device.elderly_person_id,
        device_id=device.device_id,
        name=device.name,
        location=device.location,
        is_active=device.is_active
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device_id: UUID, device_update: DeviceUpdate) -> Optional[Device]:
    """Actualizar dispositivo"""
    db_device = get_device_by_id(db, device_id)
    if not db_device:
        return None
    
    update_data = device_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_device, field, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device_heartbeat(db: Session, device_id: str) -> bool:
    """Actualizar heartbeat del dispositivo"""
    db_device = get_device_by_device_id(db, device_id)
    if not db_device:
        return False
    
    db_device.last_heartbeat = datetime.utcnow()
    db.commit()
    return True

def delete_device(db: Session, device_id: UUID) -> bool:
    """Eliminar dispositivo"""
    db_device = get_device_by_id(db, device_id)
    if not db_device:
        return False
    
    db.delete(db_device)
    db.commit()
    return True 