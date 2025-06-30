from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse
from app.models.alert import Alert
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new alert"""
    try:
        # Create alert - exclude user_id from schema data
        data_dict = alert_data.dict()
        data_dict.pop('user_id', None)  # Remove user_id if present
        
        alert = Alert(
            **data_dict,
            user_id=current_user.id
        )
        
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create alert: {str(e)}"
        )

@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get all alerts for the current user"""
    alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get a specific alert"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: UUID,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Actualizar una alerta existente"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    for field, value in alert_data.dict(exclude_unset=True).items():
        setattr(alert, field, value)
    db.commit()
    db.refresh(alert)
    return alert

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Delete an alert"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    try:
        db.delete(alert)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete alert: {str(e)}"
        ) 