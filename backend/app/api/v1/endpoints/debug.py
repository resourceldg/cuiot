from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models import DebugEvent, LocationTracking, Geofence, CaredPerson
from app.scripts.debug_utilities import DebugUtilities

router = APIRouter(prefix="/debug", tags=["debug"])


# Modelos de respuesta para OpenAPI/Swagger
class DebugEventResponse(BaseModel):
    id: str = Field(..., description="ID único del evento de debug")
    event_type: str = Field(..., description="Tipo de evento (fall, medical, emergency, etc.)")
    severity_level: str = Field(..., description="Nivel de severidad (low, medium, high, critical)")
    created_at: datetime = Field(..., description="Fecha y hora de creación del evento")
    description: str = Field(..., description="Descripción detallada del evento")
    test_scenario: str = Field(..., description="Escenario de prueba que generó este evento")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "fall",
                "severity_level": "high",
                "created_at": "2024-01-15T10:30:00Z",
                "description": "Simulación de caída detectada por sensores",
                "test_scenario": "fall_detection_test"
            }
        }


class LocationResponse(BaseModel):
    id: str = Field(..., description="ID único de la ubicación")
    latitude: float = Field(..., description="Latitud de la ubicación")
    longitude: float = Field(..., description="Longitud de la ubicación")
    created_at: datetime = Field(..., description="Fecha y hora de la ubicación")
    source_type: str = Field(..., description="Tipo de fuente (gps, wifi, manual, debug)")
    is_debug: bool = Field(..., description="Indica si es una ubicación de debug")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "latitude": -34.6037,
                "longitude": -58.3816,
                "created_at": "2024-01-15T10:30:00Z",
                "source_type": "debug",
                "is_debug": True
            }
        }


class GeofenceResponse(BaseModel):
    id: str = Field(..., description="ID único del geofence")
    name: str = Field(..., description="Nombre de la zona de seguridad")
    type: str = Field(..., description="Tipo de geofence (home, hospital, safe_zone, etc.)")
    latitude: float = Field(..., description="Latitud del centro del geofence")
    longitude: float = Field(..., description="Longitud del centro del geofence")
    radius: float = Field(..., description="Radio del geofence en metros")
    is_active: bool = Field(..., description="Indica si el geofence está activo")
    is_debug: bool = Field(..., description="Indica si es un geofence de debug")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Casa de María",
                "type": "home",
                "latitude": -34.6037,
                "longitude": -58.3816,
                "radius": 100.0,
                "is_active": True,
                "is_debug": True
            }
        }


class TestDataGenerationResponse(BaseModel):
    cared_person_id: str = Field(..., description="ID de la persona bajo cuidado creada")
    geofences: List[str] = Field(..., description="Lista de IDs de geofences creados")
    events: List[str] = Field(..., description="Lista de IDs de eventos creados")
    locations: List[str] = Field(..., description="Lista de IDs de ubicaciones creadas")
    protocol_id: str = Field(..., description="ID del protocolo de emergencia creado")

    class Config:
        schema_extra = {
            "example": {
                "cared_person_id": "550e8400-e29b-41d4-a716-446655440003",
                "geofences": ["550e8400-e29b-41d4-a716-446655440004"],
                "events": ["550e8400-e29b-41d4-a716-446655440005"],
                "locations": ["550e8400-e29b-41d4-a716-446655440006"],
                "protocol_id": "550e8400-e29b-41d4-a716-446655440007"
            }
        }


