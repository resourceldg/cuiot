from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.reminder_type import ReminderType, ReminderTypeCreate, ReminderTypeUpdate
from app.services.reminder_type import ReminderTypeService

router = APIRouter()

@router.get("/", response_model=List[ReminderType])
def get_reminder_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all reminder types"""
    service = ReminderTypeService(db)
    return service.get_reminder_types(skip=skip, limit=limit)

@router.get("/{reminder_type_id}", response_model=ReminderType)
def get_reminder_type(
    reminder_type_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific reminder type by ID"""
    service = ReminderTypeService(db)
    reminder_type = service.get_reminder_type(reminder_type_id)
    if not reminder_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder type not found"
        )
    return reminder_type

@router.post("/", response_model=ReminderType, status_code=status.HTTP_201_CREATED)
def create_reminder_type(
    reminder_type: ReminderTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new reminder type"""
    service = ReminderTypeService(db)
    return service.create_reminder_type(reminder_type)

@router.put("/{reminder_type_id}", response_model=ReminderType)
def update_reminder_type(
    reminder_type_id: int,
    reminder_type: ReminderTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update a reminder type"""
    service = ReminderTypeService(db)
    updated_reminder_type = service.update_reminder_type(reminder_type_id, reminder_type)
    if not updated_reminder_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder type not found"
        )
    return updated_reminder_type

@router.delete("/{reminder_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder_type(
    reminder_type_id: int,
    db: Session = Depends(get_db)
):
    """Delete a reminder type"""
    service = ReminderTypeService(db)
    success = service.delete_reminder_type(reminder_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder type not found"
        )

@router.post("/initialize-defaults", response_model=List[ReminderType])
def initialize_default_reminder_types(db: Session = Depends(get_db)):
    """Inicializar tipos de recordatorio por defecto del sistema"""
    return ReminderTypeService.create_default_reminder_types(db=db) 