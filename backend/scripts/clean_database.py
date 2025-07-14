#!/usr/bin/env python3
"""
Limpieza completa de la base de datos de prueba
- Borra todas las entidades principales
- Mantiene la estructura de tablas
- Listo para nueva carga de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

def clean_database():
    db: Session = next(get_db())
    try:
        print("🧹 Limpiando base de datos de prueba...")
        
        # Tablas a limpiar en orden (respetando foreign keys)
        tables_to_clean = [
            # Entidades dependientes primero
            "user_package_history",
            "cared_person_institutions", 
            "user_roles",
            "institution_reviews",
            "institution_scores",
            "shift_observations",
            "restraint_protocols",
            "medication_logs",
            "activity_participations",
            "alerts",
            "events",
            "reminders",
            "medical_referrals",
            "vital_signs",
            "diagnoses",
            "devices",
            "caregiver_assignments",
            
            # Entidades principales
            "cared_persons",
            "users",
            "packages", 
            "institutions",
            "roles",
            
            # Catálogos (opcional - mantener algunos básicos)
            # "status_types",
            # "service_types", 
            # "alert_types",
            # "event_types",
            # "reminder_types",
            # "referral_types",
            # "device_types",
            # "activity_types",
            # "shift_observation_types",
            # "medication_types",
            # "diagnosis_types",
            # "vital_sign_types",
        ]
        
        cleaned_count = 0
        for table in tables_to_clean:
            try:
                result = db.execute(text(f"DELETE FROM {table}"))
                count = result.rowcount
                if count > 0:
                    print(f"  🗑️ {table}: {count} registros eliminados")
                    cleaned_count += count
                else:
                    print(f"  ⚪ {table}: sin datos")
            except Exception as e:
                print(f"  ⚠️ Error en {table}: {e}")
                continue
        
        db.commit()
        print(f"\n✅ Limpieza completada: {cleaned_count} registros eliminados")
        
        # Verificar estado
        print("\n📊 Estado de la base de datos:")
        for table in ["users", "institutions", "packages", "roles", "cared_persons"]:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"  📋 {table}: {count} registros")
            except Exception as e:
                print(f"  ❌ {table}: error - {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_database() 