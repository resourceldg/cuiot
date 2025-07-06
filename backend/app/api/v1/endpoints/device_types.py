from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.device_type import DeviceType, DeviceTypeCreate, DeviceTypeUpdate
from app.services.device_type import DeviceTypeService

router = APIRouter()

@router.post("/", response_model=DeviceType, status_code=status.HTTP_201_CREATED)
def create_device_type(
    device_type: DeviceTypeCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo tipo de dispositivo"""
    return DeviceTypeService.create_device_type(db=db, device_type=device_type)

@router.get("/", response_model=List[DeviceType])
def get_device_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de tipos de dispositivo"""
    return DeviceTypeService.get_device_types(db=db, skip=skip, limit=limit)

@router.get("/{device_type_id}", response_model=DeviceType)
def get_device_type(
    device_type_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de dispositivo específico"""
    device_type = DeviceTypeService.get_device_type(db=db, device_type_id=device_type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type

@router.put("/{device_type_id}", response_model=DeviceType)
def update_device_type(
    device_type_id: int,
    device_type: DeviceTypeUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un tipo de dispositivo"""
    return DeviceTypeService.update_device_type(db=db, device_type_id=device_type_id, device_type=device_type)

@router.delete("/{device_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_type(
    device_type_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un tipo de dispositivo"""
    DeviceTypeService.delete_device_type(db=db, device_type_id=device_type_id)

@router.post("/initialize-defaults", response_model=List[DeviceType])
def initialize_default_device_types(db: Session = Depends(get_db)):
    """Inicializar tipos de dispositivo por defecto del sistema"""
    return DeviceTypeService.create_default_device_types(db=db) 