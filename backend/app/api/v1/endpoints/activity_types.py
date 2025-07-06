from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.activity_type import ActivityTypeService
from app.schemas.activity_type import ActivityType, ActivityTypeCreate, ActivityTypeUpdate

router = APIRouter()

@router.post("/", response_model=ActivityType, status_code=201)
def create_activity_type(
    activity_type: ActivityTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new activity type"""
    return ActivityTypeService.create(db, activity_type)

@router.get("/", response_model=List[ActivityType])
def get_activity_types(db: Session = Depends(get_db)):
    """Get all activity types"""
    return ActivityTypeService.get_all(db)

@router.get("/{activity_type_id}", response_model=ActivityType)
def get_activity_type(
    activity_type_id: UUID,
    db: Session = Depends(get_db)
):
    """Get an activity type by ID"""
    activity_type = ActivityTypeService.get_by_id(db, activity_type_id)
    if not activity_type:
        raise HTTPException(status_code=404, detail="Activity type not found")
    return activity_type

@router.put("/{activity_type_id}", response_model=ActivityType)
def update_activity_type(
    activity_type_id: UUID,
    activity_type: ActivityTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update an activity type"""
    updated_type = ActivityTypeService.update(db, activity_type_id, activity_type)
    if not updated_type:
        raise HTTPException(status_code=404, detail="Activity type not found")
    return updated_type

@router.delete("/{activity_type_id}")
def delete_activity_type(
    activity_type_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an activity type"""
    success = ActivityTypeService.delete(db, activity_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity type not found")
    return {"message": "Activity type deleted successfully"} 