from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth import AuthService
from app.services.debug import DebugService
from app.schemas.debug import DebugEventCreate, DebugEventResponse, DebugSummary

router = APIRouter()

@router.post("/events", response_model=DebugEventResponse, status_code=status.HTTP_201_CREATED)
def create_debug_event(
    event_data: DebugEventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Create a debug event"""
    return DebugService.create_debug_event(db, event_data)

@router.get("/events", response_model=List[DebugEventResponse])
def get_debug_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: str = Query(None),
    severity: str = Query(None),
    test_session: str = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Get debug events with filters"""
    events = DebugService.get_debug_events(
        db, 
        skip=skip, 
        limit=limit,
        event_type=event_type,
        severity=severity,
        test_session=test_session
    )
    return events

@router.post("/generate-test-data")
def generate_test_data(
    count: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Generate test data for development"""
    try:
        results = DebugService.generate_test_data(db, count)
        return {
            "message": "Test data generated successfully",
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate test data: {str(e)}"
        )

@router.post("/clean-test-data")
def clean_test_data(
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Clean all test data"""
    try:
        results = DebugService.clean_test_data(db)
        return {
            "message": "Test data cleaned successfully",
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clean test data: {str(e)}"
        )

@router.get("/summary", response_model=DebugSummary)
def get_debug_summary(
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Get debug summary statistics"""
    return DebugService.get_debug_summary(db)

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }
