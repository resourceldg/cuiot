from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.cared_person import CaredPersonCreate, CaredPersonUpdate, CaredPersonResponse
from app.models.cared_person import CaredPerson
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CaredPersonResponse, status_code=status.HTTP_201_CREATED)
def create_cared_person(
    cared_person_data: CaredPersonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new cared person"""
    try:
        # Create cared person - exclude user_id from schema data
        data_dict = cared_person_data.model_dump()
        data_dict.pop('user_id', None)  # Remove user_id if present
        
        cared_person = CaredPerson(
            **data_dict,
            user_id=current_user.id
        )
        
        db.add(cared_person)
        db.commit()
        db.refresh(cared_person)
        return cared_person
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create cared person: {str(e)}"
        )

@router.get("/", response_model=List[CaredPersonResponse])
def get_cared_persons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get all cared persons for the current user"""
    cared_persons = db.query(CaredPerson).filter(
        CaredPerson.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return cared_persons

@router.get("/{cared_person_id}", response_model=CaredPersonResponse)
def get_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get a specific cared person"""
    cared_person = db.query(CaredPerson).filter(
        CaredPerson.id == cared_person_id,
        CaredPerson.user_id == current_user.id
    ).first()
    
    if not cared_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cared person not found"
        )
    
    return cared_person

@router.put("/{cared_person_id}", response_model=CaredPersonResponse)
def update_cared_person(
    cared_person_id: UUID,
    cared_person_data: CaredPersonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update a cared person"""
    cared_person = db.query(CaredPerson).filter(
        CaredPerson.id == cared_person_id,
        CaredPerson.user_id == current_user.id
    ).first()
    
    if not cared_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cared person not found"
        )
    
    try:
        for field, value in cared_person_data.model_dump(exclude_unset=True).items():
            setattr(cared_person, field, value)
        
        db.commit()
        db.refresh(cared_person)
        return cared_person
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update cared person: {str(e)}"
        )

@router.delete("/{cared_person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Delete a cared person"""
    cared_person = db.query(CaredPerson).filter(
        CaredPerson.id == cared_person_id,
        CaredPerson.user_id == current_user.id
    ).first()
    
    if not cared_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cared person not found"
        )
    
    try:
        db.delete(cared_person)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete cared person: {str(e)}"
        ) 