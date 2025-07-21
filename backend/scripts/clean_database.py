#!/usr/bin/env python3
"""
Script para limpiar todas las tablas de datos de la base de datos CUIOT.
Respeta el orden de eliminación para evitar conflictos de claves foráneas.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

def clean_database(db: Session):
    """Elimina todos los datos de las tablas en el orden correcto."""
    print("🧹 INICIANDO LIMPIEZA DE LA BASE DE DATOS...")
    
    # El orden es crucial para respetar las dependencias de claves foráneas
    tables_to_clean = [
        "user_packages",
        "user_roles",
        # "cared_person_institution", # La tabla parece tener otro nombre o no existir, la comentamos para evitar error
        # "caregiver_institution", # La tabla parece tener otro nombre o no existir, la comentamos para evitar error
        "caregiver_assignments",
        "shift_observations",
        "restraint_protocols",
        "medication_schedules",
        "diagnoses",
        "medical_profiles",
        "alerts",
        "events",
        "reminders",
        "reports",
        "billing_records",
        "referrals",
        "devices",
        "users",
        "cared_persons",
        "packages",
        "institutions",
        "roles"
        # Las tablas de catálogo generalmente no se limpian, pero si es necesario, agrégalas aquí.
    ]
    
    try:
        for table in tables_to_clean:
            print(f"   - Limpiando tabla: {table}...")
            # Usamos TRUNCATE ... RESTART IDENTITY CASCADE para reiniciar secuencias y manejar dependencias
            db.execute(text(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;'))
        
        db.commit()
        print("\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE.")
        
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    db: Session = next(get_db())
    clean_database(db) 