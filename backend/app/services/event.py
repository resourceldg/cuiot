from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

# --- Listar eventos activos, con filtros ---
def get_events(db: Session, skip: int = 0, limit: int = 100, event_type: Optional[str] = None, elderly_person_id: Optional[UUID] = None, device_id: Optional[UUID] = None, start: Optional[datetime] = None, end: Optional[datetime] = None, created_by_id: Optional[UUID] = None, received_by_id: Optional[UUID] = None) -> List[Event]:
    """Obtener lista de eventos activos, con filtros opcionales"""
    query = db.query(Event).filter(Event.is_active == True)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if elderly_person_id:
        query = query.filter(Event.elderly_person_id == elderly_person_id)
    if device_id:
        query = query.filter(Event.device_id == device_id)
    if start:
        query = query.filter(Event.start_datetime >= start)
    if end:
        query = query.filter(Event.end_datetime <= end)
    if created_by_id:
        query = query.filter(Event.created_by_id == created_by_id)
    if received_by_id:
        query = query.filter(Event.received_by_id == received_by_id)
    return query.order_by(Event.start_datetime.desc()).offset(skip).limit(limit).all()

def get_event_by_id(db: Session, event_id: UUID) -> Optional[Event]:
    """Obtener evento por ID (solo si está activo)"""
    return db.query(Event).filter(Event.id == event_id, Event.is_active == True).first()

def get_events_by_device(db: Session, device_id: UUID, skip: int = 0, limit: int = 100) -> List[Event]:
    """Obtener eventos por dispositivo (solo activos)"""
    return db.query(Event).filter(Event.device_id == device_id, Event.is_active == True).offset(skip).limit(limit).all()

def get_events_by_elderly_person(db: Session, elderly_person_id: UUID, skip: int = 0, limit: int = 100) -> List[Event]:
    """Obtener eventos por adulto mayor (solo activos)"""
    return db.query(Event).filter(Event.elderly_person_id == elderly_person_id, Event.is_active == True).offset(skip).limit(limit).all()

def get_events_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 100, created_only: bool = False, received_only: bool = False) -> List[Event]:
    """Obtener eventos por usuario (creados o recibidos)"""
    query = db.query(Event).filter(Event.is_active == True)
    
    if created_only:
        query = query.filter(Event.created_by_id == user_id)
    elif received_only:
        query = query.filter(Event.received_by_id == user_id)
    else:
        # Ambos: creados o recibidos
        query = query.filter(
            (Event.created_by_id == user_id) | (Event.received_by_id == user_id)
        )
    
    return query.order_by(Event.start_datetime.desc()).offset(skip).limit(limit).all()

def create_event(db: Session, event: EventCreate) -> Event:
    """Crear nuevo evento (sensor o calendario)"""
    db_event = Event(
        elderly_person_id=event.elderly_person_id,
        device_id=event.device_id,
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        value=event.value,
        location=event.location,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        created_by_id=event.created_by_id,
        received_by_id=event.received_by_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: UUID, event_update: EventUpdate) -> Optional[Event]:
    """Actualizar evento (solo si está activo)"""
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return None
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: UUID) -> bool:
    """Soft delete: marcar evento como inactivo"""
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return False
    db_event.is_active = False
    db.commit()
    return True

# --- Tipos de evento personalizables (dummy, para panel admin) ---
def get_event_types() -> List[dict]:
    """Lista de tipos de evento predefinidos y custom"""
    return [
        {"key": "medical", "label": "Turno médico", "color": "#2563eb"},
        {"key": "family", "label": "Visita familiar", "color": "#10b981"},
        {"key": "medication", "label": "Medicación", "color": "#f59e42"},
        {"key": "kinesiologia", "label": "Kinesiología", "color": "#a855f7"},
        {"key": "nutrition", "label": "Nutrición", "color": "#f43f5e"},
        {"key": "sensor", "label": "Evento de sensor", "color": "#64748b"},
        {"key": "other", "label": "Otro", "color": "#6b7280"},
    ] 