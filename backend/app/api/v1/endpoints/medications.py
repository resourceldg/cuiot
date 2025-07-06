from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.medication import MedicationService
from app.schemas.medication import Medication, MedicationCreate, MedicationUpdate

router = APIRouter()

@router.post("/", response_model=Medication, status_code=201)
def create_medication(
    medication: MedicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new medication"""
    return MedicationService.create(db, medication)

@router.get("/{medication_id}", response_model=Medication)
def get_medication(
    medication_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a medication by ID"""
    medication = MedicationService.get_by_id(db, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

@router.get("/cared-person/{cared_person_id}", response_model=List[Medication])
def get_medications_by_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all medications for a cared person"""
    return MedicationService.get_by_cared_person(db, cared_person_id)

@router.put("/{medication_id}", response_model=Medication)
def update_medication(
    medication_id: UUID,
    medication: MedicationUpdate,
    db: Session = Depends(get_db)
):
    """Update a medication"""
    updated_medication = MedicationService.update(db, medication_id, medication)
    if not updated_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return updated_medication

@router.delete("/{medication_id}")
def delete_medication(
    medication_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a medication"""
    success = MedicationService.delete(db, medication_id)
    if not success:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"message": "Medication deleted successfully"}
