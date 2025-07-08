#!/usr/bin/env python3
"""
Script para crear los alert_types y event_types necesarios para el sistema.
"""

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.alert_type import AlertType
from app.models.event_type import EventType
from datetime import datetime

def create_alert_types(db: Session):
    """Crear los tipos de alerta necesarios para el sistema"""
    
    alert_types_data = [
        {"name": "medical_emergency", "description": "Emergencia médica", "category": "health", "severity": "critical", "icon_name": "heart", "color_code": "#ef4444"},
        {"name": "fall_detected", "description": "Caída detectada", "category": "safety", "severity": "high", "icon_name": "alert-triangle", "color_code": "#f59e0b"},
        {"name": "medication_missed", "description": "Medicación omitida", "category": "health", "severity": "medium", "icon_name": "pill", "color_code": "#3b82f6"},
        {"name": "device_offline", "description": "Dispositivo desconectado", "category": "technical", "severity": "medium", "icon_name": "wifi-off", "color_code": "#6b7280"},
        {"name": "battery_low", "description": "Batería baja", "category": "technical", "severity": "low", "icon_name": "battery", "color_code": "#f59e0b"},
        {"name": "location_alert", "description": "Alerta de ubicación", "category": "safety", "severity": "high", "icon_name": "map-pin", "color_code": "#8b5cf6"},
        {"name": "vital_signs_abnormal", "description": "Signos vitales anormales", "category": "health", "severity": "high", "icon_name": "activity", "color_code": "#ef4444"},
        {"name": "appointment_reminder", "description": "Recordatorio de cita", "category": "health", "severity": "low", "icon_name": "calendar", "color_code": "#10b981"},
    ]
    
    created_count = 0
    for alert_type_data in alert_types_data:
        try:
            # Verificar si ya existe
            existing = db.query(AlertType).filter_by(
                name=alert_type_data["name"]
            ).first()
            
            if existing:
                print(f"⏭️ Ya existe: {alert_type_data['name']}")
                continue
            
            # Crear nuevo alert_type
            alert_type = AlertType(
                name=alert_type_data["name"],
                description=alert_type_data["description"],
                category=alert_type_data["category"],
                icon_name=alert_type_data["icon_name"],
                color_code=alert_type_data["color_code"],
                is_active=True
            )
            
            db.add(alert_type)
            created_count += 1
            print(f"✅ Creado: {alert_type_data['name']}")
            
        except Exception as e:
            print(f"❌ Error creando alert_type {alert_type_data['name']}: {e}")
            continue
    
    try:
        db.commit()
        print(f"\n✅ Creados {created_count} nuevos alert_types")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando alert_types: {e}")

def create_event_types(db: Session):
    """Crear los tipos de evento necesarios para el sistema"""
    
    event_types_data = [
        {"name": "device_connected", "description": "Dispositivo conectado", "category": "technical", "severity": "info", "icon_name": "wifi", "color_code": "#10b981"},
        {"name": "device_disconnected", "description": "Dispositivo desconectado", "category": "technical", "severity": "warning", "icon_name": "wifi-off", "color_code": "#f59e0b"},
        {"name": "battery_status", "description": "Estado de batería", "category": "technical", "severity": "info", "icon_name": "battery", "color_code": "#3b82f6"},
        {"name": "location_update", "description": "Actualización de ubicación", "category": "tracking", "severity": "info", "icon_name": "map-pin", "color_code": "#8b5cf6"},
        {"name": "vital_signs_reading", "description": "Lectura de signos vitales", "category": "health", "severity": "info", "icon_name": "activity", "color_code": "#06b6d4"},
        {"name": "medication_taken", "description": "Medicación tomada", "category": "health", "severity": "info", "icon_name": "check-circle", "color_code": "#10b981"},
        {"name": "medication_missed", "description": "Medicación omitida", "category": "health", "severity": "warning", "icon_name": "x-circle", "color_code": "#f59e0b"},
        {"name": "fall_detected", "description": "Caída detectada", "category": "safety", "severity": "critical", "icon_name": "alert-triangle", "color_code": "#ef4444"},
        {"name": "appointment_scheduled", "description": "Cita programada", "category": "health", "severity": "info", "icon_name": "calendar", "color_code": "#3b82f6"},
        {"name": "appointment_completed", "description": "Cita completada", "category": "health", "severity": "info", "icon_name": "check", "color_code": "#10b981"},
    ]
    
    created_count = 0
    for event_type_data in event_types_data:
        try:
            # Verificar si ya existe
            existing = db.query(EventType).filter_by(
                name=event_type_data["name"]
            ).first()
            
            if existing:
                print(f"⏭️ Ya existe: {event_type_data['name']}")
                continue
            
            # Crear nuevo event_type
            event_type = EventType(
                name=event_type_data["name"],
                description=event_type_data["description"],
                category=event_type_data["category"],
                icon_name=event_type_data["icon_name"],
                color_code=event_type_data["color_code"],
                is_active=True
            )
            
            db.add(event_type)
            created_count += 1
            print(f"✅ Creado: {event_type_data['name']}")
            
        except Exception as e:
            print(f"❌ Error creando event_type {event_type_data['name']}: {e}")
            continue
    
    try:
        db.commit()
        print(f"\n✅ Creados {created_count} nuevos event_types")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando event_types: {e}")

def main():
    print("🚀 Creando alert_types y event_types necesarios...")
    db = next(get_db())
    try:
        print("\n📋 Creando alert_types...")
        create_alert_types(db)
        
        print("\n📋 Creando event_types...")
        create_event_types(db)
        
        print("\n✅ Alert_types y event_types creados exitosamente!")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 