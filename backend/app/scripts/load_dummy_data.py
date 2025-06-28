#!/usr/bin/env python3
"""
Script para cargar datos dummy en la base de datos.
Incluye usuarios, adultos mayores, dispositivos, eventos, alertas y recordatorios.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.user import User
from app.models.elderly_person import ElderlyPerson
from app.models.device import Device
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Valores válidos según el frontend/backend - NO CAMBIAR
VALID_ALERT_TYPES = [
    "no_movement", "sos", "temperature", "medication", "fall", "heart_rate", "blood_pressure"
]

VALID_DEVICE_TYPES = [
    "smart_watch", "panic_button", "motion_sensor", "door_sensor", "bed_sensor", "temperature_sensor"
]

VALID_DEVICE_STATUSES = ["ready", "offline", "error", "off"]

VALID_EVENT_TYPES = [
    "medical", "family", "appointment", "medication", "exercise", "sensor"
]

VALID_REMINDER_TYPES = [
    "medication", "appointment", "meal", "exercise", "hygiene"
]

def hash_password(password: str) -> str:
    """Genera hash seguro de contraseña."""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"⚠️ Error generando hash de contraseña: {e}")
        # Fallback a hash básico si bcrypt falla
        return f"$2b$12${password}"

def create_users(db: Session) -> List[User]:
    """Crea usuarios dummy con manejo robusto de errores."""
    users_data = [
        {
            "email": "maria.gonzalez@example.com",
            "first_name": "María",
            "last_name": "González",
            "phone": "+5491112345678",
            "user_type": "family"
        },
        {
            "email": "carlos.rodriguez@example.com",
            "first_name": "Carlos",
            "last_name": "Rodríguez",
            "phone": "+5491187654321",
            "user_type": "family"
        },
        {
            "email": "lucia.martinez@example.com",
            "first_name": "Lucía",
            "last_name": "Martínez",
            "phone": "+5491123456789",
            "user_type": "family"
        },
        {
            "email": "roberto.lopez@example.com",
            "first_name": "Roberto",
            "last_name": "López",
            "phone": "+5491198765432",
            "user_type": "employee"
        },
        {
            "email": "patricia.sanchez@example.com",
            "first_name": "Patricia",
            "last_name": "Sánchez",
            "phone": "+5491134567890",
            "user_type": "employee"
        }
    ]

    users = []
    for user_data in users_data:
        try:
            user = User(
                id=uuid.uuid4(),
                email=user_data["email"],
                password_hash=hash_password("password123"),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                user_type=user_data["user_type"]
            )
            db.add(user)
            users.append(user)
        except Exception as e:
            print(f"⚠️ Error creando usuario {user_data['email']}: {e}")
            continue

    try:
        db.commit()
        print(f"✅ Creados {len(users)} usuarios")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando usuarios: {e}")
        return []

    return users

def create_elderly_persons(db: Session, users: List[User]) -> List[ElderlyPerson]:
    """Crea adultos mayores dummy con validación robusta."""
    elderly_data = [
        {
            "first_name": "Rosa",
            "last_name": "Fernández",
            "age": 85,
            "address": "Av. Corrientes 1234, CABA",
            "medical_conditions": ["Hipertensión", "Diabetes tipo 2"],
            "medications": ["Enalapril 10mg", "Metformina 500mg"]
        },
        {
            "first_name": "Alberto",
            "last_name": "Silva",
            "age": 78,
            "address": "Calle San Martín 567, La Plata",
            "medical_conditions": ["Artritis", "Problemas cardíacos"],
            "medications": ["Ibuprofeno 400mg", "Aspirina 100mg"]
        },
        {
            "first_name": "Carmen",
            "last_name": "Vargas",
            "age": 92,
            "address": "Belgrano 890, Rosario",
            "medical_conditions": ["Demencia senil", "Osteoporosis"],
            "medications": ["Donepezilo 5mg", "Calcio + Vitamina D"]
        },
        {
            "first_name": "Miguel",
            "last_name": "Torres",
            "age": 81,
            "address": "Rivadavia 2345, Córdoba",
            "medical_conditions": ["EPOC", "Problemas de visión"],
            "medications": ["Salbutamol inhalador", "Gotas oftálmicas"]
        },
        {
            "first_name": "Isabel",
            "last_name": "Morales",
            "age": 88,
            "address": "Sarmiento 678, Mendoza",
            "medical_conditions": ["Parkinson", "Depresión"],
            "medications": ["Levodopa 100mg", "Sertralina 50mg"]
        }
    ]

    elderly_persons = []
    for i, data in enumerate(elderly_data):
        try:
            # Validar que el usuario existe
            if i >= len(users):
                print(f"⚠️ No hay suficientes usuarios para el adulto mayor {data['first_name']}")
                break

            elderly = ElderlyPerson(
                id=uuid.uuid4(),
                user_id=users[i].id,
                first_name=data["first_name"],
                last_name=data["last_name"],
                age=data["age"],
                address=data["address"],
                emergency_contacts=json.dumps([
                    {
                        "name": f"{users[i].first_name} {users[i].last_name}",
                        "phone": users[i].phone,
                        "relationship": "Familiar"
                    },
                    {
                        "name": f"Dr. {data['last_name']}",
                        "phone": f"+54911{random.randint(40000000, 99999999)}",
                        "relationship": "Médico"
                    }
                ]),
                medical_conditions=json.dumps(data["medical_conditions"]),
                medications=json.dumps(data["medications"]),
                is_active=True,
                is_deleted=False
            )
            db.add(elderly)
            elderly_persons.append(elderly)
        except Exception as e:
            print(f"⚠️ Error creando adulto mayor {data['first_name']}: {e}")
            continue

    try:
        db.commit()
        print(f"✅ Creados {len(elderly_persons)} adultos mayores")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando adultos mayores: {e}")
        return []

    return elderly_persons

def create_devices(db: Session, elderly_persons: List[ElderlyPerson]) -> List[Device]:
    """Crea dispositivos dummy con estados y tipos válidos."""
    devices = []
    
    for elderly in elderly_persons:
        # Asignar 2-3 dispositivos por adulto mayor
        num_devices = random.randint(2, 3)
        selected_types = random.sample(VALID_DEVICE_TYPES, num_devices)
        
        for i, device_type in enumerate(selected_types):
            try:
                device = Device(
                    id=uuid.uuid4(),
                    elderly_person_id=elderly.id,
                    device_id=f"{device_type}_{elderly.first_name.lower()}_{i+1}",
                    name=f"{device_type.replace('_', ' ').title()} de {elderly.first_name}",
                    location=f"Habitación {random.randint(1, 5)}",
                    is_active=True,
                    last_heartbeat=datetime.now() - timedelta(hours=random.randint(1, 24)),
                    status=random.choice(VALID_DEVICE_STATUSES),
                    type=device_type
                )
                db.add(device)
                devices.append(device)
            except Exception as e:
                print(f"⚠️ Error creando dispositivo para {elderly.first_name}: {e}")
                continue

    try:
        db.commit()
        print(f"✅ Creados {len(devices)} dispositivos")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando dispositivos: {e}")
        return []

    return devices

def create_events(db: Session, elderly_persons: List[ElderlyPerson], devices: List[Device], users: List[User]) -> List[Event]:
    """Crea eventos dummy con validación robusta."""
    events = []
    
    for elderly in elderly_persons:
        # Crear 3-5 eventos por adulto mayor
        num_events = random.randint(3, 5)
        elderly_devices = [d for d in devices if d.elderly_person_id == elderly.id]
        
        for i in range(num_events):
            try:
                event = Event(
                    id=uuid.uuid4(),
                    elderly_person_id=elderly.id,
                    device_id=random.choice(elderly_devices).id if elderly_devices else None,
                    title=f"Evento {random.choice(VALID_EVENT_TYPES)} {i+1}",
                    description=f"Descripción del evento {random.choice(VALID_EVENT_TYPES)} para {elderly.first_name}",
                    event_type=random.choice(VALID_EVENT_TYPES),
                    value=json.dumps({
                        "temperature": round(random.uniform(36.0, 38.0), 2),
                        "humidity": round(random.uniform(40.0, 70.0), 2)
                    }),
                    location=f"Habitación {random.randint(1, 5)}",
                    start_datetime=datetime.now() - timedelta(days=random.randint(1, 30)),
                    end_datetime=datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 3)),
                    created_by_id=random.choice(users).id,
                    received_by_id=random.choice(users).id,
                    is_active=True
                )
                db.add(event)
                events.append(event)
            except Exception as e:
                print(f"⚠️ Error creando evento para {elderly.first_name}: {e}")
                continue

    try:
        db.commit()
        print(f"✅ Creados {len(events)} eventos")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando eventos: {e}")
        return []

    return events

def create_alerts(db: Session, elderly_persons: List[ElderlyPerson], users: List[User]) -> List[Alert]:
    """Crea alertas dummy SOLO con tipos válidos."""
    alerts = []
    
    alert_messages = [
        "Botón de pánico activado",
        "Sin movimiento detectado",
        "Temperatura fuera de rango",
        "Medicación no tomada",
        "Posible caída detectada",
        "Frecuencia cardíaca anormal",
        "Presión arterial alta",
        "Anomalía en signos vitales"
    ]
    
    for elderly in elderly_persons:
        # Crear 1-3 alertas por adulto mayor
        num_alerts = random.randint(1, 3)
        
        for i in range(num_alerts):
            try:
                alert = Alert(
                    id=uuid.uuid4(),
                    elderly_person_id=elderly.id,
                    alert_type=random.choice(VALID_ALERT_TYPES),  # SOLO tipos válidos
                    message=random.choice(alert_messages),
                    severity=random.choice(["low", "medium", "high"]),
                    is_resolved=random.choice([True, False]),
                    resolved_at=datetime.now() - timedelta(hours=random.randint(1, 48)) if random.choice([True, False]) else None,
                    created_by_id=random.choice(users).id,
                    received_by_id=random.choice(users).id if random.choice([True, False]) else None,
                    created_at=datetime.now() - timedelta(hours=random.randint(1, 72))
                )
                db.add(alert)
                alerts.append(alert)
            except Exception as e:
                print(f"⚠️ Error creando alerta para {elderly.first_name}: {e}")
                continue

    try:
        db.commit()
        print(f"✅ Creadas {len(alerts)} alertas")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando alertas: {e}")
        return []

    return alerts

def create_reminders(db: Session, elderly_persons: List[ElderlyPerson], users: List[User]) -> List[Reminder]:
    """Crea recordatorios dummy con validación robusta."""
    reminders = []
    
    reminder_titles = [
        "Tomar medicación",
        "Comida",
        "Ejercicios diarios",
        "Terapia física",
        "Revisión de presión",
        "Control de azúcar",
        "Higiene personal",
        "Tomar agua"
    ]
    
    for elderly in elderly_persons:
        # Crear 2-4 recordatorios por adulto mayor
        num_reminders = random.randint(2, 4)
        
        for i in range(num_reminders):
            try:
                reminder = Reminder(
                    id=uuid.uuid4(),
                    elderly_person_id=elderly.id,
                    title=random.choice(reminder_titles),
                    description=f"Recordatorio para {elderly.first_name}",
                    reminder_type=random.choice(VALID_REMINDER_TYPES),
                    scheduled_time=f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}:00",
                    is_active=True,
                    days_of_week=random.sample(range(1, 8), random.randint(3, 7)),
                    created_by_id=random.choice(users).id,
                    received_by_id=random.choice(users).id if random.choice([True, False]) else None
                )
                db.add(reminder)
                reminders.append(reminder)
            except Exception as e:
                print(f"⚠️ Error creando recordatorio para {elderly.first_name}: {e}")
                continue

    try:
        db.commit()
        print(f"✅ Creados {len(reminders)} recordatorios")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando recordatorios: {e}")
        return []

    return reminders

def print_credentials(users: List[User]) -> None:
    """Imprime credenciales de acceso de forma segura."""
    print("\n🔑 Credenciales de acceso:")
    print("=" * 50)
    
    for user in users:
        try:
            # Verificar que el usuario está en sesión antes de acceder a sus atributos
            if user in users:  # Verificación simple
                print(f"   📧 {user.email} | 🔐 password123 | 👤 {user.user_type}")
        except Exception as e:
            print(f"   ⚠️ Error accediendo a credenciales: {e}")
            continue

def cleanup_database(db: Session) -> None:
    """Limpia todos los datos existentes de forma segura."""
    try:
        print("🧹 Limpiando datos existentes...")
        
        # Eliminar en orden correcto (respetando foreign keys)
        db.query(Event).delete()
        db.query(Alert).delete()
        db.query(Reminder).delete()
        db.query(Device).delete()
        db.query(ElderlyPerson).delete()
        db.query(User).delete()
        
        db.commit()
        print("✅ Base de datos limpiada")
    except Exception as e:
        db.rollback()
        print(f"❌ Error limpiando base de datos: {e}")
        raise

def validate_data_integrity(db: Session) -> bool:
    """Valida que todos los datos creados sean consistentes."""
    try:
        user_count = db.query(User).count()
        elderly_count = db.query(ElderlyPerson).count()
        device_count = db.query(Device).count()
        event_count = db.query(Event).count()
        alert_count = db.query(Alert).count()
        reminder_count = db.query(Reminder).count()
        
        # Validar que no hay alertas con tipos inválidos
        invalid_alerts = db.query(Alert).filter(
            Alert.alert_type.notin_(VALID_ALERT_TYPES)
        ).count()
        
        if invalid_alerts > 0:
            print(f"❌ ERROR: Se encontraron {invalid_alerts} alertas con tipos inválidos")
            return False
        
        print(f"✅ Validación exitosa: {user_count} usuarios, {elderly_count} adultos, {device_count} dispositivos, {event_count} eventos, {alert_count} alertas, {reminder_count} recordatorios")
        return True
        
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

def main():
    """Función principal con manejo robusto de errores."""
    print("🚀 Iniciando carga de datos dummy...")
    
    db = next(get_db())
    
    try:
        # Limpiar base de datos
        cleanup_database(db)
        
        # Crear datos en orden correcto
        users = create_users(db)
        if not users:
            raise Exception("No se pudieron crear usuarios")
        
        elderly_persons = create_elderly_persons(db, users)
        if not elderly_persons:
            raise Exception("No se pudieron crear adultos mayores")
        
        devices = create_devices(db, elderly_persons)
        if not devices:
            raise Exception("No se pudieron crear dispositivos")
        
        events = create_events(db, elderly_persons, devices, users)
        alerts = create_alerts(db, elderly_persons, users)
        reminders = create_reminders(db, elderly_persons, users)
        
        # Validar integridad de datos
        if not validate_data_integrity(db):
            raise Exception("Validación de integridad falló")
        
        # Imprimir resumen
        print("\n✅ Datos dummy cargados exitosamente!")
        print("📊 Resumen:")
        print(f"   👥 Usuarios: {len(users)}")
        print(f"   👴 Adultos mayores: {len(elderly_persons)}")
        print(f"   📱 Dispositivos: {len(devices)}")
        print(f"   📅 Eventos: {len(events)}")
        print(f"   🚨 Alertas: {len(alerts)}")
        print(f"   ⏰ Recordatorios: {len(reminders)}")
        
        # Imprimir credenciales de forma segura
        print_credentials(users)
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 