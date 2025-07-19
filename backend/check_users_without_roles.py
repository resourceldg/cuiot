#!/usr/bin/env python3
"""
Script para verificar usuarios sin roles asignados
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

def check_users_without_roles():
    """Verificar usuarios sin roles asignados"""
    db = SessionLocal()
    try:
        print("🔍 VERIFICANDO USUARIOS SIN ROLES")
        print("=" * 60)
        
        # Consulta SQL directa para encontrar usuarios sin roles
        query = text("""
            SELECT 
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                u.is_active,
                u.created_at,
                COUNT(ur.id) as role_count
            FROM users u
            LEFT JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            WHERE u.is_active = true
            GROUP BY u.id, u.email, u.first_name, u.last_name, u.is_active, u.created_at
            HAVING COUNT(ur.id) = 0
            ORDER BY u.created_at DESC
        """)
        
        result = db.execute(query)
        users_without_roles = result.fetchall()
        
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   - Usuarios sin roles: {len(users_without_roles)}")
        
        # Contar total de usuarios activos
        total_users = db.query(User).filter(User.is_active == True).count()
        print(f"   - Total usuarios activos: {total_users}")
        print(f"   - Porcentaje sin roles: {(len(users_without_roles) / total_users * 100):.1f}%")
        
        if users_without_roles:
            print(f"\n👥 USUARIOS SIN ROLES:")
            print("-" * 60)
            for user in users_without_roles:
                print(f"   - {user.email} ({user.first_name} {user.last_name or ''})")
                print(f"     ID: {user.id}")
                print(f"     Creado: {user.created_at}")
                print()
        else:
            print(f"\n✅ TODOS LOS USUARIOS TIENEN ROLES ASIGNADOS")
        
        # Verificar roles disponibles
        print(f"\n📋 ROLES DISPONIBLES:")
        roles = db.query(Role).filter(Role.is_active == True).all()
        for role in roles:
            print(f"   - {role.name}: {role.description}")
        
        # Verificar asignaciones de roles
        print(f"\n🔗 ASIGNACIONES DE ROLES:")
        role_assignments = db.query(UserRole).filter(UserRole.is_active == True).all()
        role_counts = {}
        for assignment in role_assignments:
            role_name = assignment.role.name if assignment.role else "Desconocido"
            role_counts[role_name] = role_counts.get(role_name, 0) + 1
        
        for role_name, count in role_counts.items():
            print(f"   - {role_name}: {count} usuarios")
        
        return users_without_roles
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        raise
    finally:
        db.close()

def fix_users_without_roles():
    """Asignar rol por defecto a usuarios sin roles"""
    db = SessionLocal()
    try:
        print("\n🔧 ASIGNANDO ROLES POR DEFECTO")
        print("=" * 60)
        
        # Buscar usuarios sin roles
        query = text("""
            SELECT u.id
            FROM users u
            LEFT JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            WHERE u.is_active = true
            GROUP BY u.id
            HAVING COUNT(ur.id) = 0
        """)
        
        result = db.execute(query)
        users_without_roles = result.fetchall()
        
        if not users_without_roles:
            print("✅ No hay usuarios sin roles que corregir")
            return
        
        # Buscar rol por defecto (family_member)
        default_role = db.query(Role).filter(Role.name == 'family_member').first()
        if not default_role:
            print("❌ No se encontró el rol 'family_member' para asignar por defecto")
            return
        
        print(f"📋 Asignando rol '{default_role.name}' a {len(users_without_roles)} usuarios...")
        
        fixed_count = 0
        for user_row in users_without_roles:
            user_id = user_row[0]
            
            # Verificar si ya existe una asignación inactiva
            existing_assignment = db.query(UserRole).filter(
                UserRole.user_id == user_id,
                UserRole.role_id == default_role.id
            ).first()
            
            if existing_assignment:
                # Reactivar asignación existente
                existing_assignment.is_active = True
                print(f"   ✅ Reactivado rol para usuario {user_id}")
            else:
                # Crear nueva asignación
                new_assignment = UserRole(
                    user_id=user_id,
                    role_id=default_role.id,
                    is_active=True
                )
                db.add(new_assignment)
                print(f"   ✅ Creado nuevo rol para usuario {user_id}")
            
            fixed_count += 1
        
        db.commit()
        print(f"\n🎉 CORRECCIÓN COMPLETADA")
        print(f"   - Usuarios corregidos: {fixed_count}")
        print(f"   - Rol asignado: {default_role.name}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la corrección: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 VERIFICANDO USUARIOS SIN ROLES")
    print("=" * 60)
    
    # Verificar estado actual
    users_without_roles = check_users_without_roles()
    
    # Preguntar si corregir
    if users_without_roles:
        print(f"\n❓ ¿Deseas asignar rol por defecto a {len(users_without_roles)} usuarios? (s/n): ", end="")
        response = input().strip().lower()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            fix_users_without_roles()
            print(f"\n🔍 VERIFICACIÓN POST-CORRECCIÓN:")
            check_users_without_roles()
        else:
            print("❌ Corrección cancelada por el usuario")
    else:
        print("✅ No hay usuarios sin roles que corregir")
    
    print("\n🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 60) 