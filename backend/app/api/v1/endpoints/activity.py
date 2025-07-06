from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.activity import ActivityService
from app.schemas.activity import Activity, ActivityCreate, ActivityUpdate

router = APIRouter()

@router.post("/", response_model=Activity, status_code=201)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db)
):
    """Create a new activity"""
    return ActivityService.create(db, activity)

@router.get("/", response_model=List[Activity])
def get_activities(db: Session = Depends(get_db)):
    """Get all activities"""
    return ActivityService.get_all(db)

@router.get("/{activity_id}", response_model=Activity)
def get_activity(
    activity_id: UUID,
    db: Session = Depends(get_db)
):
    """Get an activity by ID"""
    activity = ActivityService.get_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: UUID,
    activity: ActivityUpdate,
    db: Session = Depends(get_db)
):
    """Update an activity"""
    updated = ActivityService.update(db, activity_id, activity)
    if not updated:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated

@router.delete("/{activity_id}")
def delete_activity(
    activity_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an activity"""
    success = ActivityService.delete(db, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"} 