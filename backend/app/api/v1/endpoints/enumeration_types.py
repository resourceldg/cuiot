from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.enumeration_type import EnumerationTypeService
from app.schemas.enumeration_type import EnumerationType, EnumerationTypeCreate, EnumerationTypeUpdate

router = APIRouter()

@router.post("/", response_model=EnumerationType, status_code=201)
def create_enumeration_type(
    enumeration_type: EnumerationTypeCreate,
    db: Session = Depends(get_db)
):
    """Create a new enumeration type"""
    return EnumerationTypeService.create(db, enumeration_type)

@router.get("/", response_model=List[EnumerationType])
def get_enumeration_types(db: Session = Depends(get_db)):
    """Get all enumeration types"""
    return EnumerationTypeService.get_all(db)

@router.get("/{enumeration_type_id}", response_model=EnumerationType)
def get_enumeration_type(
    enumeration_type_id: UUID,
    db: Session = Depends(get_db)
):
    """Get an enumeration type by ID"""
    enumeration_type = EnumerationTypeService.get_by_id(db, enumeration_type_id)
    if not enumeration_type:
        raise HTTPException(status_code=404, detail="Enumeration type not found")
    return enumeration_type

@router.put("/{enumeration_type_id}", response_model=EnumerationType)
def update_enumeration_type(
    enumeration_type_id: UUID,
    enumeration_type: EnumerationTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update an enumeration type"""
    updated_type = EnumerationTypeService.update(db, enumeration_type_id, enumeration_type)
    if not updated_type:
        raise HTTPException(status_code=404, detail="Enumeration type not found")
    return updated_type

@router.delete("/{enumeration_type_id}")
def delete_enumeration_type(
    enumeration_type_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an enumeration type"""
    success = EnumerationTypeService.delete(db, enumeration_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Enumeration type not found")
    return {"message": "Enumeration type deleted successfully"} 