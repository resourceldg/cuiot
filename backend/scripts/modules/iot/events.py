#!/usr/bin/env python3
"""
Módulo de eventos IoT
Poblar eventos del sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.event_type import EventType
from utils.data_generators import DataGenerator

def populate_events(db: Session, devices_data=None, existing_data=None):
    """
    Poblar eventos del sistema IoT
    
    Args:
        db: Sesión de base de datos
        devices_data: Datos de dispositivos creados
        existing_data: Datos existentes (tipos de evento)
    
    Returns:
        dict: Eventos creados
    """
    print("   📊 Poblando eventos IoT...")
    
    # Obtener datos existentes
    event_types = existing_data.get("event_types", {}) if existing_data else {}
    devices = devices_data.get("devices", {}) if devices_data else {}
    
    # Si no hay datos existentes, obtener de la base de datos
    if not event_types:
        event_types = {et.name: et for et in db.query(EventType).all()}
    
    if not devices:
        from app.models.device import Device
        devices = {f"device_{d.id}": d for d in db.query(Device).all()}
    
    events = {}
    
    # Crear eventos para cada dispositivo
    for device_key, device in devices.items():
        # Crear 3-5 eventos por dispositivo
        num_events = min(5, len(event_types))
        event_type_names = list(event_types.keys())[:num_events]
        
        for event_type_name in event_type_names:
            event_type = event_types[event_type_name]
            
            # Generar datos del evento
            event_data = DataGenerator.generate_event_data(
                event_type_id=event_type.id,
                device_id=device.id
            )
            
            # Verificar si ya existe
            existing_event = db.query(Event).filter(
                Event.device_id == device.id,
                Event.event_type_id == event_type.id,
                Event.message == event_data["message"]
            ).first()
            
            if existing_event:
                events[f"{device_key}_{event_type_name}"] = existing_event
                continue
            
            # Crear evento
            event = Event(**event_data)
            db.add(event)
            db.flush()
            
            events[f"{device_key}_{event_type_name}"] = event
    
    db.commit()
    print(f"      ✅ {len(events)} eventos creados")
    
    return events 