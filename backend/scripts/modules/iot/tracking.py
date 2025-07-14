#!/usr/bin/env python3
"""
Módulo de seguimiento de ubicación
Poblar geofences y tracking de ubicación
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from app.models.geofence import Geofence
from app.models.location_tracking import LocationTracking
from app.models.cared_person import CaredPerson
from app.models.user import User
from utils.data_generators import DataGenerator

def populate_tracking(db: Session, existing_data=None):
    """
    Poblar geofences y seguimiento de ubicación
    
    Args:
        db: Sesión de base de datos
        existing_data: Datos existentes (usuarios, personas cuidadas)
    
    Returns:
        dict: Geofences y tracking creados
    """
    print("   📍 Poblando seguimiento de ubicación...")
    
    # Obtener datos existentes
    users = existing_data.get("users", {}) if existing_data else {}
    cared_persons = existing_data.get("cared_persons", {}) if existing_data else {}
    
    # Si no hay datos existentes, obtener de la base de datos
    if not users:
        users = {user.email: user for user in db.query(User).all()}
    
    if not cared_persons:
        cared_persons = {f"{cp.first_name}_{cp.last_name}": cp for cp in db.query(CaredPerson).all()}
    
    geofences = {}
    location_tracking = {}
    
    # Crear geofences para algunos usuarios
    user_emails = list(users.keys())
    users_with_geofences = user_emails[:min(3, len(user_emails))]
    
    for user_email in users_with_geofences:
        user = users[user_email]
        
        # Crear 1-2 geofences por usuario
        for i in range(2):
            geofence_data = DataGenerator.generate_geofence_data(user.id)
            
            # Verificar si ya existe
            existing_geofence = db.query(Geofence).filter(
                Geofence.user_id == user.id,
                Geofence.name == geofence_data["name"]
            ).first()
            
            if existing_geofence:
                geofences[f"{user_email}_{geofence_data['name']}"] = existing_geofence
                continue
            
            # Crear geofence
            geofence = Geofence(**geofence_data)
            db.add(geofence)
            db.flush()
            
            geofences[f"{user_email}_{geofence_data['name']}"] = geofence
    
    # Crear tracking de ubicación para personas cuidadas
    cared_person_keys = list(cared_persons.keys())
    cared_persons_with_tracking = cared_person_keys[:min(2, len(cared_person_keys))]
    
    for cared_person_key in cared_persons_with_tracking:
        cared_person = cared_persons[cared_person_key]
        
        # Crear 3-5 registros de ubicación por persona
        for i in range(4):
            tracking_data = DataGenerator.generate_location_tracking_data(cared_person.id)
            
            # Verificar si ya existe
            existing_tracking = db.query(LocationTracking).filter(
                LocationTracking.cared_person_id == cared_person.id,
                LocationTracking.recorded_at == tracking_data["recorded_at"]
            ).first()
            
            if existing_tracking:
                location_tracking[f"{cared_person_key}_{i}"] = existing_tracking
                continue
            
            # Crear tracking
            tracking = LocationTracking(**tracking_data)
            db.add(tracking)
            db.flush()
            
            location_tracking[f"{cared_person_key}_{i}"] = tracking
    
    db.commit()
    print(f"      ✅ {len(geofences)} geofences creados")
    print(f"      ✅ {len(location_tracking)} registros de ubicación creados")
    
    return {
        "geofences": geofences,
        "location_tracking": location_tracking
    } 