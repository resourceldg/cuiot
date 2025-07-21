#!/usr/bin/env python3
"""
Script final de población de datos para CUIOT
- Basado en reglas de negocio y estructura UML
- Roles corregidos según especificaciones
- Sin duplicaciones
- Población completa de todas las entidades
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, timezone
import json
import uuid
from random import choice

# Importar todos los modelos necesarios
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.models.institution import Institution
from app.models.package import Package, UserPackage
from app.models.cared_person import CaredPerson
from app.models.status_type import StatusType
from app.models.device_type import DeviceType
from app.models.alert_type import AlertType
from app.models.event_type import EventType
from app.models.reminder_type import ReminderType
from app.models.service_type import ServiceType
from app.models.caregiver_assignment_type import CaregiverAssignmentType
from app.models.shift_observation_type import ShiftObservationType
from app.models.referral_type import ReferralType
from app.models.relationship_type import RelationshipType
from app.models.report_type import ReportType
# from app.models.activity_type import ActivityType  # ELIMINADO
# from app.models.difficulty_level import DifficultyLevel  # ELIMINADO
from app.models.device import Device
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.caregiver_assignment import CaregiverAssignment
from app.models.cared_person_institution import CaredPersonInstitution
from app.models.caregiver_institution import CaregiverInstitution
from app.models.diagnosis import Diagnosis
from app.models.medical_profile import MedicalProfile
from app.models.medication_schedule import MedicationSchedule
from app.models.restraint_protocol import RestraintProtocol
from app.models.shift_observation import ShiftObservation
from app.models.referral import Referral
from app.models.report import Report
from app.models.billing_record import BillingRecord
from app.services.auth import AuthService

def populate_catalog_tables(db: Session):
    """Poblar todas las tablas de catálogo normalizadas"""
    print("📋 Poblando tablas de catálogo...")
    
    # 1. Status Types
    status_types_data = [
        {"name": "active", "description": "Activo", "category": "general"},
        {"name": "inactive", "description": "Inactivo", "category": "general"},
        {"name": "pending", "description": "Pendiente", "category": "general"},
        {"name": "completed", "description": "Completado", "category": "general"},
        {"name": "cancelled", "description": "Cancelado", "category": "general"},
        {"name": "suspended", "description": "Suspendido", "category": "general"},
        {"name": "maintenance", "description": "En mantenimiento", "category": "device"},
        {"name": "error", "description": "Error", "category": "device"},
        {"name": "offline", "description": "Desconectado", "category": "device"},
        {"name": "online", "description": "Conectado", "category": "device"},
        {"name": "paid", "description": "Pagado", "category": "billing"},
        {"name": "unpaid", "description": "No pagado", "category": "billing"},
        {"name": "overdue", "description": "Vencido", "category": "billing"},
        {"name": "acknowledged", "description": "Reconocido", "category": "alert"},
        {"name": "resolved", "description": "Resuelto", "category": "alert"},
        {"name": "escalated", "description": "Escalado", "category": "alert"},
    ]
    
    status_types = {}
    for data in status_types_data:
        status = db.query(StatusType).filter(StatusType.name == data["name"]).first()
        if not status:
            status = StatusType(**data)
            db.add(status)
            db.flush()
        status_types[data["name"]] = status
    
    # 2. Device Types
    device_types_data = [
        {"name": "motion_sensor", "description": "Sensor de movimiento", "category": "sensor", "icon_name": "motion", "color_code": "#FF6B6B"},
        {"name": "temperature_sensor", "description": "Sensor de temperatura", "category": "sensor", "icon_name": "thermometer", "color_code": "#4ECDC4"},
        {"name": "gps_tracker", "description": "Rastreador GPS", "category": "tracker", "icon_name": "map-pin", "color_code": "#45B7D1"},
        {"name": "camera", "description": "Cámara de seguridad", "category": "camera", "icon_name": "camera", "color_code": "#96CEB4"},
        {"name": "wearable", "description": "Dispositivo wearable", "category": "wearable", "icon_name": "watch", "color_code": "#FFEAA7"},
        {"name": "fall_detector", "description": "Detector de caídas", "category": "sensor", "icon_name": "alert-triangle", "color_code": "#DDA0DD"},
    ]
    
    device_types = {}
    for data in device_types_data:
        device_type = db.query(DeviceType).filter(DeviceType.name == data["name"]).first()
        if not device_type:
            device_type = DeviceType(**data)
            db.add(device_type)
            db.flush()
        device_types[data["name"]] = device_type
    
    # 3. Alert Types
    alert_types_data = [
        {"name": "fall_detected", "description": "Caída detectada", "category": "health", "icon_name": "alert-triangle", "color_code": "#FF0000"},
        {"name": "temperature_high", "description": "Temperatura alta", "category": "health", "icon_name": "thermometer", "color_code": "#FF6B6B"},
        {"name": "device_offline", "description": "Dispositivo desconectado", "category": "system", "icon_name": "wifi-off", "color_code": "#FFA500"},
        {"name": "medication_due", "description": "Medicación pendiente", "category": "health", "icon_name": "pill", "color_code": "#4ECDC4"},
        {"name": "geofence_exit", "description": "Salida de zona segura", "category": "security", "icon_name": "map-pin", "color_code": "#FFD93D"},
    ]
    
    alert_types = {}
    for data in alert_types_data:
        alert_type = db.query(AlertType).filter(AlertType.name == data["name"]).first()
        if not alert_type:
            alert_type = AlertType(**data)
            db.add(alert_type)
            db.flush()
        alert_types[data["name"]] = alert_type
    
    # 4. Event Types
    event_types_data = [
        {"name": "motion_detected", "description": "Movimiento detectado", "category": "sensor", "icon_name": "activity", "color_code": "#4ECDC4"},
        {"name": "temperature_reading", "description": "Lectura de temperatura", "category": "sensor", "icon_name": "thermometer", "color_code": "#FF6B6B"},
        {"name": "location_update", "description": "Actualización de ubicación", "category": "tracker", "icon_name": "map-pin", "color_code": "#45B7D1"},
        {"name": "device_status", "description": "Estado del dispositivo", "category": "system", "icon_name": "settings", "color_code": "#96CEB4"},
    ]
    
    event_types = {}
    for data in event_types_data:
        event_type = db.query(EventType).filter(EventType.name == data["name"]).first()
        if not event_type:
            event_type = EventType(**data)
            db.add(event_type)
            db.flush()
        event_types[data["name"]] = event_type
    
    # 5. Reminder Types
    reminder_types_data = [
        {"name": "medication", "description": "Medicación", "category": "health", "icon_name": "pill", "color_code": "#4ECDC4"},
        {"name": "appointment", "description": "Cita médica", "category": "health", "icon_name": "calendar", "color_code": "#45B7D1"},
        {"name": "exercise", "description": "Ejercicio", "category": "health", "icon_name": "activity", "color_code": "#96CEB4"},
        {"name": "meal", "description": "Comida", "category": "daily", "icon_name": "utensils", "color_code": "#FFEAA7"},
        {"name": "hygiene", "description": "Higiene", "category": "daily", "icon_name": "droplets", "color_code": "#DDA0DD"},
    ]
    
    reminder_types = {}
    for data in reminder_types_data:
        reminder_type = db.query(ReminderType).filter(ReminderType.name == data["name"]).first()
        if not reminder_type:
            reminder_type = ReminderType(**data)
            db.add(reminder_type)
            db.flush()
        reminder_types[data["name"]] = reminder_type
    
    # 6. Service Types
    service_types_data = [
        {"name": "inpatient", "description": "Internación", "category": "healthcare"},
        {"name": "outpatient", "description": "Ambulatorio", "category": "healthcare"},
        {"name": "day_care", "description": "Cuidado diurno", "category": "caregiving"},
        {"name": "emergency", "description": "Emergencia", "category": "healthcare"},
        {"name": "consultation", "description": "Consulta", "category": "healthcare"},
        {"name": "rehabilitation", "description": "Rehabilitación", "category": "healthcare"},
        {"name": "therapy", "description": "Terapia", "category": "healthcare"},
        {"name": "nursing", "description": "Enfermería", "category": "healthcare"},
    ]
    
    service_types = {}
    for data in service_types_data:
        service_type = db.query(ServiceType).filter(ServiceType.name == data["name"]).first()
        if not service_type:
            service_type = ServiceType(**data)
            db.add(service_type)
            db.flush()
        service_types[data["name"]] = service_type
    
    # 7. Caregiver Assignment Types
    caregiver_assignment_types_data = [
        {"name": "full_time", "description": "Tiempo completo", "category": "schedule"},
        {"name": "part_time", "description": "Tiempo parcial", "category": "schedule"},
        {"name": "on_call", "description": "De guardia", "category": "schedule"},
        {"name": "night_shift", "description": "Turno nocturno", "category": "schedule"},
        {"name": "weekend", "description": "Fines de semana", "category": "schedule"},
    ]
    
    caregiver_assignment_types = {}
    for data in caregiver_assignment_types_data:
        assignment_type = db.query(CaregiverAssignmentType).filter(CaregiverAssignmentType.name == data["name"]).first()
        if not assignment_type:
            assignment_type = CaregiverAssignmentType(**data)
            db.add(assignment_type)
            db.flush()
        caregiver_assignment_types[data["name"]] = assignment_type
    
    # 8. Shift Observation Types
    shift_observation_types_data = [
        {"name": "morning", "description": "Turno mañana", "category": "shift"},
        {"name": "afternoon", "description": "Turno tarde", "category": "shift"},
        {"name": "night", "description": "Turno noche", "category": "shift"},
        {"name": "special", "description": "Turno especial", "category": "shift"},
    ]
    
    shift_observation_types = {}
    for data in shift_observation_types_data:
        observation_type = db.query(ShiftObservationType).filter(ShiftObservationType.name == data["name"]).first()
        if not observation_type:
            observation_type = ShiftObservationType(**data)
            db.add(observation_type)
            db.flush()
        shift_observation_types[data["name"]] = observation_type
    
    # 9. Referral Types
    referral_types_data = [
        {"name": "caregiver", "description": "Referido por cuidador", "category": "referral"},
        {"name": "institution", "description": "Referido por institución", "category": "referral"},
        {"name": "family", "description": "Referido por familiar", "category": "referral"},
        {"name": "cared_person", "description": "Referido por persona cuidada", "category": "referral"},
    ]
    
    referral_types = {}
    for data in referral_types_data:
        referral_type = db.query(ReferralType).filter(ReferralType.name == data["name"]).first()
        if not referral_type:
            referral_type = ReferralType(**data)
            db.add(referral_type)
            db.flush()
        referral_types[data["name"]] = referral_type
    
    # 10. Relationship Types
    relationship_types_data = [
        {"name": "employee", "description": "Empleado"},
        {"name": "contractor", "description": "Contratista"},
        {"name": "volunteer", "description": "Voluntario"},
        {"name": "consultant", "description": "Consultor"},
    ]
    
    relationship_types = {}
    for data in relationship_types_data:
        relationship_type = db.query(RelationshipType).filter(RelationshipType.name == data["name"]).first()
        if not relationship_type:
            relationship_type = RelationshipType(**data)
            db.add(relationship_type)
            db.flush()
        relationship_types[data["name"]] = relationship_type
    
    # 11. Report Types
    report_types_data = [
        {"name": "daily", "description": "Reporte diario"},
        {"name": "weekly", "description": "Reporte semanal"},
        {"name": "monthly", "description": "Reporte mensual"},
        {"name": "incident", "description": "Reporte de incidente"},
        {"name": "medical", "description": "Reporte médico"},
    ]
    
    report_types = {}
    for data in report_types_data:
        report_type = db.query(ReportType).filter(ReportType.name == data["name"]).first()
        if not report_type:
            report_type = ReportType(**data)
            db.add(report_type)
            db.flush()
        report_types[data["name"]] = report_type
    
    # 12. Activity Types - ELIMINADO (tabla no existe en BD)
    # activity_types_data = [
    #     {"type_name": "physical_exercise", "description": "Ejercicio físico", "requirements": {"equipment": ["silla", "bastón"], "skills": ["movilidad básica"]}},
    #     {"type_name": "cognitive_stimulation", "description": "Estimulación cognitiva", "requirements": {"equipment": ["puzzles", "libros"], "skills": ["concentración"]}},
    #     {"type_name": "social_interaction", "description": "Interacción social", "requirements": {"equipment": [], "skills": ["comunicación"]}},
    #     {"type_name": "art_therapy", "description": "Terapia artística", "requirements": {"equipment": ["pinceles", "papel"], "skills": ["creatividad"]}},
    # ]
    
    # activity_types = {}
    # for data in activity_types_data:
    #     activity_type = db.query(ActivityType).filter(ActivityType.type_name == data["type_name"]).first()
    #     if not activity_type:
    #         activity_type = ActivityType(**data)
    #         db.add(activity_type)
    #         db.flush()
    #     activity_types[data["type_name"]] = activity_type
    
    # 13. Difficulty Levels - ELIMINADO (tabla no existe en BD)
    # difficulty_levels_data = [
    #     {"name": "easy", "description": "Fácil", "color_code": "#4ECDC4"},
    #     {"name": "moderate", "description": "Moderado", "color_code": "#FFEAA7"},
    #     {"name": "difficult", "description": "Difícil", "color_code": "#FF6B6B"},
    #     {"name": "expert", "description": "Experto", "color_code": "#DDA0DD"},
    # ]
    
    # difficulty_levels = {}
    # for data in difficulty_levels_data:
    #     difficulty_level = db.query(DifficultyLevel).filter(DifficultyLevel.name == data["name"]).first()
    #     if not difficulty_level:
    #         difficulty_level = DifficultyLevel(**data)
    #         db.add(difficulty_level)
    #         db.flush()
    #     difficulty_levels[data["name"]] = difficulty_level
    
    db.commit()
    print(f"   ✅ Tablas de catálogo pobladas")
    
    return {
        "status_types": status_types,
        "device_types": device_types,
        "alert_types": alert_types,
        "event_types": event_types,
        "reminder_types": reminder_types,
        "service_types": service_types,
        "caregiver_assignment_types": caregiver_assignment_types,
        "shift_observation_types": shift_observation_types,
        "referral_types": referral_types,
        "relationship_types": relationship_types,
        "report_types": report_types,
        # "activity_types": activity_types,  # ELIMINADO
        # "difficulty_levels": difficulty_levels,  # ELIMINADO
    }

def populate_roles(db: Session):
    """Poblar roles del sistema"""
    print("👥 Poblando roles...")
    
    roles_data = [
        {"name": "admin", "description": "Administrador del sistema (Sysadmin)"},
        {"name": "institution_admin", "description": "Administrador de institución"},
        {"name": "caregiver", "description": "Cuidador profesional"},
        {"name": "family_member", "description": "Familiar de persona cuidada"},
        {"name": "caredperson", "description": "Persona bajo cuidado"},
        {"name": "medical_staff", "description": "Personal médico"},
        {"name": "freelance_caregiver", "description": "Cuidador freelance"},
        {"name": "institution_staff", "description": "Personal de institución"},
    ]
    
    roles = {}
    for data in roles_data:
        role = db.query(Role).filter(Role.name == data["name"]).first()
        if not role:
            now = datetime.now(timezone.utc)
            role = Role(**data, created_at=now, updated_at=now)
            db.add(role)
            db.flush()
        roles[data["name"]] = role
    
    db.commit()
    print(f"   ✅ {len(roles)} roles creados")
    return roles

def populate_institutions(db: Session):
    """Poblar instituciones"""
    print("🏥 Poblando instituciones...")
    
    institutions_data = [
        {
            "name": "Hospital General San Martín",
            "institution_type": "hospital",
            "address": "Av. San Martín 1234, CABA",
            "phone": "+54 11 4123-4567",
            "email": "info@hospitalsanmartin.com",
            "description": "Hospital general con servicios de geriatría"
        },
        {
            "name": "Clínica Santa María",
            "institution_type": "clinic",
            "address": "Calle Santa María 567, CABA",
            "phone": "+54 11 4789-0123",
            "email": "contacto@clinicasantamaria.com",
            "description": "Clínica especializada en cuidados geriátricos"
        },
        {
            "name": "Centro de Cuidados El Amanecer",
            "institution_type": "care_center",
            "address": "Ruta 5 Km 25, San Isidro",
            "phone": "+54 11 4567-8901",
            "email": "info@elamanecer.com",
            "description": "Centro de cuidados diurnos y residenciales"
        },
        {
            "name": "Residencia Los Abuelos",
            "institution_type": "nursing_home",
            "address": "Av. Libertador 890, Vicente López",
            "phone": "+54 11 4345-6789",
            "email": "residencia@losabuelos.com",
            "description": "Residencia geriátrica con atención 24/7"
        },
        {
            "name": "Centro Médico Integral",
            "institution_type": "medical_center",
            "address": "Calle Principal 321, San Fernando",
            "phone": "+54 11 4234-5678",
            "email": "centro@medicointegral.com",
            "description": "Centro médico con especialidad en geriatría"
        }
    ]
    
    institutions = {}
    for data in institutions_data:
        institution = db.query(Institution).filter(Institution.name == data["name"]).first()
        if not institution:
            institution = Institution(**data)
            db.add(institution)
            db.flush()
        institutions[data["name"]] = institution
    
    db.commit()
    print(f"   ✅ {len(institutions)} instituciones creadas")
    return institutions

def populate_packages(db: Session):
    """Poblar paquetes de servicios"""
    print("📦 Poblando paquetes...")
    
    packages_data = [
        {
            "name": "Básico",
            "package_type": "individual",
            "price_monthly": 50000,  # $500 ARS
            "description": "Cuidados básicos con monitoreo esencial",
            "features": {"monitoring": True, "alerts": True, "reports": False, "devices": 1, "users": 2}
        },
        {
            "name": "Estándar",
            "package_type": "individual",
            "price_monthly": 75000,  # $750 ARS
            "description": "Cuidados estándar con reportes básicos",
            "features": {"monitoring": True, "alerts": True, "reports": True, "devices": 2, "users": 3}
        },
        {
            "name": "Premium",
            "package_type": "professional",
            "price_monthly": 100000,  # $1000 ARS
            "description": "Cuidados premium con funcionalidades avanzadas",
            "features": {"monitoring": True, "alerts": True, "reports": True, "devices": 3, "users": 5, "advanced_analytics": True}
        },
        {
            "name": "Especializado",
            "package_type": "professional",
            "price_monthly": 125000,  # $1250 ARS
            "description": "Cuidados especializados con personalización",
            "features": {"monitoring": True, "alerts": True, "reports": True, "devices": 5, "users": 10, "advanced_analytics": True, "customization": True}
        },
        {
            "name": "Intensivo",
            "package_type": "institutional",
            "price_monthly": 150000,  # $1500 ARS
            "description": "Cuidados intensivos para instituciones",
            "features": {"monitoring": True, "alerts": True, "reports": True, "devices": 10, "users": 20, "advanced_analytics": True, "customization": True, "priority_support": True}
        }
    ]
    
    packages = {}
    for data in packages_data:
        package = db.query(Package).filter(Package.name == data["name"]).first()
        if not package:
            package = Package(**data)
            db.add(package)
            db.flush()
        packages[data["name"]] = package
    
    db.commit()
    print(f"   ✅ {len(packages)} paquetes creados")
    return packages

def populate_users(db: Session, roles: dict, institutions: dict):
    """Poblar usuarios"""
    print("👤 Poblando usuarios...")
    
    users_data = [
        # Admin (Sysadmin)
        {
            "email": "admin@cuiot.com",
            "password": "admin123",
            "first_name": "Sistema",
            "last_name": "Administrador",
            "phone": "+54 11 9999-0000",
            "role": "admin",
            "institution": None
        },
        # Admins de instituciones
        {
            "email": "admin.hospital@cuiot.com",
            "password": "admin123",
            "first_name": "María",
            "last_name": "González",
            "phone": "+54 11 1111-1111",
            "role": "institution_admin",
            "institution": "Hospital General San Martín"
        },
        {
            "email": "admin.clinica@cuiot.com",
            "password": "admin123",
            "first_name": "Carlos",
            "last_name": "Rodríguez",
            "phone": "+54 11 2222-2222",
            "role": "institution_admin",
            "institution": "Clínica Santa María"
        },
        # Cuidadores profesionales
        {
            "email": "cuidador1@cuiot.com",
            "password": "cuidador123",
            "first_name": "Ana",
            "last_name": "López",
            "phone": "+54 11 3333-3333",
            "role": "caregiver",
            "institution": "Centro de Cuidados El Amanecer"
        },
        {
            "email": "cuidador2@cuiot.com",
            "password": "cuidador123",
            "first_name": "Juan",
            "last_name": "Pérez",
            "phone": "+54 11 4444-4444",
            "role": "caregiver",
            "institution": "Residencia Los Abuelos"
        },
        # Cuidadores freelance
        {
            "email": "freelance1@cuiot.com",
            "password": "freelance123",
            "first_name": "Lucía",
            "last_name": "Martínez",
            "phone": "+54 11 5555-5555",
            "role": "freelance_caregiver",
            "institution": None,
            "is_freelance": True,
            "hourly_rate": 1500  # $15 ARS por hora
        },
        {
            "email": "freelance2@cuiot.com",
            "password": "freelance123",
            "first_name": "Roberto",
            "last_name": "Fernández",
            "phone": "+54 11 6666-6666",
            "role": "freelance_caregiver",
            "institution": None,
            "is_freelance": True,
            "hourly_rate": 1800  # $18 ARS por hora
        },
        # Familiares
        {
            "email": "familiar1@cuiot.com",
            "password": "familiar123",
            "first_name": "Laura",
            "last_name": "Martínez",
            "phone": "+54 11 7777-7777",
            "role": "family_member",
            "institution": None
        },
        {
            "email": "familiar2@cuiot.com",
            "password": "familiar123",
            "first_name": "Pedro",
            "last_name": "García",
            "phone": "+54 11 8888-8888",
            "role": "family_member",
            "institution": None
        },
        # Personas cuidadas
        {
            "email": "paciente1@cuiot.com",
            "password": "paciente123",
            "first_name": "Doña Carmen",
            "last_name": "García",
            "phone": "+54 11 9999-1111",
            "role": "caredperson",
            "institution": None
        },
        {
            "email": "paciente2@cuiot.com",
            "password": "paciente123",
            "first_name": "Don Manuel",
            "last_name": "López",
            "phone": "+54 11 9999-2222",
            "role": "caredperson",
            "institution": None
        },
        # Personal médico
        {
            "email": "medico1@cuiot.com",
            "password": "medico123",
            "first_name": "Dr. Patricia",
            "last_name": "Silva",
            "phone": "+54 11 7777-7777",
            "role": "medical_staff",
            "institution": "Centro Médico Integral"
        },
        {
            "email": "medico2@cuiot.com",
            "password": "medico123",
            "first_name": "Dr. Alejandro",
            "last_name": "Ruiz",
            "phone": "+54 11 7777-8888",
            "role": "medical_staff",
            "institution": "Hospital General San Martín"
        },
        # Personal de institución
        {
            "email": "staff1@cuiot.com",
            "password": "staff123",
            "first_name": "Sofía",
            "last_name": "Hernández",
            "phone": "+54 11 6666-9999",
            "role": "institution_staff",
            "institution": "Centro de Cuidados El Amanecer"
        }
    ]
    
    users = {}
    for user_data in users_data:
        # Verificar si el usuario ya existe
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if user:
            users[user_data["email"]] = user
            continue
        
        # Obtener institución si se especifica
        institution_id = None
        if user_data.get("institution"):
            institution = institutions.get(user_data["institution"])
            if institution:
                institution_id = institution.id
        
        # Crear usuario
        user = User(
            email=user_data["email"],
            password_hash=AuthService.get_password_hash(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data["phone"],
            is_active=True,
            institution_id=institution_id,
            is_freelance=user_data.get("is_freelance", False),
            hourly_rate=user_data.get("hourly_rate"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(user)
        db.flush()
        
        # Asignar rol
        role = roles.get(user_data["role"])
        if role:
            user_role = UserRole(
                user_id=user.id,
                role_id=role.id,
                created_at=datetime.utcnow()
            )
            db.add(user_role)
        
        users[user_data["email"]] = user
    
    db.commit()
    print(f"   ✅ {len(users)} usuarios creados")
    return users

def assign_packages_to_users(db: Session, users: dict, roles: dict, packages: dict):
    """Asigna paquetes a usuarios con roles permitidos"""
    print("📦 Asignando paquetes a usuarios permitidos...")
    allowed_roles = {"institution_admin", "caredperson", "family", "family_member"}
    paquetes = list(packages.values())
    count = 0
    for user in users.values():
        # Obtener roles activos del usuario
        user_roles = db.query(UserRole).filter_by(user_id=user.id, is_active=True).all()
        user_role_names = set()
        for ur in user_roles:
            role = db.query(Role).filter_by(id=ur.role_id).first()
            if role:
                user_role_names.add(role.name)
        if user_role_names & allowed_roles:
            # Asignar un paquete aleatorio
            paquete = choice(paquetes)
            existing = db.query(UserPackage).filter_by(user_id=user.id, package_id=paquete.id, is_active=True).first()
            if not existing:
                up = UserPackage(
                    user_id=user.id,
                    package_id=paquete.id,
                    is_active=True,
                    start_date=datetime.utcnow(),
                    end_date=None,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(up)
                count += 1
    db.commit()
    print(f"   ✅ {count} paquetes asignados a usuarios permitidos")

def populate_cared_persons(db: Session, users: dict):
    """Poblar personas cuidadas"""
    print("👴 Poblando personas cuidadas...")
    
    cared_persons_data = [
        {
            "first_name": "Doña Carmen",
            "last_name": "García",
            "date_of_birth": date(1945, 3, 15),
            "user_email": "familiar1@cuiot.com",
            "phone": "+54 11 9999-1111",
            "email": "carmen.garcia@email.com",
            "emergency_contact": "Laura Martínez",
            "emergency_phone": "+54 11 7777-7777",
            "blood_type": "A+",
            "care_level": "medium",
            "mobility_level": "assisted",
            "address": "Av. Corrientes 1234, CABA",
            "medical_contact_name": "Dr. Patricia Silva",
            "medical_contact_phone": "+54 11 7777-7777",
            "family_contact_name": "Laura Martínez",
            "family_contact_phone": "+54 11 7777-7777"
        },
        {
            "first_name": "Don Manuel",
            "last_name": "López",
            "date_of_birth": date(1941, 7, 22),
            "user_email": "familiar2@cuiot.com",
            "phone": "+54 11 9999-2222",
            "email": "manuel.lopez@email.com",
            "emergency_contact": "Pedro García",
            "emergency_phone": "+54 11 8888-8888",
            "blood_type": "O+",
            "care_level": "high",
            "mobility_level": "wheelchair",
            "address": "Calle San Juan 567, CABA",
            "medical_contact_name": "Dr. Alejandro Ruiz",
            "medical_contact_phone": "+54 11 7777-8888",
            "family_contact_name": "Pedro García",
            "family_contact_phone": "+54 11 8888-8888"
        },
        {
            "first_name": "Sra. Rosa",
            "last_name": "Martínez",
            "date_of_birth": date(1948, 11, 8),
            "user_email": "cuidador1@cuiot.com",
            "phone": "+54 11 9999-3333",
            "email": "rosa.martinez@email.com",
            "emergency_contact": "Ana López",
            "emergency_phone": "+54 11 3333-3333",
            "blood_type": "B+",
            "care_level": "medium",
            "mobility_level": "independent",
            "address": "Ruta 5 Km 25, San Isidro",
            "medical_contact_name": "Dr. Patricia Silva",
            "medical_contact_phone": "+54 11 7777-7777",
            "family_contact_name": "Ana López",
            "family_contact_phone": "+54 11 3333-3333"
        },
        {
            "first_name": "Sr. Antonio",
            "last_name": "Rodríguez",
            "date_of_birth": date(1944, 5, 12),
            "user_email": "cuidador2@cuiot.com",
            "phone": "+54 11 9999-4444",
            "email": "antonio.rodriguez@email.com",
            "emergency_contact": "Juan Pérez",
            "emergency_phone": "+54 11 4444-4444",
            "blood_type": "AB+",
            "care_level": "critical",
            "mobility_level": "bedridden",
            "address": "Av. Libertador 890, Vicente López",
            "medical_contact_name": "Dr. Alejandro Ruiz",
            "medical_contact_phone": "+54 11 7777-8888",
            "family_contact_name": "Juan Pérez",
            "family_contact_phone": "+54 11 4444-4444"
        }
    ]
    
    cared_persons = {}
    for data in cared_persons_data:
        # Verificar si ya existe
        existing = db.query(CaredPerson).filter(
            CaredPerson.first_name == data["first_name"],
            CaredPerson.last_name == data["last_name"]
        ).first()
        
        if existing:
            cared_persons[f"{data['first_name']} {data['last_name']}"] = existing
            continue
        
        # Obtener usuario representante
        user = users.get(data["user_email"])
        if not user:
            continue
        
        cared_person = CaredPerson(
            first_name=data["first_name"],
            last_name=data["last_name"],
            date_of_birth=data["date_of_birth"],
            user_id=user.id,
            phone=data["phone"],
            email=data["email"],
            emergency_contact=data["emergency_contact"],
            emergency_phone=data["emergency_phone"],
            blood_type=data["blood_type"],
            care_level=data["care_level"],
            mobility_level=data["mobility_level"],
            address=data["address"],
            medical_contact_name=data["medical_contact_name"],
            medical_contact_phone=data["medical_contact_phone"],
            family_contact_name=data["family_contact_name"],
            family_contact_phone=data["family_contact_phone"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(cared_person)
        db.flush()
        cared_persons[f"{data['first_name']} {data['last_name']}"] = cared_person
    
    db.commit()
    print(f"   ✅ {len(cared_persons)} personas cuidadas creadas")
    return cared_persons

def main():
    """Función principal"""
    db: Session = next(get_db())
    
    try:
        print("🚀 INICIANDO POBLACIÓN COMPLETA DE BASE DE DATOS CUIOT")
        print("=" * 70)
        
        # 1. Poblar tablas de catálogo (base del sistema)
        print("\n1️⃣ POBLANDO TABLAS DE CATÁLOGO...")
        catalogs = populate_catalog_tables(db)
        
        # 2. Poblar roles
        print("\n2️⃣ POBLANDO ROLES...")
        roles = populate_roles(db)
        
        # 3. Poblar instituciones
        print("\n3️⃣ POBLANDO INSTITUCIONES...")
        institutions = populate_institutions(db)
        
        # 4. Poblar paquetes
        print("\n4️⃣ POBLANDO PAQUETES...")
        packages = populate_packages(db)
        
        # 5. Poblar usuarios
        print("\n5️⃣ POBLANDO USUARIOS...")
        users = populate_users(db, roles, institutions)
        
        # Asignar paquetes a usuarios permitidos
        # 6. Poblar personas cuidadas
        print("\n6️⃣ POBLANDO PERSONAS CUIDADAS...")
        cared_persons = populate_cared_persons(db, users)
        
        # RESUMEN FINAL
        print("\n" + "=" * 70)
        print("🎉 POBLACIÓN COMPLETA FINALIZADA EXITOSAMENTE")
        print("=" * 70)
        print("📊 RESUMEN:")
        print(f"   📋 Tablas de catálogo: {len(catalogs)} tipos")
        print(f"   👥 Roles: {len(roles)}")
        print(f"   🏥 Instituciones: {len(institutions)}")
        print(f"   📦 Paquetes: {len(packages)}")
        print(f"   👤 Usuarios: {len(users)}")
        print(f"   👴 Personas cuidadas: {len(cared_persons)}")
        
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("   Admin (Sysadmin): admin@cuiot.com / admin123")
        print("   Admin Institución: admin.hospital@cuiot.com / admin123")
        print("   Cuidador: cuidador1@cuiot.com / cuidador123")
        print("   Familiar: familiar1@cuiot.com / familiar123")
        print("   Persona Cuidada: paciente1@cuiot.com / paciente123")
        print("   Médico: medico1@cuiot.com / medico123")
        print("   Freelance: freelance1@cuiot.com / freelance123")
        
        print("\n✅ ¡Base de datos lista para desarrollo y pruebas!")
        
    except Exception as e:
        print(f"❌ Error durante la población: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 