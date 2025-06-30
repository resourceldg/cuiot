from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from app.models.device import Device
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new device"""
    try:
        # Create device - exclude user_id from schema data
        data_dict = device_data.dict()
        data_dict.pop('user_id', None)  # Remove user_id if present
        
        device = Device(
            **data_dict,
            user_id=current_user.id
        )
        
        db.add(device)
        db.commit()
        db.refresh(device)
        return device
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create device: {str(e)}"
        )

@router.get("/", response_model=List[DeviceResponse])
def get_devices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get all devices for the current user"""
    devices = db.query(Device).filter(
        Device.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return devices

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get a specific device"""
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: UUID,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update a device"""
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    try:
        for field, value in device_data.dict(exclude_unset=True).items():
            setattr(device, field, value)
        
        db.commit()
        db.refresh(device)
        return device
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update device: {str(e)}"
        )

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Delete a device"""
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    try:
        db.delete(device)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete device: {str(e)}"
        ) 