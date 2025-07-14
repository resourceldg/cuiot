import random
from datetime import datetime
from app.core.database import get_db
from app.models.institution import Institution

INSTITUTION_TYPES = [
    "hospital", "clinic", "nursing_home", "assisted_living", "home_care",
    "rehabilitation_center", "hospice", "day_care", "other"
]

SAMPLE_INSTITUTIONS = [
    {
        "name": "Residencia San José",
        "description": "Centro de cuidado integral para adultos mayores.",
        "institution_type": "nursing_home",
        "address": "Av. Siempre Viva 123, Ciudad Central",
        "phone": "+54 11 5555-1234",
        "email": "contacto@san-jose.com",
        "website": "https://san-jose.com",
        "latitude": -34.6037,
        "longitude": -58.3816,
        "tax_id": "20304050607",
        "license_number": "LIC-2024-001",
        "capacity": 80,
        "is_verified": True
    },
    {
        "name": "Clínica Los Robles",
        "description": "Clínica especializada en rehabilitación y cuidados paliativos.",
        "institution_type": "clinic",
        "address": "Calle Robles 456, Barrio Norte",
        "phone": "+54 11 5555-5678",
        "email": "info@losrobles.com",
        "website": "https://losrobles.com",
        "latitude": -34.6000,
        "longitude": -58.3700,
        "tax_id": "20987654321",
        "license_number": "LIC-2024-002",
        "capacity": 120,
        "is_verified": True
    },
    {
        "name": "Hogar Luz de Vida",
        "description": "Hogar de día para adultos mayores con actividades recreativas y asistencia médica.",
        "institution_type": "day_care",
        "address": "Av. Libertad 789, Villa Sur",
        "phone": "+54 11 5555-7890",
        "email": "hogar@luzdevida.com",
        "website": "https://luzdevida.com",
        "latitude": -34.6100,
        "longitude": -58.3900,
        "tax_id": "20123456789",
        "license_number": "LIC-2024-003",
        "capacity": 60,
        "is_verified": False
    }
]

def populate_institutions():
    db = next(get_db())
    created = 0
    for data in SAMPLE_INSTITUTIONS:
        inst = db.query(Institution).filter_by(name=data["name"]).first()
        if not inst:
            inst = Institution(**data)
            db.add(inst)
            created += 1
    db.commit()
    print(f"✅ Instituciones creadas: {created} (idempotente)")
    db.close()

if __name__ == "__main__":
    populate_institutions() 