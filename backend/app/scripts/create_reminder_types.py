#!/usr/bin/env python3
"""
Script para crear los reminder_types necesarios para el sistema.
"""

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.reminder_type import ReminderType
from datetime import datetime

def create_reminder_types(db: Session):
    """Crear los tipos de recordatorio necesarios para el sistema"""
    
    reminder_types_data = [
        {"name": "medication", "description": "Recordatorio de medicación", "category": "health", "icon_name": "pill", "color_code": "#ef4444"},
        {"name": "appointment", "description": "Recordatorio de cita médica", "category": "health", "icon_name": "calendar", "color_code": "#3b82f6"},
        {"name": "exercise", "description": "Recordatorio de ejercicio", "category": "health", "icon_name": "activity", "color_code": "#10b981"},
        {"name": "meal", "description": "Recordatorio de comida", "category": "health", "icon_name": "utensils", "color_code": "#f59e0b"},
        {"name": "hygiene", "description": "Recordatorio de higiene personal", "category": "care", "icon_name": "shower", "color_code": "#8b5cf6"},
        {"name": "social", "description": "Recordatorio de actividad social", "category": "wellness", "icon_name": "users", "color_code": "#06b6d4"},
        {"name": "checkup", "description": "Recordatorio de revisión médica", "category": "health", "icon_name": "stethoscope", "color_code": "#84cc16"},
        {"name": "meditation", "description": "Recordatorio de meditación", "category": "wellness", "icon_name": "heart", "color_code": "#ec4899"},
    ]
    
    created_count = 0
    for reminder_type_data in reminder_types_data:
        try:
            # Verificar si ya existe
            existing = db.query(ReminderType).filter_by(
                name=reminder_type_data["name"]
            ).first()
            
            if existing:
                print(f"⏭️ Ya existe: {reminder_type_data['name']}")
                continue
            
            # Crear nuevo reminder_type
            reminder_type = ReminderType(
                name=reminder_type_data["name"],
                description=reminder_type_data["description"],
                category=reminder_type_data["category"],
                icon_name=reminder_type_data["icon_name"],
                color_code=reminder_type_data["color_code"],
                is_active=True
            )
            
            db.add(reminder_type)
            created_count += 1
            print(f"✅ Creado: {reminder_type_data['name']}")
            
        except Exception as e:
            print(f"❌ Error creando reminder_type {reminder_type_data['name']}: {e}")
            continue
    
    try:
        db.commit()
        print(f"\n✅ Creados {created_count} nuevos reminder_types")
        print("✅ Reminder_types creados exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando reminder_types: {e}")

def main():
    print("🚀 Creando reminder_types necesarios...")
    db = next(get_db())
    try:
        create_reminder_types(db)
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 