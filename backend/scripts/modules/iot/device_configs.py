#!/usr/bin/env python3
"""
Módulo de población de configuraciones de dispositivos (DeviceConfig)
Genera configuraciones personalizadas para dispositivos IoT con datos realistas e idempotencia.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.device_config import DeviceConfig
from app.models.device import Device
from app.models.user import User
from datetime import datetime, timedelta
import random
import json

def generate_sensor_config():
    """Generar configuración de sensor realista"""
    config = {
        "sampling_rate": random.choice([1, 5, 10, 30, 60]),  # segundos
        "threshold_min": random.uniform(15.0, 25.0),
        "threshold_max": random.uniform(25.0, 35.0),
        "calibration_offset": random.uniform(-2.0, 2.0),
        "alert_enabled": random.choice([True, False]),
        "data_retention_days": random.choice([7, 30, 90, 365]),
        "battery_save_mode": random.choice([True, False])
    }
    return json.dumps(config)

def generate_alert_config():
    """Generar configuración de alertas realista"""
    config = {
        "email_alerts": random.choice([True, False]),
        "sms_alerts": random.choice([True, False]),
        "push_notifications": random.choice([True, False]),
        "alert_cooldown_minutes": random.randint(5, 60),
        "escalation_enabled": random.choice([True, False]),
        "escalation_delay_minutes": random.randint(15, 120),
        "recipients": [
            "primary_caregiver",
            "family_member",
            "emergency_contact"
        ],
        "quiet_hours": {
            "enabled": random.choice([True, False]),
            "start": "22:00",
            "end": "07:00"
        }
    }
    return json.dumps(config)

def generate_notification_config():
    """Generar configuración de notificaciones realista"""
    config = {
        "notification_types": {
            "daily_summary": random.choice([True, False]),
            "weekly_report": random.choice([True, False]),
            "medication_reminders": random.choice([True, False]),
            "appointment_reminders": random.choice([True, False]),
            "system_updates": random.choice([True, False])
        },
        "delivery_methods": {
            "email": random.choice([True, False]),
            "sms": random.choice([True, False]),
            "push": random.choice([True, False]),
            "in_app": True
        },
        "frequency": random.choice(["immediate", "hourly", "daily", "weekly"]),
        "language": random.choice(["es", "en", "pt"]),
        "timezone": "America/Argentina/Buenos_Aires"
    }
    return json.dumps(config)

def generate_sampling_config():
    """Generar configuración de muestreo realista"""
    config = {
        "sampling_interval": random.choice([1, 5, 10, 30, 60]),  # segundos
        "batch_size": random.randint(10, 100),
        "compression_enabled": random.choice([True, False]),
        "data_format": random.choice(["json", "csv", "binary"]),
        "transmission_mode": random.choice(["real_time", "batch", "on_demand"]),
        "retry_attempts": random.randint(1, 5),
        "timeout_seconds": random.randint(30, 300)
    }
    return json.dumps(config)

def generate_threshold_config():
    """Generar configuración de umbrales realista"""
    config = {
        "temperature": {
            "min": random.uniform(15.0, 20.0),
            "max": random.uniform(25.0, 30.0),
            "critical_min": random.uniform(10.0, 15.0),
            "critical_max": random.uniform(30.0, 35.0)
        },
        "humidity": {
            "min": random.uniform(30.0, 40.0),
            "max": random.uniform(60.0, 70.0)
        },
        "heart_rate": {
            "min": random.randint(50, 60),
            "max": random.randint(100, 120),
            "critical_min": random.randint(40, 50),
            "critical_max": random.randint(120, 140)
        },
        "blood_pressure": {
            "systolic_min": random.randint(90, 100),
            "systolic_max": random.randint(140, 160),
            "diastolic_min": random.randint(60, 70),
            "diastolic_max": random.randint(90, 100)
        }
    }
    return json.dumps(config)

def generate_calibration_config():
    """Generar configuración de calibración realista"""
    config = {
        "last_calibration": datetime.utcnow().isoformat(),
        "calibration_interval_days": random.randint(30, 365),
        "calibration_method": random.choice(["auto", "manual", "reference"]),
        "offset_values": {
            "temperature": random.uniform(-1.0, 1.0),
            "humidity": random.uniform(-5.0, 5.0),
            "pressure": random.uniform(-2.0, 2.0)
        },
        "drift_correction": random.choice([True, False]),
        "reference_device": f"REF_{random.randint(1000, 9999)}"
    }
    return json.dumps(config)

def generate_network_config():
    """Generar configuración de red realista"""
    config = {
        "wifi": {
            "ssid": f"Network_{random.randint(1, 100)}",
            "security": random.choice(["WPA2", "WPA3", "Open"]),
            "auto_reconnect": random.choice([True, False]),
            "power_save": random.choice([True, False])
        },
        "cellular": {
            "enabled": random.choice([True, False]),
            "apn": "internet",
            "roaming_enabled": random.choice([True, False])
        },
        "bluetooth": {
            "enabled": random.choice([True, False]),
            "discoverable": random.choice([True, False]),
            "pairing_mode": random.choice([True, False])
        },
        "ip_config": {
            "dhcp_enabled": random.choice([True, False]),
            "static_ip": "192.168.1.100",
            "dns_servers": ["8.8.8.8", "8.8.4.4"]
        }
    }
    return json.dumps(config)

def generate_security_config():
    """Generar configuración de seguridad realista"""
    config = {
        "encryption": {
            "enabled": random.choice([True, False]),
            "algorithm": random.choice(["AES-256", "AES-128", "ChaCha20"]),
            "key_rotation_days": random.randint(30, 365)
        },
        "authentication": {
            "method": random.choice(["token", "certificate", "password"]),
            "token_expiry_hours": random.randint(24, 168),
            "max_failed_attempts": random.randint(3, 10)
        },
        "access_control": {
            "whitelist_enabled": random.choice([True, False]),
            "allowed_ips": ["192.168.1.0/24", "10.0.0.0/8"],
            "time_restrictions": {
                "enabled": random.choice([True, False]),
                "allowed_hours": "06:00-22:00"
            }
        },
        "audit_logging": {
            "enabled": random.choice([True, False]),
            "log_level": random.choice(["info", "warning", "error", "debug"]),
            "retention_days": random.randint(30, 365)
        }
    }
    return json.dumps(config)

def generate_power_config():
    """Generar configuración de energía realista"""
    config = {
        "battery_management": {
            "low_battery_threshold": random.randint(10, 25),
            "critical_battery_threshold": random.randint(5, 15),
            "power_save_mode": random.choice([True, False]),
            "auto_shutdown": random.choice([True, False])
        },
        "charging": {
            "fast_charge_enabled": random.choice([True, False]),
            "max_charge_current": random.uniform(1.0, 3.0),
            "temperature_monitoring": random.choice([True, False])
        },
        "sleep_mode": {
            "enabled": random.choice([True, False]),
            "sleep_interval_minutes": random.randint(5, 60),
            "wake_on_motion": random.choice([True, False]),
            "wake_on_timer": random.choice([True, False])
        },
        "power_source": {
            "primary": random.choice(["battery", "usb", "ac"]),
            "backup_enabled": random.choice([True, False]),
            "ups_connected": random.choice([True, False])
        }
    }
    return json.dumps(config)

def populate_device_configs(db, existing_data=None):
    print("   ⚙️ Poblando configuraciones de dispositivos...")
    
    # Obtener dispositivos y usuarios existentes
    devices = db.query(Device).all()
    users = db.query(User).all()
    
    if not devices:
        print("   ⚠️ No hay dispositivos en la base de datos. Ejecuta primero el módulo de dispositivos.")
        return
    
    if not users:
        print("   ⚠️ No hay usuarios en la base de datos. Ejecuta primero el módulo de usuarios.")
        return
    
    # Obtener tipos de configuración disponibles
    config_types = DeviceConfig.get_config_types()
    
    # Generar configuraciones por dispositivo
    configs_created = 0
    
    for device in devices:
        # Generar múltiples configuraciones por dispositivo
        num_configs = random.randint(2, 5)
        configs_for_device = random.sample(config_types, min(num_configs, len(config_types)))
        
        for config_type in configs_for_device:
            # Verificar si ya existe esta configuración para el dispositivo
            existing = db.query(DeviceConfig).filter_by(
                device_id=device.id,
                config_type=config_type
            ).first()
            
            if not existing:
                # Generar datos específicos según el tipo de configuración
                if config_type == "sensor_config":
                    config_data = generate_sensor_config()
                    config_name = f"Configuración de Sensor - {device.name}"
                    description = f"Configuración de sensores para {device.name} ({device.type})"
                elif config_type == "alert_config":
                    config_data = generate_alert_config()
                    config_name = f"Configuración de Alertas - {device.name}"
                    description = f"Configuración de alertas para {device.name}"
                elif config_type == "notification_config":
                    config_data = generate_notification_config()
                    config_name = f"Configuración de Notificaciones - {device.name}"
                    description = f"Configuración de notificaciones para {device.name}"
                elif config_type == "sampling_config":
                    config_data = generate_sampling_config()
                    config_name = f"Configuración de Muestreo - {device.name}"
                    description = f"Configuración de muestreo para {device.name}"
                elif config_type == "threshold_config":
                    config_data = generate_threshold_config()
                    config_name = f"Configuración de Umbrales - {device.name}"
                    description = f"Configuración de umbrales para {device.name}"
                elif config_type == "calibration_config":
                    config_data = generate_calibration_config()
                    config_name = f"Configuración de Calibración - {device.name}"
                    description = f"Configuración de calibración para {device.name}"
                elif config_type == "network_config":
                    config_data = generate_network_config()
                    config_name = f"Configuración de Red - {device.name}"
                    description = f"Configuración de red para {device.name}"
                elif config_type == "security_config":
                    config_data = generate_security_config()
                    config_name = f"Configuración de Seguridad - {device.name}"
                    description = f"Configuración de seguridad para {device.name}"
                elif config_type == "power_config":
                    config_data = generate_power_config()
                    config_name = f"Configuración de Energía - {device.name}"
                    description = f"Configuración de energía para {device.name}"
                else:
                    config_data = json.dumps({"default": True, "device_type": device.type})
                    config_name = f"Configuración General - {device.name}"
                    description = f"Configuración general para {device.name}"
                
                # Crear configuración de dispositivo
                device_config = DeviceConfig(
                    device_id=device.id,
                    config_type=config_type,
                    config_name=config_name,
                    config_data=config_data,
                    description=description,
                    is_active=random.choice([True, True, True, False]),  # 75% activas
                    is_default=random.choice([True, False]),
                    version=f"1.{random.randint(0, 9)}.{random.randint(0, 9)}",
                    applied_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    applied_by=random.choice(users).id if users else None,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(device_config)
                configs_created += 1
    
    db.commit()
    print(f"   ⚙️ {configs_created} configuraciones de dispositivos creadas")

def populate_device_configs_complete(db, existing_data=None):
    populate_device_configs(db, existing_data)

if __name__ == "__main__":
    from app.core.database import get_db
    db = next(get_db())
    try:
        populate_device_configs_complete(db)
    finally:
        db.close() 