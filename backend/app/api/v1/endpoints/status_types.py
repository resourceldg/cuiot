from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.status_type import StatusType, StatusTypeCreate, StatusTypeUpdate
from app.services.status_type import StatusTypeService

router = APIRouter()


@router.post("/", response_model=StatusType, status_code=status.HTTP_201_CREATED)
def create_status_type(
    status_type: StatusTypeCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo tipo de estado"""
    return StatusTypeService.create_status_type(db=db, status_type=status_type)


@router.get("/", response_model=List[StatusType])
def get_status_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de tipos de estado"""
    return StatusTypeService.get_status_types(db=db, skip=skip, limit=limit)


@router.get("/{status_type_id}", response_model=StatusType)
def get_status_type(
    status_type_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de estado por ID"""
    status_type = StatusTypeService.get_status_type(db=db, status_type_id=status_type_id)
    if not status_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de estado no encontrado"
        )
    return status_type


@router.get("/category/{category}", response_model=List[StatusType])
def get_status_types_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    """Obtener tipos de estado por categoría"""
    return StatusTypeService.get_status_types_by_category(db=db, category=category)


@router.put("/{status_type_id}", response_model=StatusType)
def update_status_type(
    status_type_id: int,
    status_type: StatusTypeUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un tipo de estado"""
    updated_status_type = StatusTypeService.update_status_type(
        db=db, status_type_id=status_type_id, status_type=status_type
    )
    if not updated_status_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de estado no encontrado"
        )
    return updated_status_type


@router.delete("/{status_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status_type(
    status_type_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un tipo de estado (soft delete)"""
    success = StatusTypeService.delete_status_type(db=db, status_type_id=status_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de estado no encontrado"
        )


@router.post("/initialize-defaults", response_model=List[StatusType])
def initialize_default_status_types(db: Session = Depends(get_db)):
    """Inicializar tipos de estado por defecto del sistema"""
    return StatusTypeService.create_default_status_types(db=db) 