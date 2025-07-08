#!/usr/bin/env python3
"""
Script para crear un usuario administrador en la base de datos CUIOT
"""

import sys
import os
import asyncio
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.database import get_db
from app.models.user import User
from app.models.user_type import UserType
from app.models.role import Role
from app.services.auth import AuthService
from sqlalchemy.orm import Session

async def create_admin_user():
    """Crear usuario administrador del sistema"""
    
    # Datos del admin
    admin_data = {
        "email": "admin@cuiot.com",
        "first_name": "Administrador",
        "last_name": "del Sistema",
        "password": "Admin123!",  # Contraseña temporal
        "phone": "+1234567890",
        "is_active": True,
        "is_verified": True
    }
    
    try:
        # Obtener sesión de base de datos
        db = next(get_db())
        
        # Verificar si ya existe un admin
        existing_admin = db.query(User).filter(User.email == admin_data["email"]).first()
        if existing_admin:
            print(f"❌ Ya existe un usuario admin con el email: {admin_data['email']}")
            return False
        
        # Obtener el rol de admin
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("❌ No se encontró el rol 'admin' en la base de datos")
            return False
        
        # Crear el usuario admin
        hashed_password = AuthService.get_password_hash(admin_data["password"])
        
        admin_user = User(
            email=admin_data["email"],
            first_name=admin_data["first_name"],
            last_name=admin_data["last_name"],
            password_hash=hashed_password,
            phone=admin_data["phone"],
            is_active=admin_data["is_active"],
            is_verified=admin_data["is_verified"]
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Asignar rol admin al usuario
        from app.models.user_role import UserRole
        from datetime import datetime
        
        user_role = UserRole(
            user_id=admin_user.id,
            role_id=admin_role.id,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(user_role)
        db.commit()
        
        print("✅ Usuario administrador creado exitosamente!")
        print(f"📧 Email: {admin_data['email']}")
        print(f"🔑 Contraseña: {admin_data['password']}")
        print(f"🆔 ID: {admin_user.id}")
        print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear el usuario admin: {str(e)}")
        return False
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 Creando usuario administrador para CUIOT...")
    print("=" * 50)
    
    # Ejecutar la creación del admin
    success = asyncio.run(create_admin_user())
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 ¡Usuario admin creado exitosamente!")
        print("\n📋 URLs de acceso:")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📊 Adminer (DB): http://localhost:8080")
        print("\n🔐 Credenciales:")
        print("   Email: admin@cuiot.com")
        print("   Contraseña: Admin123!")
    else:
        print("\n❌ No se pudo crear el usuario admin")
        sys.exit(1)

if __name__ == "__main__":
    main() 