#!/usr/bin/env python3
"""
Generadores de datos realistas para población de base de datos
"""

import random
import uuid
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any

class DataGenerator:
    """Generador de datos realistas para entidades del sistema"""
    
    # Nombres de dispositivos por categoría
    DEVICE_NAMES = [
        # Sensores básicos (originales)
        "Sensor de Temperatura", "Sensor de Movimiento", "GPS Tracker", "Cámara de Seguridad",
        "Wearable Smart Watch", "Detector de Caídas",
        
        # Sensores médicos
        "Monitor de Presión Arterial", "Monitor de Glucosa", "Oxímetro de Pulso", "Monitor ECG",
        "Termómetro Digital", "Estetoscopio Digital", "Monitor de Ritmo Cardíaco",
        
        # Sensores ambientales
        "Sensor de Humedad", "Sensor de Calidad del Aire", "Sensor de Iluminación", "Sensor de Ruido",
        "Detector de CO2", "Sensor de Presión Atmosférica", "Sensor de Radiación UV",
        
        # Dispositivos de seguridad
        "Detector de Humo", "Detector de Gas", "Sensor de Puerta", "Sensor de Ventana",
        "Alarma de Intrusión", "Cámara de Vigilancia", "Sistema de Cerradura Inteligente",
        
        # Dispositivos de asistencia
        "Dispensador de Medicamentos", "Botón de Emergencia", "Báscula Inteligente", "Espejo Inteligente",
        "Andador Inteligente", "Silla de Ruedas Motorizada", "Elevador de Escaleras",
        
        # Monitores de actividad
        "Sensor de Cama", "Sensor de Silla", "Sensor de Baño", "Sensor de Refrigerador",
        "Sensor de Cocina", "Sensor de Lavadora", "Sensor de Secadora",
        
        # Dispositivos de comunicación
        "Altavoz Inteligente", "Intercomunicador de Video", "Teléfono Adaptado", "Tablet Inteligente",
        "Reloj con Llamadas", "Pendiente con Micrófono", "Gafas de Realidad Aumentada",
        
        # Control ambiental
        "Termostato Inteligente", "Sistema de Iluminación", "Persianas Automáticas", "Purificador de Aire",
        "Humidificador Inteligente", "Ventilador Inteligente", "Calefactor Inteligente"
    ]
    
    DEVICE_LOCATIONS = [
        "Living Room", "Bedroom", "Kitchen", "Bathroom", "Entrance",
        "Patio", "Garden", "Garage", "Office", "Dining Room"
    ]
    
    EVENT_DESCRIPTIONS = [
        "Movimiento detectado en zona de alto tráfico",
        "Temperatura elevada detectada",
        "Dispositivo reconectado exitosamente",
        "Nueva ubicación registrada",
        "Estado del dispositivo actualizado",
        "Lectura de sensores completada",
        "Configuración aplicada correctamente",
        "Mantenimiento programado iniciado"
    ]
    
    ALERT_DESCRIPTIONS = [
        "Posible caída detectada - requiere atención inmediata",
        "Temperatura corporal elevada - monitorear síntomas",
        "Dispositivo desconectado por más de 30 minutos",
        "Medicación pendiente por más de 2 horas",
        "Salida de zona segura detectada",
        "Actividad inusual en horario nocturno",
        "Dispositivo con batería baja",
        "Error de comunicación con sensor"
    ]
    
    @staticmethod
    def generate_device_data(device_type_id: int, package_id: str, user_id: str = None, **kwargs) -> Dict[str, Any]:
        """Generar datos realistas para un dispositivo"""
        device_name = random.choice(DataGenerator.DEVICE_NAMES)
        location = random.choice(DataGenerator.DEVICE_LOCATIONS)
        
        data = {
            "device_id": f"DEV-{uuid.uuid4().hex[:8].upper()}",  # Campo requerido
            "name": device_name,
            "device_type_id": device_type_id,
            "package_id": package_id,
            "location": location,
            "type": "sensor",  # Campo requerido
            "serial_number": f"SN-{uuid.uuid4().hex[:8].upper()}",
            "firmware_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "battery_level": random.randint(20, 100),
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            **kwargs
        }
        
        # Solo agregar user_id si se proporciona
        if user_id is not None:
            data["user_id"] = user_id
            
        return data
    
    @staticmethod
    def generate_event_data(event_type_id: int, device_id: int, **kwargs) -> Dict[str, Any]:
        """Generar datos realistas para un evento"""
        description = random.choice(DataGenerator.EVENT_DESCRIPTIONS)
        
        event_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "location": random.choice(DataGenerator.DEVICE_LOCATIONS),
            "value": random.uniform(20.0, 40.0) if "temperature" in description.lower() else None
        }
        
        return {
            "event_type_id": event_type_id,
            "device_id": device_id,
            "message": description,
            "event_data": json.dumps(event_data),  # Convertir a JSON string
            "severity": random.choice(["info", "warning", "error", "critical"]),
            "event_time": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
            **kwargs
        }
    
    @staticmethod
    def generate_alert_data(alert_type_id: int, device_id: int, **kwargs) -> Dict[str, Any]:
        """Generar datos realistas para una alerta"""
        description = random.choice(DataGenerator.ALERT_DESCRIPTIONS)
        
        alert_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "location": random.choice(DataGenerator.DEVICE_LOCATIONS),
            "value": random.uniform(20.0, 40.0) if "temperature" in description.lower() else None,
            "threshold_exceeded": random.choice([True, False])
        }
        
        return {
            "alert_type_id": alert_type_id,
            "device_id": device_id,
            "title": f"Alerta: {description[:50]}...",
            "message": description,
            "alert_data": json.dumps(alert_data),  # Convertir a JSON string
            "severity": random.choice(["low", "medium", "high", "critical"]),
            "priority": random.randint(1, 10),
            "escalation_level": random.randint(0, 3),
            "acknowledged_at": datetime.now(timezone.utc) - timedelta(minutes=random.randint(5, 60)) if random.choice([True, False]) else None,
            "resolved_at": datetime.now(timezone.utc) - timedelta(minutes=random.randint(10, 120)) if random.choice([True, False]) else None,
            "created_at": datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 30)),
            "updated_at": datetime.now(timezone.utc),
            **kwargs
        }
    
    @staticmethod
    def generate_device_config_data(device_id: int, **kwargs) -> Dict[str, Any]:
        """Generar datos de configuración para un dispositivo"""
        config_data = {
            "sensitivity": random.randint(1, 10) if random.choice([True, False]) else None,
            "threshold": random.uniform(20.0, 40.0) if random.choice([True, False]) else None,
            "schedule": {
                "start_time": "08:00",
                "end_time": "20:00",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
            } if random.choice([True, False]) else None,
            "notifications": {
                "email": True,
                "sms": random.choice([True, False]),
                "push": True
            }
        }
        
        config_type = random.choice(["sensitivity", "threshold", "schedule", "notification"])
        
        return {
            "device_id": device_id,
            "config_type": config_type,
            "config_name": f"Configuración {config_type.title()}",
            "config_data": json.dumps(config_data),  # Convertir a JSON string
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            **kwargs
        }
    
    @staticmethod
    def generate_location_tracking_data(cared_person_id: int, **kwargs) -> Dict[str, Any]:
        """Generar datos de seguimiento de ubicación"""
        # Coordenadas aproximadas de Buenos Aires
        base_lat = -34.6037
        base_lng = -58.3816
        
        recorded_time = datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 60))
        
        return {
            "cared_person_id": cared_person_id,
            "latitude": base_lat + random.uniform(-0.01, 0.01),
            "longitude": base_lng + random.uniform(-0.01, 0.01),
            "accuracy": random.uniform(5.0, 50.0),
            "speed": random.uniform(0.0, 5.0),
            "heading": random.uniform(0.0, 360.0),
            "altitude": random.uniform(0.0, 100.0),
            "location_name": random.choice(["Casa", "Hospital", "Centro Comercial", "Parque", "Farmacia"]),
            "address": f"Calle {random.randint(1, 1000)}, Buenos Aires",
            "place_type": random.choice(["home", "hospital", "store", "park", "other"]),
            "tracking_method": random.choice(["gps", "wifi", "cell_tower"]),
            "battery_level": random.randint(20, 100),
            "signal_strength": random.randint(1, 5),
            "recorded_at": recorded_time,
            "received_at": recorded_time + timedelta(seconds=random.randint(1, 30)),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            **kwargs
        }
    
    @staticmethod
    def generate_geofence_data(user_id: int, **kwargs) -> Dict[str, Any]:
        """Generar datos de geofence"""
        # Coordenadas aproximadas de Buenos Aires
        base_lat = -34.6037
        base_lng = -58.3816
        
        return {
            "user_id": user_id,
            "name": random.choice(["Casa", "Hospital", "Centro Comercial", "Parque", "Farmacia"]),
            "description": f"Zona segura: {random.choice(['Hogar', 'Institución médica', 'Área de recreación'])}",
            "geofence_type": random.choice(["safe_zone", "home_zone", "medical_zone", "custom_zone"]),
            "center_latitude": base_lat + random.uniform(-0.02, 0.02),
            "center_longitude": base_lng + random.uniform(-0.02, 0.02),
            "radius": random.uniform(50.0, 500.0),
            "trigger_action": random.choice(["enter", "exit", "both"]),
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            **kwargs
        } 