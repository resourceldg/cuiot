#!/usr/bin/env python3
"""
Script para poblar datos de testing necesarios para los tests.
"""

import sys
import os
sys.path.insert(0, '/app')

from app.core.database import get_db
from app.models.care_type import CareType
from app.models.status_type import StatusType
from app.models.shift_observation_type import ShiftObservationType

def populate_test_data():
    """Poblar datos de testing necesarios"""
    db = next(get_db())
    
    try:
        print("🔧 Poblando datos de testing...")
        
        # Poblar CareTypes
        print("\n🏥 Poblando CareTypes...")
        care_types_data = [
            {"name": "delegated", "description": "Delegated care"},
            {"name": "direct", "description": "Direct care"},
            {"name": "supervised", "description": "Supervised care"},
            {"name": "independent", "description": "Independent care"}
        ]
        
        for care_data in care_types_data:
            existing = db.query(CareType).filter(CareType.name == care_data["name"]).first()
            if not existing:
                care_type = CareType(**care_data)
                db.add(care_type)
                print(f"  ✅ Creado: {care_data['name']}")
            else:
                print(f"  ⏭️  Ya existe: {care_data['name']}")
        
        # Poblar StatusTypes
        print("\n📊 Poblando StatusTypes...")
        status_types_data = [
            {"name": "active", "description": "Active status", "category": "general"},
            {"name": "inactive", "description": "Inactive status", "category": "general"},
            {"name": "pending", "description": "Pending status", "category": "general"},
            {"name": "completed", "description": "Completed status", "category": "general"},
            {"name": "cancelled", "description": "Cancelled status", "category": "general"},
            {"name": "draft", "description": "Draft status", "category": "general"},
            {"name": "verified", "description": "Verified status", "category": "general"},
            {"name": "suspended", "description": "Suspended status", "category": "general"},
            {"name": "expired", "description": "Expired status", "category": "general"},
            {"name": "approved", "description": "Approved status", "category": "general"},
            {"name": "rejected", "description": "Rejected status", "category": "general"},
            {"name": "in_progress", "description": "In progress status", "category": "general"},
            {"name": "on_hold", "description": "On hold status", "category": "general"},
            {"name": "resolved", "description": "Resolved status", "category": "general"},
            {"name": "escalated", "description": "Escalated status", "category": "general"}
        ]
        
        for status_data in status_types_data:
            existing = db.query(StatusType).filter(StatusType.name == status_data["name"]).first()
            if not existing:
                status_type = StatusType(**status_data)
                db.add(status_type)
                print(f"  ✅ Creado: {status_data['name']}")
            else:
                print(f"  ⏭️  Ya existe: {status_data['name']}")
        
        # Poblar ShiftObservationTypes adicionales si no existen
        print("\n👁️ Verificando ShiftObservationTypes...")
        shift_types_data = [
            {"name": "morning", "description": "Morning shift"},
            {"name": "afternoon", "description": "Afternoon shift"},
            {"name": "night", "description": "Night shift"}
        ]
        
        for shift_data in shift_types_data:
            existing = db.query(ShiftObservationType).filter(ShiftObservationType.name == shift_data["name"]).first()
            if not existing:
                shift_type = ShiftObservationType(**shift_data)
                db.add(shift_type)
                print(f"  ✅ Creado: {shift_data['name']}")
            else:
                print(f"  ⏭️  Ya existe: {shift_data['name']}")
        
        # Commit changes
        db.commit()
        print("\n✅ Datos de testing poblados correctamente")
        
    except Exception as e:
        print(f"❌ Error durante el poblamiento: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_test_data() 