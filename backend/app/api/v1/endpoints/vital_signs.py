from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.vital_sign import VitalSignService
from app.schemas.vital_sign import VitalSign, VitalSignCreate, VitalSignUpdate

router = APIRouter()

@router.post("/", response_model=VitalSign, status_code=201)
def create_vital_sign(
    vital_sign: VitalSignCreate,
    db: Session = Depends(get_db)
):
    """Create a new vital sign"""
    return VitalSignService.create(db, vital_sign)

@router.get("/{vital_sign_id}", response_model=VitalSign)
def get_vital_sign(
    vital_sign_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a vital sign by ID"""
    vital_sign = VitalSignService.get_by_id(db, vital_sign_id)
    if not vital_sign:
        raise HTTPException(status_code=404, detail="Vital sign not found")
    return vital_sign

@router.get("/shift-observation/{shift_observation_id}", response_model=List[VitalSign])
def get_vital_signs_by_shift_observation(
    shift_observation_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all vital signs for a shift observation"""
    return VitalSignService.get_by_shift_observation(db, shift_observation_id)

@router.put("/{vital_sign_id}", response_model=VitalSign)
def update_vital_sign(
    vital_sign_id: UUID,
    vital_sign: VitalSignUpdate,
    db: Session = Depends(get_db)
):
    """Update a vital sign"""
    updated_vital_sign = VitalSignService.update(db, vital_sign_id, vital_sign)
    if not updated_vital_sign:
        raise HTTPException(status_code=404, detail="Vital sign not found")
    return updated_vital_sign

@router.delete("/{vital_sign_id}")
def delete_vital_sign(
    vital_sign_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a vital sign"""
    success = VitalSignService.delete(db, vital_sign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vital sign not found")
    return {"message": "Vital sign deleted successfully"}
