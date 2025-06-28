from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.models import DebugEvent, LocationTracking, Geofence, CaredPerson
from app.scripts.debug_utilities import DebugUtilities

router = APIRouter(prefix="/debug", tags=["debug"])


def get_utilities(db: Session = Depends(get_db)):
    return DebugUtilities(db)


@router.post("/generate-test-data", summary="Generar datos de prueba para debug")
def generate_test_data(user_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    data = utilities.generate_test_data(user_id)
    return {
        "cared_person_id": str(data["cared_person"].id),
        "geofences": [str(g.id) for g in data["geofences"]],
        "events": [str(e.id) for e in data["events"]],
        "locations": [str(l.id) for l in data["locations"]],
        "protocol_id": str(data["protocol"].id)
    }


@router.post("/cleanup-test-data", summary="Limpiar datos de prueba para una persona")
def cleanup_test_data(cared_person_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    utilities.cleanup_test_data(cared_person_id)
    return {"detail": "Datos de prueba eliminados"}


@router.get("/debug-events", response_model=List[dict], summary="Listar eventos de debug")
def list_debug_events(
    cared_person_id: Optional[uuid.UUID] = None,
    event_type: Optional[str] = None,
    limit: int = Query(100, le=200),
    db: Session = Depends(get_db)
):
    events = DebugEvent.get_debug_events(db, cared_person_id, event_type, limit)
    return [
        {
            "id": str(e.id),
            "event_type": e.event_type,
            "severity_level": e.severity_level,
            "created_at": e.created_at,
            "description": e.description,
            "test_scenario": e.test_scenario
        } for e in events
    ]


@router.get("/locations", response_model=List[dict], summary="Listar ubicaciones de debug")
def list_debug_locations(
    cared_person_id: uuid.UUID,
    limit: int = Query(100, le=200),
    db: Session = Depends(get_db)
):
    locations = LocationTracking.get_debug_locations(db, cared_person_id)
    return [
        {
            "id": str(l.id),
            "latitude": l.latitude,
            "longitude": l.longitude,
            "created_at": l.created_at,
            "source_type": l.source_type,
            "is_debug": l.is_debug
        } for l in locations[:limit]
    ]


@router.get("/geofences", response_model=List[dict], summary="Listar geofences de debug")
def list_debug_geofences(
    cared_person_id: Optional[uuid.UUID] = None,
    db: Session = Depends(get_db)
):
    geofences = Geofence.get_debug_geofences(db, cared_person_id)
    return [
        {
            "id": str(g.id),
            "name": g.name,
            "type": g.geofence_type,
            "latitude": g.latitude,
            "longitude": g.longitude,
            "radius": g.radius,
            "is_active": g.is_active,
            "is_debug": g.is_debug
        } for g in geofences
    ]


@router.get("/summary", summary="Resumen de datos de debug")
def debug_summary(cared_person_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    return utilities.get_debug_summary(cared_person_id) 