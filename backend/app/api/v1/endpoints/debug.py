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


@router.post(
    "/generate-test-data",
    summary="Generar datos de prueba para debug",
    description="""
    Genera un conjunto completo de datos de prueba para desarrollo y testing del frontend.
    Incluye persona bajo cuidado, ubicaciones simuladas, eventos de debug, geofences y un protocolo de emergencia.
    Permite probar flujos de monitoreo, alertas y protocolos sin dispositivos IoT ni app móvil.
    """
)
def generate_test_data(user_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    data = utilities.generate_test_data(user_id)
    return {
        "cared_person_id": str(data["cared_person"].id),
        "geofences": [str(g.id) for g in data["geofences"]],
        "events": [str(e.id) for e in data["events"]],
        "locations": [str(l.id) for l in data["locations"]],
        "protocol_id": str(data["protocol"].id)
    }


@router.post(
    "/cleanup-test-data",
    summary="Limpiar datos de prueba para una persona",
    description="""
    Elimina todos los datos de prueba generados para una persona bajo cuidado: ubicaciones, eventos, geofences y la persona.
    Útil para limpiar el entorno de testing antes de nuevas pruebas o para evitar contaminación de datos.
    """
)
def cleanup_test_data(cared_person_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    utilities.cleanup_test_data(cared_person_id)
    return {"detail": "Datos de prueba eliminados"}


@router.get(
    "/debug-events",
    response_model=List[dict],
    summary="Listar eventos de debug",
    description="""
    Lista los eventos simulados de debug asociados a una persona bajo cuidado.
    Permite filtrar por tipo de evento y limitar la cantidad de resultados.
    Útil para visualizar y testear flujos de alertas y protocolos desde el frontend.
    """
)
def list_debug_events(
    cared_person_id: Optional[uuid.UUID] = Query(None, description="ID de la persona bajo cuidado"),
    event_type: Optional[str] = Query(None, description="Tipo de evento de debug (fall, medical, etc.)"),
    limit: int = Query(100, le=200, description="Máximo de resultados a devolver (default 100, máximo 200)"),
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


@router.get(
    "/locations",
    response_model=List[dict],
    summary="Listar ubicaciones de debug",
    description="""
    Lista las ubicaciones simuladas o de debug asociadas a una persona bajo cuidado.
    Permite probar visualización de mapas, trayectorias y lógica de geofences en el frontend.
    """
)
def list_debug_locations(
    cared_person_id: uuid.UUID = Query(..., description="ID de la persona bajo cuidado"),
    limit: int = Query(100, le=200, description="Máximo de resultados a devolver (default 100, máximo 200)"),
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


@router.get(
    "/geofences",
    response_model=List[dict],
    summary="Listar geofences de debug",
    description="""
    Lista las zonas de seguridad (geofences) de debug asociadas a una persona bajo cuidado.
    Permite probar lógica de entrada/salida de zonas, alertas y visualización en mapas.
    """
)
def list_debug_geofences(
    cared_person_id: Optional[uuid.UUID] = Query(None, description="ID de la persona bajo cuidado (opcional)"),
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


@router.get(
    "/summary",
    summary="Resumen de datos de debug",
    description="""
    Devuelve un resumen de los datos de debug generados para una persona bajo cuidado:
    cantidad de ubicaciones, eventos, geofences, última ubicación y último evento.
    Útil para monitorear el estado del entorno de pruebas.
    """
)
def debug_summary(cared_person_id: uuid.UUID = Query(..., description="ID de la persona bajo cuidado"), utilities: DebugUtilities = Depends(get_utilities)):
    return utilities.get_debug_summary(cared_person_id) 