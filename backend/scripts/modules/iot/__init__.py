"""
Módulo IoT - Entidades relacionadas con dispositivos, eventos y alertas
"""

from .devices import populate_devices
from .events import populate_events
from .alerts import populate_alerts
from .tracking import populate_tracking

def populate_iot_module(db, existing_data=None):
    """
    Poblar todas las entidades del módulo IoT
    
    Args:
        db: Sesión de base de datos
        existing_data: Datos existentes de otros módulos (usuarios, tipos, etc.)
    
    Returns:
        dict: Datos creados en este módulo
    """
    print("🔌 POBLANDO MÓDULO IoT...")
    
    # Poblar dispositivos
    devices_data = populate_devices(db, existing_data)
    
    # Poblar eventos
    events_data = populate_events(db, devices_data, existing_data)
    
    # Poblar alertas
    alerts_data = populate_alerts(db, devices_data, existing_data)
    
    # Poblar seguimiento de ubicación
    tracking_data = populate_tracking(db, existing_data)
    
    print("   ✅ Módulo IoT poblado exitosamente")
    
    return {
        "devices": devices_data,
        "events": events_data,
        "alerts": alerts_data,
        "tracking": tracking_data
    } 