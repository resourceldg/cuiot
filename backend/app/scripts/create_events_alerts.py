#!/usr/bin/env python3
"""
Script para crear eventos y alertas de prueba.
"""

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event
from app.models.alert import Alert
from app.models.event_type import EventType
from app.models.alert_type import AlertType
from app.models.status_type import StatusType
from app.models.cared_person import CaredPerson
from app.models.device import Device
from app.models.user import User
from datetime import datetime, timedelta
import random
import uuid
import json

def get_status_type_id(db: Session, name: str, category: str) -> int:
    status_type = db.query(StatusType).filter_by(name=name, category=category).first()
    if not status_type:
        raise Exception(f"No se encontró status_type para name='{name}', category='{category}'")
    return status_type.id

def get_event_type_id(db: Session, name: str) -> int:
    event_type = db.query(EventType).filter_by(name=name).first()
    if not event_type:
        raise Exception(f"No se encontró event_type para name='{name}'")
    return event_type.id

def get_alert_type_id(db: Session, name: str) -> int:
    alert_type = db.query(AlertType).filter_by(name=name).first()
    if not alert_type:
        raise Exception(f"No se encontró alert_type para name='{name}'")
    return alert_type.id

def create_events(db: Session, cared_persons: list, devices: list) -> list:
    """Crear eventos de prueba"""
    events = []
    
    # Obtener tipos de eventos
    event_types = {
        'device_connected': get_event_type_id(db, 'device_connected'),
        'device_disconnected': get_event_type_id(db, 'device_disconnected'),
        'battery_status': get_event_type_id(db, 'battery_status'),
        'location_update': get_event_type_id(db, 'location_update'),
        'vital_signs_reading': get_event_type_id(db, 'vital_signs_reading'),
        'medication_taken': get_event_type_id(db, 'medication_taken'),
        'medication_missed': get_event_type_id(db, 'medication_missed'),
        'fall_detected': get_event_type_id(db, 'fall_detected'),
        'appointment_scheduled': get_event_type_id(db, 'appointment_scheduled'),
        'appointment_completed': get_event_type_id(db, 'appointment_completed')
    }
    
    # Crear eventos para cada persona bajo cuidado
    for cared in cared_persons:
        # Obtener dispositivos de esta persona
        person_devices = [d for d in devices if d.cared_person_id == cared.id]
        
        # Crear entre 5-15 eventos por persona
        num_events = random.randint(5, 15)
        
        for i in range(num_events):
            try:
                # Seleccionar tipo de evento aleatorio
                event_type_name = random.choice(list(event_types.keys()))
                event_type_id = event_types[event_type_name]
                
                # Seleccionar dispositivo aleatorio de la persona
                device = random.choice(person_devices) if person_devices else None
                
                # Crear datos del evento según el tipo
                event_data = {}
                message = ""
                
                if event_type_name == 'device_connected':
                    message = f"Dispositivo {device.name if device else 'desconocido'} conectado"
                    event_data = {"device_id": str(device.id) if device else None}
                elif event_type_name == 'device_disconnected':
                    message = f"Dispositivo {device.name if device else 'desconocido'} desconectado"
                    event_data = {"device_id": str(device.id) if device else None}
                elif event_type_name == 'battery_status':
                    battery_level = random.randint(10, 100)
                    message = f"Batería del dispositivo {device.name if device else 'desconocido'}: {battery_level}%"
                    event_data = {"battery_level": battery_level, "device_id": str(device.id) if device else None}
                elif event_type_name == 'location_update':
                    lat = random.uniform(-34.6, -34.5)  # Buenos Aires
                    lon = random.uniform(-58.5, -58.4)
                    message = f"Ubicación actualizada: {lat:.4f}, {lon:.4f}"
                    event_data = {"latitude": lat, "longitude": lon}
                elif event_type_name == 'vital_signs_reading':
                    heart_rate = random.randint(60, 100)
                    blood_pressure = f"{random.randint(110, 140)}/{random.randint(70, 90)}"
                    message = f"Signos vitales: FC {heart_rate} bpm, PA {blood_pressure} mmHg"
                    event_data = {"heart_rate": heart_rate, "blood_pressure": blood_pressure}
                elif event_type_name == 'medication_taken':
                    message = f"Medicación tomada correctamente"
                    event_data = {"medication": "Medicamento prescrito"}
                elif event_type_name == 'medication_missed':
                    message = f"Medicación omitida - requiere atención"
                    event_data = {"medication": "Medicamento prescrito", "missed_time": datetime.now().isoformat()}
                elif event_type_name == 'fall_detected':
                    message = f"¡Caída detectada! - Requiere atención inmediata"
                    event_data = {"severity": "high", "location": "Hogar"}
                elif event_type_name == 'appointment_scheduled':
                    appointment_date = datetime.now() + timedelta(days=random.randint(1, 30))
                    message = f"Cita médica programada para {appointment_date.strftime('%d/%m/%Y %H:%M')}"
                    event_data = {"appointment_date": appointment_date.isoformat()}
                elif event_type_name == 'appointment_completed':
                    message = f"Cita médica completada exitosamente"
                    event_data = {"status": "completed"}
                
                # Crear evento
                event = Event(
                    id=uuid.uuid4(),
                    event_type_id=event_type_id,
                    event_subtype=event_type_name,
                    severity=random.choice(['low', 'medium', 'high']),
                    event_data=json.dumps(event_data),
                    message=message,
                    source='device' if device else 'system',
                    latitude=random.uniform(-34.6, -34.5) if event_type_name == 'location_update' else None,
                    longitude=random.uniform(-58.5, -58.4) if event_type_name == 'location_update' else None,
                    event_time=datetime.now() - timedelta(hours=random.randint(0, 72)),
                    user_id=cared.user_id,
                    cared_person_id=cared.id,
                    device_id=device.id if device else None,
                    is_active=True
                )
                
                events.append(event)
                
            except Exception as e:
                print(f"Error creando evento {i+1} para {cared.first_name}: {e}")
                continue
    
    # Guardar eventos en lote
    if events:
        db.add_all(events)
        db.commit()
        print(f"✅ Creados {len(events)} eventos")
    else:
        print("❌ No se crearon eventos")
    
    return events

