from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.medication_schedule import (
    MedicationScheduleBase,
    MedicationScheduleCreate,
    MedicationScheduleUpdate,
    MedicationSchedule
)
from app.services.medication_schedule import MedicationScheduleService

router = APIRouter()

@router.post("/", response_model=MedicationSchedule, status_code=status.HTTP_201_CREATED)
def create_medication_schedule(
    medication_schedule: MedicationScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new medication schedule"""
    return MedicationScheduleService.create(db, medication_schedule)

@router.get("/{schedule_id}", response_model=MedicationSchedule)
def get_medication_schedule(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get medication schedule by ID"""
    medication_schedule = MedicationScheduleService.get_by_id(db, schedule_id)
    if not medication_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication schedule not found"
        )
    return medication_schedule

@router.get("/cared-person/{cared_person_id}", response_model=List[MedicationSchedule])
def get_medication_schedules_by_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all medication schedules for a cared person"""
    return MedicationScheduleService.get_by_cared_person_id(db, cared_person_id)

@router.get("/cared-person/{cared_person_id}/active", response_model=List[MedicationSchedule])
def get_active_medication_schedules(
    cared_person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active medication schedules for a cared person"""
    return MedicationScheduleService.get_active_schedules(db, cared_person_id)

@router.get("/", response_model=List[MedicationSchedule])
def get_all_medication_schedules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all medication schedules"""
    return MedicationScheduleService.get_all(db, skip=skip, limit=limit)

@router.put("/{schedule_id}", response_model=MedicationSchedule)
def update_medication_schedule(
    schedule_id: UUID,
    medication_schedule: MedicationScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update medication schedule"""
    try:
        return MedicationScheduleService.update(db, schedule_id, medication_schedule)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication_schedule(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete medication schedule"""
    try:
        MedicationScheduleService.delete(db, schedule_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 