from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.caregiver_assignment_type import CaregiverAssignmentType, CaregiverAssignmentTypeCreate, CaregiverAssignmentTypeUpdate
from app.services.caregiver_assignment_type import CaregiverAssignmentTypeService

router = APIRouter()

@router.get("/", response_model=List[CaregiverAssignmentType])
def get_caregiver_assignment_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all caregiver assignment types"""
    service = CaregiverAssignmentTypeService(db)
    return service.get_caregiver_assignment_types(skip=skip, limit=limit)

@router.get("/{caregiver_assignment_type_id}", response_model=CaregiverAssignmentType)
def get_caregiver_assignment_type(
    caregiver_assignment_type_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific caregiver assignment type by ID"""
    service = CaregiverAssignmentTypeService(db)
    caregiver_assignment_type = service.get_caregiver_assignment_type(caregiver_assignment_type_id)
    if not caregiver_assignment_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver assignment type not found"
        )
    return caregiver_assignment_type

@router.post("/", response_model=CaregiverAssignmentType, status_code=status.HTTP_201_CREATED)
def create_caregiver_assignment_type(
    caregiver_assignment_type: CaregiverAssignmentTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new caregiver assignment type"""
    service = CaregiverAssignmentTypeService(db)
    return service.create_caregiver_assignment_type(caregiver_assignment_type)

@router.put("/{caregiver_assignment_type_id}", response_model=CaregiverAssignmentType)
def update_caregiver_assignment_type(
    caregiver_assignment_type_id: int,
    caregiver_assignment_type: CaregiverAssignmentTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update a caregiver assignment type"""
    service = CaregiverAssignmentTypeService(db)
    updated_caregiver_assignment_type = service.update_caregiver_assignment_type(caregiver_assignment_type_id, caregiver_assignment_type)
    if not updated_caregiver_assignment_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver assignment type not found"
        )
    return updated_caregiver_assignment_type

@router.delete("/{caregiver_assignment_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_caregiver_assignment_type(
    caregiver_assignment_type_id: int,
    db: Session = Depends(get_db)
):
    """Delete a caregiver assignment type"""
    service = CaregiverAssignmentTypeService(db)
    success = service.delete_caregiver_assignment_type(caregiver_assignment_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver assignment type not found"
        ) 