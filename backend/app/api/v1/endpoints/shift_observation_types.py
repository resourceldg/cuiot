from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.shift_observation_type import ShiftObservationType, ShiftObservationTypeCreate, ShiftObservationTypeUpdate
from app.services.shift_observation_type import ShiftObservationTypeService

router = APIRouter()

@router.get("/", response_model=List[ShiftObservationType])
def get_shift_observation_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all shift observation types"""
    service = ShiftObservationTypeService(db)
    return service.get_shift_observation_types(skip=skip, limit=limit)

@router.get("/{shift_observation_type_id}", response_model=ShiftObservationType)
def get_shift_observation_type(
    shift_observation_type_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific shift observation type by ID"""
    service = ShiftObservationTypeService(db)
    shift_observation_type = service.get_shift_observation_type(shift_observation_type_id)
    if not shift_observation_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift observation type not found"
        )
    return shift_observation_type

@router.post("/", response_model=ShiftObservationType, status_code=status.HTTP_201_CREATED)
def create_shift_observation_type(
    shift_observation_type: ShiftObservationTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new shift observation type"""
    service = ShiftObservationTypeService(db)
    return service.create_shift_observation_type(shift_observation_type)

@router.put("/{shift_observation_type_id}", response_model=ShiftObservationType)
def update_shift_observation_type(
    shift_observation_type_id: int,
    shift_observation_type: ShiftObservationTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update a shift observation type"""
    service = ShiftObservationTypeService(db)
    updated_shift_observation_type = service.update_shift_observation_type(shift_observation_type_id, shift_observation_type)
    if not updated_shift_observation_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift observation type not found"
        )
    return updated_shift_observation_type

@router.delete("/{shift_observation_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_observation_type(
    shift_observation_type_id: int,
    db: Session = Depends(get_db)
):
    """Delete a shift observation type"""
    service = ShiftObservationTypeService(db)
    success = service.delete_shift_observation_type(shift_observation_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift observation type not found"
        ) 