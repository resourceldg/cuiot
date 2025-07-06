from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.services.reminder import ReminderService
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new reminder"""
    try:
        # Set user_id from current user
        reminder_data.user_id = current_user.id
        
        reminder = ReminderService.create_reminder(db, reminder_data)
        return reminder
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create reminder: {str(e)}"
        )

@router.get("/", response_model=List[ReminderResponse])
def get_reminders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get all reminders for the current user"""
    reminders, _ = ReminderService.get_reminders_by_user(db, current_user.id, skip, limit)
    return reminders

@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get a specific reminder"""
    reminder = ReminderService.get_reminder(db, reminder_id)
    
    if not reminder or reminder.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    return reminder

@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: UUID,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update a reminder"""
    reminder = ReminderService.get_reminder(db, reminder_id)
    
    if not reminder or reminder.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    try:
        updated_reminder = ReminderService.update_reminder(db, reminder_id, reminder_data)
        return updated_reminder
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update reminder: {str(e)}"
        )

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Delete a reminder"""
    reminder = ReminderService.get_reminder(db, reminder_id)
    
    if not reminder or reminder.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    try:
        success = ReminderService.delete_reminder(db, reminder_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete reminder"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete reminder: {str(e)}"
        ) 