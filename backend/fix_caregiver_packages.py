#!/usr/bin/env python3
"""
Script específico para corregir usuarios con rol caregiver que tienen paquetes incorrectamente.

Problema: Usuarios con rol 'caregiver' que tienen paquetes cuando no deberían.
Solución: Remover paquetes de usuarios que SOLO tienen rol 'caregiver' (sin otros roles que permitan paquetes).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from sqlalchemy import text
import uuid
from datetime import date, datetime

def get_roles_with_packages():
    """Roles que pueden tener paquetes según la lógica de negocio"""
    return {
        "individual": ["cared_person_self", "caredperson", "family_member"],
        "institutional": ["institution_admin"]
    }

def should_have_package(user_roles: list) -> bool:
    """
    Determinar si un usuario debería tener paquete basado en sus roles
    """
    roles_with_packages = get_roles_with_packages()
    
    for role in user_roles:
        if role in roles_with_packages["individual"] or role in roles_with_packages["institutional"]:
            return True
    
    return False

def fix_caregiver_packages():
    """Corregir paquetes de usuarios con rol caregiver"""
    db = next(get_db())
    
    try:
        print("🔧 Iniciando corrección específica de usuarios caregiver...")
        
        # 1. Obtener usuarios que SOLO tienen rol caregiver
        users_only_caregiver = db.execute(text("""
            SELECT u.id, u.email, array_agg(r.name) as roles
            FROM users u 
            JOIN user_roles ur ON u.id = ur.user_id 
            JOIN roles r ON ur.role_id = r.id 
            WHERE u.is_active = true
            GROUP BY u.id, u.email
            HAVING array_agg(r.name) = ARRAY['caregiver'::varchar]
        """)).fetchall()
        
        print(f"📊 Usuarios que SOLO tienen rol caregiver: {len(users_only_caregiver)}")
        
        corrections_made = 0
        
        for user_data in users_only_caregiver:
            user_id = user_data[0]
            user_email = user_data[1]
            user_roles = user_data[2]
            
            # Verificar si tiene paquetes
            packages = db.execute(text("""
                SELECT up.id, p.name, p.package_type
                FROM user_packages up
                JOIN packages p ON up.package_id = p.id
                WHERE up.user_id = :user_id
            """), {"user_id": user_id}).fetchall()
            
            if packages:
                print(f"\n👤 Usuario: {user_email}")
                print(f"   Roles: {user_roles}")
                print(f"   Paquetes actuales: {[f'{p[1]} ({p[2]})' for p in packages]}")
                print(f"   Debería tener paquete: {should_have_package(user_roles)}")
                
                if not should_have_package(user_roles):
                    print(f"   ❌ REMOVIENDO paquetes incorrectos")
                    
                    # Primero eliminar add-ons asociados
                    db.execute(text("""
                        DELETE FROM user_package_add_ons 
                        WHERE user_package_id IN (
                            SELECT id FROM user_packages WHERE user_id = :user_id
                        )
                    """), {"user_id": user_id})
                    
                    # Luego eliminar los paquetes
                    db.execute(text("DELETE FROM user_packages WHERE user_id = :user_id"), 
                              {"user_id": user_id})
                    
                    corrections_made += 1
                else:
                    print(f"   ✅ Correcto (tiene roles que permiten paquetes)")
            else:
                print(f"\n👤 Usuario: {user_email}")
                print(f"   Roles: {user_roles}")
                print(f"   Paquetes: Ninguno")
                print(f"   ✅ Correcto")
        
        # 2. Verificar usuarios con múltiples roles incluyendo caregiver
        users_multiple_roles = db.execute(text("""
            SELECT u.id, u.email, array_agg(r.name) as roles
            FROM users u 
            JOIN user_roles ur ON u.id = ur.user_id 
            JOIN roles r ON ur.role_id = r.id 
            WHERE u.is_active = true
            GROUP BY u.id, u.email
            HAVING 'caregiver' = ANY(array_agg(r.name)) AND array_length(array_agg(r.name), 1) > 1
        """)).fetchall()
        
        print(f"\n📊 Usuarios con múltiples roles incluyendo caregiver: {len(users_multiple_roles)}")
        
        for user_data in users_multiple_roles:
            user_id = user_data[0]
            user_email = user_data[1]
            user_roles = user_data[2]
            
            packages = db.execute(text("""
                SELECT up.id, p.name, p.package_type
                FROM user_packages up
                JOIN packages p ON up.package_id = p.id
                WHERE up.user_id = :user_id
            """), {"user_id": user_id}).fetchall()
            
            print(f"\n👤 Usuario: {user_email}")
            print(f"   Roles: {user_roles}")
            print(f"   Paquetes: {[f'{p[1]} ({p[2]})' for p in packages] if packages else 'Ninguno'}")
            print(f"   Debería tener paquete: {should_have_package(user_roles)}")
            
            if should_have_package(user_roles):
                print(f"   ✅ Correcto (tiene roles que permiten paquetes)")
            else:
                print(f"   ⚠️  Revisar (tiene múltiples roles pero ninguno permite paquetes)")
        
        # Commit de cambios
        if corrections_made > 0:
            db.commit()
            print(f"\n🎉 Correcciones completadas:")
            print(f"   - Paquetes removidos de usuarios solo caregiver: {corrections_made}")
        else:
            print(f"\n✅ No se requirieron correcciones")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la corrección: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_caregiver_packages() 