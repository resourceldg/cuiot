from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import Dict, Any
from datetime import datetime, timedelta
import psutil
import os

from app.core.database import get_db
from app.models.user import User
from app.models.elderly_person import ElderlyPerson
from app.models.device import Device
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.event import Event

router = APIRouter()

@router.get("/")
async def health_check():
    """
    Endpoint básico de verificación de salud del sistema
    
    Retorna información básica sobre el estado del API
    """
    return {
        "status": "healthy",
        "message": "Viejos Son Los Trapos API funcionando correctamente",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@router.get("/db")
async def database_health_check(db: Session = Depends(get_db)):
    """
    Verificar conexión y estado de la base de datos
    
    Incluye:
    - Conexión a PostgreSQL
    - Tiempo de respuesta
    - Estado de las tablas principales
    """
    try:
        start_time = datetime.utcnow()
        
        # Verificar conexión básica
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        
        # Calcular tiempo de respuesta
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Obtener información de la base de datos
        db_info = db.execute(text("SELECT version()")).fetchone()
        db_version = db_info[0] if db_info else "Unknown"
        
        # Verificar tablas principales
        tables_status = {}
        tables = ["users", "elderly_persons", "devices", "alerts", "reminders", "events"]
        
        for table in tables:
            try:
                count_result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = count_result.fetchone()[0]
                tables_status[table] = {"status": "ok", "count": count}
            except Exception as e:
                tables_status[table] = {"status": "error", "error": str(e)}
        
        return {
            "status": "healthy",
            "database": {
                "connection": "connected",
                "version": db_version,
                "response_time_ms": round(response_time * 1000, 2),
                "tables": tables_status
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": {
                "connection": "disconnected",
                "error": str(e)
            },
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/system")
async def system_health_check():
    """
    Verificar estado del sistema operativo y recursos
    
    Incluye:
    - Uso de CPU y memoria
    - Espacio en disco
    - Información del proceso
    """
    try:
        # Información del sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Información del proceso actual
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        return {
            "status": "healthy",
            "system": {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": round((disk.used / disk.total) * 100, 2)
                },
                "process": {
                    "memory_mb": round(process_memory.rss / (1024**2), 2),
                    "cpu_percent": process.cpu_percent(),
                    "threads": process.num_threads()
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "system": {
                "error": str(e)
            },
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/stats")
async def system_statistics(db: Session = Depends(get_db)):
    """
    Obtener estadísticas del sistema
    
    Incluye:
    - Conteos de entidades principales
    - Alertas activas y críticas
    - Recordatorios activos
    - Dispositivos conectados
    """
    try:
        # Conteos básicos
        users_count = db.query(User).count()
        elderly_count = db.query(ElderlyPerson).count()
        devices_count = db.query(Device).count()
        alerts_count = db.query(Alert).count()
        reminders_count = db.query(Reminder).count()
        events_count = db.query(Event).count()
        
        # Alertas por estado
        unresolved_alerts = db.query(Alert).filter(Alert.is_resolved == False).count()
        critical_alerts = db.query(Alert).filter(
            Alert.severity == "critical",
            Alert.is_resolved == False
        ).count()
        
        # Recordatorios activos
        active_reminders = db.query(Reminder).filter(Reminder.is_active == True).count()
        
        # Dispositivos conectados
        connected_devices = db.query(Device).filter(Device.is_online == True).count()
        
        # Alertas de las últimas 24 horas
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_alerts = db.query(Alert).filter(Alert.created_at >= yesterday).count()
        
        return {
            "status": "healthy",
            "statistics": {
                "entities": {
                    "users": users_count,
                    "elderly_persons": elderly_count,
                    "devices": devices_count,
                    "alerts": alerts_count,
                    "reminders": reminders_count,
                    "events": events_count
                },
                "alerts": {
                    "total": alerts_count,
                    "unresolved": unresolved_alerts,
                    "critical": critical_alerts,
                    "last_24h": recent_alerts
                },
                "reminders": {
                    "total": reminders_count,
                    "active": active_reminders
                },
                "devices": {
                    "total": devices_count,
                    "connected": connected_devices,
                    "connection_rate": round((connected_devices / devices_count * 100) if devices_count > 0 else 0, 2)
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "statistics": {
                "error": str(e)
            },
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/full")
async def full_health_check(db: Session = Depends(get_db)):
    """
    Verificación completa de salud del sistema
    
    Combina todas las verificaciones en un solo endpoint
    """
    try:
        # Obtener todas las verificaciones
        basic_health = await health_check()
        db_health = await database_health_check(db)
        system_health = await system_health_check()
        stats = await system_statistics(db)
        
        # Determinar estado general
        overall_status = "healthy"
        if (db_health["status"] == "unhealthy" or 
            system_health["status"] == "unhealthy" or
            stats["status"] == "unhealthy"):
            overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "checks": {
                "basic": basic_health,
                "database": db_health,
                "system": system_health,
                "statistics": stats
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/ping")
async def ping():
    """
    Endpoint simple de ping para verificar que el servicio está respondiendo
    
    Útil para health checks de load balancers y monitoreo
    """
    return {
        "pong": True,
        "timestamp": datetime.utcnow().isoformat()
    } 