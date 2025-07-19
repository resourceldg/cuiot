#!/usr/bin/env python3
"""
Script simple para probar la eliminación de usuarios con CASCADE DELETE
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid

def test_cascade_delete():
    """Probar la eliminación de usuarios con CASCADE DELETE"""
    database_url = os.getenv("DATABASE_URL", "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db")
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    
    print("🧪 Probando eliminación de usuarios con CASCADE DELETE...")
    
    with Session() as session:
        try:
            # Crear un usuario de prueba
            user_id = str(uuid.uuid4())
            print(f"📝 Creando usuario de prueba con ID: {user_id}")
            
            # Insertar usuario
            result = session.execute(text("""
                INSERT INTO users (id, email, first_name, last_name, password_hash, is_freelance, is_verified, is_active, created_at, updated_at)
                VALUES (:user_id, :email, :first_name, :last_name, :password_hash, :is_freelance, :is_verified, :is_active, NOW(), NOW())
                RETURNING id, email
            """), {
                'user_id': user_id,
                'email': 'test.cascade@cuiot.com',
                'first_name': 'Test',
                'last_name': 'Cascade',
                'password_hash': 'pbkdf2:sha256:dummyhash',
                'is_freelance': False,
                'is_verified': False,
                'is_active': True
            })
            
            user_data = result.fetchone()
            print(f"✅ Usuario creado: {user_data[1]}")
            
            # Asignar un rol
            role_result = session.execute(text("""
                INSERT INTO user_roles (user_id, role_id, assigned_at, is_active, created_at, updated_at)
                SELECT :user_id, r.id, NOW(), true, NOW(), NOW()
                FROM roles r
                WHERE r.name = 'family_member'
                LIMIT 1
                RETURNING user_id, role_id
            """), {'user_id': user_id})
            
            role_data = role_result.fetchone()
            if role_data:
                print(f"✅ Rol asignado: user_id={role_data[0]}, role_id={role_data[1]}")
            
            # Verificar que el usuario existe
            check_result = session.execute(text("""
                SELECT u.id, u.email, COUNT(ur.id) as roles_count
                FROM users u
                LEFT JOIN user_roles ur ON u.id = ur.user_id
                WHERE u.id = :user_id
                GROUP BY u.id, u.email
            """), {'user_id': user_id})
            
            user_check = check_result.fetchone()
            if user_check:
                print(f"✅ Usuario verificado: {user_check[1]} con {user_check[2]} roles")
            
            # Ahora eliminar el usuario usando CASCADE DELETE
            print(f"🗑️  Eliminando usuario: {user_id}")
            
            # Usar la función de eliminación
            delete_result = session.execute(text("""
                SELECT delete_user_complete(:user_id)
            """), {'user_id': user_id})
            
            delete_success = delete_result.scalar()
            print(f"✅ Resultado de eliminación: {delete_success}")
            
            # Verificar que el usuario fue eliminado
            verify_result = session.execute(text("""
                SELECT COUNT(*) as user_count
                FROM users
                WHERE id = :user_id
            """), {'user_id': user_id})
            
            user_count = verify_result.scalar()
            print(f"✅ Usuarios restantes con ese ID: {user_count}")
            
            # Verificar que los roles también fueron eliminados
            roles_result = session.execute(text("""
                SELECT COUNT(*) as roles_count
                FROM user_roles
                WHERE user_id = :user_id
            """), {'user_id': user_id})
            
            roles_count = roles_result.scalar()
            print(f"✅ Roles restantes para ese usuario: {roles_count}")
            
            if user_count == 0 and roles_count == 0:
                print("🎉 ¡Prueba exitosa! CASCADE DELETE funciona correctamente")
                return True
            else:
                print("❌ Prueba fallida: algunos registros no fueron eliminados")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            session.rollback()
            return False

def main():
    """Función principal"""
    print("🚀 Iniciando prueba de CASCADE DELETE...")
    
    success = test_cascade_delete()
    
    if success:
        print("\n✅ Todas las pruebas pasaron exitosamente!")
        print("💡 El refactor del DDL con CASCADE DELETE está funcionando correctamente")
    else:
        print("\n❌ Algunas pruebas fallaron")
        print("💡 Revisar los logs para identificar el problema")

if __name__ == "__main__":
    main() 