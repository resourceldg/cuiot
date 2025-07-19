#!/usr/bin/env python3
"""
Script para asignar roles por defecto a usuarios sin roles
"""

import os
import sys
sys.path.append('/app')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.core.config import settings

# Crear conexión a la base de datos
engine = create_engine(settings.get_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fix_users_without_roles():
    """Asignar rol por defecto a usuarios sin roles"""
    db = SessionLocal()
    try:
        print("🔧 ASIGNANDO ROLES POR DEFECTO")
        print("=" * 60)
        
        # Buscar usuarios sin roles
        query = text("""
            SELECT u.id, u.email, u.first_name, u.last_name
            FROM users u
            LEFT JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            WHERE u.is_active = true
            GROUP BY u.id, u.email, u.first_name, u.last_name
            HAVING COUNT(ur.id) = 0
        """)
        
        result = db.execute(query)
        users_without_roles = result.fetchall()
        
        if not users_without_roles:
            print("✅ No hay usuarios sin roles que corregir")
            return
        
        print(f"📋 Encontrados {len(users_without_roles)} usuarios sin roles")
        
        # Buscar rol por defecto (family_member)
        default_role = db.query(Role).filter(Role.name == 'family_member').first()
        if not default_role:
            print("❌ No se encontró el rol 'family_member' para asignar por defecto")
            return
        
        print(f"🎯 Asignando rol '{default_role.name}' a todos los usuarios sin roles...")
        
        fixed_count = 0
        for user_row in users_without_roles:
            user_id = user_row[0]
            user_email = user_row[1]
            
            # Verificar si ya existe una asignación inactiva
            existing_assignment = db.query(UserRole).filter(
                UserRole.user_id == user_id,
                UserRole.role_id == default_role.id
            ).first()
            
            if existing_assignment:
                # Reactivar asignación existente
                existing_assignment.is_active = True
                print(f"   ✅ Reactivado rol para: {user_email}")
            else:
                # Crear nueva asignación
                new_assignment = UserRole(
                    user_id=user_id,
                    role_id=default_role.id,
                    is_active=True
                )
                db.add(new_assignment)
                print(f"   ✅ Creado nuevo rol para: {user_email}")
            
            fixed_count += 1
        
        db.commit()
        print(f"\n🎉 CORRECCIÓN COMPLETADA")
        print(f"   - Usuarios corregidos: {fixed_count}")
        print(f"   - Rol asignado: {default_role.name}")
        
        # Verificación post-corrección
        print(f"\n🔍 VERIFICACIÓN POST-CORRECCIÓN:")
        verify_fix()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la corrección: {e}")
        raise
    finally:
        db.close()

def verify_fix():
    """Verificar que la corrección funcionó"""
    db = SessionLocal()
    try:
        # Contar usuarios sin roles después de la corrección
        query = text("""
            SELECT COUNT(*) as count
            FROM users u
            LEFT JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            WHERE u.is_active = true
            GROUP BY u.id
            HAVING COUNT(ur.id) = 0
        """)
        
        result = db.execute(query)
        users_still_without_roles = len(result.fetchall())
        
        # Contar total de usuarios activos
        total_users = db.query(User).filter(User.is_active == True).count()
        
        print(f"   - Usuarios sin roles restantes: {users_still_without_roles}")
        print(f"   - Total usuarios activos: {total_users}")
        
        if users_still_without_roles == 0:
            print(f"   ✅ TODOS LOS USUARIOS TIENEN ROLES ASIGNADOS")
        else:
            print(f"   ⚠️  Aún quedan {users_still_without_roles} usuarios sin roles")
        
        # Mostrar distribución de roles
        print(f"\n📊 DISTRIBUCIÓN DE ROLES:")
        role_assignments = db.query(UserRole).filter(UserRole.is_active == True).all()
        role_counts = {}
        for assignment in role_assignments:
            role_name = assignment.role.name if assignment.role else "Desconocido"
            role_counts[role_name] = role_counts.get(role_name, 0) + 1
        
        for role_name, count in sorted(role_counts.items()):
            print(f"   - {role_name}: {count} usuarios")
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 CORRIGIENDO USUARIOS SIN ROLES")
    print("=" * 60)
    
    fix_users_without_roles()
    
    print("\n🎉 CORRECCIÓN COMPLETADA")
    print("=" * 60) 