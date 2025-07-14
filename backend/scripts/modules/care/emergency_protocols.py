#!/usr/bin/env python3
"""
Módulo de población de protocolos de emergencia (EmergencyProtocol)
Genera protocolos globales y por institución, con datos realistas e idempotencia.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.models.emergency_protocol import EmergencyProtocol
from app.models.institution import Institution
from app.models.status_type import StatusType
from datetime import datetime
import random
import json

def generate_protocol_steps():
    steps = [
        "Evaluar la situación y mantener la calma",
        "Contactar a los servicios de emergencia si es necesario",
        "Notificar a los familiares o responsables",
        "Registrar el incidente en el sistema",
        "Realizar seguimiento y cierre del protocolo"
    ]
    random.shuffle(steps)
    return steps

def generate_contacts():
    contacts = [
        {"name": "Emergencias Médicas", "phone": "+54 911 1234-5678", "type": "medical"},
        {"name": "Bomberos", "phone": "+54 911 8765-4321", "type": "fire"},
        {"name": "Policía", "phone": "+54 911 1122-3344", "type": "police"},
        {"name": "Contacto Familiar", "phone": "+54 911 9988-7766", "type": "family"}
    ]
    return random.sample(contacts, k=random.randint(2, 4))

def populate_emergency_protocols(db, existing_data=None):
    print("   🚨 Poblando protocolos de emergencia...")
    # Obtener tipos y crisis disponibles
    protocol_types = EmergencyProtocol.get_protocol_types()
    crisis_types = EmergencyProtocol.get_crisis_types()
    status_types = {s.name: s for s in db.query(StatusType).all()}
    institutions = db.query(Institution).all()

    # Protocolos globales (sin institución)
    for t in protocol_types:
        for c in crisis_types:
            name = f"Protocolo Global: {t} - {c}"
            existing = db.query(EmergencyProtocol).filter_by(name=name, institution_id=None).first()
            if not existing:
                status_type = status_types.get("active")
                protocol = EmergencyProtocol(
                    name=name,
                    protocol_type=t,
                    crisis_type=c,
                    description=f"Protocolo global para {c} ({t})",
                    steps=json.dumps(generate_protocol_steps()),
                    contacts=json.dumps(generate_contacts()),
                    trigger_conditions=f"Condiciones para {c}",
                    severity_threshold=random.choice(["low", "medium", "high"]),
                    is_active=True,
                    is_default=True,
                    institution_id=None,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(protocol)
    db.commit()

    # Protocolos por institución
    for inst in institutions:
        for t in protocol_types:
            for c in crisis_types:
                name = f"Protocolo {inst.name}: {t} - {c}"
                existing = db.query(EmergencyProtocol).filter_by(name=name, institution_id=inst.id).first()
                if not existing:
                    status_type = status_types.get("active")
                    protocol = EmergencyProtocol(
                        name=name,
                        protocol_type=t,
                        crisis_type=c,
                        description=f"Protocolo institucional para {c} ({t}) en {inst.name}",
                        steps=json.dumps(generate_protocol_steps()),
                        contacts=json.dumps(generate_contacts()),
                        trigger_conditions=f"Condiciones para {c} en {inst.name}",
                        severity_threshold=random.choice(["low", "medium", "high"]),
                        is_active=True,
                        is_default=False,
                        institution_id=inst.id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(protocol)
    db.commit()
    print(f"   🚨 Protocolos de emergencia poblados (globales y por institución)")

def populate_emergency_protocols_complete(db, existing_data=None):
    populate_emergency_protocols(db, existing_data)

if __name__ == "__main__":
    from app.core.database import get_db
    db = next(get_db())
    try:
        populate_emergency_protocols_complete(db)
    finally:
        db.close() 