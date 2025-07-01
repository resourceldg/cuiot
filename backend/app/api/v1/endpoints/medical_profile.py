from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.medical_profile import (
    MedicalProfileCreate, MedicalProfileUpdate, MedicalProfileResponse
)
from app.services.medical_profile import MedicalProfileService

router = APIRouter()

@router.post("/", response_model=MedicalProfileResponse, status_code=status.HTTP_201_CREATED)
def create_medical_profile(
    medical_profile: MedicalProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new medical profile"""
    return MedicalProfileService.create(db, medical_profile)

@router.get("/{medical_profile_id}", response_model=MedicalProfileResponse)
def get_medical_profile(
    medical_profile_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get medical profile by ID"""
    medical_profile = MedicalProfileService.get_by_id(db, medical_profile_id)
    if not medical_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical profile not found"
        )
    return medical_profile

@router.get("/cared-person/{cared_person_id}", response_model=MedicalProfileResponse)
def get_medical_profile_by_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get medical profile by cared person ID"""
    medical_profile = MedicalProfileService.get_by_cared_person_id(db, cared_person_id)
    if not medical_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical profile not found for this cared person"
        )
    return medical_profile

@router.get("/", response_model=List[MedicalProfileResponse])
def get_all_medical_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all medical profiles"""
    return MedicalProfileService.get_all(db, skip=skip, limit=limit)

@router.put("/{medical_profile_id}", response_model=MedicalProfileResponse)
def update_medical_profile(
    medical_profile_id: UUID,
    medical_profile: MedicalProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update medical profile"""
    try:
        return MedicalProfileService.update(db, medical_profile_id, medical_profile)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{medical_profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medical_profile(
    medical_profile_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete medical profile"""
    try:
        MedicalProfileService.delete(db, medical_profile_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 