class DebugSummaryResponse(BaseModel):
    cared_person_name: str = Field(..., description="Nombre de la persona bajo cuidado")
    total_locations: int = Field(..., description="Total de ubicaciones registradas")
    total_events: int = Field(..., description="Total de eventos registrados")
    total_geofences: int = Field(..., description="Total de geofences configurados")
    last_location: Optional[dict] = Field(None, description="Última ubicación registrada")
    last_event: Optional[dict] = Field(None, description="Último evento registrado")
    created_at: datetime = Field(..., description="Fecha de creación de los datos de prueba")

    class Config:
        schema_extra = {
            "example": {
                "cared_person_name": "María González",
                "total_locations": 25,
                "total_events": 3,
                "total_geofences": 2,
                "last_location": {
                    "latitude": -34.6037,
                    "longitude": -58.3816,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "last_event": {
                    "event_type": "fall",
                    "severity_level": "high",
                    "created_at": "2024-01-15T10:25:00Z"
                },
                "created_at": "2024-01-15T10:00:00Z"
            }
        }


def get_utilities(db: Session = Depends(get_db)):
    return DebugUtilities(db)


@router.post(
    "/generate-test-data",
    response_model=TestDataGenerationResponse,
    summary="Generar datos de prueba para debug",
    description="""
    **Genera un conjunto completo de datos de prueba para desarrollo y testing del frontend.**
    
    ### ¿Qué incluye?
    - **Persona bajo cuidado**: Con datos realistas y protocolo de emergencia asociado
    - **Ubicaciones simuladas**: Trayectoria realista de movimientos durante el día
    - **Eventos de debug**: Caídas, emergencias médicas, salidas de zona segura
    - **Geofences**: Zonas de seguridad (casa, hospital, áreas seguras)
    - **Protocolo de emergencia**: Configurado para la persona creada
    
    ### Casos de uso
    - Probar flujos de monitoreo sin dispositivos IoT
    - Testear alertas y notificaciones
    - Validar protocolos de emergencia
    - Desarrollar visualizaciones de mapas y trayectorias
    - Simular diferentes escenarios de cuidado
    
    ### Parámetros
    - `user_id`: ID del usuario que solicita la generación (debe existir en el sistema)
    
    ### Respuesta
    Retorna los IDs de todos los elementos creados para facilitar el testing posterior.
    """,
    responses={
        200: {
            "description": "Datos de prueba generados exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "cared_person_id": "550e8400-e29b-41d4-a716-446655440003",
                        "geofences": ["550e8400-e29b-41d4-a716-446655440004"],
                        "events": ["550e8400-e29b-41d4-a716-446655440005"],
                        "locations": ["550e8400-e29b-41d4-a716-446655440006"],
                        "protocol_id": "550e8400-e29b-41d4-a716-446655440007"
                    }
                }
            }
        },
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Usuario no encontrado"}
                }
            }
        }
    }
)
def generate_test_data(user_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    """
    Genera datos de prueba completos para una persona bajo cuidado.
    
    Args:
        user_id: ID del usuario que solicita la generación
        utilities: Utilidades de debug inyectadas por FastAPI
        
    Returns:
        TestDataGenerationResponse: IDs de todos los elementos creados
        
    Raises:
        HTTPException: Si el usuario no existe
    """
    data = utilities.generate_test_data(user_id)
    return TestDataGenerationResponse(
        cared_person_id=str(data["cared_person"].id),
        geofences=[str(g.id) for g in data["geofences"]],
        events=[str(e.id) for e in data["events"]],
        locations=[str(l.id) for l in data["locations"]],
        protocol_id=str(data["protocol"].id)
    )


@router.post(
    "/cleanup-test-data",
    summary="Limpiar datos de prueba para una persona",
    description="""
    **Elimina todos los datos de prueba generados para una persona bajo cuidado.**
    
    ### ¿Qué elimina?
    - Todas las ubicaciones de debug asociadas
    - Todos los eventos de debug asociados
    - Todos los geofences de debug asociados
    - La persona bajo cuidado (si fue creada para debug)
    - Protocolos de emergencia asociados
    
    ### Casos de uso
    - Limpiar el entorno antes de nuevas pruebas
    - Evitar contaminación de datos entre tests
    - Resetear el estado del sistema para demos
    - Mantener la base de datos limpia en desarrollo
    
    ### Parámetros
    - `cared_person_id`: ID de la persona bajo cuidado a limpiar
    
    ### ⚠️ Advertencia
    Esta operación es **irreversible**. Todos los datos de debug se eliminan permanentemente.
    """,
    responses={
        200: {
            "description": "Datos de prueba eliminados exitosamente",
            "content": {
                "application/json": {
                    "example": {"detail": "Datos de prueba eliminados"}
                }
            }
        },
        404: {
            "description": "Persona bajo cuidado no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Persona bajo cuidado no encontrada"}
                }
            }
        }
    }
)
def cleanup_test_data(cared_person_id: uuid.UUID, utilities: DebugUtilities = Depends(get_utilities)):
    """
    Elimina todos los datos de prueba para una persona bajo cuidado.
    
    Args:
        cared_person_id: ID de la persona bajo cuidado
        utilities: Utilidades de debug inyectadas por FastAPI
        
    Returns:
        dict: Confirmación de eliminación
        
    Raises:
        HTTPException: Si la persona no existe
    """
    utilities.cleanup_test_data(cared_person_id)
    return {"detail": "Datos de prueba eliminados"}


