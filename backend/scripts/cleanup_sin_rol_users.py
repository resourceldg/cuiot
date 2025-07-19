#!/usr/bin/env python3
"""
Script para limpiar usuarios que quedaron con el rol 'sin_rol' y están causando problemas.
Este script:
1. Identifica usuarios que solo tienen el rol 'sin_rol'
2. Los elimina completamente de la base de datos
3. Limpia cualquier referencia a estos usuarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from sqlalchemy import func

def cleanup_sin_rol_users():
    """Limpia usuarios que solo tienen el rol 'sin_rol'"""
    db = next(get_db())
    
    try:
        print("🔍 Buscando usuarios con rol 'sin_rol'...")
        
        # Buscar el rol 'sin_rol'
        sin_rol = db.query(Role).filter(Role.name == "sin_rol").first()
        if not sin_rol:
            print("❌ No se encontró el rol 'sin_rol'")
            return
        
        print(f"✅ Rol 'sin_rol' encontrado con ID: {sin_rol.id}")
        
        # Buscar usuarios que solo tienen el rol 'sin_rol'
        users_with_sin_rol = db.query(User).join(UserRole, User.id == UserRole.user_id).filter(
            UserRole.role_id == sin_rol.id,
            UserRole.is_active == True
        ).all()
        
        print(f"🔍 Encontrados {len(users_with_sin_rol)} usuarios con rol 'sin_rol'")
        
        users_to_delete = []
        
        for user in users_with_sin_rol:
            # Contar cuántos roles activos tiene el usuario
            active_roles_count = db.query(func.count(UserRole.id)).filter(
                UserRole.user_id == user.id,
                UserRole.is_active == True
            ).scalar()
            
            print(f"👤 Usuario: {user.email} - Roles activos: {active_roles_count}")
            
            # Si solo tiene el rol 'sin_rol', marcarlo para eliminación
            if active_roles_count == 1:
                users_to_delete.append(user)
                print(f"   ❌ Marcado para eliminación (solo tiene sin_rol)")
            else:
                print(f"   ✅ Mantener (tiene otros roles)")
        
        if not users_to_delete:
            print("✅ No hay usuarios que necesiten ser eliminados")
            return
        
        print(f"\n🗑️ Usuarios a eliminar ({len(users_to_delete)}):")
        for user in users_to_delete:
            print(f"   - {user.email} ({user.first_name} {user.last_name})")
        
        # Confirmar eliminación
        response = input(f"\n¿Eliminar estos {len(users_to_delete)} usuarios? (s/N): ")
        if response.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        # Desactivar usuarios problemáticos en lugar de eliminarlos
        deactivated_count = 0
        for user in users_to_delete:
            try:
                print(f"🚫 Desactivando usuario: {user.email}")
                
                # Desactivar el usuario
                from sqlalchemy import text
                db.execute(text(f"UPDATE users SET is_active = false WHERE id = '{user.id}'"))
                deactivated_count += 1
                
            except Exception as e:
                print(f"❌ Error desactivando {user.email}: {e}")
                db.rollback()
                continue
        
        db.commit()
        print(f"✅ {deactivated_count} usuarios desactivados exitosamente")
        
        # Verificar si quedan usuarios con sin_rol
        remaining_users = db.query(User).join(UserRole).filter(
            UserRole.role_id == sin_rol.id,
            UserRole.is_active == True
        ).count()
        
        print(f"🔍 Usuarios restantes con rol 'sin_rol': {remaining_users}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def list_sin_rol_users():
    """Lista usuarios con rol 'sin_rol' sin eliminarlos"""
    db = next(get_db())
    
    try:
        print("🔍 Listando usuarios con rol 'sin_rol'...")
        
        # Buscar el rol 'sin_rol'
        sin_rol = db.query(Role).filter(Role.name == "sin_rol").first()
        if not sin_rol:
            print("❌ No se encontró el rol 'sin_rol'")
            return
        
        # Buscar usuarios con rol 'sin_rol'
        users_with_sin_rol = db.query(User).join(UserRole, User.id == UserRole.user_id).filter(
            UserRole.role_id == sin_rol.id,
            UserRole.is_active == True
        ).all()
        
        print(f"🔍 Encontrados {len(users_with_sin_rol)} usuarios con rol 'sin_rol':")
        
        for user in users_with_sin_rol:
            # Contar roles activos
            active_roles_count = db.query(func.count(UserRole.id)).filter(
                UserRole.user_id == user.id,
                UserRole.is_active == True
            ).scalar()
            
            status = "❌ SOLO SIN_ROL" if active_roles_count == 1 else "✅ TIENE OTROS ROLES"
            print(f"   {status} - {user.email} ({user.first_name} {user.last_name}) - Roles activos: {active_roles_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_sin_rol_users()
    else:
        cleanup_sin_rol_users() 