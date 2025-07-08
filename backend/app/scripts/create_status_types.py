#!/usr/bin/env python3
"""
Script para crear los status_types necesarios para el sistema.
"""

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.status_type import StatusType
from datetime import datetime

def create_status_types(db: Session):
    """Crear los tipos de estado necesarios para el sistema"""
    
    status_types_data = [
        # Alert status types
        {"name": "active", "description": "Alerta activa y pendiente de atención", "category": "alert_status"},
        {"name": "acknowledged", "description": "Alerta reconocida por el personal", "category": "alert_status"},
        {"name": "resolved", "description": "Alerta resuelta", "category": "alert_status"},
        {"name": "dismissed", "description": "Alerta descartada", "category": "alert_status"},
        {"name": "escalated", "description": "Alerta escalada a nivel superior", "category": "alert_status"},
        
        # Reminder status types
        {"name": "pending", "description": "Recordatorio pendiente", "category": "reminder_status"},
        {"name": "completed", "description": "Recordatorio completado", "category": "reminder_status"},
        {"name": "missed", "description": "Recordatorio perdido", "category": "reminder_status"},
        {"name": "cancelled", "description": "Recordatorio cancelado", "category": "reminder_status"},
        {"name": "snoozed", "description": "Recordatorio pospuesto", "category": "reminder_status"},
        
        # Device status types
        {"name": "active", "description": "Dispositivo activo y funcionando", "category": "device_status"},
        {"name": "inactive", "description": "Dispositivo inactivo", "category": "device_status"},
        {"name": "maintenance", "description": "Dispositivo en mantenimiento", "category": "device_status"},
        {"name": "error", "description": "Dispositivo con error", "category": "device_status"},
        {"name": "offline", "description": "Dispositivo desconectado", "category": "device_status"},
        {"name": "testing", "description": "Dispositivo en pruebas", "category": "device_status"},
    ]
    
    created_count = 0
    for status_data in status_types_data:
        try:
            # Verificar si ya existe
            existing = db.query(StatusType).filter_by(
                name=status_data["name"], 
                category=status_data["category"]
            ).first()
            
            if not existing:
                status_type = StatusType(
                    name=status_data["name"],
                    description=status_data["description"],
                    category=status_data["category"],
                    is_active=True
                )
                db.add(status_type)
                db.flush()  # Flush individual para evitar conflictos
                created_count += 1
                print(f"✅ Creado: {status_data['category']} - {status_data['name']}")
            else:
                print(f"⏭️ Ya existe: {status_data['category']} - {status_data['name']}")
                
        except Exception as e:
            print(f"❌ Error creando {status_data['name']}: {e}")
            db.rollback()
            continue
    
    try:
        db.commit()
        print(f"\n✅ Creados {created_count} nuevos status_types")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando status_types: {e}")
        return False
    
    return True

def main():
    print("🚀 Creando status_types necesarios...")
    db = next(get_db())
    
    try:
        success = create_status_types(db)
        if success:
            print("✅ Status_types creados exitosamente!")
        else:
            print("❌ Error creando status_types")
    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 