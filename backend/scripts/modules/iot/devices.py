#!/usr/bin/env python3
"""
Módulo de dispositivos IoT
Poblar dispositivos y configuraciones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.device_config import DeviceConfig
from app.models.device_type import DeviceType
from app.models.user import User
from utils.data_generators import DataGenerator

def populate_devices(db: Session, existing_data=None):
    """
    Poblar dispositivos IoT y sus configuraciones
    
    Args:
        db: Sesión de base de datos
        existing_data: Datos existentes (paquetes, tipos de dispositivo, instituciones, personas cuidadas)
    
    Returns:
        dict: Dispositivos y configuraciones creados
    """
    print("   📱 Poblando dispositivos IoT...")
    
    # Obtener datos existentes
    packages = existing_data.get("packages", {}) if existing_data else {}
    device_types = existing_data.get("device_types", {}) if existing_data else {}
    institutions = existing_data.get("institutions", {}) if existing_data else {}
    cared_persons = existing_data.get("cared_persons", {}) if existing_data else {}
    users = existing_data.get("users", {}) if existing_data else {}
    
    # Si no hay datos existentes, obtener de la base de datos
    if not device_types:
        device_types = {dt.name: dt for dt in db.query(DeviceType).all()}
    
    if not packages:
        from app.models.package import Package
        packages = {p.name: p for p in db.query(Package).all()}
    
    if not institutions:
        from app.models.institution import Institution
        institutions = {i.name: i for i in db.query(Institution).all()}
    
    if not cared_persons:
        from app.models.cared_person import CaredPerson
        cared_persons = {f"{cp.first_name}_{cp.last_name}": cp for cp in db.query(CaredPerson).all()}
    
    devices = {}
    device_configs = {}
    
    # Crear dispositivos asociados a paquetes
    package_names = list(packages.keys())
    
    for package_name in package_names[:3]:  # Máximo 3 paquetes
        package = packages[package_name]
        
        # Determinar el propietario del paquete (institución, familiar, o persona autocuidada)
        owner_type = "institution" if package.package_type in ["professional", "institutional"] else "individual"
        
        if owner_type == "institution":
            # Buscar una institución para asociar
            institution_names = list(institutions.keys())
            if institution_names:
                institution = institutions[institution_names[0]]  # Usar la primera institución
                owner_id = institution.id
                owner_type = "institution"
            else:
                continue
        else:
            # Para paquetes individuales, buscar una persona cuidada de tipo autocuidado
            autocare_persons = [cp for cp in cared_persons.values() if cp.care_type_id == 1]  # self_care
            if autocare_persons:
                cared_person = autocare_persons[0]
                owner_id = cared_person.id
                owner_type = "cared_person"
            else:
                continue
        
        # Crear 2-4 dispositivos por paquete según las características del paquete
        max_devices = package.features.get("devices", 2) if package.features else 2
        num_devices = min(max_devices, len(device_types))
        device_type_names = list(device_types.keys())[:num_devices]
        
        for device_type_name in device_type_names:
            device_type = device_types[device_type_name]
            
            # Generar datos del dispositivo
            device_data = DataGenerator.generate_device_data(
                device_type_id=device_type.id,
                package_id=package.id
            )
            
            # Agregar campos específicos según la regla de negocio
            if owner_type == "institution":
                device_data["institution_id"] = owner_id
            elif owner_type == "cared_person":
                device_data["cared_person_id"] = owner_id
            
            # Verificar si ya existe
            existing_device = db.query(Device).filter(
                Device.name == device_data["name"],
                Device.institution_id == (owner_id if owner_type == "institution" else None),
                Device.cared_person_id == (owner_id if owner_type == "cared_person" else None)
            ).first()
            
            if existing_device:
                devices[f"{package_name}_{device_data['name']}"] = existing_device
                continue
            
            # Crear dispositivo
            device = Device(**device_data)
            db.add(device)
            db.flush()
            
            devices[f"{package_name}_{device_data['name']}"] = device
            
            # Crear configuración para el dispositivo
            config_data = DataGenerator.generate_device_config_data(device.id)
            
            config = DeviceConfig(**config_data)
            db.add(config)
            db.flush()
            
            device_configs[f"config_{device.id}"] = config
    
    db.commit()
    print(f"      ✅ {len(devices)} dispositivos creados")
    print(f"      ✅ {len(device_configs)} configuraciones creadas")
    
    return {
        "devices": devices,
        "device_configs": device_configs
    } 