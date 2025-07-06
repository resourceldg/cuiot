from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.allergy import AllergyService
from app.schemas.allergy import Allergy, AllergyCreate, AllergyUpdate

router = APIRouter()

@router.post("/", response_model=Allergy, status_code=201)
def create_allergy(
    allergy: AllergyCreate,
    db: Session = Depends(get_db)
):
    """Create a new allergy"""
    return AllergyService.create(db, allergy)

@router.get("/{allergy_id}", response_model=Allergy)
def get_allergy(
    allergy_id: UUID,
    db: Session = Depends(get_db)
):
    """Get an allergy by ID"""
    allergy = AllergyService.get_by_id(db, allergy_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return allergy

@router.get("/cared-person/{cared_person_id}", response_model=List[Allergy])
def get_allergies_by_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all allergies for a cared person"""
    return AllergyService.get_by_cared_person(db, cared_person_id)

@router.put("/{allergy_id}", response_model=Allergy)
def update_allergy(
    allergy_id: UUID,
    allergy: AllergyUpdate,
    db: Session = Depends(get_db)
):
    """Update an allergy"""
    updated_allergy = AllergyService.update(db, allergy_id, allergy)
    if not updated_allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return updated_allergy

@router.delete("/{allergy_id}")
def delete_allergy(
    allergy_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an allergy"""
    success = AllergyService.delete(db, allergy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return {"message": "Allergy deleted successfully"}
