from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.services.status_type import StatusTypeService
from app.services.reminder_type import ReminderTypeService
from app.services.alert_type import AlertTypeService
from app.services.event_type import EventTypeService
from app.services.device_type import DeviceTypeService

router = APIRouter()

@router.post("/initialize-all-catalogs")
def initialize_all_catalogs(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Initialize all normalized catalogs with default data.
    This endpoint ensures all catalogs are populated for testing and development.
    """
    try:
        results = {}
        
        # Initialize status_types
        status_result = StatusTypeService.create_default_status_types(db)
        results["status_types"] = len(status_result)
        
        # Initialize reminder_types
        reminder_result = ReminderTypeService.create_default_reminder_types(db)
        results["reminder_types"] = len(reminder_result)
        
        # Initialize alert_types
        alert_result = AlertTypeService.create_default_alert_types(db)
        results["alert_types"] = len(alert_result)
        
        # Initialize event_types
        event_result = EventTypeService.create_default_event_types(db)
        results["event_types"] = len(event_result)
        
        # Initialize device_types
        device_result = DeviceTypeService.create_default_device_types(db)
        results["device_types"] = len(device_result)
        
        return {
            "message": "All catalogs initialized successfully",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing catalogs: {str(e)}")

@router.get("/catalog-status")
def get_catalog_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get the current status of all normalized catalogs.
    """
    try:
        status = {}
        
        # Check status_types
        status_service = StatusTypeService(db)
        status["status_types"] = len(status_service.get_all())
        
        # Check reminder_types
        reminder_service = ReminderTypeService(db)
        status["reminder_types"] = len(reminder_service.get_all())
        
        # Check alert_types
        alert_service = AlertTypeService(db)
        status["alert_types"] = len(alert_service.get_all())
        
        # Check event_types
        event_service = EventTypeService(db)
        status["event_types"] = len(event_service.get_all())
        
        # Check device_types
        device_service = DeviceTypeService(db)
        status["device_types"] = len(device_service.get_all())
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting catalog status: {str(e)}") 