#!/usr/bin/env python3
"""
Script para verificar y poblar datos de testing necesarios para los tests.
"""

import sys
import os
sys.path.insert(0, '/app')

from app.core.database import get_db
from app.models.reminder_type import ReminderType
from app.models.alert_type import AlertType
from app.models.event_type import EventType
from app.models.device_type import DeviceType
from app.models.shift_observation_type import ShiftObservationType
from app.models.care_type import CareType
from app.models.status_type import StatusType

def verify_and_populate_test_data():
    """Verificar y poblar datos de testing necesarios"""
    db = next(get_db())
    
    try:
        print("🔍 Verificando datos de testing...")
        
        # Verificar ReminderTypes
        print("\n📋 Verificando ReminderTypes...")
        reminder_types = db.query(ReminderType).all()
        print(f"ReminderTypes encontrados: {len(reminder_types)}")
        for rt in reminder_types:
            print(f"  - ID: {rt.id}, Name: {rt.name}")
        
        # Verificar AlertTypes
        print("\n🚨 Verificando AlertTypes...")
        alert_types = db.query(AlertType).all()
        print(f"AlertTypes encontrados: {len(alert_types)}")
        for at in alert_types:
            print(f"  - ID: {at.id}, Name: {at.name}")
        
        # Verificar EventTypes
        print("\n📅 Verificando EventTypes...")
        event_types = db.query(EventType).all()
        print(f"EventTypes encontrados: {len(event_types)}")
        for et in event_types:
            print(f"  - ID: {et.id}, Name: {et.name}")
        
        # Verificar DeviceTypes
        print("\n📱 Verificando DeviceTypes...")
        device_types = db.query(DeviceType).all()
        print(f"DeviceTypes encontrados: {len(device_types)}")
        for dt in device_types:
            print(f"  - ID: {dt.id}, Name: {dt.name}")
        
        # Verificar ShiftObservationTypes
        print("\n👁️ Verificando ShiftObservationTypes...")
        shift_types = db.query(ShiftObservationType).all()
        print(f"ShiftObservationTypes encontrados: {len(shift_types)}")
        for st in shift_types:
            print(f"  - ID: {st.id}, Name: {st.name}")
        
        # Verificar CareTypes
        print("\n🏥 Verificando CareTypes...")
        care_types = db.query(CareType).all()
        print(f"CareTypes encontrados: {len(care_types)}")
        for ct in care_types:
            print(f"  - ID: {ct.id}, Name: {ct.name}")
        
        # Verificar StatusTypes
        print("\n📊 Verificando StatusTypes...")
        status_types = db.query(StatusType).all()
        print(f"StatusTypes encontrados: {len(status_types)}")
        for st in status_types:
            print(f"  - ID: {st.id}, Name: {st.name}, Category: {st.category}")
        
        print("\n✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    verify_and_populate_test_data() 