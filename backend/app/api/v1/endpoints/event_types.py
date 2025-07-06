from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.event_type import EventType, EventTypeCreate, EventTypeUpdate
from app.services.event_type import EventTypeService

router = APIRouter()

@router.get("/", response_model=List[EventType])
def get_event_types(db: Session = Depends(get_db)):
    """Obtener todos los tipos de evento"""
    return EventTypeService.get_all_event_types(db=db)

# ... otros endpoints ...

@router.post("/initialize-defaults", response_model=List[EventType])
def initialize_default_event_types(db: Session = Depends(get_db)):
    """Inicializar tipos de evento por defecto del sistema"""
    return EventTypeService.create_default_event_types(db=db) 