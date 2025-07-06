from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.alert_type import AlertType, AlertTypeCreate, AlertTypeUpdate
from app.services.alert_type import AlertTypeService

router = APIRouter()

@router.post("/", response_model=AlertType, status_code=status.HTTP_201_CREATED)
def create_alert_type(
    alert_type: AlertTypeCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo tipo de alerta"""
    return AlertTypeService.create_alert_type(db=db, alert_type=alert_type)

@router.get("/", response_model=List[AlertType])
def get_alert_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de tipos de alerta"""
    return AlertTypeService.get_alert_types(db=db, skip=skip, limit=limit)

@router.get("/{alert_type_id}", response_model=AlertType)
def get_alert_type(
    alert_type_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de alerta por ID"""
    alert_type = AlertTypeService.get_alert_type(db=db, alert_type_id=alert_type_id)
    if not alert_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de alerta no encontrado"
        )
    return alert_type

@router.put("/{alert_type_id}", response_model=AlertType)
def update_alert_type(
    alert_type_id: int,
    alert_type: AlertTypeUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un tipo de alerta"""
    updated_alert_type = AlertTypeService.update_alert_type(
        db=db, alert_type_id=alert_type_id, alert_type=alert_type
    )
    if not updated_alert_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de alerta no encontrado"
        )
    return updated_alert_type

@router.delete("/{alert_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_type(
    alert_type_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un tipo de alerta (soft delete)"""
    success = AlertTypeService.delete_alert_type(db=db, alert_type_id=alert_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de alerta no encontrado"
        )

@router.post("/initialize-defaults", response_model=List[AlertType])
def initialize_default_alert_types(db: Session = Depends(get_db)):
    """Inicializar tipos de alerta por defecto del sistema"""
    return AlertTypeService.create_default_alert_types(db=db) 