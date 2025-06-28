#!/usr/bin/env python3
"""
Script para cargar datos dummy en la base de datos
Maneja correctamente los tipos JSONB y UUID de PostgreSQL
"""

import sys
import os
import uuid
from datetime import datetime, timedelta
import random
import json
from typing import List, Dict, Any

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.models.elderly_person import ElderlyPerson
from app.models.device import Device
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.services.auth import get_password_hash
from sqlalchemy import text

def clear_all_data(db: Session):
    """Borra todos los datos de las tablas principales en orden seguro"""
    print("🧹 Borrando datos previos...")
    db.execute(text('''
        DELETE FROM alerts;
        DELETE FROM reminders;
        DELETE FROM events;
        DELETE FROM devices;
        DELETE FROM elderly_persons;
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
            password_hash=get_password_hash(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data["phone"],
            user_type=user_data["user_type"]
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    print(f"✅ Creados {len(users)} usuarios")
    return users

def create_dummy_elderly_persons(db: Session, users: List[User]) -> List[ElderlyPerson]:
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
        # Asignar usuario familiar
        user = users[i] if i < len(users) else users[0]
        
        # Verificar si ya existe
        existing_elderly = db.query(ElderlyPerson).filter(
            ElderlyPerson.first_name == elderly_data_item["first_name"],
            ElderlyPerson.last_name == elderly_data_item["last_name"]
        ).first()
        
        if existing_elderly:
            elderly_persons.append(existing_elderly)
            continue
            
        elderly = ElderlyPerson(
            user_id=user.id,
            first_name=elderly_data_item["first_name"],
            last_name=elderly_data_item["last_name"],
            age=elderly_data_item["age"],
            address=elderly_data_item["address"],
            emergency_contacts=elderly_data_item["emergency_contacts"],  # JSONB se maneja automáticamente
            medical_conditions=elderly_data_item["medical_conditions"],  # Asegurarse que es lista de objetos
            medications=elderly_data_item["medications"],  # Asegurarse que es lista de objetos
            is_active=True
        )
        db.add(elderly)
        elderly_persons.append(elderly)
    
    db.commit()
    print(f"✅ Creados {len(elderly_persons)} adultos mayores")
    return elderly_persons

def create_dummy_devices(db: Session, elderly_persons: List[ElderlyPerson]) -> List[Device]:
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
                elderly_person_id=elderly.id,
                device_id=f"ESP32_{elderly.first_name}_{device_type}_{i+1}",
                name=f"{device_type.replace('_', ' ').title()} de {elderly.first_name}",
                location=location,
                is_active=True,
                last_heartbeat=datetime.now() - timedelta(minutes=random.randint(1, 60)),
                status=random.choice(["ready", "ready", "ready", "offline"]),  # Mayoría ready
                type=device_type
            )
            db.add(device)
            devices.append(device)
    
    db.commit()
    print(f"✅ Creados {len(devices)} dispositivos")
    return devices

def create_dummy_events(db: Session, elderly_persons: List[ElderlyPerson], devices: List[Device], users: List[User]) -> List[Event]:
    """Crear eventos dummy"""
    event_types = ["medical", "family", "medication", "sensor", "kinesiologia", "nutrition", "other"]
    
    events = []
    
    # Crear eventos de calendario (médicos, familia, etc.)
    for elderly in elderly_persons:
        # Eventos médicos
        for i in range(random.randint(2, 4)):
            event = Event(
                elderly_person_id=elderly.id,
                title=f"Consulta médica - {elderly.first_name}",
                description=f"Revisión rutinaria con el médico",
                event_type="medical",
                location="Centro Médico",
                start_datetime=datetime.now() + timedelta(days=random.randint(1, 30)),
                end_datetime=datetime.now() + timedelta(days=random.randint(1, 30), hours=1),
                created_by_id=users[0].id,
                is_active=True
            )
            db.add(event)
            events.append(event)
        
        # Eventos familiares
        for i in range(random.randint(1, 3)):
            event = Event(
                elderly_person_id=elderly.id,
                title=f"Visita familiar - {elderly.first_name}",
                description=f"Visita de familiares",
                event_type="family",
                location="Casa",
                start_datetime=datetime.now() + timedelta(days=random.randint(1, 14)),
                end_datetime=datetime.now() + timedelta(days=random.randint(1, 14), hours=2),
                created_by_id=users[0].id,
                is_active=True
            )
            db.add(event)
            events.append(event)
        
        # Eventos de medicación
        for i in range(random.randint(3, 6)):
            event = Event(
                elderly_person_id=elderly.id,
                title=f"Recordatorio medicación - {elderly.first_name}",
                description=f"Tomar medicación prescrita",
                event_type="medication",
                location="Casa",
                start_datetime=datetime.now() + timedelta(days=random.randint(0, 7)),
                end_datetime=datetime.now() + timedelta(days=random.randint(0, 7), minutes=30),
                created_by_id=users[0].id,
                is_active=True
            )
            db.add(event)
            events.append(event)
    
    # Crear eventos de sensores (pasados)
    for device in devices:
        if device.type in ["motion_sensor", "temperature_sensor", "fall_detector"]:
            # Eventos de movimiento
            for i in range(random.randint(5, 15)):
                event_time = datetime.now() - timedelta(hours=random.randint(1, 72))
                event = Event(
                    elderly_person_id=device.elderly_person_id,
                    device_id=device.id,
                    title=f"Actividad detectada - {device.name}",
                    description=f"Movimiento detectado en {device.location}",
                    event_type="sensor",
                    value={
                        "sensor_type": device.type,
                        "location": device.location,
                        "intensity": random.randint(1, 10),
                        "battery": random.randint(20, 100)
                    },
                    location=device.location,
                    start_datetime=event_time,
                    end_datetime=event_time + timedelta(minutes=random.randint(1, 5)),
                    created_by_id=users[0].id,
                    is_active=True
                )
                db.add(event)
                events.append(event)
            
            # Eventos de temperatura (si es sensor de temperatura)
            if device.type == "temperature_sensor":
                for i in range(random.randint(3, 8)):
                    event_time = datetime.now() - timedelta(hours=random.randint(1, 48))
                    temperature = random.uniform(18.0, 28.0)
                    event = Event(
                        elderly_person_id=device.elderly_person_id,
                        device_id=device.id,
                        title=f"Lectura de temperatura - {device.name}",
                        description=f"Temperatura: {temperature:.1f}°C",
                        event_type="sensor",
                        value={
                            "sensor_type": "temperature",
                            "temperature": temperature,
                            "humidity": random.uniform(40.0, 70.0),
                            "location": device.location
                        },
                        location=device.location,
                        start_datetime=event_time,
                        end_datetime=event_time + timedelta(minutes=1),
                        created_by_id=users[0].id,
                        is_active=True
                    )
                    db.add(event)
                    events.append(event)
    
    db.commit()
    print(f"✅ Creados {len(events)} eventos")
    return events

def create_dummy_alerts(db: Session, elderly_persons: List[ElderlyPerson], users: List[User]) -> List[Alert]:
    """Crear alertas dummy"""
    alert_types = ["no_movement", "fall", "medication", "temperature", "sos", "heart_rate", "blood_pressure"]
    severities = ["low", "medium", "high", "critical"]
    
    alerts = []
    
    for elderly in elderly_persons:
        # Crear 1-3 alertas por adulto mayor
        num_alerts = random.randint(1, 3)
        for i in range(num_alerts):
            alert_type = random.choice(alert_types)
            severity = random.choice(severities)
            
            # Generar mensaje según el tipo
            messages = {
                "no_movement": f"{elderly.first_name} no ha tenido actividad en las últimas 2 horas",
                "fall": f"Posible caída detectada para {elderly.first_name}",
                "medication": f"{elderly.first_name} no ha tomado su medicación",
                "temperature": f"Temperatura anormal detectada para {elderly.first_name}",
                "sos": f"Botón SOS activado por {elderly.first_name}",
                "heart_rate": f"Frecuencia cardíaca anormal para {elderly.first_name}",
                "blood_pressure": f"Presión arterial anormal para {elderly.first_name}"
            }
            
            alert = Alert(
                elderly_person_id=elderly.id,
                alert_type=alert_type,
                severity=severity,
                message=messages.get(alert_type, f"Alerta para {elderly.first_name}"),
                is_resolved=random.choice([True, True, False]),  # Mayoría resueltas
                created_by_id=users[0].id,
                is_active=True
            )
            db.add(alert)
            alerts.append(alert)
    
    db.commit()
    print(f"✅ Creados {len(alerts)} alertas")
    return alerts

def create_dummy_reminders(db: Session, elderly_persons: List[ElderlyPerson], users: List[User]) -> List[Reminder]:
    """Crear recordatorios dummy"""
    reminder_types = ["medication", "appointment", "exercise", "meal", "social"]
    
    reminders = []
    
    for elderly in elderly_persons:
        # Crear 2-4 recordatorios por adulto mayor
        num_reminders = random.randint(2, 4)
        for i in range(num_reminders):
            reminder_type = random.choice(reminder_types)
            
            # Generar título y descripción según el tipo
            titles = {
                "medication": f"Medicación - {elderly.first_name}",
                "appointment": f"Cita médica - {elderly.first_name}",
                "exercise": f"Ejercicio - {elderly.first_name}",
                "meal": f"Comida - {elderly.first_name}",
                "social": f"Actividad social - {elderly.first_name}"
            }
            
            descriptions = {
                "medication": "Tomar medicación prescrita",
                "appointment": "Recordatorio de cita médica",
                "exercise": "Realizar ejercicios de rehabilitación",
                "meal": "Preparar comida saludable",
                "social": "Llamar a familiares o amigos"
            }
            
            reminder = Reminder(
                elderly_person_id=elderly.id,
                title=titles.get(reminder_type, f"Recordatorio - {elderly.first_name}"),
                description=descriptions.get(reminder_type, "Recordatorio general"),
                scheduled_time=datetime.now() + timedelta(days=random.randint(1, 7), hours=random.randint(0, 23)),
                is_active=True,
                created_by_id=users[0].id,
                reminder_type=reminder_type
            )
            db.add(reminder)
            reminders.append(reminder)
    
    db.commit()
    print(f"✅ Creados {len(reminders)} recordatorios")
    return reminders

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
        
        print("\n🎉 ¡Datos dummy cargados exitosamente!")
        print(f"📊 Resumen:")
        print(f"   • Usuarios: {len(users)}")
        print(f"   • Adultos mayores: {len(elderly_persons)}")
        print(f"   • Dispositivos: {len(devices)}")
        print(f"   • Eventos: {len(events)}")
        print(f"   • Alertas: {len(alerts)}")
        print(f"   • Recordatorios: {len(reminders)}")
        
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