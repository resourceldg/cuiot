import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import random
import string
from datetime import datetime, timedelta, date
from app.core.database import get_db
from app.models.referral import Referral, ReferralCommission
from app.models.medical_referral import MedicalReferral
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.institution import Institution
from app.models.status_type import StatusType
from app.models.referral_type import ReferralType
from sqlalchemy import func
import uuid

# Utilidades

def random_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_random_status_type(db, allowed=None):
    q = db.query(StatusType)
    if allowed:
        q = q.filter(StatusType.name.in_(allowed))
    return q.order_by(func.random()).first()

def get_random_referral_type(db):
    return db.query(ReferralType).order_by(func.random()).first()

def populate_referrals():
    db = next(get_db())
    created = 0
    # Obtener usuarios, personas cuidadas, instituciones
    users = db.query(User).filter(User.is_active == True).all()
    cared_persons = db.query(CaredPerson).all()
    institutions = db.query(Institution).filter(Institution.is_verified == True).all()
    referral_types = db.query(ReferralType).all()
    status_types = db.query(StatusType).all()
    if not users or not cared_persons or not referral_types:
        print("⚠️  Faltan usuarios, personas cuidadas o tipos de referencia.")
        db.close()
        return
    print("🔗 Generando referencias (Referral)...")
    # Obtener usuarios institucionales (admins de instituciones)
    institution_admins = {}
    for inst in institutions:
        # Buscar un usuario con institution_id == inst.id y rol institucional
        admin = next((u for u in users if u.institution_id == inst.id), None)
        if admin:
            institution_admins[inst.id] = admin

    for i in range(30):
        referrer_type = random.choice(["caregiver", "family", "institution", "cared_person"])
        if referrer_type == "caregiver":
            caregivers = [u for u in users if any(r.name == "caregiver" for r in getattr(u, "roles", []))]
            if not caregivers:
                continue
            referrer = random.choice(caregivers)
            referrer_id = referrer.id
        elif referrer_type == "family":
            families = [u for u in users if any(r.name == "family" for r in getattr(u, "roles", []))]
            if not families:
                continue
            referrer = random.choice(families)
            referrer_id = referrer.id
        elif referrer_type == "institution":
            # Usar UUID de un admin institucional
            possible_insts = [inst for inst in institutions if inst.id in institution_admins]
            if not possible_insts:
                continue  # No hay admin institucional, omitir
            inst = random.choice(possible_insts)
            referrer_id = institution_admins[inst.id].id
        else:  # cared_person
            if not cared_persons:
                continue
            referrer = random.choice(cared_persons)
            referrer_id = referrer.user_id if referrer.user_id else None
            if not referrer_id:
                continue  # Omitir si la persona cuidada no tiene usuario
        referred_email = f"referido{i}@mail.com"
        referred_name = f"Referido {i}"
        referred_phone = f"+54 9 11 {random.randint(1000,9999)}-{random.randint(1000,9999)}"
        referral_type = random.choice(referral_types)
        status_type = random.choice(status_types)
        referral_code = random_code(10)
        # Idempotencia: no duplicar por código
        if db.query(Referral).filter_by(referral_code=referral_code).first():
            continue
        referral = Referral(
            id=uuid.uuid4(),
            referral_code=random_code(10),
            referrer_type=referrer_type,
            referrer_id=referrer_id,
            referred_email=f"referido{i}@mail.com",
            referred_name=f"Referido {i}",
            referred_phone=f"+54 9 11 {random.randint(1000,9999)}-{random.randint(1000,9999)}",
            referral_type_id=random.choice(referral_types).id if referral_types else 1,
            status_type_id=random.choice(status_types).id if status_types else None,
            registered_at=datetime.now() - timedelta(days=random.randint(0, 30)),
            converted_at=None,
            expired_at=None,
            commission_amount=random.choice([None, 1000.0, 1500.0]),
            commission_paid=random.choice([True, False]),
            commission_paid_at=datetime.now() - timedelta(days=random.randint(0, 30)),
            notes=random.choice([
                "Referido por recomendación personal.",
                "Referido por institución asociada."
            ]),
            source=random.choice(["email", "phone", "whatsapp", "in_person"]),
            is_active=True
        )
        db.add(referral)
        created += 1
    db.commit()
    print(f"✅ Referrals creados: {created} (idempotente)")
    db.close()

def populate_medical_referrals():
    db = next(get_db())
    created = 0
    cared_persons = db.query(CaredPerson).all()
    status_types = db.query(StatusType).all()
    if not cared_persons or not status_types:
        print("⚠️  Faltan personas cuidadas o tipos de estado.")
        db.close()
        return
    print("🏥 Generando derivaciones médicas (MedicalReferral)...")
    referral_types = ["medical", "specialist", "therapy", "diagnostic"]
    priorities = ["low", "medium", "high", "urgent"]
    for i in range(30):
        cared_person = random.choice(cared_persons)
        referral_type = random.choice(referral_types)
        referred_by = random.choice([
            "Dr. Juan Pérez", "Dra. Ana Torres", "Lic. Marta Gómez", "Dr. Carlos Ruiz"
        ])
        referred_to = random.choice([
            "Hospital Central", "Clínica del Sur", "Especialista en Cardiología", "Centro de Diagnóstico"
        ])
        reason = random.choice([
            "Evaluación de condición crónica.",
            "Consulta por síntomas agudos.",
            "Seguimiento post-operatorio.",
            "Estudio diagnóstico complementario."
        ])
        status_type = random.choice(status_types)
        referral_date = date.today() - timedelta(days=random.randint(0, 60))
        appointment_date = datetime.now() + timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None
        completed_date = (appointment_date + timedelta(days=1)) if appointment_date and random.choice([True, False]) else None
        priority = random.choice(priorities)
        notes = random.choice([
            "Paciente con cobertura total.",
            "Requiere autorización previa.",
            "Derivación urgente por cuadro agudo.",
            "Seguimiento programado."
        ])
        insurance_info = random.choice([
            "OSDE 410", "Swiss Medical", "Galeno", "Particular", None
        ])
        # Idempotencia: no duplicar por combinación persona+tipo+fecha
        if db.query(MedicalReferral).filter_by(cared_person_id=cared_person.id, referral_type=referral_type, referral_date=referral_date).first():
            continue
        medical_referral = MedicalReferral(
            cared_person_id=cared_person.id,
            referral_type=referral_type,
            referred_by=referred_by,
            referred_to=referred_to,
            reason=reason,
            status_type_id=status_type.id,
            referral_date=referral_date,
            appointment_date=appointment_date,
            completed_date=completed_date,
            priority=priority,
            notes=notes,
            insurance_info=insurance_info
        )
        db.add(medical_referral)
        created += 1
    db.commit()
    print(f"✅ MedicalReferrals creados: {created} (idempotente)")
    db.close()

def populate_referrals_complete():
    print("🔄 Iniciando población de referencias y derivaciones médicas...")
    populate_referrals()
    populate_medical_referrals()
    print("✅ Población de referencias y derivaciones completada!")

if __name__ == "__main__":
    populate_referrals_complete() 