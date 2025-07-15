#!/usr/bin/env python3
"""
Poblar institution_packages: asigna todos los paquetes institucionales a todas las instituciones activas.
"""
from datetime import date
from app.core.database import get_db
from app.models.institution import Institution
from app.models.package import Package
from app.models.institution_package import InstitutionPackage
from app.models.status_type import StatusType

def populate_institution_packages():
    db = next(get_db())
    institutions = db.query(Institution).filter(Institution.is_active == True).all()
    packages = db.query(Package).filter(Package.package_type == "institutional", Package.is_active == True).all()
    status_types = db.query(StatusType).filter(StatusType.category == "subscription").all()
    active_status_id = next((st.id for st in status_types if st.name == "active"), status_types[0].id)

    created = 0
    for institution in institutions:
        for package in packages:
            # Verificar si ya existe la suscripción
            existing = db.query(InstitutionPackage).filter_by(
                institution_id=institution.id,
                package_id=package.id
            ).first()
            if existing:
                continue
            inst_pkg = InstitutionPackage(
                institution_id=institution.id,
                package_id=package.id,
                start_date=date.today(),
                end_date=None,
                status_type_id=active_status_id
            )
            db.add(inst_pkg)
            created += 1
    db.commit()
    db.close()
    print(f"✅ InstitutionPackages creados: {created}")

if __name__ == "__main__":
    populate_institution_packages() 