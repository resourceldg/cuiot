#!/usr/bin/env python3
"""
Script para corregir asignaciones incorrectas de paquetes según la lógica de roles.

Lógica de negocio:
- Roles que pueden tener paquetes individuales: cared_person_self, caredperson, family_member
- Roles que pueden tener paquetes institucionales: institution_admin
- Roles que NO requieren paquetes: caregiver, institution_staff, medical_staff, freelance_caregiver, admin, sin_rol
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.user import User
from app.models.role import Role
from app.models.package import Package
from app.models.package import UserPackage
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
from datetime import date, datetime

def get_roles_with_packages():
    """Roles que pueden tener paquetes según la lógica de negocio"""
    return {
        "individual": ["cared_person_self", "caredperson", "family_member"],
        "institutional": ["institution_admin"]
    }

def get_roles_without_packages():
    """Roles que NO requieren paquetes"""
    return [
        "caregiver", "institution_staff", "medical_staff", 
        "freelance_caregiver", "admin", "sin_rol"
    ]

def get_user_roles(db: Session, user_id: str) -> list:
    """Obtener roles de un usuario"""
    result = db.execute(text("""
        SELECT r.name 
        FROM user_roles ur 
        JOIN roles r ON ur.role_id = r.id 
        WHERE ur.user_id = :user_id AND ur.is_active = true
    """), {"user_id": user_id}).fetchall()
    return [row[0] for row in result]

def should_have_package(user_roles: list) -> tuple:
    """
    Determinar si un usuario debería tener paquete y de qué tipo
    Returns: (should_have, package_type)
    """
    roles_with_packages = get_roles_with_packages()
    
    for role in user_roles:
        if role in roles_with_packages["individual"]:
            return True, "individual"
        elif role in roles_with_packages["institutional"]:
            return True, "institutional"
    
    return False, None

def get_default_package(db: Session, package_type: str) -> str | None:
    """Obtener el ID del paquete por defecto para un tipo"""
    package = db.query(Package).filter(
        Package.package_type == package_type,
        Package.is_active == True
    ).first()
    return str(package.id) if package else None

def fix_package_assignments():
    """Corregir asignaciones de paquetes según la lógica de roles"""
    db = next(get_db())
    
    try:
        print("🔧 Iniciando corrección de asignaciones de paquetes...")
        
        # 1. Obtener todos los usuarios con sus paquetes actuales
        users_with_packages = db.execute(text("""
            SELECT DISTINCT u.id, u.email, up.package_id, p.package_type, p.name
            FROM users u
            LEFT JOIN user_packages up ON u.id = up.user_id
            LEFT JOIN packages p ON up.package_id = p.id
            WHERE u.is_active = true
        """)).fetchall()
        
        print(f"📊 Total de usuarios activos: {len(users_with_packages)}")
        
        corrections_made = 0
        packages_removed = 0
        packages_added = 0
        
        for user_data in users_with_packages:
            user_id = user_data[0]
            user_email = user_data[1]
            current_package_id = user_data[2]
            current_package_type = user_data[3]
            current_package_name = user_data[4]
            
            # Obtener roles del usuario
            user_roles = get_user_roles(db, user_id)
            
            # Determinar si debería tener paquete
            should_have, expected_package_type = should_have_package(user_roles)
            
            print(f"\n👤 Usuario: {user_email}")
            print(f"   Roles: {user_roles}")
            print(f"   Paquete actual: {current_package_name or 'Ninguno'}")
            print(f"   Debería tener paquete: {should_have} ({expected_package_type or 'N/A'})")
            
            # Caso 1: Usuario NO debería tener paquete pero lo tiene
            if not should_have and current_package_id:
                print(f"   ❌ REMOVIENDO paquete incorrecto")
                # Primero eliminar add-ons asociados
                db.execute(text("DELETE FROM user_package_add_ons WHERE user_package_id IN (SELECT id FROM user_packages WHERE user_id = :user_id)"), 
                          {"user_id": user_id})
                # Luego eliminar el paquete
                db.execute(text("DELETE FROM user_packages WHERE user_id = :user_id"), 
                          {"user_id": user_id})
                packages_removed += 1
                corrections_made += 1
            
            # Caso 2: Usuario SÍ debería tener paquete pero no lo tiene
            elif should_have and not current_package_id:
                default_package_id = get_default_package(db, expected_package_type)
                if default_package_id:
                    print(f"   ✅ AGREGANDO paquete {expected_package_type} por defecto")
                    
                    # Crear nueva asignación de paquete
                    new_user_package = UserPackage(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        package_id=default_package_id,
                        start_date=date.today(),
                        auto_renew=True,
                        billing_cycle="monthly",
                        current_amount=0,
                        next_billing_date=date.today(),
                        legal_capacity_verified=False,
                        referral_commission_applied=False,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.add(new_user_package)
                    packages_added += 1
                    corrections_made += 1
                else:
                    print(f"   ⚠️  No se encontró paquete por defecto para tipo {expected_package_type}")
            
            # Caso 3: Usuario tiene paquete pero de tipo incorrecto
            elif should_have and current_package_id and current_package_type != expected_package_type:
                print(f"   🔄 CAMBIANDO paquete de {current_package_type} a {expected_package_type}")
                
                # Primero eliminar add-ons asociados
                db.execute(text("DELETE FROM user_package_add_ons WHERE user_package_id IN (SELECT id FROM user_packages WHERE user_id = :user_id)"), 
                          {"user_id": user_id})
                # Luego eliminar el paquete actual
                db.execute(text("DELETE FROM user_packages WHERE user_id = :user_id"), 
                          {"user_id": user_id})
                
                # Agregar paquete correcto
                default_package_id = get_default_package(db, expected_package_type)
                if default_package_id:
                    new_user_package = UserPackage(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        package_id=default_package_id,
                        start_date=date.today(),
                        auto_renew=True,
                        billing_cycle="monthly",
                        current_amount=0,
                        next_billing_date=date.today(),
                        legal_capacity_verified=False,
                        referral_commission_applied=False,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    db.add(new_user_package)
                    packages_added += 1
                    corrections_made += 1
                else:
                    print(f"   ⚠️  No se encontró paquete por defecto para tipo {expected_package_type}")
            
            else:
                print(f"   ✅ Correcto")
        
        # Commit de cambios
        if corrections_made > 0:
            db.commit()
            print(f"\n🎉 Correcciones completadas:")
            print(f"   - Paquetes removidos: {packages_removed}")
            print(f"   - Paquetes agregados: {packages_added}")
            print(f"   - Total de correcciones: {corrections_made}")
        else:
            print(f"\n✅ No se requirieron correcciones")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la corrección: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_package_assignments() 