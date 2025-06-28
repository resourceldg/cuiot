from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.core.validations import validate_user_can_create_reports, validate_user_exists
from app.schemas.event import Event, EventCreate, EventUpdate
from app.services.event import (
    get_events, get_event_by_id, create_event, update_event, delete_event,
    get_events_by_device, get_events_by_elderly_person, get_events_by_user, get_event_types
)

router = APIRouter()

@router.get("/", response_model=List[Event])
async def get_all_events(
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = Query(None),
    elderly_person_id: Optional[UUID] = Query(None),
    device_id: Optional[UUID] = Query(None),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    created_by_id: Optional[UUID] = Query(None, description="Filtrar por usuario creador"),
    received_by_id: Optional[UUID] = Query(None, description="Filtrar por usuario receptor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener lista de eventos (sensores y calendario) con filtros"""
    events = get_events(
        db, skip=skip, limit=limit, event_type=event_type, 
        elderly_person_id=elderly_person_id, device_id=device_id, 
        start=start, end=end, created_by_id=created_by_id, received_by_id=received_by_id
    )
    return events

@router.get("/user/{user_id}", response_model=List[Event])
async def get_events_by_user_id(
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    created_only: bool = Query(False, description="Solo eventos creados por el usuario"),
    received_only: bool = Query(False, description="Solo eventos recibidos por el usuario"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener eventos por usuario (creados o recibidos)"""
    events = get_events_by_user(db, user_id, skip=skip, limit=limit, created_only=created_only, received_only=received_only)
    return events

@router.get("/device/{device_id}", response_model=List[Event])
async def get_events_by_device_id(
    device_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener eventos por dispositivo"""
    events = get_events_by_device(db, device_id, skip=skip, limit=limit)
    return events

@router.get("/elderly/{elderly_person_id}", response_model=List[Event])
async def get_events_by_elderly_person_id(
    elderly_person_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener eventos por adulto mayor"""
    events = get_events_by_elderly_person(db, elderly_person_id, skip=skip, limit=limit)
    return events

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtener evento por ID"""
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )
    return event

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_new_event(
    event: EventCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo evento (sensor o calendario)"""
    try:
        # Validar que el usuario puede crear reportes
        validate_user_can_create_reports(current_user)
        
        # Validar que el usuario creador existe
        if event.created_by_id != current_user.id:
            validate_user_exists(db, event.created_by_id)
        
        # Validar que el usuario receptor existe (si se especifica)
        if event.received_by_id:
            validate_user_exists(db, event.received_by_id)
        
        return create_event(db, event)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear evento: {str(e)}"
        )

@router.put("/{event_id}", response_model=Event)
async def update_existing_event(
    event_id: UUID, 
    event_update: EventUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar evento existente"""
    event = update_event(db, event_id, event_update)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_event(
    event_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar evento (soft delete)"""
    success = delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )

@router.get("/types/list", response_model=List[dict])
async def get_event_types_list():
    """Obtener lista de tipos de evento para el panel admin/calendario"""
    return get_event_types() 