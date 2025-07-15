#!/usr/bin/env python3
"""
Poblar status_types para la categoría 'subscription'.
"""
from app.core.database import get_db
from app.models.status_type import StatusType
from datetime import datetime

def populate_subscription_status_types():
    db = next(get_db())
    status_names = [
        ("active", "Suscripción activa"),
        ("suspended", "Suscripción suspendida"),
        ("cancelled", "Suscripción cancelada"),
        ("expired", "Suscripción expirada"),
        ("pending", "Suscripción pendiente"),
        ("trial", "Suscripción en prueba")
    ]
    created = 0
    for name, desc in status_names:
        existing = db.query(StatusType).filter_by(name=name, category="subscription").first()
        if existing:
            continue
        st = StatusType(
            name=name,
            description=desc,
            category="subscription",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(st)
        created += 1
    db.commit()
    db.close()
    print(f"✅ StatusTypes de suscripción creados: {created}")

if __name__ == "__main__":
    populate_subscription_status_types() 