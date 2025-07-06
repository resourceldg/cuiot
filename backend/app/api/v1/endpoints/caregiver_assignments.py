from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.services.caregiver_assignment import CaregiverAssignmentService
from app.schemas.caregiver_assignment import (
    CaregiverAssignmentCreate, 
    CaregiverAssignmentUpdate, 
    CaregiverAssignmentResponse
)
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CaregiverAssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_caregiver_assignment(
    assignment_data: CaregiverAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new caregiver assignment"""
    try:
        # Set assigned_by from current user
        assignment_data.assigned_by = current_user.id
        
        assignment = CaregiverAssignmentService.create_assignment(db, assignment_data)
        return assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create caregiver assignment: {str(e)}"
        )

@router.get("/", response_model=List[CaregiverAssignmentResponse])
def get_caregiver_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    caregiver_id: Optional[UUID] = None,
    cared_person_id: Optional[UUID] = None,
    assignment_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    status_type_id: Optional[int] = None,
    is_primary: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get caregiver assignments with optional filters"""
    try:
        assignments, total = CaregiverAssignmentService.get_assignments(
            db=db,
            skip=skip,
            limit=limit,
            caregiver_id=caregiver_id,
            cared_person_id=cared_person_id,
            assignment_type=assignment_type,
            is_active=is_active,
            status_type_id=status_type_id,
            is_primary=is_primary
        )
        return assignments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get caregiver assignments: {str(e)}"
        )

@router.get("/{assignment_id}", response_model=CaregiverAssignmentResponse)
def get_caregiver_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get a specific caregiver assignment"""
    assignment = CaregiverAssignmentService.get_assignment(db, assignment_id)
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver assignment not found"
        )
    
    return assignment

@router.put("/{assignment_id}", response_model=CaregiverAssignmentResponse)
def update_caregiver_assignment(
    assignment_id: int,
    assignment_data: CaregiverAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update a caregiver assignment"""
    assignment = CaregiverAssignmentService.get_assignment(db, assignment_id)
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver assignment not found"
        )
    
    try:
        updated_assignment = CaregiverAssignmentService.update_assignment(db, assignment_id, assignment_data)
        return updated_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update caregiver assignment: {str(e)}"
        )

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_caregiver_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Delete a caregiver assignment"""
    assignment = CaregiverAssignmentService.get_assignment(db, assignment_id)
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver assignment not found"
        )
    
    try:
        success = CaregiverAssignmentService.delete_assignment(db, assignment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete caregiver assignment"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete caregiver assignment: {str(e)}"
        )

@router.get("/caregiver/{caregiver_id}", response_model=List[CaregiverAssignmentResponse])
def get_assignments_by_caregiver(
    caregiver_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get assignments for a specific caregiver"""
    try:
        assignments, total = CaregiverAssignmentService.get_assignments_by_caregiver(
            db=db,
            caregiver_id=caregiver_id,
            skip=skip,
            limit=limit
        )
        return assignments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get caregiver assignments: {str(e)}"
        )

@router.get("/cared-person/{cared_person_id}", response_model=List[CaregiverAssignmentResponse])
def get_assignments_by_cared_person(
    cared_person_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get assignments for a specific cared person"""
    try:
        assignments, total = CaregiverAssignmentService.get_assignments_by_cared_person(
            db=db,
            cared_person_id=cared_person_id,
            skip=skip,
            limit=limit
        )
        return assignments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cared person assignments: {str(e)}"
        )

@router.get("/cared-person/{cared_person_id}/primary", response_model=CaregiverAssignmentResponse)
def get_primary_caregiver(
    cared_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get the primary caregiver for a cared person"""
    try:
        assignment = CaregiverAssignmentService.get_primary_caregiver(db, cared_person_id)
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Primary caregiver not found for this cared person"
            )
        
        return assignment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get primary caregiver: {str(e)}"
        )

@router.get("/active/list", response_model=List[CaregiverAssignmentResponse])
def get_active_assignments(
    cared_person_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get active caregiver assignments"""
    try:
        assignments = CaregiverAssignmentService.get_active_assignments(db, cared_person_id)
        return assignments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active assignments: {str(e)}"
        ) 