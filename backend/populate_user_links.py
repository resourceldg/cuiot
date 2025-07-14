#!/usr/bin/env python3
"""
Asigna instituciones y paquetes a usuarios de prueba para tests de filtrado.
"""
import os
import sys
from datetime import date, timedelta
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.models.user import User
from app.models.institution import Institution
from app.models.package import Package, UserPackage
from app.models.user_role import UserRole
from app.models.role import Role
from app.core.database import engine

Session = sessionmaker(bind=engine)
session = Session()

try:
    users = session.query(User).order_by(User.created_at).all()
    institutions = session.query(Institution).all()
    packages = session.query(Package).all()
    roles = session.query(Role).all()

    if not users or not institutions or not packages:
        print("❌ Faltan usuarios, instituciones o paquetes para asignar.")
        sys.exit(1)

    print(f"Usuarios: {len(users)}, Instituciones: {len(institutions)}, Paquetes: {len(packages)}")

    # Asignar instituciones alternando
    for i, user in enumerate(users):
        if i % 2 == 0:
            user.institution_id = institutions[i % len(institutions)].id
        else:
            user.institution_id = None

    # Asignar paquetes alternando (y combinando con institución)
    for i, user in enumerate(users):
        if i % 3 == 0:
            # Asignar paquete 1
            pkg = packages[0]
        elif i % 3 == 1:
            # Asignar paquete 2
            pkg = packages[1]
        else:
            # Sin paquete
            continue
        # Crear UserPackage
        up = UserPackage(
            id=uuid.uuid4(),
            user_id=user.id,
            package_id=pkg.id,
            start_date=date.today() - timedelta(days=10),
            end_date=None,
            auto_renew=True,
            billing_cycle="monthly",
            current_amount=pkg.price_monthly,
            next_billing_date=date.today() + timedelta(days=20),
            status_type_id=None  # Asume activo por defecto
        )
        session.add(up)

    session.commit()
    print("✅ Instituciones y paquetes asignados a usuarios de prueba.")
except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()
finally:
    session.close() 