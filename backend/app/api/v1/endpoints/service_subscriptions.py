from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.services.service_subscription import ServiceSubscriptionService
from app.schemas.service_subscription import (
    ServiceSubscriptionCreate, 
    ServiceSubscriptionUpdate, 
    ServiceSubscriptionResponse
)
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ServiceSubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_service_subscription(
    subscription_data: ServiceSubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new service subscription"""
    try:
        # Set user_id from current user if not provided
        if not subscription_data.user_id:
            subscription_data.user_id = current_user.id
        
        subscription = ServiceSubscriptionService.create_subscription(db, subscription_data)
        return subscription
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create service subscription: {str(e)}"
        )

@router.get("/", response_model=List[ServiceSubscriptionResponse])
def get_service_subscriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[UUID] = None,
    institution_id: Optional[int] = None,
    subscription_type: Optional[str] = None,
    service_name: Optional[str] = None,
    is_active: Optional[bool] = None,
    status_type_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get service subscriptions with optional filters"""
    try:
        # If no user_id specified, use current user
        if not user_id:
            user_id = current_user.id
        
        subscriptions, total = ServiceSubscriptionService.get_subscriptions(
            db=db,
            skip=skip,
            limit=limit,
            user_id=user_id,
            institution_id=institution_id,
            subscription_type=subscription_type,
            service_name=service_name,
            is_active=is_active,
            status_type_id=status_type_id
        )
        return subscriptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get service subscriptions: {str(e)}"
        )

@router.get("/{subscription_id}", response_model=ServiceSubscriptionResponse)
def get_service_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get a specific service subscription"""
    subscription = ServiceSubscriptionService.get_subscription(db, subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service subscription not found"
        )
    
    # Check if user has access to this subscription
    if subscription.user_id and subscription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this subscription"
        )
    
    return subscription

@router.put("/{subscription_id}", response_model=ServiceSubscriptionResponse)
def update_service_subscription(
    subscription_id: int,
    subscription_data: ServiceSubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update a service subscription"""
    subscription = ServiceSubscriptionService.get_subscription(db, subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service subscription not found"
        )
    
    # Check if user has access to this subscription
    if subscription.user_id and subscription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this subscription"
        )
    
    try:
        updated_subscription = ServiceSubscriptionService.update_subscription(db, subscription_id, subscription_data)
        return updated_subscription
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update service subscription: {str(e)}"
        )

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Delete a service subscription"""
    subscription = ServiceSubscriptionService.get_subscription(db, subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service subscription not found"
        )
    
    # Check if user has access to this subscription
    if subscription.user_id and subscription.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this subscription"
        )
    
    try:
        success = ServiceSubscriptionService.delete_subscription(db, subscription_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete service subscription"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete service subscription: {str(e)}"
        )

@router.get("/user/{user_id}", response_model=List[ServiceSubscriptionResponse])
def get_subscriptions_by_user(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get subscriptions for a specific user"""
    # Check if user has access to view other user's subscriptions
    if user_id != current_user.id:
        # TODO: Add role-based access control here
        pass
    
    try:
        subscriptions, total = ServiceSubscriptionService.get_subscriptions_by_user(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit
        )
        return subscriptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user subscriptions: {str(e)}"
        )

@router.get("/institution/{institution_id}", response_model=List[ServiceSubscriptionResponse])
def get_subscriptions_by_institution(
    institution_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get subscriptions for a specific institution"""
    try:
        subscriptions, total = ServiceSubscriptionService.get_subscriptions_by_institution(
            db=db,
            institution_id=institution_id,
            skip=skip,
            limit=limit
        )
        return subscriptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get institution subscriptions: {str(e)}"
        )

@router.get("/active/list", response_model=List[ServiceSubscriptionResponse])
def get_active_subscriptions(
    user_id: Optional[UUID] = None,
    institution_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get active service subscriptions"""
    try:
        # If no user_id specified, use current user
        if not user_id:
            user_id = current_user.id
        
        subscriptions = ServiceSubscriptionService.get_active_subscriptions(db, user_id, institution_id)
        return subscriptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active subscriptions: {str(e)}"
        )

@router.get("/type/{subscription_type}", response_model=List[ServiceSubscriptionResponse])
def get_subscriptions_by_type(
    subscription_type: str,
    user_id: Optional[UUID] = None,
    institution_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get subscriptions by type"""
    try:
        # If no user_id specified, use current user
        if not user_id:
            user_id = current_user.id
        
        subscriptions = ServiceSubscriptionService.get_subscriptions_by_type(
            db=db,
            subscription_type=subscription_type,
            user_id=user_id,
            institution_id=institution_id
        )
        return subscriptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get subscriptions by type: {str(e)}"
        ) 