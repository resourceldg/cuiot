from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.service_type import ServiceType, ServiceTypeCreate, ServiceTypeUpdate
from app.services.service_type import ServiceTypeService

router = APIRouter()

@router.get("/", response_model=List[ServiceType])
def get_service_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all service types"""
    service = ServiceTypeService(db)
    return service.get_service_types(skip=skip, limit=limit)

@router.get("/{service_type_id}", response_model=ServiceType)
def get_service_type(
    service_type_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific service type by ID"""
    service = ServiceTypeService(db)
    service_type = service.get_service_type(service_type_id)
    if not service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found"
        )
    return service_type

@router.post("/", response_model=ServiceType, status_code=status.HTTP_201_CREATED)
def create_service_type(
    service_type: ServiceTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new service type"""
    service = ServiceTypeService(db)
    return service.create_service_type(service_type)

@router.put("/{service_type_id}", response_model=ServiceType)
def update_service_type(
    service_type_id: int,
    service_type: ServiceTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update a service type"""
    service = ServiceTypeService(db)
    updated_service_type = service.update_service_type(service_type_id, service_type)
    if not updated_service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found"
        )
    return updated_service_type

@router.delete("/{service_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_type(
    service_type_id: int,
    db: Session = Depends(get_db)
):
    """Delete a service type"""
    service = ServiceTypeService(db)
    success = service.delete_service_type(service_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found"
        ) 