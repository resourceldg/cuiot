from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.medical_condition import MedicalConditionService
from app.schemas.medical_condition import MedicalCondition, MedicalConditionCreate, MedicalConditionUpdate

router = APIRouter()

@router.post("/", response_model=MedicalCondition, status_code=201)
def create_medical_condition(
    medical_condition: MedicalConditionCreate,
    db: Session = Depends(get_db)
):
    """Create a new medical condition"""
    return MedicalConditionService.create(db, medical_condition)

@router.get("/{medical_condition_id}", response_model=MedicalCondition)
def get_medical_condition(
    medical_condition_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a medical condition by ID"""
    medical_condition = MedicalConditionService.get_by_id(db, medical_condition_id)
    if not medical_condition:
        raise HTTPException(status_code=404, detail="Medical condition not found")
    return medical_condition

@router.get("/cared-person/{cared_person_id}", response_model=List[MedicalCondition])
def get_medical_conditions_by_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all medical conditions for a cared person"""
    return MedicalConditionService.get_by_cared_person(db, cared_person_id)

@router.put("/{medical_condition_id}", response_model=MedicalCondition)
def update_medical_condition(
    medical_condition_id: UUID,
    medical_condition: MedicalConditionUpdate,
    db: Session = Depends(get_db)
):
    """Update a medical condition"""
    updated_condition = MedicalConditionService.update(db, medical_condition_id, medical_condition)
    if not updated_condition:
        raise HTTPException(status_code=404, detail="Medical condition not found")
    return updated_condition

@router.delete("/{medical_condition_id}")
def delete_medical_condition(
    medical_condition_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a medical condition"""
    success = MedicalConditionService.delete(db, medical_condition_id)
    if not success:
        raise HTTPException(status_code=404, detail="Medical condition not found")
    return {"message": "Medical condition deleted successfully"} 