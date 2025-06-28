from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.alert import AlertService
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse, AlertListResponse
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()

@router.get("/", response_model=AlertListResponse)
async def get_alerts(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    alert_type: Optional[str] = Query(None, description="Filtrar por tipo de alerta"),
    severity: Optional[str] = Query(None, description="Filtrar por severidad"),
    is_resolved: Optional[bool] = Query(None, description="Filtrar por estado de resolución"),
    created_by_id: Optional[UUID] = Query(None, description="Filtrar por usuario creador"),
    received_by_id: Optional[UUID] = Query(None, description="Filtrar por usuario receptor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener lista de alertas con filtros opcionales
    
    - **skip**: Número de registros a saltar para paginación
    - **limit**: Límite de registros a retornar (máximo 1000)
    - **elderly_person_id**: Filtrar por adulto mayor específico
    - **alert_type**: Filtrar por tipo de alerta (no_movement, sos, temperature, etc.)
    - **severity**: Filtrar por severidad (low, medium, high, critical)
    - **is_resolved**: Filtrar por estado de resolución
    - **created_by_id**: Filtrar por usuario creador
    - **received_by_id**: Filtrar por usuario receptor
    """
    try:
        alerts, total = AlertService.get_alerts(
            db=db,
            skip=skip,
            limit=limit,
            elderly_person_id=elderly_person_id,
            alert_type=alert_type,
            severity=severity,
            is_resolved=is_resolved,
            created_by_id=created_by_id,
            received_by_id=received_by_id
        )
        
        return AlertListResponse(
            alerts=alerts,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alertas: {str(e)}"
        )

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener una alerta específica por ID
    
    - **alert_id**: ID único de la alerta
    """
    try:
        alert = AlertService.get_alert(db, alert_id)
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {alert_id} no encontrada"
            )
        
        return alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alerta: {str(e)}"
        )

@router.get("/elderly/{elderly_person_id}", response_model=AlertListResponse)
async def get_alerts_by_elderly_person(
    elderly_person_id: UUID,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener alertas de un adulto mayor específico
    
    - **elderly_person_id**: ID del adulto mayor
    - **skip**: Número de registros a saltar para paginación
    - **limit**: Límite de registros a retornar
    """
    try:
        alerts, total = AlertService.get_alerts_by_elderly_person(
            db=db,
            elderly_person_id=elderly_person_id,
            skip=skip,
            limit=limit
        )
        
        return AlertListResponse(
            alerts=alerts,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alertas del adulto mayor: {str(e)}"
        )

@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva alerta
    
    - **elderly_person_id**: ID del adulto mayor
    - **alert_type**: Tipo de alerta (no_movement, sos, temperature, medication, fall, heart_rate, blood_pressure)
    - **message**: Mensaje descriptivo de la alerta
    - **severity**: Nivel de severidad (low, medium, high, critical)
    """
    try:
        alert = AlertService.create_alert(db, alert_data)
        return alert
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear alerta: {str(e)}"
        )

@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: UUID,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar una alerta existente
    
    - **alert_id**: ID de la alerta a actualizar
    - **message**: Nuevo mensaje (opcional)
    - **severity**: Nueva severidad (opcional)
    - **is_resolved**: Estado de resolución (opcional)
    """
    try:
        alert = AlertService.update_alert(db, alert_id, alert_data)
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {alert_id} no encontrada"
            )
        
        return alert
    except HTTPException:
        raise
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar alerta: {str(e)}"
        )

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar una alerta
    
    - **alert_id**: ID de la alerta a eliminar
    """
    try:
        success = AlertService.delete_alert(db, alert_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {alert_id} no encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar alerta: {str(e)}"
        )

@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marcar una alerta como resuelta
    
    - **alert_id**: ID de la alerta a marcar como resuelta
    """
    try:
        alert = AlertService.resolve_alert(db, alert_id)
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {alert_id} no encontrada"
            )
        
        return alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al resolver alerta: {str(e)}"
        )

@router.get("/unresolved/list", response_model=List[AlertResponse])
async def get_unresolved_alerts(
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener lista de alertas no resueltas
    
    - **elderly_person_id**: Filtrar por adulto mayor específico (opcional)
    """
    try:
        alerts = AlertService.get_unresolved_alerts(db, elderly_person_id)
        return alerts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alertas no resueltas: {str(e)}"
        )

@router.get("/critical/list", response_model=List[AlertResponse])
async def get_critical_alerts(
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener lista de alertas críticas
    
    - **elderly_person_id**: Filtrar por adulto mayor específico (opcional)
    """
    try:
        alerts = AlertService.get_critical_alerts(db, elderly_person_id)
        return alerts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alertas críticas: {str(e)}"
        )

@router.get("/user/{user_id}", response_model=AlertListResponse)
async def get_alerts_by_user(
    user_id: UUID,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    created_only: bool = Query(False, description="Solo alertas creadas por el usuario"),
    received_only: bool = Query(False, description="Solo alertas recibidas por el usuario"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener alertas por usuario (creadas o recibidas)
    
    - **user_id**: ID del usuario
    - **skip**: Número de registros a saltar para paginación
    - **limit**: Límite de registros a retornar
    - **created_only**: Solo alertas creadas por el usuario
    - **received_only**: Solo alertas recibidas por el usuario
    """
    try:
        alerts, total = AlertService.get_alerts_by_user(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            created_only=created_only,
            received_only=received_only
        )
        
        return AlertListResponse(
            alerts=alerts,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alertas del usuario: {str(e)}"
        ) 