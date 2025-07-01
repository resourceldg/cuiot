from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.medication_log import (
    MedicationLogCreate, MedicationLogUpdate, MedicationLogResponse
)
from app.services.medication_log import MedicationLogService

router = APIRouter()

@router.post("/", response_model=MedicationLogResponse, status_code=status.HTTP_201_CREATED)
def create_medication_log(
    medication_log: MedicationLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new medication log entry"""
    return MedicationLogService.create(db, medication_log)

@router.get("/{log_id}", response_model=MedicationLogResponse)
def get_medication_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get medication log by ID"""
    medication_log = MedicationLogService.get_by_id(db, log_id)
    if not medication_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication log not found"
        )
    return medication_log

@router.get("/schedule/{schedule_id}", response_model=List[MedicationLogResponse])
def get_medication_logs_by_schedule(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all medication logs for a specific schedule"""
    return MedicationLogService.get_by_schedule_id(db, schedule_id)

@router.get("/cared-person/{cared_person_id}", response_model=List[MedicationLogResponse])
def get_medication_logs_by_cared_person(
    cared_person_id: UUID,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get medication logs for a cared person"""
    return MedicationLogService.get_by_cared_person_id(db, cared_person_id, limit=limit)

@router.get("/cared-person/{cared_person_id}/recent", response_model=List[MedicationLogResponse])
def get_recent_medication_logs(
    cared_person_id: UUID,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent medication logs for a cared person"""
    return MedicationLogService.get_recent_logs(db, cared_person_id, days=days)

@router.get("/", response_model=List[MedicationLogResponse])
def get_all_medication_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all medication logs"""
    return MedicationLogService.get_all(db, skip=skip, limit=limit)

@router.put("/{log_id}", response_model=MedicationLogResponse)
def update_medication_log(
    log_id: UUID,
    medication_log: MedicationLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update medication log"""
    try:
        return MedicationLogService.update(db, log_id, medication_log)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication_log(
    log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete medication log"""
    try:
        MedicationLogService.delete(db, log_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 