@router.get(
    "/debug-events",
    response_model=List[DebugEventResponse],
    summary="Listar eventos de debug",
    description="""
    **Lista los eventos simulados de debug asociados a una persona bajo cuidado.**
    
    ### Tipos de eventos disponibles
    - `fall`: Simulación de caída
    - `medical`: Emergencia médica
    - `emergency`: Situación de emergencia general
    - `geofence_exit`: Salida de zona segura
    - `geofence_entry`: Entrada a zona segura
    - `device_offline`: Dispositivo desconectado
    - `battery_low`: Batería baja
    
    ### Niveles de severidad
    - `low`: Evento menor, no requiere acción inmediata
    - `medium`: Evento moderado, requiere atención
    - `high`: Evento importante, requiere acción rápida
    - `critical`: Evento crítico, requiere acción inmediata
    
    ### Filtros disponibles
    - `cared_person_id`: Filtrar por persona específica
    - `event_type`: Filtrar por tipo de evento
    - `limit`: Limitar cantidad de resultados (máximo 200)
    
    ### Casos de uso
    - Visualizar historial de eventos en el frontend
    - Testear flujos de alertas y notificaciones
    - Validar protocolos de emergencia
    - Analizar patrones de comportamiento
    """,
    responses={
        200: {
            "description": "Lista de eventos de debug",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "event_type": "fall",
                            "severity_level": "high",
                            "created_at": "2024-01-15T10:30:00Z",
                            "description": "Simulación de caída detectada por sensores",
                            "test_scenario": "fall_detection_test"
                        }
                    ]
                }
            }
        }
    }
)
def list_debug_events(
    cared_person_id: Optional[uuid.UUID] = Query(None, description="ID de la persona bajo cuidado (opcional)"),
    event_type: Optional[str] = Query(None, description="Tipo de evento de debug (fall, medical, emergency, etc.)"),
    limit: int = Query(100, le=200, description="Máximo de resultados a devolver (default 100, máximo 200)"),
    db: Session = Depends(get_db)
):
    """
    Lista eventos de debug con filtros opcionales.
    
    Args:
        cared_person_id: ID de la persona bajo cuidado (opcional)
        event_type: Tipo de evento a filtrar (opcional)
        limit: Límite de resultados (máximo 200)
        db: Sesión de base de datos
        
    Returns:
        List[DebugEventResponse]: Lista de eventos de debug
    """
    events = DebugEvent.get_debug_events(
        db, 
        cared_person_id=cared_person_id, 
        event_type=event_type, 
        limit=limit
    )
    return [
        DebugEventResponse(
            id=str(e.id),
            event_type=e.event_type,
            severity_level=e.severity_level,
            created_at=e.created_at,
            description=e.description,
            test_scenario=e.test_scenario
        ) for e in events
    ]


@router.get(
    "/locations",
    response_model=List[LocationResponse],
    summary="Listar ubicaciones de debug",
    description="""
    **Lista las ubicaciones simuladas o de debug asociadas a una persona bajo cuidado.**
    
    ### Tipos de fuente
    - `gps`: Ubicación GPS real
    - `wifi`: Ubicación por WiFi
    - `manual`: Ubicación ingresada manualmente
    - `debug`: Ubicación simulada para testing
    
    ### Casos de uso
    - Visualizar trayectorias en mapas
    - Probar lógica de geofences
    - Analizar patrones de movimiento
    - Validar algoritmos de tracking
    - Simular diferentes escenarios de ubicación
    
    ### Parámetros
    - `cared_person_id`: ID de la persona bajo cuidado (requerido)
    - `limit`: Límite de resultados (máximo 200)
    
    ### Ordenamiento
    Los resultados se ordenan por fecha de creación (más recientes primero).
    """,
    responses={
        200: {
            "description": "Lista de ubicaciones de debug",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440001",
                            "latitude": -34.6037,
                            "longitude": -58.3816,
                            "created_at": "2024-01-15T10:30:00Z",
                            "source_type": "debug",
                            "is_debug": True
                        }
                    ]
                }
            }
        },
        400: {
            "description": "ID de persona bajo cuidado requerido",
            "content": {
                "application/json": {
                    "example": {"detail": "cared_person_id es requerido"}
                }
            }
        }
    }
)
def list_debug_locations(
    cared_person_id: uuid.UUID = Query(..., description="ID de la persona bajo cuidado"),
    limit: int = Query(100, le=200, description="Máximo de resultados a devolver (default 100, máximo 200)"),
    db: Session = Depends(get_db)
):
    """
    Lista ubicaciones de debug para una persona bajo cuidado.
    
    Args:
        cared_person_id: ID de la persona bajo cuidado
        limit: Límite de resultados (máximo 200)
        db: Sesión de base de datos
        
    Returns:
        List[LocationResponse]: Lista de ubicaciones de debug
    """
    locations = LocationTracking.get_debug_locations(db, cared_person_id)
    return [
        LocationResponse(
            id=str(l.id),
            latitude=l.latitude,
            longitude=l.longitude,
            created_at=l.created_at,
            source_type=l.source_type,
            is_debug=l.is_debug
        ) for l in locations[:limit]
    ]


