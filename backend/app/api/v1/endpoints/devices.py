from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.device import Device, DeviceCreate, DeviceUpdate
from app.services.device import (
    get_devices, get_device_by_id, create_device,
    update_device, delete_device, get_devices_by_elderly_person
)

router = APIRouter()

@router.get("/", response_model=List[Device])
async def get_all_devices(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obtener lista de dispositivos IoT"""
    devices = get_devices(db, skip=skip, limit=limit)
    return devices

@router.get("/elderly/{elderly_person_id}", response_model=List[Device])
async def get_devices_by_elderly_person_id(
    elderly_person_id: UUID, 
    db: Session = Depends(get_db)
):
    """Obtener dispositivos por adulto mayor"""
    devices = get_devices_by_elderly_person(db, elderly_person_id)
    return devices

@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: UUID, db: Session = Depends(get_db)):
    """Obtener dispositivo por ID"""
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )
    return device

@router.post("/", response_model=Device, status_code=status.HTTP_201_CREATED)
async def create_new_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """Crear nuevo dispositivo IoT"""
    try:
        return create_device(db, device)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear dispositivo: {str(e)}"
        )

@router.put("/{device_id}", response_model=Device)
async def update_existing_device(
    device_id: UUID, 
    device_update: DeviceUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar dispositivo existente"""
    device = update_device(db, device_id, device_update)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )
    return device

@router.patch("/{device_id}/activate", response_model=Device)
async def activate_device(device_id: UUID, db: Session = Depends(get_db)):
    """Activar dispositivo"""
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )
    
    device.is_active = True
    db.commit()
    db.refresh(device)
    return device

@router.patch("/{device_id}/deactivate", response_model=Device)
async def deactivate_device(device_id: UUID, db: Session = Depends(get_db)):
    """Desactivar dispositivo"""
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        )
    
    device.is_active = False
    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_device(device_id: UUID, db: Session = Depends(get_db)):
    """Eliminar dispositivo"""
    success = delete_device(db, device_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado"
        ) 