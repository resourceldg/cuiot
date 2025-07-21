#!/usr/bin/env python3
"""
Script simple para probar autenticación y carga de roles
"""

import sys
import os
from app.core.database import get_db
from app.models.role import Role
from app.models.user import User
from app.services.auth import AuthService

def test_roles_direct():
    """Probar carga directa de roles desde la base de datos"""
    print("🔧 Probando carga directa de roles desde la BD...")
    
    try:
        db = next(get_db())
        roles = db.query(Role).filter(Role.is_active == True).all()
        
        print(f"✅ Roles encontrados: {len(roles)}")
        for role in roles:
            status = "✅ Activo" if role.is_active else "❌ Inactivo"
            print(f"   - {role.name}: {status}")
        
        return len(roles) > 0
        
    except Exception as e:
        print(f"❌ Error cargando roles: {e}")
        return False

def test_admin_user():
    """Probar si existe el usuario admin"""
    print("\n🔧 Verificando usuario admin...")
    
    try:
        db = next(get_db())
        admin_user = db.query(User).filter(User.email == "admin@cuiot.com").first()
        
        if admin_user:
            print(f"✅ Usuario admin encontrado: {admin_user.email}")
            print(f"   - ID: {admin_user.id}")
            print(f"   - Activo: {admin_user.is_active}")
            return True
        else:
            print("❌ Usuario admin no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando admin: {e}")
        return False

def test_auth_service():
    """Probar el servicio de autenticación"""
    print("\n🔧 Probando servicio de autenticación...")
    
    try:
        db = next(get_db())
        
        # Intentar autenticar con credenciales conocidas
        user = AuthService.authenticate_user(db, "admin@cuiot.com", "Admin123!")
        
        if user:
            print(f"✅ Autenticación exitosa: {user.email}")
            print(f"   - ID: {user.id}")
            print(f"   - Activo: {user.is_active}")
            
            # Verificar permisos
            has_permission = user.has_permission("users.read", db)
            print(f"   - Permiso users.read: {has_permission}")
            
            return True
        else:
            print("❌ Autenticación falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de autenticación y roles")
    print("=" * 50)
    
    # Probar carga directa de roles
    roles_ok = test_roles_direct()
    
    # Probar usuario admin
    admin_ok = test_admin_user()
    
    # Probar autenticación
    auth_ok = test_auth_service()
    
    print("\n" + "=" * 50)
    print("📋 Resumen de pruebas:")
    print(f"   Roles en BD: {'✅' if roles_ok else '❌'}")
    print(f"   Usuario admin: {'✅' if admin_ok else '❌'}")
    print(f"   Autenticación: {'✅' if auth_ok else '❌'}")
    
    if roles_ok and admin_ok and auth_ok:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("✅ El problema está en el frontend, no en el backend")
        return True
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        print("❌ El problema está en el backend")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 