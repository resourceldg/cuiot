from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import psutil
import os
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.device import Device
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.event import Event
from app.models.institution import Institution
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.alert_type import AlertType
from app.models.status_type import StatusType
from app.services.auth import AuthService

router = APIRouter()

@router.get("/summary", tags=["dashboard"])
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    if not (current_user.has_role("admin") or current_user.has_role("institution_admin")):
        raise HTTPException(status_code=403, detail="Solo administradores pueden ver el dashboard")

    # Usuarios
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    new_users = db.query(User).filter(User.created_at >= datetime.utcnow() - timedelta(days=30)).count()

    # Personas bajo cuidado
    total_cared = db.query(CaredPerson).count()

    # Dispositivos
    total_devices = db.query(Device).count()
    active_devices = db.query(Device).filter(Device.is_active == True).count()
    offline_devices = db.query(Device).filter(Device.is_active == True, Device.last_seen < datetime.utcnow() - timedelta(hours=1)).count()

    # Alertas
    total_alerts = db.query(Alert).count()
    pending_alerts = db.query(Alert).filter(Alert.is_resolved == False).count() if hasattr(Alert, 'is_resolved') else None
    critical_alerts = db.query(Alert).filter(Alert.severity == "critical").count() if hasattr(Alert, 'severity') else None

    # Recordatorios
    total_reminders = db.query(Reminder).count()
    active_reminders = db.query(Reminder).filter(Reminder.is_active == True).count()

    # Instituciones
    total_institutions = db.query(Institution).count() if Institution else None

    # Eventos
    total_events = db.query(Event).count()

    # Ingresos (mock, para ejemplo)
    monthly_income = 120000  # Simulado
    monthly_income_change = 12.5  # Simulado

    # Uptime (mock, para ejemplo)
    uptime = 99.98

    # Recursos del sistema
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent

    return {
        "users": {
            "active": active_users,
            "total": total_users,
            "new_last_30d": new_users
        },
        "cared_persons": total_cared,
        "devices": {
            "active": active_devices,
            "total": total_devices,
            "offline": offline_devices
        },
        "alerts": {
            "total": total_alerts,
            "pending": pending_alerts,
            "critical": critical_alerts
        },
        "reminders": {
            "total": total_reminders,
            "active": active_reminders
        },
        "institutions": total_institutions,
        "events": total_events,
        "monthly_income": {
            "amount": monthly_income,
            "change_percent": monthly_income_change
        },
        "uptime": uptime,
        "system": {
            "cpu": cpu_percent,
            "memory": memory_percent
        },
        "last_update": datetime.utcnow().isoformat()
    }

@router.get("/charts")
async def get_dashboard_charts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener datos para gráficos del dashboard"""
    try:
        # Verificar si el usuario es admin
        user_roles = db.query(UserRole).filter(
            UserRole.user_id == current_user.id,
            UserRole.is_active == True
        ).all()
        
        is_admin = any(
            db.query(Role).filter(Role.id == role.role_id, Role.name == "admin").first()
            for role in user_roles
        )
        
        if not is_admin:
            raise HTTPException(status_code=403, detail="Acceso denegado")
        
        # Datos para gráfico de actividad de usuarios (últimos 7 días)
        user_activity_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            
            active_users = db.query(User).filter(
                and_(
                    User.is_active == True,
                    User.last_login >= start_date,
                    User.last_login < end_date
                )
            ).count()
            
            user_activity_data.append({
                "date": start_date.strftime("%Y-%m-%d"),
                "active_users": active_users
            })
        
        user_activity_data.reverse()  # Ordenar cronológicamente
        
        # Datos para gráfico de alertas por tipo (join con AlertType y StatusType)
        alert_types_data = (
            db.query(
                AlertType.name.label('alert_type_name'),
                func.count(Alert.id).label('count')
            )
            .join(Alert, Alert.alert_type_id == AlertType.id)
            .join(StatusType, Alert.status_type_id == StatusType.id)
            .filter(StatusType.name == "active")
            .group_by(AlertType.name)
            .all()
        )
        
        # Datos para gráfico de dispositivos por estado
        device_status_data = db.query(
            Device.status_type_id,
            func.count(Device.id).label('count')
        ).filter(
            Device.is_active == True
        ).group_by(Device.status_type_id).all()
        
        # Mapear status_type_id a nombres
        status_names = {
            1: "Activo",
            2: "Inactivo", 
            3: "Mantenimiento",
            4: "Error",
            5: "Offline"
        }
        
        # Datos para gráfico de eventos por día (últimos 7 días)
        event_activity_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            
            events_count = db.query(Event).filter(
                and_(
                    Event.is_active == True,
                    Event.created_at >= start_date,
                    Event.created_at < end_date
                )
            ).count()
            
            event_activity_data.append({
                "date": start_date.strftime("%Y-%m-%d"),
                "events": events_count
            })
        
        event_activity_data.reverse()  # Ordenar cronológicamente
        
        # Gráfico de personas bajo cuidado por nivel
        care_levels_data = (
            db.query(
                CaredPerson.care_level,
                func.count(CaredPerson.id).label('count')
            )
            .group_by(CaredPerson.care_level)
            .all()
        )
        care_levels_chart = {
            "labels": [item.care_level.capitalize() for item in care_levels_data],
            "datasets": [{
                "label": "Personas bajo Cuidado por Nivel",
                "data": [item.count for item in care_levels_data],
                "backgroundColor": [
                    "#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"
                ]
            }]
        }
        
        return {
            "user_activity": {
                "labels": [item["date"] for item in user_activity_data],
                "datasets": [{
                    "label": "Usuarios Activos",
                    "data": [item["active_users"] for item in user_activity_data],
                    "borderColor": "#3b82f6",
                    "backgroundColor": "rgba(59, 130, 246, 0.1)",
                    "tension": 0.4
                }]
            },
            "alert_types": {
                "labels": [item.alert_type_name for item in alert_types_data],
                "datasets": [{
                    "label": "Alertas por Tipo",
                    "data": [item.count for item in alert_types_data],
                    "backgroundColor": [
                        "#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"
                    ]
                }]
            },
            "device_status": {
                "labels": [status_names.get(item.status_type_id, f"Estado {item.status_type_id}") for item in device_status_data],
                "datasets": [{
                    "label": "Dispositivos por Estado",
                    "data": [item.count for item in device_status_data],
                    "backgroundColor": [
                        "#10b981", "#f59e0b", "#ef4444", "#6b7280", "#8b5cf6"
                    ]
                }]
            },
            "event_activity": {
                "labels": [item["date"] for item in event_activity_data],
                "datasets": [{
                    "label": "Eventos por Día",
                    "data": [item["events"] for item in event_activity_data],
                    "borderColor": "#10b981",
                    "backgroundColor": "rgba(16, 185, 129, 0.4)",
                    "tension": 0.4
                }]
            },
            "care_levels": care_levels_chart
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 