from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.reminder import ReminderService
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse, ReminderListResponse
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()

@router.get("/", response_model=ReminderListResponse)
async def get_reminders(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    reminder_type: Optional[str] = Query(None, description="Filtrar por tipo de recordatorio"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    created_by_id: Optional[UUID] = Query(None, description="Filtrar por usuario creador"),
    received_by_id: Optional[UUID] = Query(None, description="Filtrar por usuario receptor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener lista de recordatorios con filtros opcionales
    
    - **skip**: Número de registros a saltar para paginación
    - **limit**: Límite de registros a retornar (máximo 1000)
    - **elderly_person_id**: Filtrar por adulto mayor específico
    - **reminder_type**: Filtrar por tipo de recordatorio (medication, appointment, activity, etc.)
    - **is_active**: Filtrar por estado activo
    - **created_by_id**: Filtrar por usuario creador
    - **received_by_id**: Filtrar por usuario receptor
    """
    try:
        reminders, total = ReminderService.get_reminders(
            db=db,
            skip=skip,
            limit=limit,
            elderly_person_id=elderly_person_id,
            reminder_type=reminder_type,
            is_active=is_active,
            created_by_id=created_by_id,
            received_by_id=received_by_id
        )
        
        return ReminderListResponse(
            reminders=reminders,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorios: {str(e)}"
        )

@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener un recordatorio específico por ID
    
    - **reminder_id**: ID único del recordatorio
    """
    try:
        reminder = ReminderService.get_reminder(db, reminder_id)
        
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recordatorio con ID {reminder_id} no encontrado"
            )
        
        return reminder
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorio: {str(e)}"
        )

@router.get("/elderly/{elderly_person_id}", response_model=ReminderListResponse)
async def get_reminders_by_elderly_person(
    elderly_person_id: UUID,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener recordatorios de un adulto mayor específico
    
    - **elderly_person_id**: ID del adulto mayor
    - **skip**: Número de registros a saltar para paginación
    - **limit**: Límite de registros a retornar
    """
    try:
        reminders, total = ReminderService.get_reminders_by_elderly_person(
            db=db,
            elderly_person_id=elderly_person_id,
            skip=skip,
            limit=limit
        )
        
        return ReminderListResponse(
            reminders=reminders,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorios del adulto mayor: {str(e)}"
        )

@router.post("/", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear un nuevo recordatorio
    
    - **elderly_person_id**: ID del adulto mayor
    - **title**: Título del recordatorio
    - **description**: Descripción opcional
    - **reminder_type**: Tipo de recordatorio (medication, appointment, activity, meal, exercise, hydration)
    - **scheduled_time**: Hora programada para el recordatorio
    - **days_of_week**: Días de la semana (1-7, donde 1=Lunes, opcional)
    """
    try:
        reminder = ReminderService.create_reminder(db, reminder_data)
        return reminder
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
            detail=f"Error al crear recordatorio: {str(e)}"
        )

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: UUID,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar un recordatorio existente
    
    - **reminder_id**: ID del recordatorio a actualizar
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **reminder_type**: Nuevo tipo (opcional)
    - **scheduled_time**: Nueva hora programada (opcional)
    - **is_active**: Estado activo (opcional)
    - **days_of_week**: Nuevos días de la semana (opcional)
    """
    try:
        reminder = ReminderService.update_reminder(db, reminder_id, reminder_data)
        
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recordatorio con ID {reminder_id} no encontrado"
            )
        
        return reminder
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
            detail=f"Error al actualizar recordatorio: {str(e)}"
        )

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar un recordatorio
    
    - **reminder_id**: ID del recordatorio a eliminar
    """
    try:
        success = ReminderService.delete_reminder(db, reminder_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recordatorio con ID {reminder_id} no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar recordatorio: {str(e)}"
        )

@router.patch("/{reminder_id}/activate", response_model=ReminderResponse)
async def activate_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Activar un recordatorio
    
    - **reminder_id**: ID del recordatorio a activar
    """
    try:
        reminder = ReminderService.activate_reminder(db, reminder_id)
        
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recordatorio con ID {reminder_id} no encontrado"
            )
        
        return reminder
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al activar recordatorio: {str(e)}"
        )

@router.patch("/{reminder_id}/deactivate", response_model=ReminderResponse)
async def deactivate_reminder(
    reminder_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Desactivar un recordatorio
    
    - **reminder_id**: ID del recordatorio a desactivar
    """
    try:
        reminder = ReminderService.deactivate_reminder(db, reminder_id)
        
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recordatorio con ID {reminder_id} no encontrado"
            )
        
        return reminder
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar recordatorio: {str(e)}"
        )

@router.get("/active/list", response_model=List[ReminderResponse])
async def get_active_reminders(
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener lista de recordatorios activos
    
    - **elderly_person_id**: Filtrar por adulto mayor específico (opcional)
    """
    try:
        reminders = ReminderService.get_active_reminders(db, elderly_person_id)
        return reminders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorios activos: {str(e)}"
        )

@router.get("/type/{reminder_type}/list", response_model=List[ReminderResponse])
async def get_reminders_by_type(
    reminder_type: str,
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener recordatorios por tipo
    
    - **reminder_type**: Tipo de recordatorio (medication, appointment, activity, etc.)
    - **elderly_person_id**: Filtrar por adulto mayor específico (opcional)
    """
    try:
        reminders = ReminderService.get_reminders_by_type(db, reminder_type, elderly_person_id)
        return reminders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorios por tipo: {str(e)}"
        )

@router.get("/medication/list", response_model=List[ReminderResponse])
async def get_medication_reminders(
    elderly_person_id: Optional[UUID] = Query(None, description="Filtrar por adulto mayor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener recordatorios de medicación
    
    - **elderly_person_id**: Filtrar por adulto mayor específico (opcional)
    """
    try:
        reminders = ReminderService.get_medication_reminders(db, elderly_person_id)
        return reminders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorios de medicación: {str(e)}"
        )

@router.get("/user/{user_id}", response_model=ReminderListResponse)
async def get_reminders_by_user(
    user_id: UUID,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    created_only: bool = Query(False, description="Solo recordatorios creados por el usuario"),
    received_only: bool = Query(False, description="Solo recordatorios recibidos por el usuario"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener recordatorios por usuario (creados o recibidos)
    
    - **user_id**: ID del usuario
    - **skip**: Número de registros a saltar para paginación
    - **limit**: Límite de registros a retornar
    - **created_only**: Solo recordatorios creados por el usuario
    - **received_only**: Solo recordatorios recibidos por el usuario
    """
    try:
        reminders, total = ReminderService.get_reminders_by_user(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            created_only=created_only,
            received_only=received_only
        )
        
        return ReminderListResponse(
            reminders=reminders,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener recordatorios del usuario: {str(e)}"
        ) 