def create_alerts(db: Session, cared_persons: list, devices: list) -> list:
    """Crear alertas de prueba"""
    alerts = []
    
    # Obtener tipos de alertas
    alert_types = {
        'medical_emergency': get_alert_type_id(db, 'medical_emergency'),
        'fall_detected': get_alert_type_id(db, 'fall_detected'),
        'medication_missed': get_alert_type_id(db, 'medication_missed'),
        'device_offline': get_alert_type_id(db, 'device_offline'),
        'battery_low': get_alert_type_id(db, 'battery_low'),
        'location_alert': get_alert_type_id(db, 'location_alert'),
        'vital_signs_abnormal': get_alert_type_id(db, 'vital_signs_abnormal'),
        'appointment_reminder': get_alert_type_id(db, 'appointment_reminder')
    }
    
    # Obtener status types
    status_types = {
        'active': get_status_type_id(db, 'active', 'alert_status'),
        'acknowledged': get_status_type_id(db, 'acknowledged', 'alert_status'),
        'resolved': get_status_type_id(db, 'resolved', 'alert_status')
    }
    
    # Crear alertas para cada persona bajo cuidado
    for cared in cared_persons:
        # Obtener dispositivos de esta persona
        person_devices = [d for d in devices if d.cared_person_id == cared.id]
        
        # Crear entre 2-8 alertas por persona
        num_alerts = random.randint(2, 8)
        
        for i in range(num_alerts):
            try:
                # Seleccionar tipo de alerta aleatorio
                alert_type_name = random.choice(list(alert_types.keys()))
                alert_type_id = alert_types[alert_type_name]
                
                # Seleccionar dispositivo aleatorio de la persona
                device = random.choice(person_devices) if person_devices else None
                
                # Seleccionar status aleatorio
                status_name = random.choice(list(status_types.keys()))
                status_type_id = status_types[status_name]
                
                # Crear datos de la alerta según el tipo
                alert_data = {}
                title = ""
                message = ""
                severity = random.choice(['low', 'medium', 'high'])
                
                if alert_type_name == 'medical_emergency':
                    title = f"Emergencia médica - {cared.first_name}"
                    message = f"Se ha detectado una emergencia médica para {cared.first_name}. Requiere atención inmediata."
                    severity = 'high'
                    alert_data = {"emergency_type": "medical", "priority": "critical"}
                elif alert_type_name == 'fall_detected':
                    title = f"Caída detectada - {cared.first_name}"
                    message = f"Se ha detectado una caída para {cared.first_name}. Verificar estado."
                    severity = 'high'
                    alert_data = {"fall_location": "Hogar", "device_id": str(device.id) if device else None}
                elif alert_type_name == 'medication_missed':
                    title = f"Medicación omitida - {cared.first_name}"
                    message = f"{cared.first_name} no ha tomado su medicación programada."
                    severity = 'medium'
                    alert_data = {"medication": "Medicamento prescrito", "missed_time": datetime.now().isoformat()}
                elif alert_type_name == 'device_offline':
                    title = f"Dispositivo desconectado - {device.name if device else 'Desconocido'}"
                    message = f"El dispositivo {device.name if device else 'desconocido'} está desconectado."
                    severity = 'medium'
                    alert_data = {"device_id": str(device.id) if device else None, "offline_since": datetime.now().isoformat()}
                elif alert_type_name == 'battery_low':
                    title = f"Batería baja - {device.name if device else 'Dispositivo'}"
                    message = f"La batería del dispositivo {device.name if device else 'desconocido'} está baja."
                    severity = 'low'
                    alert_data = {"battery_level": random.randint(5, 20), "device_id": str(device.id) if device else None}
                elif alert_type_name == 'location_alert':
                    title = f"Alerta de ubicación - {cared.first_name}"
                    message = f"{cared.first_name} se encuentra fuera de la zona segura."
                    severity = 'medium'
                    alert_data = {"current_location": "Fuera de zona segura", "safe_zone": "Hogar"}
                elif alert_type_name == 'vital_signs_abnormal':
                    title = f"Signos vitales anormales - {cared.first_name}"
                    message = f"Los signos vitales de {cared.first_name} están fuera del rango normal."
                    severity = 'high'
                    alert_data = {"heart_rate": random.randint(100, 150), "blood_pressure": "180/100"}
                elif alert_type_name == 'appointment_reminder':
                    title = f"Recordatorio de cita - {cared.first_name}"
                    message = f"Recordatorio: {cared.first_name} tiene una cita médica programada."
                    severity = 'low'
                    alert_data = {"appointment_date": (datetime.now() + timedelta(days=1)).isoformat()}
                
                # Crear alerta
                alert = Alert(
                    id=uuid.uuid4(),
                    alert_type_id=alert_type_id,
                    alert_subtype=alert_type_name,
                    severity=severity,
                    title=title,
                    message=message,
                    alert_data=json.dumps(alert_data),
                    status_type_id=status_type_id,
                    priority=random.randint(1, 10),
                    escalation_level=random.randint(1, 3),
                    user_id=cared.user_id,
                    cared_person_id=cared.id,
                    device_id=device.id if device else None,
                    created_at=datetime.now() - timedelta(hours=random.randint(0, 48))
                )
                
                alerts.append(alert)
                
            except Exception as e:
                print(f"Error creando alerta {i+1} para {cared.first_name}: {e}")
                continue
    
    # Guardar alertas en lote
    if alerts:
        db.add_all(alerts)
        db.commit()
        print(f"✅ Creadas {len(alerts)} alertas")
    else:
        print("❌ No se crearon alertas")
    
    return alerts

def main():
    """Función principal"""
    print("🚀 Creando eventos y alertas de prueba...")
    
    db = next(get_db())
    
    try:
        # Obtener datos existentes
        cared_persons = db.query(CaredPerson).filter(CaredPerson.is_active == True).all()
        devices = db.query(Device).filter(Device.is_active == True).all()
        
        if not cared_persons:
            print("❌ No hay personas bajo cuidado para crear eventos/alertas")
            return
        
        print(f"📋 Creando eventos para {len(cared_persons)} personas...")
        events = create_events(db, cared_persons, devices)
        
        print(f"📋 Creando alertas para {len(cared_persons)} personas...")
        alerts = create_alerts(db, cared_persons, devices)
        
        # Validación final
        total_events = db.query(Event).count()
        total_alerts = db.query(Alert).count()
        
        print(f"\n✅ Eventos y alertas creados exitosamente!")
        print(f"📊 Resumen:")
        print(f"   📅 Eventos: {total_events}")
        print(f"   🚨 Alertas: {total_alerts}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 