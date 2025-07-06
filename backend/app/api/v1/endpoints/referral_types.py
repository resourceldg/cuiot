from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.referral_type import ReferralType, ReferralTypeCreate, ReferralTypeUpdate
from app.services.referral_type import ReferralTypeService

router = APIRouter()

@router.get("/", response_model=List[ReferralType])
def get_referral_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all referral types"""
    service = ReferralTypeService(db)
    return service.get_referral_types(skip=skip, limit=limit)

@router.get("/{referral_type_id}", response_model=ReferralType)
def get_referral_type(
    referral_type_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific referral type by ID"""
    service = ReferralTypeService(db)
    referral_type = service.get_referral_type(referral_type_id)
    if not referral_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referral type not found"
        )
    return referral_type

@router.post("/", response_model=ReferralType, status_code=status.HTTP_201_CREATED)
def create_referral_type(
    referral_type: ReferralTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new referral type"""
    service = ReferralTypeService(db)
    return service.create_referral_type(referral_type)

@router.put("/{referral_type_id}", response_model=ReferralType)
def update_referral_type(
    referral_type_id: int,
    referral_type: ReferralTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update a referral type"""
    service = ReferralTypeService(db)
    updated_referral_type = service.update_referral_type(referral_type_id, referral_type)
    if not updated_referral_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referral type not found"
        )
    return updated_referral_type

@router.delete("/{referral_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_referral_type(
    referral_type_id: int,
    db: Session = Depends(get_db)
):
    """Delete a referral type"""
    service = ReferralTypeService(db)
    success = service.delete_referral_type(referral_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referral type not found"
        ) 