@router.get(
    "/geofences",
    response_model=List[GeofenceResponse],
    summary="Listar geofences de debug",
    description="""
    **Lista las zonas de seguridad (geofences) de debug asociadas a una persona bajo cuidado.**
    
    ### Tipos de geofence
    - `home`: Zona del hogar
    - `hospital`: Zona de hospital o centro médico
    - `safe_zone`: Zona segura predefinida
    - `custom`: Zona personalizada
    
    ### Casos de uso
    - Visualizar zonas de seguridad en mapas
    - Probar lógica de entrada/salida de zonas
    - Validar alertas de geofence
    - Configurar nuevas zonas de seguridad
    - Simular diferentes escenarios de geofence
    
    ### Parámetros
    - `cared_person_id`: ID de la persona bajo cuidado (opcional, si no se proporciona lista todos)
    - `limit`: Límite de resultados (máximo 200)
    
    ### Información adicional
    - Solo geofences activos se consideran para alertas
    - Los geofences de debug se marcan con `is_debug: true`
    - El radio se especifica en metros
    """,
    responses={
        200: {
            "description": "Lista de geofences de debug",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440002",
                            "name": "Casa de María",
                            "type": "home",
                            "latitude": -34.6037,
                            "longitude": -58.3816,
                            "radius": 100.0,
                            "is_active": True,
                            "is_debug": True
                        }
                    ]
                }
            }
        }
    }
)
def list_debug_geofences(
    cared_person_id: Optional[uuid.UUID] = Query(None, description="ID de la persona bajo cuidado (opcional)"),
    db: Session = Depends(get_db)
):
    """
    Lista geofences de debug, opcionalmente filtrados por persona.
    
    Args:
        cared_person_id: ID de la persona bajo cuidado (opcional)
        db: Sesión de base de datos
        
    Returns:
        List[GeofenceResponse]: Lista de geofences de debug
    """
    geofences = Geofence.get_debug_geofences(db, cared_person_id=cared_person_id)
    return [
        GeofenceResponse(
            id=str(g.id),
            name=g.name,
            type=g.geofence_type,
            latitude=g.latitude,
            longitude=g.longitude,
            radius=g.radius,
            is_active=g.is_active,
            is_debug=g.is_debug
        ) for g in geofences
    ]


@router.get(
    "/summary",
    response_model=DebugSummaryResponse,
    summary="Resumen de datos de debug",
    description="""
    **Devuelve un resumen completo de los datos de debug generados para una persona bajo cuidado.**
    
    ### Información incluida
    - **Estadísticas generales**: Cantidad de ubicaciones, eventos y geofences
    - **Última ubicación**: Coordenadas y timestamp de la ubicación más reciente
    - **Último evento**: Detalles del evento más reciente registrado
    - **Información de la persona**: Nombre y fecha de creación de datos
    
    ### Casos de uso
    - Dashboard de resumen para desarrollo
    - Monitoreo del estado del entorno de pruebas
    - Validación de datos generados
    - Verificación de integridad de datos de debug
    - Resumen para demos y presentaciones
    
    ### Parámetros
    - `cared_person_id`: ID de la persona bajo cuidado (requerido)
    
    ### Información adicional
    - Si no hay ubicaciones o eventos, esos campos serán `null`
    - La fecha de creación corresponde al momento en que se generaron los datos de prueba
    """,
    responses={
        200: {
            "description": "Resumen de datos de debug",
            "content": {
                "application/json": {
                    "example": {
                        "cared_person_name": "María González",
                        "total_locations": 25,
                        "total_events": 3,
                        "total_geofences": 2,
                        "last_location": {
                            "latitude": -34.6037,
                            "longitude": -58.3816,
                            "created_at": "2024-01-15T10:30:00Z"
                        },
                        "last_event": {
                            "event_type": "fall",
                            "severity_level": "high",
                            "created_at": "2024-01-15T10:25:00Z"
                        },
                        "created_at": "2024-01-15T10:00:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Persona bajo cuidado no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Persona bajo cuidado no encontrada"}
                }
            }
        }
    }
)
def debug_summary(
    cared_person_id: uuid.UUID = Query(..., description="ID de la persona bajo cuidado"), 
    utilities: DebugUtilities = Depends(get_utilities)
):
    """
    Obtiene un resumen completo de los datos de debug para una persona.
    
    Args:
        cared_person_id: ID de la persona bajo cuidado
        utilities: Utilidades de debug inyectadas por FastAPI
        
    Returns:
        DebugSummaryResponse: Resumen completo de datos de debug
        
    Raises:
        HTTPException: Si la persona no existe
    """
    return utilities.get_debug_summary(cared_person_id) 