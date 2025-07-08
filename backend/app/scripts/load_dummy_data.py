#!/usr/bin/env python3
"""
Script para cargar datos dummy en la base de datos.
Incluye usuarios, personas bajo cuidado, dispositivos, eventos, alertas y recordatorios.
"""

import json
import random
import uuid
from datetime import datetime, timedelta, date
from typing import List

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.device import Device
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.institution import Institution
from app.models.medical_condition import MedicalCondition
from app.models.medication import Medication
from app.models.status_type import StatusType

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

VALID_ALERT_TYPES = [
    "health_alert", "security_alert", "environmental_alert", "device_alert",
    "location_alert", "medication_alert", "appointment_alert", "system_alert"
]

VALID_DEVICE_TYPES = [
    "sensor", "tracker", "camera", "smartphone", "tablet", 
    "wearable", "medical_device", "environmental_sensor"
]

VALID_DEVICE_STATUSES = ["active", "inactive", "maintenance", "error", "offline"]

VALID_EVENT_TYPES = [
    "sensor_event", "system_event", "user_action", "alert_event",
    "device_event", "location_event", "health_event"
]

VALID_REMINDER_TYPES = [
    "medication", "appointment", "meal", "exercise", "hygiene"
]

def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"⚠️ Error generando hash de contraseña: {e}")
        return f"$2b$12${password}"

def create_institutions(db: Session) -> List[Institution]:
    """Crear instituciones de ejemplo"""
    institutions_data = [
        {
            "name": "Centro de Cuidado San Martín",
            "description": "Centro especializado en cuidado de personas bajo cuidado",
            "institution_type": "nursing_home",
            "address": "Av. San Martín 1234, CABA",
            "phone": "+5491112345678",
            "email": "info@centrosanmartin.com"
        },
        {
            "name": "Clínica Santa María",
            "description": "Clínica especializada en geriatría",
            "institution_type": "clinic",
            "address": "Belgrano 567, La Plata",
            "phone": "+5491187654321",
            "email": "contacto@clinicasantamaria.com"
        }
    ]
    
    institutions = []
    for inst_data in institutions_data:
        try:
            institution = Institution(
                name=inst_data["name"],
                description=inst_data["description"],
                institution_type=inst_data["institution_type"],
                address=inst_data["address"],
                phone=inst_data["phone"],
                email=inst_data["email"],
                is_verified=True
            )
            db.add(institution)
            db.flush()
            institutions.append(institution)
        except Exception as e:
            print(f"⚠️ Error creando institución {inst_data['name']}: {e}")
            continue
    
    try:
        db.commit()
        print(f"✅ Creadas {len(institutions)} instituciones")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando instituciones: {e}")
        return []
    return institutions

