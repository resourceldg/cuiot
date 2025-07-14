#!/usr/bin/env python3
"""
Módulo de alertas IoT
Poblar alertas del sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.alert_type import AlertType
from utils.data_generators import DataGenerator

def populate_alerts(db: Session, devices_data=None, existing_data=None):
    """
    Poblar alertas del sistema IoT
    
    Args:
        db: Sesión de base de datos
        devices_data: Datos de dispositivos creados
        existing_data: Datos existentes (tipos de alerta)
    
    Returns:
        dict: Alertas creadas
    """
    print("   🚨 Poblando alertas IoT...")
    
    # Obtener datos existentes
    alert_types = existing_data.get("alert_types", {}) if existing_data else {}
    devices = devices_data.get("devices", {}) if devices_data else {}
    
    # Si no hay datos existentes, obtener de la base de datos
    if not alert_types:
        alert_types = {at.name: at for at in db.query(AlertType).all()}
    
    if not devices:
        from app.models.device import Device
        devices = {f"device_{d.id}": d for d in db.query(Device).all()}
    
    alerts = {}
    
    # Crear alertas para algunos dispositivos (no todos)
    device_keys = list(devices.keys())
    devices_with_alerts = device_keys[:min(3, len(device_keys))]  # Máximo 3 dispositivos con alertas
    
    for device_key in devices_with_alerts:
        device = devices[device_key]
        
        # Crear 1-2 alertas por dispositivo
        num_alerts = min(2, len(alert_types))
        alert_type_names = list(alert_types.keys())[:num_alerts]
        
        for alert_type_name in alert_type_names:
            alert_type = alert_types[alert_type_name]
            
            # Generar datos de la alerta
            alert_data = DataGenerator.generate_alert_data(
                alert_type_id=alert_type.id,
                device_id=device.id
            )
            
            # Verificar si ya existe
            existing_alert = db.query(Alert).filter(
                Alert.device_id == device.id,
                Alert.alert_type_id == alert_type.id,
                Alert.message == alert_data["message"]
            ).first()
            
            if existing_alert:
                alerts[f"{device_key}_{alert_type_name}"] = existing_alert
                continue
            
            # Crear alerta
            alert = Alert(**alert_data)
            db.add(alert)
            db.flush()
            
            alerts[f"{device_key}_{alert_type_name}"] = alert
    
    db.commit()
    print(f"      ✅ {len(alerts)} alertas creadas")
    
    return alerts 