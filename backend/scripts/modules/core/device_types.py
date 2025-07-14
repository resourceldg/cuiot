#!/usr/bin/env python3
"""
Módulo Core: Gestión de Tipos de Dispositivos
Consolida la funcionalidad para agregar y gestionar tipos de dispositivos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import get_db
from app.models.device_type import DeviceType
from sqlalchemy.orm import Session
from .catalog_types import populate_catalog_types

class DeviceTypeManager:
    """Gestor de tipos de dispositivos"""
    
    # Tipos de dispositivos especializados para el ecosistema IoT de cuidado
    DEVICE_TYPES_DATA = [
        # Sensores médicos
        {
            "name": "blood_pressure_monitor",
            "description": "Monitor de presión arterial automático",
            "category": "medical_sensor",
            "icon_name": "heart-pulse",
            "color_code": "#dc2626"
        },
        {
            "name": "glucose_monitor",
            "description": "Monitor de glucosa en sangre",
            "category": "medical_sensor", 
            "icon_name": "droplets",
            "color_code": "#059669"
        },
        {
            "name": "pulse_oximeter",
            "description": "Oxímetro de pulso para medir saturación de oxígeno",
            "category": "medical_sensor",
            "icon_name": "activity",
            "color_code": "#7c3aed"
        },
        {
            "name": "ecg_monitor",
            "description": "Monitor de electrocardiograma portátil",
            "category": "medical_sensor",
            "icon_name": "heart",
            "color_code": "#dc2626"
        },
        
        # Sensores ambientales
        {
            "name": "humidity_sensor",
            "description": "Sensor de humedad ambiental",
            "category": "environmental_sensor",
            "icon_name": "cloud-rain",
            "color_code": "#0ea5e9"
        },
        {
            "name": "air_quality_sensor",
            "description": "Sensor de calidad del aire",
            "category": "environmental_sensor",
            "icon_name": "wind",
            "color_code": "#10b981"
        },
        {
            "name": "light_sensor",
            "description": "Sensor de iluminación ambiental",
            "category": "environmental_sensor",
            "icon_name": "sun",
            "color_code": "#f59e0b"
        },
        {
            "name": "noise_sensor",
            "description": "Sensor de nivel de ruido",
            "category": "environmental_sensor",
            "icon_name": "volume-2",
            "color_code": "#8b5cf6"
        },
        
        # Dispositivos de seguridad
        {
            "name": "smoke_detector",
            "description": "Detector de humo inteligente",
            "category": "security_device",
            "icon_name": "flame",
            "color_code": "#f97316"
        },
        {
            "name": "gas_detector",
            "description": "Detector de gas (CO, propano, etc.)",
            "category": "security_device",
            "icon_name": "alert-triangle",
            "color_code": "#ef4444"
        },
        {
            "name": "door_sensor",
            "description": "Sensor de apertura de puertas",
            "category": "security_device",
            "icon_name": "door-open",
            "color_code": "#6b7280"
        },
        {
            "name": "window_sensor",
            "description": "Sensor de apertura de ventanas",
            "category": "security_device",
            "icon_name": "window",
            "color_code": "#3b82f6"
        },
        
        # Dispositivos de asistencia
        {
            "name": "smart_pill_dispenser",
            "description": "Dispensador inteligente de medicamentos",
            "category": "assistance_device",
            "icon_name": "pill",
            "color_code": "#8b5cf6"
        },
        {
            "name": "emergency_button",
            "description": "Botón de emergencia portátil",
            "category": "assistance_device",
            "icon_name": "alert-circle",
            "color_code": "#dc2626"
        },
        {
            "name": "smart_scale",
            "description": "Báscula inteligente con análisis corporal",
            "category": "assistance_device",
            "icon_name": "scale",
            "color_code": "#059669"
        },
        {
            "name": "smart_mirror",
            "description": "Espejo inteligente con reconocimiento facial",
            "category": "assistance_device",
            "icon_name": "user",
            "color_code": "#6366f1"
        },
        
        # Dispositivos de monitoreo de actividad
        {
            "name": "bed_sensor",
            "description": "Sensor de ocupación de cama",
            "category": "activity_monitor",
            "icon_name": "bed",
            "color_code": "#7c3aed"
        },
        {
            "name": "chair_sensor",
            "description": "Sensor de ocupación de silla",
            "category": "activity_monitor",
            "icon_name": "chair",
            "color_code": "#8b5cf6"
        },
        {
            "name": "toilet_sensor",
            "description": "Sensor de uso del baño",
            "category": "activity_monitor",
            "icon_name": "bathroom",
            "color_code": "#0ea5e9"
        },
        {
            "name": "refrigerator_sensor",
            "description": "Sensor de apertura de refrigerador",
            "category": "activity_monitor",
            "icon_name": "refrigerator",
            "color_code": "#10b981"
        },
        
        # Dispositivos de comunicación
        {
            "name": "smart_speaker",
            "description": "Altavoz inteligente con asistente de voz",
            "category": "communication_device",
            "icon_name": "speaker",
            "color_code": "#f59e0b"
        },
        {
            "name": "video_intercom",
            "description": "Intercomunicador de video para entrada",
            "category": "communication_device",
            "icon_name": "video",
            "color_code": "#3b82f6"
        },
        {
            "name": "smart_phone",
            "description": "Teléfono inteligente adaptado para adultos mayores",
            "category": "communication_device",
            "icon_name": "phone",
            "color_code": "#6366f1"
        },
        
        # Dispositivos de control ambiental
        {
            "name": "smart_thermostat",
            "description": "Termostato inteligente",
            "category": "environmental_control",
            "icon_name": "thermometer",
            "color_code": "#f97316"
        },
        {
            "name": "smart_lighting",
            "description": "Sistema de iluminación inteligente",
            "category": "environmental_control",
            "icon_name": "lightbulb",
            "color_code": "#f59e0b"
        },
        {
            "name": "smart_blinds",
            "description": "Persianas inteligentes automáticas",
            "category": "environmental_control",
            "icon_name": "blinds",
            "color_code": "#6b7280"
        },
        {
            "name": "air_purifier",
            "description": "Purificador de aire inteligente",
            "category": "environmental_control",
            "icon_name": "wind",
            "color_code": "#10b981"
        }
    ]
    
    @classmethod
    def populate_device_types(cls, db: Session = None):
        """Poblar tipos de dispositivos especializados"""
        if db is None:
            db = next(get_db())
        
        try:
            print("🔧 AGREGANDO TIPOS DE DISPOSITIVOS ESPECIALIZADOS")
            print("=" * 60)
            
            # Verificar tipos existentes
            existing_types = {dt.name for dt in db.query(DeviceType).all()}
            
            print(f"📊 Tipos existentes: {len(existing_types)}")
            print(f"📊 Nuevos tipos a agregar: {len(cls.DEVICE_TYPES_DATA)}")
            
            added_count = 0
            for device_type_data in cls.DEVICE_TYPES_DATA:
                if device_type_data["name"] not in existing_types:
                    device_type = DeviceType(**device_type_data)
                    db.add(device_type)
                    print(f"   ✅ {device_type.name} - {device_type.description}")
                    added_count += 1
                else:
                    print(f"   ⚠️  {device_type_data['name']} ya existe")
            
            db.commit()
            print(f"\n✅ Se agregaron {added_count} nuevos tipos de dispositivos")
            
            # Mostrar resumen final
            total_types = db.query(DeviceType).count()
            print(f"\n📊 Total de tipos de dispositivos: {total_types}")
            
            print("\n📋 CATEGORÍAS DISPONIBLES:")
            categories = db.query(DeviceType.category).distinct().all()
            for category in categories:
                count = db.query(DeviceType).filter(DeviceType.category == category[0]).count()
                print(f"   - {category[0]}: {count} dispositivos")
            
            print("\n✅ Proceso completado exitosamente")
            return added_count
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.rollback()
            raise
        finally:
            if db is not None:
                db.close()
    
    @classmethod
    def get_device_types_by_category(cls, db: Session = None):
        """Obtener tipos de dispositivos agrupados por categoría"""
        if db is None:
            db = next(get_db())
        
        try:
            categories = db.query(DeviceType.category).distinct().all()
            result = {}
            
            for category in categories:
                device_types = db.query(DeviceType).filter(
                    DeviceType.category == category[0],
                    DeviceType.is_active == True
                ).all()
                result[category[0]] = device_types
            
            return result
            
        finally:
            if db is not None:
                db.close()

def main():
    """Función principal para ejecutar desde línea de comandos"""
    DeviceTypeManager.populate_device_types()

if __name__ == "__main__":
    main() 