def create_roles(db: Session) -> List[Role]:
    """Crear roles del sistema"""
    roles_data = [
        {"name": "admin", "description": "Administrador del sistema"},
        {"name": "caregiver", "description": "Cuidador profesional"},
        {"name": "family", "description": "Familiar"},
        {"name": "patient", "description": "Paciente"},
        {"name": "institution_admin", "description": "Administrador de institución"}
    ]
    
    roles = []
    for role_data in roles_data:
        try:
            role = Role(
                id=uuid.uuid4(),
                name=role_data["name"],
                description=role_data["description"],
                is_system=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(role)
            db.flush()
            roles.append(role)
        except Exception as e:
            print(f"⚠️ Error creando rol {role_data['name']}: {e}")
            continue
    
    try:
        db.commit()
        print(f"✅ Creados {len(roles)} roles")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando roles: {e}")
        return []
    return roles

def create_users(db: Session, institutions: List[Institution]) -> List[User]:
    users_data = [
        # Usuario admin principal solicitado
        {
            "email": "admin@cuiot.com",
            "username": "admin",
            "first_name": "Administrador",
            "last_name": "CUIOT",
            "phone": "+5491100000000",
            "is_freelance": False,
            "institution_id": None,
            "password": "Admin123!"
        },
        # Usuarios originales
        {
            "email": "maria.gonzalez@example.com",
            "username": "maria.gonzalez",
            "first_name": "María",
            "last_name": "González",
            "phone": "+5491112345678",
            "is_freelance": False,
            "institution_id": institutions[0].id if institutions else None,
            "password": "password123"
        },
        {
            "email": "carlos.rodriguez@example.com",
            "username": "carlos.rodriguez",
            "first_name": "Carlos",
            "last_name": "Rodríguez",
            "phone": "+5491187654321",
            "is_freelance": True,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "lucia.martinez@example.com",
            "username": "lucia.martinez",
            "first_name": "Lucía",
            "last_name": "Martínez",
            "phone": "+5491123456789",
            "is_freelance": False,
            "institution_id": institutions[1].id if len(institutions) > 1 else None,
            "password": "password123"
        },
        {
            "email": "roberto.lopez@example.com",
            "username": "roberto.lopez",
            "first_name": "Roberto",
            "last_name": "López",
            "phone": "+5491198765432",
            "is_freelance": True,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "patricia.sanchez@example.com",
            "username": "patricia.sanchez",
            "first_name": "Patricia",
            "last_name": "Sánchez",
            "phone": "+5491134567890",
            "is_freelance": False,
            "institution_id": institutions[0].id if institutions else None,
            "password": "password123"
        },
        # Cuidadores adicionales
        {
            "email": "ana.torres@example.com",
            "username": "ana.torres",
            "first_name": "Ana",
            "last_name": "Torres",
            "phone": "+5491145678901",
            "is_freelance": True,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "jorge.mendoza@example.com",
            "username": "jorge.mendoza",
            "first_name": "Jorge",
            "last_name": "Mendoza",
            "phone": "+5491156789012",
            "is_freelance": False,
            "institution_id": institutions[0].id if institutions else None,
            "password": "password123"
        },
        {
            "email": "silvia.ramirez@example.com",
            "username": "silvia.ramirez",
            "first_name": "Silvia",
            "last_name": "Ramírez",
            "phone": "+5491167890123",
            "is_freelance": True,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "miguel.herrera@example.com",
            "username": "miguel.herrera",
            "first_name": "Miguel",
            "last_name": "Herrera",
            "phone": "+5491178901234",
            "is_freelance": False,
            "institution_id": institutions[1].id if len(institutions) > 1 else None,
            "password": "password123"
        },
        # Familiares adicionales
        {
            "email": "carlos.fernandez@example.com",
            "username": "carlos.fernandez",
            "first_name": "Carlos",
            "last_name": "Fernández",
            "phone": "+5491189012345",
            "is_freelance": False,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "maria.silva@example.com",
            "username": "maria.silva",
            "first_name": "María",
            "last_name": "Silva",
            "phone": "+5491190123456",
            "is_freelance": False,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "juan.vargas@example.com",
            "username": "juan.vargas",
            "first_name": "Juan",
            "last_name": "Vargas",
            "phone": "+5491101234567",
            "is_freelance": False,
            "institution_id": None,
            "password": "password123"
        },
        # Administradores de instituciones
        {
            "email": "director.sanmartin@example.com",
            "username": "director.sanmartin",
            "first_name": "Dr. Roberto",
            "last_name": "García",
            "phone": "+5491111111111",
            "is_freelance": False,
            "institution_id": institutions[0].id if institutions else None,
            "password": "password123"
        },
        {
            "email": "director.santamaria@example.com",
            "username": "director.santamaria",
            "first_name": "Dra. Elena",
            "last_name": "Rodríguez",
            "phone": "+5491122222222",
            "is_freelance": False,
            "institution_id": institutions[1].id if len(institutions) > 1 else None,
            "password": "password123"
        },
        # Pacientes/usuarios finales
        {
            "email": "rosa.fernandez@example.com",
            "username": "rosa.fernandez",
            "first_name": "Rosa",
            "last_name": "Fernández",
            "phone": "+5491133333333",
            "is_freelance": False,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "alberto.silva@example.com",
            "username": "alberto.silva",
            "first_name": "Alberto",
            "last_name": "Silva",
            "phone": "+5491144444444",
            "is_freelance": False,
            "institution_id": None,
            "password": "password123"
        },
        {
            "email": "carmen.vargas@example.com",
            "username": "carmen.vargas",
            "first_name": "Carmen",
            "last_name": "Vargas",
            "phone": "+5491155555555",
            "is_freelance": False,
            "institution_id": None,
            "password": "password123"
        }
    ]
    users = []
    for user_data in users_data:
        try:
            user = User(
                id=uuid.uuid4(),
                email=user_data["email"],
                username=user_data["username"],
                password_hash=hash_password(user_data.get("password", "password123")),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                is_freelance=user_data["is_freelance"],
                institution_id=user_data["institution_id"],
                is_verified=True,
                is_active=True
            )
            db.add(user)
            db.flush()
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

# Diccionario de roles por email para asignación profesional y clara
default_user_roles = {
    # Admin principal
    "admin@cuiot.com": ["admin"],
    # Usuarios originales
    "maria.gonzalez@example.com": ["admin"],
    "carlos.rodriguez@example.com": ["caregiver"],
    "lucia.martinez@example.com": ["family"],
    "roberto.lopez@example.com": ["caregiver"],
    "patricia.sanchez@example.com": ["institution_admin"],
    # Cuidadores adicionales
    "ana.torres@example.com": ["caregiver"],
    "jorge.mendoza@example.com": ["caregiver"],
    "silvia.ramirez@example.com": ["caregiver"],
    "miguel.herrera@example.com": ["caregiver"],
    # Familiares adicionales
    "carlos.fernandez@example.com": ["family"],
    "maria.silva@example.com": ["family"],
    "juan.vargas@example.com": ["family"],
    # Administradores de instituciones
    "director.sanmartin@example.com": ["institution_admin"],
    "director.santamaria@example.com": ["institution_admin"],
    # Pacientes/usuarios finales
    "rosa.fernandez@example.com": ["patient"],
    "alberto.silva@example.com": ["patient"],
    "carmen.vargas@example.com": ["patient"]
}

def assign_roles(db: Session, users: List[User]):
    for user in users:
        roles = default_user_roles.get(user.email, [])
        for role_name in roles:
            try:
                # Recargar el usuario desde la base de datos por email
                db_user = db.query(User).filter_by(email=user.email).first()
                if not db_user:
                    print(f"⚠️ Usuario {user.email} no encontrado para asignar rol {role_name}")
                    continue
                UserRole.assign_role_to_user(db, db_user.id, role_name)
            except Exception as e:
                print(f"⚠️ Error asignando rol {role_name} a {user.email}: {e}")
    print("✅ Roles asignados a los usuarios")

def create_cared_persons(db: Session, users: List[User]) -> List[CaredPerson]:
    cared_data = [
        # Personas originales
        {
            "first_name": "Rosa",
            "last_name": "Fernández",
            "date_of_birth": date(1939, 5, 12),
            "gender": "F",
            "address": "Av. Corrientes 1234, CABA",
            "medical_conditions": [
                {"condition_name": "Hipertensión"},
                {"condition_name": "Diabetes tipo 2"}
            ],
            "medications": [
                {"medication_name": "Enalapril 10mg"},
                {"medication_name": "Metformina 500mg"}
            ],
            "care_level": "medium"
        },
        {
            "first_name": "Alberto",
            "last_name": "Silva",
            "date_of_birth": date(1946, 8, 22),
            "gender": "M",
            "address": "Calle San Martín 567, La Plata",
            "medical_conditions": [
                {"condition_name": "Artritis"},
                {"condition_name": "Problemas cardíacos"}
            ],
            "medications": [
                {"medication_name": "Ibuprofeno 400mg"},
                {"medication_name": "Aspirina 100mg"}
            ],
            "care_level": "high"
        },
        {
            "first_name": "Carmen",
            "last_name": "Vargas",
            "date_of_birth": date(1932, 2, 3),
            "gender": "F",
            "address": "Belgrano 890, Rosario",
            "medical_conditions": [
                {"condition_name": "Demencia senil"},
                {"condition_name": "Osteoporosis"}
            ],
            "medications": [
                {"medication_name": "Donepezilo 5mg"},
                {"medication_name": "Calcio + Vitamina D"}
            ],
            "care_level": "critical"
        },
        # Personas adicionales
        {
            "first_name": "Elena",
            "last_name": "González",
            "date_of_birth": date(1941, 3, 15),
            "gender": "F",
            "address": "Palermo 2345, CABA",
            "medical_conditions": [
                {"condition_name": "Artritis reumatoide"},
                {"condition_name": "Glaucoma"}
            ],
            "medications": [
                {"medication_name": "Metotrexato 2.5mg"},
                {"medication_name": "Timolol 0.5%"}
            ],
            "care_level": "high"
        },
        {
            "first_name": "Manuel",
            "last_name": "Rodríguez",
            "date_of_birth": date(1935, 7, 8),
            "gender": "M",
            "address": "Villa Crespo 789, CABA",
            "medical_conditions": [
                {"condition_name": "EPOC"},
                {"condition_name": "Insuficiencia cardíaca"}
            ],
            "medications": [
                {"medication_name": "Salbutamol inhalador"},
                {"medication_name": "Furosemida 40mg"}
            ],
            "care_level": "critical"
        },
        {
            "first_name": "Isabel",
            "last_name": "López",
            "date_of_birth": date(1948, 11, 20),
            "gender": "F",
            "address": "San Telmo 456, CABA",
            "medical_conditions": [
                {"condition_name": "Depresión"},
                {"condition_name": "Insomnio"}
            ],
            "medications": [
                {"medication_name": "Sertralina 50mg"},
                {"medication_name": "Zolpidem 10mg"}
            ],
            "care_level": "medium"
        },
        {
            "first_name": "Francisco",
            "last_name": "Martínez",
            "date_of_birth": date(1937, 9, 3),
            "gender": "M",
            "address": "Recoleta 123, CABA",
            "medical_conditions": [
                {"condition_name": "Parkinson"},
                {"condition_name": "Temblor esencial"}
            ],
            "medications": [
                {"medication_name": "Levodopa 100mg"},
                {"medication_name": "Propranolol 40mg"}
            ],
            "care_level": "high"
        },
        {
            "first_name": "Dolores",
            "last_name": "Pérez",
            "date_of_birth": date(1943, 12, 10),
            "gender": "F",
            "address": "Caballito 567, CABA",
            "medical_conditions": [
                {"condition_name": "Osteoporosis severa"},
                {"condition_name": "Fractura de cadera"}
            ],
            "medications": [
                {"medication_name": "Alendronato 70mg"},
                {"medication_name": "Vitamina D3 1000UI"}
            ],
            "care_level": "critical"
        },
        {
            "first_name": "Antonio",
            "last_name": "García",
            "date_of_birth": date(1940, 4, 25),
            "gender": "M",
            "address": "Almagro 890, CABA",
            "medical_conditions": [
                {"condition_name": "Cáncer de próstata"},
                {"condition_name": "Anemia"}
            ],
            "medications": [
                {"medication_name": "Bicalutamida 50mg"},
                {"medication_name": "Sulfato ferroso 325mg"}
            ],
            "care_level": "high"
        },
        {
            "first_name": "Teresa",
            "last_name": "Sánchez",
            "date_of_birth": date(1934, 6, 18),
            "gender": "F",
            "address": "Villa Urquiza 345, CABA",
            "medical_conditions": [
                {"condition_name": "Alzheimer temprano"},
                {"condition_name": "Incontinencia urinaria"}
            ],
            "medications": [
                {"medication_name": "Rivastigmina 1.5mg"},
                {"medication_name": "Oxybutinina 5mg"}
            ],
            "care_level": "critical"
        },
        {
            "first_name": "José",
            "last_name": "Torres",
            "date_of_birth": date(1945, 1, 30),
            "gender": "M",
            "address": "Belgrano 678, CABA",
            "medical_conditions": [
                {"condition_name": "Diabetes tipo 1"},
                {"condition_name": "Retinopatía diabética"}
            ],
            "medications": [
                {"medication_name": "Insulina NPH"},
                {"medication_name": "Ranibizumab inyección"}
            ],
            "care_level": "high"
        },
        {
            "first_name": "Ana",
            "last_name": "Ruiz",
            "date_of_birth": date(1938, 8, 14),
            "gender": "F",
            "address": "Colegiales 234, CABA",
            "medical_conditions": [
                {"condition_name": "Hipotiroidismo"},
                {"condition_name": "Osteoartritis"}
            ],
            "medications": [
                {"medication_name": "Levotiroxina 50mcg"},
                {"medication_name": "Glucosamina 1500mg"}
            ],
            "care_level": "medium"
        },
        {
            "first_name": "Miguel",
            "last_name": "Jiménez",
            "date_of_birth": date(1936, 10, 5),
            "gender": "M",
            "address": "Villa Pueyrredón 456, CABA",
            "medical_conditions": [
                {"condition_name": "Accidente cerebrovascular"},
                {"condition_name": "Hemiparesia derecha"}
            ],
            "medications": [
                {"medication_name": "Warfarina 5mg"},
                {"medication_name": "Atorvastatina 20mg"}
            ],
            "care_level": "critical"
        },
        {
            "first_name": "Carmen",
            "last_name": "Moreno",
            "date_of_birth": date(1942, 2, 28),
            "gender": "F",
            "address": "Villa Devoto 789, CABA",
            "medical_conditions": [
                {"condition_name": "Fibromialgia"},
                {"condition_name": "Síndrome de fatiga crónica"}
            ],
            "medications": [
                {"medication_name": "Pregabalina 75mg"},
                {"medication_name": "Amitriptilina 25mg"}
            ],
            "care_level": "medium"
        }
    ]
    cared_persons = []
    for i, data in enumerate(cared_data):
        try:
            cared = CaredPerson(
                id=uuid.uuid4(),
                first_name=data["first_name"],
                last_name=data["last_name"],
                date_of_birth=data["date_of_birth"],
                gender=data["gender"],
                address=data["address"],
                care_level=data["care_level"],
                user_id=users[i % len(users)].id,
                is_active=True
            )
            db.add(cared)
            db.flush()
            # Insertar condiciones médicas normalizadas
            for cond in data.get("medical_conditions", []):
                mc = MedicalCondition(
                    cared_person_id=cared.id,
                    condition_name=cond["condition_name"]
                )
                db.add(mc)
            # Insertar medicamentos normalizados
            for med in data.get("medications", []):
                m = Medication(
                    cared_person_id=cared.id,
                    medication_name=med["medication_name"]
                )
                db.add(m)
            cared_persons.append(cared)
        except Exception as e:
            print(f"⚠️ Error creando persona bajo cuidado {data['first_name']}: {e}")
            continue
    try:
        db.commit()
        print(f"✅ Creadas {len(cared_persons)} personas bajo cuidado")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando personas bajo cuidado: {e}")
        return []
    return cared_persons

def create_devices(db: Session, cared_persons: List[CaredPerson]) -> List[Device]:
    devices = []
    for cared in cared_persons:
        num_devices = random.randint(2, 4)
        for i in range(num_devices):
            device_type = random.choice(VALID_DEVICE_TYPES)
            try:
                device = Device(
                    id=uuid.uuid4(),
                    device_id=f"{device_type}_{cared.first_name.lower()}_{cared.last_name.lower()}_{i+1}",
                    name=f"Dispositivo {device_type} de {cared.first_name} {cared.last_name}",
                    type=device_type,
                    cared_person_id=cared.id,
                    battery_level=random.randint(20, 100),
                    signal_strength=random.randint(50, 100),
                    last_seen=datetime.now() - timedelta(hours=random.randint(0, 24))
                )
                db.add(device)
                db.flush()
                devices.append(device)
            except Exception as e:
                print(f"⚠️ Error creando dispositivo para {cared.first_name}: {e}")
                continue
    try:
        db.commit()
        print(f"✅ Creados {len(devices)} dispositivos")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando dispositivos: {e}")
        return []
    return devices

def create_events(db: Session, cared_persons: List[CaredPerson], devices: List[Device]) -> List[Event]:
    events = []
    for cared in cared_persons:
        cared_devices = [d for d in devices if d.cared_person_id == cared.id]
        num_events = random.randint(2, 4)
        for i in range(num_events):
            try:
                event = Event(
                    id=uuid.uuid4(),
                    cared_person_id=cared.id,
                    device_id=random.choice(cared_devices).id if cared_devices else None,
                    event_type=random.choice(VALID_EVENT_TYPES),
                    event_subtype=f"subtype_{i+1}",
                    severity=random.choice(["info", "warning", "error"]),
                    message=f"Evento {i+1} para {cared.first_name}",
                    event_time=datetime.now() - timedelta(days=random.randint(0, 30)),
                    source="device"
                )
                db.add(event)
                events.append(event)
            except Exception as e:
                print(f"⚠️ Error creando evento para {cared.first_name}: {e}")
                continue
    try:
        db.commit()
        print(f"✅ Creados {len(events)} eventos")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando eventos: {e}")
        return []
    return events

def get_status_type_id(db: Session, name: str, category: str) -> int:
    status_type = db.query(StatusType).filter_by(name=name, category=category).first()
    if not status_type:
        raise Exception(f"No se encontró status_type para name='{name}', category='{category}'")
    return status_type.id

def create_alerts(db: Session, cared_persons: List[CaredPerson]) -> List[Alert]:
    alerts = []
    for cared in cared_persons:
        num_alerts = random.randint(1, 3)
        for i in range(num_alerts):
            try:
                status_name = random.choice(["active", "acknowledged", "resolved"])
                status_type_id = get_status_type_id(db, status_name, "alert_status")
                alert = Alert(
                    id=uuid.uuid4(),
                    cared_person_id=cared.id,
                    alert_type=random.choice(VALID_ALERT_TYPES),
                    alert_subtype=f"subtype_{i+1}",
                    title=f"Alerta {i+1} para {cared.first_name}",
                    message=f"Alerta {i+1} para {cared.first_name}",
                    severity=random.choice(["low", "medium", "high", "critical"]),
                    status_type_id=status_type_id,
                    priority=random.randint(1, 10),
                    escalation_level=random.randint(0, 3)
                )
                db.add(alert)
                alerts.append(alert)
            except Exception as e:
                print(f"⚠️ Error creando alerta para {cared.first_name}: {e}")
                continue
    try:
        db.commit()
        print(f"✅ Creadas {len(alerts)} alertas")
    except Exception as e:
        db.rollback()
        print(f"❌ Error guardando alertas: {e}")
        return []
    return alerts

def create_reminders(db: Session, cared_persons: List[CaredPerson]) -> List[Reminder]:
    reminders = []
    for cared in cared_persons:
        num_reminders = random.randint(2, 4)
        for i in range(num_reminders):
            try:
                status_name = "pending"
                status_type_id = get_status_type_id(db, status_name, "reminder_status")
                reminder = Reminder(
                    id=uuid.uuid4(),
                    cared_person_id=cared.id,
                    title=f"Recordatorio {i+1} para {cared.first_name}",
                    description=f"Recordatorio para {cared.first_name}",
                    reminder_type_id=1,  # Usar un ID válido de reminder_type
                    scheduled_time=datetime.now() + timedelta(hours=random.randint(1, 24)),
                    status_type_id=status_type_id,
                    priority=random.randint(1, 10),
                    is_important=random.choice([True, False]),
                    is_active=True
                )
                db.add(reminder)
                reminders.append(reminder)
            except Exception as e:
                print(f"⚠️ Error creando recordatorio para {cared.first_name}: {e}")
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
    print("\n🔑 Credenciales de acceso:")
    print("=" * 50)
    for user in users:
        try:
            print(f"   📧 {user.email} | 🔐 password123")
        except Exception as e:
            print(f"   ⚠️ Error accediendo a credenciales: {e}")
            continue

def cleanup_database(db: Session) -> None:
    try:
        print("🧹 Limpiando datos existentes...")
        
        # Limpiar en orden de dependencias (hijos primero)
        try:
            db.query(Event).delete()
            print("   ✅ Events limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Event: {e}")
            db.rollback()
            
        try:
            db.query(Alert).delete()
            print("   ✅ Alerts limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Alert: {e}")
            db.rollback()
            
        try:
            db.query(Reminder).delete()
            print("   ✅ Reminders limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Reminder: {e}")
            db.rollback()
            
        try:
            db.query(Device).delete()
            print("   ✅ Devices limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Device: {e}")
            db.rollback()
            
        try:
            db.query(MedicalCondition).delete()
            print("   ✅ MedicalConditions limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar MedicalCondition: {e}")
            db.rollback()
            
        try:
            db.query(Medication).delete()
            print("   ✅ Medications limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Medication: {e}")
            db.rollback()
            
        try:
            db.query(CaredPerson).delete()
            print("   ✅ CaredPersons limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar CaredPerson: {e}")
            db.rollback()
            
        try:
            db.query(UserRole).delete()
            print("   ✅ UserRoles limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar UserRole: {e}")
            db.rollback()
            
        try:
            db.query(User).delete()
            print("   ✅ Users limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar User: {e}")
            db.rollback()
            
        try:
            db.query(Role).delete()
            print("   ✅ Roles limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Role: {e}")
            db.rollback()
            
        try:
            db.query(Institution).delete()
            print("   ✅ Institutions limpiados")
        except Exception as e:
            print(f"   ⚠️  No se pudo limpiar Institution: {e}")
            db.rollback()
            
        db.commit()
        print("✅ Base de datos limpiada completamente")
    except Exception as e:
        db.rollback()
        print(f"❌ Error limpiando base de datos: {e}")
        raise

def validate_data_integrity(db: Session) -> bool:
    try:
        user_count = db.query(User).count()
        cared_count = db.query(CaredPerson).count()
        device_count = db.query(Device).count()
        event_count = db.query(Event).count()
        alert_count = db.query(Alert).count()
        reminder_count = db.query(Reminder).count()
        institution_count = db.query(Institution).count()
        role_count = db.query(Role).count()
        
        print(f"✅ Validación exitosa: {user_count} usuarios, {cared_count} personas bajo cuidado, {device_count} dispositivos, {event_count} eventos, {alert_count} alertas, {reminder_count} recordatorios, {institution_count} instituciones, {role_count} roles")
        return True
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

def main():
    print("🚀 Iniciando carga de datos dummy...")
    db = next(get_db())
    try:
        cleanup_database(db)
        institutions = create_institutions(db)
        roles = create_roles(db)
        users = create_users(db, institutions)
        if not users:
            raise Exception("No se pudieron crear usuarios")
        assign_roles(db, users)
        cared_persons = create_cared_persons(db, users)
        if not cared_persons:
            raise Exception("No se pudieron crear personas bajo cuidado")
        devices = create_devices(db, cared_persons)
        if not devices:
            raise Exception("No se pudieron crear dispositivos")
        events = create_events(db, cared_persons, devices)
        alerts = create_alerts(db, cared_persons)
        reminders = create_reminders(db, cared_persons)
        if not validate_data_integrity(db):
            raise Exception("Validación de integridad falló")
        print("\n✅ Datos dummy cargados exitosamente!")
        print("📊 Resumen:")
        print(f"   🏥 Instituciones: {len(institutions)}")
        print(f"   👥 Usuarios: {len(users)}")
        print(f"   • Personas bajo cuidado: {len(cared_persons)}")
        print(f"   📱 Dispositivos: {len(devices)}")
        print(f"   📅 Eventos: {len(events)}")
        print(f"   🚨 Alertas: {len(alerts)}")
        print(f"   ⏰ Recordatorios: {len(reminders)}")
        print_credentials(users)
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 