#!/usr/bin/env python3
"""
Script para cargar datos dummy en la base de datos
Maneja correctamente los tipos JSONB y UUID de PostgreSQL
"""

import sys
import os
import uuid
from datetime import datetime, timedelta, date
import random
import json
from typing import List, Dict, Any

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.device import Device
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.report import Report
from app.services.auth import AuthService
from sqlalchemy import text

def clear_all_data(db: Session):
    """Borra todos los datos de las tablas principales en orden seguro"""
    print("🧹 Borrando datos previos...")
    db.execute(text('''
        DELETE FROM reports;
        DELETE FROM alerts;
        DELETE FROM reminders;
        DELETE FROM events;
        DELETE FROM devices;
        DELETE FROM cared_persons;
        DELETE FROM users;
    '''))
    db.commit()
    print("✅ Tablas limpiadas")

def create_dummy_users(db: Session) -> List[User]:
    """Crear usuarios dummy"""
    users_data = [
        {
            "email": "lucia.garcia@email.com",
            "password": "password123",
            "first_name": "Lucía",
            "last_name": "García",
            "phone": "+34 600 123 456",
            "user_type": "family"
        },
        {
            "email": "maria.rodriguez@email.com",
            "password": "password123",
            "first_name": "María",
            "last_name": "Rodríguez",
            "phone": "+34 600 234 567",
            "user_type": "family"
        },
        {
            "email": "carlos.lopez@email.com",
            "password": "password123",
            "first_name": "Carlos",
            "last_name": "López",
            "phone": "+34 600 345 678",
            "user_type": "family"
        },
        {
            "email": "admin@viejostrapos.com",
            "password": "admin123",
            "first_name": "Administrador",
            "last_name": "Sistema",
            "phone": "+34 600 999 999",
            "user_type": "employee"
        }
    ]
    
    users = []
    for user_data in users_data:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            users.append(existing_user)
            continue
        user = User(
            email=user_data["email"],
            hashed_password=AuthService.get_password_hash(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data["phone"]
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    print(f"✅ Creados {len(users)} usuarios")
    return users

def create_dummy_elderly_persons(db: Session, users: List[User]) -> List[CaredPerson]:
    """Crear adultos mayores dummy"""
    elderly_data = [
        {
            "first_name": "Rosa",
            "last_name": "García",
            "age": 78,
            "address": "Calle Mayor 123, Madrid",
            "emergency_contacts": [
                {"name": "Lucía García", "phone": "+34 600 123 456", "relationship": "Hija"},
                {"name": "Dr. Martínez", "phone": "+34 600 111 222", "relationship": "Médico"}
            ],
            "medical_conditions": [
                {"condition": "Hipertensión", "severity": "moderada", "medication": "Enalapril"},
                {"condition": "Diabetes tipo 2", "severity": "leve", "medication": "Metformina"}
            ],
            "medications": [
                {"name": "Enalapril", "dosage": "10mg", "frequency": "1 vez al día", "time": "08:00"},
                {"name": "Metformina", "dosage": "500mg", "frequency": "2 veces al día", "time": "08:00 y 20:00"}
            ]
        },
        {
            "first_name": "Manuel",
            "last_name": "Rodríguez",
            "age": 82,
            "address": "Avenida de la Paz 45, Barcelona",
            "emergency_contacts": [
                {"name": "María Rodríguez", "phone": "+34 600 234 567", "relationship": "Hija"},
                {"name": "Dr. Sánchez", "phone": "+34 600 333 444", "relationship": "Médico"}
            ],
            "medical_conditions": [
                {"condition": "Artritis", "severity": "moderada", "medication": "Ibuprofeno"},
                {"condition": "Problemas cardíacos", "severity": "leve", "medication": "Aspirina"}
            ],
            "medications": [
                {"name": "Ibuprofeno", "dosage": "400mg", "frequency": "3 veces al día", "time": "08:00, 14:00, 20:00"},
                {"name": "Aspirina", "dosage": "100mg", "frequency": "1 vez al día", "time": "08:00"}
            ]
        },
        {
            "first_name": "Carmen",
            "last_name": "López",
            "age": 75,
            "address": "Plaza España 7, Valencia",
            "emergency_contacts": [
                {"name": "Carlos López", "phone": "+34 600 345 678", "relationship": "Hijo"},
                {"name": "Dr. García", "phone": "+34 600 555 666", "relationship": "Médico"}
            ],
            "medical_conditions": [
                {"condition": "Osteoporosis", "severity": "leve", "medication": "Calcio + Vitamina D"},
                {"condition": "Insomnio", "severity": "leve", "medication": "Melatonina"}
            ],
            "medications": [
                {"name": "Calcio + Vitamina D", "dosage": "1000mg", "frequency": "1 vez al día", "time": "12:00"},
                {"name": "Melatonina", "dosage": "3mg", "frequency": "1 vez al día", "time": "22:00"}
            ]
        }
    ]
    
    elderly_persons = []
    for i, elderly_data_item in enumerate(elderly_data):
        user = users[i] if i < len(users) else users[0]
        existing_elderly = db.query(CaredPerson).filter(
            CaredPerson.first_name == elderly_data_item["first_name"],
            CaredPerson.last_name == elderly_data_item["last_name"]
        ).first()
        if existing_elderly:
            elderly_persons.append(existing_elderly)
            continue
        # Calcular date_of_birth a partir de la edad
        edad = elderly_data_item.get("age", 80)
        today = date.today()
        date_of_birth = today - timedelta(days=edad*365)
        elderly = CaredPerson(
            user_id=user.id,
            first_name=elderly_data_item["first_name"],
            last_name=elderly_data_item["last_name"],
            date_of_birth=date_of_birth,
            address=elderly_data_item["address"],
            emergency_contact=elderly_data_item["emergency_contacts"][0]["name"] if elderly_data_item.get("emergency_contacts") else None,
            emergency_phone=elderly_data_item["emergency_contacts"][0]["phone"] if elderly_data_item.get("emergency_contacts") else None,
            medical_conditions=str(elderly_data_item.get("medical_conditions", [])),
            medications=str(elderly_data_item.get("medications", [])),
            is_active=True
        )
        db.add(elderly)
        elderly_persons.append(elderly)
    
    db.commit()
    print(f"✅ Creados {len(elderly_persons)} adultos mayores")
    return elderly_persons

def create_dummy_devices(db: Session, elderly_persons: List[CaredPerson]) -> List[Device]:
    """Crear dispositivos dummy"""
    device_types = ["smart_watch", "panic_button", "motion_sensor", "temperature_sensor", "fall_detector"]
    locations = ["Sala de estar", "Dormitorio", "Cocina", "Baño", "Pasillo"]
    
    devices = []
    for elderly in elderly_persons:
        # Crear 2-3 dispositivos por adulto mayor
        num_devices = random.randint(2, 3)
        for i in range(num_devices):
            device_type = random.choice(device_types)
            location = random.choice(locations)
            
            device = Device(
                device_id=str(uuid.uuid4()),
                device_type=random.choice(device_types),
                model="Model X",
                manufacturer="Acme Corp",
                serial_number=str(uuid.uuid4()),
                status="active",
                battery_level=random.randint(50, 100),
                signal_strength=random.randint(50, 100),
                location_description=random.choice(locations),
                cared_person_id=elderly.id,
                user_id=elderly.user_id
            )
            db.add(device)
            devices.append(device)
    
    db.commit()
    print(f"✅ Creados {len(devices)} dispositivos")
    return devices

def create_dummy_events(db: Session, elderly_persons: List[CaredPerson], devices: List[Device], users: List[User]) -> List[Event]:
    """Crear eventos dummy"""
    event_types = ["medical", "family", "medication", "sensor", "kinesiologia", "nutrition", "other"]
    
    events = []
    
    # Crear eventos de calendario (médicos, familia, etc.)
    for elderly in elderly_persons:
        # Eventos médicos
        for i in range(random.randint(2, 4)):
            event = Event(
                cared_person_id=elderly.id,
                event_type="medical",
                event_subtype="checkup",
                severity="info",
                message=f"Consulta médica rutinaria para {elderly.first_name}",
                event_data=json.dumps({"doctor": "Dr. Martínez"}),
                event_time=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.add(event)
            events.append(event)
        
        # Eventos familiares
        for i in range(random.randint(1, 3)):
            event = Event(
                cared_person_id=elderly.id,
                event_type="family",
                event_subtype="visit",
                severity="info",
                message=f"Visita familiar para {elderly.first_name}",
                event_data=json.dumps({"visitor": "Familiar"}),
                event_time=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.add(event)
            events.append(event)
        
        # Eventos de medicación
        for i in range(random.randint(3, 6)):
            event = Event(
                cared_person_id=elderly.id,
                event_type="medication",
                event_subtype="reminder",
                severity="info",
                message=f"Recordatorio de medicación para {elderly.first_name}",
                event_data=json.dumps({"medication": "Medicación prescrita"}),
                event_time=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.add(event)
            events.append(event)
    
    # Crear eventos de sensores (pasados)
    for device in devices:
        # Eventos de movimiento
        if device.device_type in ["motion_sensor", "temperature_sensor", "fall_detector"]:
            for i in range(random.randint(5, 15)):
                event = Event(
                    cared_person_id=device.cared_person_id,
                    device_id=device.id,
                    event_type="sensor_event",
                    event_subtype="motion_detected",
                    severity="info",
                    message=f"Actividad detectada por {device.device_type}",
                    event_data=json.dumps({
                        "sensor_type": device.device_type,
                        "location": device.location_description,
                        "battery_level": device.battery_level
                    }),
                    source=device.device_id,
                    event_time=datetime.now() - timedelta(hours=random.randint(1, 72))
                )
                db.add(event)
                events.append(event)
        
        # Eventos de temperatura
        if device.device_type == "temperature_sensor":
            for i in range(random.randint(3, 8)):
                temperature = random.uniform(18.0, 28.0)
                event = Event(
                    cared_person_id=device.cared_person_id,
                    device_id=device.id,
                    event_type="sensor_event",
                    event_subtype="temperature_reading",
                    severity="info",
                    message=f"Lectura de temperatura: {temperature:.1f}°C",
                    event_data=json.dumps({
                        "temperature": temperature,
                        "location": device.location_description,
                        "unit": "celsius"
                    }),
                    source=device.device_id,
                    event_time=datetime.now() - timedelta(hours=random.randint(1, 72))
                )
                db.add(event)
                events.append(event)
    
    db.commit()
    print(f"✅ Creados {len(events)} eventos")
    return events

def create_dummy_alerts(db: Session, elderly_persons: List[CaredPerson], users: List[User]) -> List[Alert]:
    """Crear alertas dummy"""
    alert_types = ["health_alert", "security_alert", "environmental_alert", "device_alert"]
    alert_titles = [
        "Temperatura corporal elevada",
        "Caída detectada",
        "Dispositivo sin batería",
        "Movimiento inusual",
        "Medicamento no tomado",
        "Cita médica próxima",
        "Sensor offline",
        "Actividad anormal"
    ]
    
    alerts = []
    for elderly in elderly_persons:
        # Alertas de salud
        for i in range(random.randint(1, 3)):
            alert = Alert(
                alert_type="health_alert",
                alert_subtype="temperature_high",
                severity=random.choice(["medium", "high"]),
                title=random.choice(alert_titles),
                message=f"Alerta de salud para {elderly.first_name}",
                alert_data=json.dumps({"temperature": random.uniform(37.5, 39.0)}),
                status=random.choice(["active", "acknowledged", "resolved"]),
                priority=random.randint(3, 8),
                escalation_level=random.randint(0, 2),
                cared_person_id=elderly.id,
                user_id=elderly.user_id
            )
            db.add(alert)
            alerts.append(alert)
        
        # Alertas de seguridad
        for i in range(random.randint(1, 2)):
            alert = Alert(
                alert_type="security_alert",
                alert_subtype="fall_detected",
                severity="high",
                title="Caída detectada",
                message=f"Posible caída detectada para {elderly.first_name}",
                alert_data=json.dumps({"location": elderly.address}),
                status="active",
                priority=8,
                escalation_level=1,
                cared_person_id=elderly.id,
                user_id=elderly.user_id
            )
            db.add(alert)
            alerts.append(alert)
        
        # Alertas de dispositivo
        for i in range(random.randint(1, 2)):
            alert = Alert(
                alert_type="device_alert",
                alert_subtype="low_battery",
                severity="medium",
                title="Batería baja en dispositivo",
                message=f"Dispositivo con batería baja para {elderly.first_name}",
                alert_data=json.dumps({"battery_level": random.randint(5, 20)}),
                status="active",
                priority=5,
                escalation_level=0,
                cared_person_id=elderly.id,
                user_id=elderly.user_id
            )
            db.add(alert)
            alerts.append(alert)
    
    db.commit()
    print(f"✅ Creadas {len(alerts)} alertas")
    return alerts

def create_dummy_reminders(db: Session, elderly_persons: List[CaredPerson], users: List[User]) -> List[Reminder]:
    """Crear recordatorios dummy"""
    reminder_types = ["medication", "appointment", "task", "exercise", "meal"]
    reminder_titles = [
        "Tomar Enalapril",
        "Cita con el médico",
        "Ejercicio de fisioterapia",
        "Comida principal",
        "Tomar Metformina",
        "Revisión de presión arterial",
        "Paseo diario",
        "Medicación nocturna",
        "Consulta de seguimiento",
        "Ejercicios de memoria"
    ]
    
    reminders = []
    for elderly in elderly_persons:
        # Recordatorios de medicación
        for i in range(random.randint(2, 4)):
            reminder = Reminder(
                reminder_type="medication",
                title=random.choice(reminder_titles),
                description=f"Recordatorio de medicación para {elderly.first_name}",
                scheduled_time=datetime.now() + timedelta(hours=random.randint(1, 24)),
                due_date=date.today() + timedelta(days=random.randint(0, 7)),
                repeat_pattern=random.choice(["daily", "weekly", "none"]),
                status=random.choice(["pending", "completed", "missed"]),
                priority=random.randint(3, 8),
                is_important=random.choice([True, False]),
                reminder_data=json.dumps({"medication": "Enalapril", "dosage": "10mg"}),
                notes=f"Notas para {elderly.first_name}",
                user_id=elderly.user_id,
                cared_person_id=elderly.id,
                completed_by=random.choice([None, elderly.user_id]) if random.choice([True, False]) else None
            )
            db.add(reminder)
            reminders.append(reminder)
        
        # Recordatorios de citas
        for i in range(random.randint(1, 2)):
            reminder = Reminder(
                reminder_type="appointment",
                title="Cita médica",
                description=f"Cita médica para {elderly.first_name}",
                scheduled_time=datetime.now() + timedelta(days=random.randint(1, 14)),
                due_date=date.today() + timedelta(days=random.randint(1, 14)),
                repeat_pattern="none",
                status="pending",
                priority=7,
                is_important=True,
                reminder_data=json.dumps({"doctor": "Dr. Martínez", "location": "Centro Médico"}),
                notes="Llevar documentación médica",
                user_id=elderly.user_id,
                cared_person_id=elderly.id
            )
            db.add(reminder)
            reminders.append(reminder)
        
        # Recordatorios de tareas
        for i in range(random.randint(1, 3)):
            reminder = Reminder(
                reminder_type="task",
                title=random.choice(["Ejercicio físico", "Revisión de dispositivos", "Limpieza"]),
                description=f"Tarea diaria para {elderly.first_name}",
                scheduled_time=datetime.now() + timedelta(hours=random.randint(2, 12)),
                due_date=date.today(),
                repeat_pattern="daily",
                status="pending",
                priority=random.randint(4, 6),
                is_important=False,
                reminder_data=json.dumps({"task_type": "daily_routine"}),
                notes="Rutina diaria de cuidado",
                user_id=elderly.user_id,
                cared_person_id=elderly.id
            )
            db.add(reminder)
            reminders.append(reminder)
    
    db.commit()
    print(f"✅ Creados {len(reminders)} recordatorios")
    return reminders

def create_dummy_reports(db: Session, elderly_persons: List[CaredPerson], users: List[User]) -> List[Report]:
    """Crear reportes dummy"""
    report_types = ["general", "medical", "behavioral", "incident", "progress"]
    report_titles = [
        "Evaluación mensual de salud",
        "Incidente de caída menor",
        "Progreso en terapia física",
        "Cambio en medicación",
        "Visita al médico",
        "Reporte de comportamiento",
        "Actualización de estado general",
        "Incidente con dispositivo",
        "Evaluación nutricional",
        "Reporte de actividad física"
    ]
    
    reports = []
    for elderly in elderly_persons:
        # Crear 2-4 reportes por persona
        num_reports = random.randint(2, 4)
        for i in range(num_reports):
            # Fecha aleatoria en los últimos 30 días
            days_ago = random.randint(0, 30)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            report = Report(
                title=random.choice(report_titles),
                description=f"Reporte detallado sobre el estado y progreso de {elderly.first_name} {elderly.last_name}. Se observan mejoras en su condición general y se mantiene el plan de cuidado establecido.",
                report_type=random.choice(report_types),
                cared_person_id=elderly.id,
                created_by_id=elderly.user_id,
                created_at=created_at,
                is_autocuidado=random.choice([True, False]),
                attached_files=[]  # Sin archivos adjuntos por ahora
            )
            db.add(report)
            reports.append(report)
    
    db.commit()
    print(f"✅ Creados {len(reports)} reportes")
    return reports

def main():
    """Función principal para cargar todos los datos dummy"""
    print("🚀 Iniciando carga de datos dummy...")
    
    db = SessionLocal()
    try:
        clear_all_data(db)
        # Crear usuarios
        users = create_dummy_users(db)
        
        # Crear adultos mayores
        elderly_persons = create_dummy_elderly_persons(db, users)
        
        # Crear dispositivos
        devices = create_dummy_devices(db, elderly_persons)
        
        # Crear eventos
        events = create_dummy_events(db, elderly_persons, devices, users)
        
        # Crear alertas
        alerts = create_dummy_alerts(db, elderly_persons, users)
        
        # Crear recordatorios
        reminders = create_dummy_reminders(db, elderly_persons, users)
        
        # Crear reportes
        reports = create_dummy_reports(db, elderly_persons, users)
        
        print("\n🎉 ¡Datos dummy cargados exitosamente!")
        print(f"📊 Resumen:")
        print(f"   • Usuarios: {len(users)}")
        print(f"   • Adultos mayores: {len(elderly_persons)}")
        print(f"   • Dispositivos: {len(devices)}")
        print(f"   • Eventos: {len(events)}")
        print(f"   • Alertas: {len(alerts)}")
        print(f"   • Recordatorios: {len(reminders)}")
        print(f"   • Reportes: {len(reports)}")
        
        print(f"\n🔑 Credenciales de acceso:")
        print(f"   • Email: lucia.garcia@email.com")
        print(f"   • Password: password123")
        print(f"   • URL: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Error al cargar datos dummy: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 