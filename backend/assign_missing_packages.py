#!/usr/bin/env python3
"""
Script específico para asignar paquetes a usuarios con rol family_member que no los tienen.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.user import User
from app.models.role import Role
from app.models.package import Package, UserPackage
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
from datetime import date, datetime

def get_default_individual_package(db: Session) -> str | None:
    """Obtener el ID del paquete individual por defecto"""
    package = db.query(Package).filter(
        Package.package_type == "individual",
        Package.is_active == True
    ).first()
    return str(package.id) if package else None

def get_active_status_type_id(db: Session) -> int | None:
    """Obtener el ID del status_type 'active'"""
    from app.models.status_type import StatusType
    status = db.query(StatusType).filter(StatusType.name == "active").first()
    return status.id if status else None

def assign_packages_to_family_members():
    """Asignar paquetes a usuarios con rol family_member que no los tienen"""
    
    db = next(get_db())
    
    try:
        # Obtener usuarios con rol family_member que no tienen paquetes
        users_without_packages = db.execute(text("""
            SELECT u.id, u.email, array_agg(r.name) as roles
            FROM users u 
            JOIN user_roles ur ON u.id = ur.user_id 
            JOIN roles r ON ur.role_id = r.id 
            WHERE u.is_active = true
            GROUP BY u.id, u.email
            HAVING 'family_member' = ANY(array_agg(r.name))
            AND NOT EXISTS (
                SELECT 1 FROM user_packages up WHERE up.user_id = u.id
            )
        """)).fetchall()
        
        print(f"📋 Usuarios con rol family_member sin paquetes: {len(users_without_packages)}")
        
        if not users_without_packages:
            print("✅ No hay usuarios que requieran asignación de paquetes")
            return
        
        # Obtener paquete individual por defecto
        default_package_id = get_default_individual_package(db)
        if not default_package_id:
            print("❌ No se encontró paquete individual por defecto")
            return
        
        # Obtener status_type_id para "active"
        active_status_id = get_active_status_type_id(db)
        if not active_status_id:
            print("❌ No se encontró status_type 'active'")
            return
        
        print(f"📦 Paquete por defecto: {default_package_id}")
        print(f"📊 Status active ID: {active_status_id}")
        
        packages_assigned = 0
        
        for user_id, email, roles in users_without_packages:
            print(f"\n👤 Asignando paquete a: {email}")
            print(f"   Roles: {roles}")
            
            # Calcular next_billing_date (un mes desde hoy)
            from datetime import timedelta
            next_billing = date.today() + timedelta(days=30)
            
            # Obtener precio del paquete
            package = db.query(Package).filter(Package.id == default_package_id).first()
            current_amount = package.price_monthly if package else 0
            
            # Crear nueva asignación de paquete
            new_user_package = UserPackage(
                id=str(uuid.uuid4()),
                user_id=str(user_id),
                package_id=default_package_id,
                start_date=date.today(),
                end_date=None,
                auto_renew=True,
                billing_cycle="monthly",
                current_amount=current_amount,
                next_billing_date=next_billing,
                status_type_id=active_status_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.add(new_user_package)
            packages_assigned += 1
            print(f"   ✅ Paquete asignado")
        
        # Confirmar cambios
        db.commit()
        print(f"\n🎉 Proceso completado:")
        print(f"   📦 Paquetes asignados: {packages_assigned}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando asignación de paquetes a usuarios family_member...")
    assign_packages_to_family_members()
    print("✅ Proceso completado") 