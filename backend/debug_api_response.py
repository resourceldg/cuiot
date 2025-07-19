#!/usr/bin/env python3
"""
Script para verificar qué datos está enviando la API para los usuarios específicos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.user import UserService
import json

def debug_api_response():
    """Verificar qué datos está enviando la API"""
    
    db = next(get_db())
    
    try:
        print("🔍 Verificando respuesta de la API...")
        
        # Obtener usuarios con roles usando el servicio
        users = UserService.get_users_with_roles(db, limit=10)
        
        print(f"📊 Total de usuarios obtenidos: {len(users)}")
        
        # Buscar usuarios específicos
        specific_emails = [
            "admin.clinica@cuiot.com",
            "carmen.reyes.20250715141707336212@cuiot.com", 
            "paciente2@cuiot.com"
        ]
        
        for email in specific_emails:
            print(f"\n👤 Verificando: {email}")
            
            # Buscar usuario en la respuesta
            user = None
            for u in users:
                if u.email == email:
                    user = u
                    break
            
            if not user:
                print(f"   ❌ Usuario no encontrado en la respuesta de la API")
                continue
            
            print(f"   ✅ Usuario encontrado: {user.first_name} {user.last_name}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔄 Activo: {user.is_active}")
            print(f"   🏷️  Roles: {user.roles}")
            
            # Verificar paquetes
            if hasattr(user, 'package_subscriptions'):
                print(f"   📦 Package subscriptions: {len(user.package_subscriptions)}")
                for i, pkg in enumerate(user.package_subscriptions):
                    print(f"      {i+1}. {pkg}")
            else:
                print(f"   ❌ No tiene atributo package_subscriptions")
            
            # Convertir a dict para ver la estructura completa
            user_dict = {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'roles': user.roles,
                'package_subscriptions': user.package_subscriptions if hasattr(user, 'package_subscriptions') else None
            }
            
            print(f"   📋 Estructura completa:")
            print(json.dumps(user_dict, indent=2, default=str))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Verificando respuesta de la API...")
    success = debug_api_response()
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Verificación falló")
        sys.exit(1) 