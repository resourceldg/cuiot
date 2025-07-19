#!/usr/bin/env python3
"""
Script para debuggear la serialización en el servicio específicamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.user import UserService
from app.schemas.user import UserPackageResponse
import json

def debug_service_serialization():
    """Debuggear la serialización en el servicio"""
    
    db = next(get_db())
    
    try:
        print("🔍 Debuggeando serialización en el servicio...")
        
        # Obtener usuarios con roles usando el servicio
        users = UserService.get_users_with_roles(db, limit=10)
        
        print(f"📊 Total de usuarios obtenidos: {len(users)}")
        
        # Buscar usuarios específicos que deberían tener paquetes
        target_emails = [
            "admin.clinica@cuiot.com",
            "paciente2@cuiot.com"
        ]
        
        for user in users:
            if user.email in target_emails:
                print(f"\n👤 Usuario encontrado: {user.email}")
                print(f"👤 Tipo del usuario: {type(user)}")
                print(f"👤 Roles: {user.roles}")
                print(f"👤 package_subscriptions: {user.package_subscriptions}")
                print(f"👤 Tipo de package_subscriptions: {type(user.package_subscriptions)}")
                
                if user.package_subscriptions:
                    first_package = user.package_subscriptions[0]
                    print(f"👤 Primer paquete: {first_package}")
                    print(f"👤 Tipo del primer paquete: {type(first_package)}")
                    
                    # Intentar acceder a los campos
                    try:
                        print(f"👤 package_name: {first_package.package_name}")
                    except Exception as e:
                        print(f"❌ Error accediendo a package_name: {e}")
                    
                    try:
                        print(f"👤 id: {first_package.id}")
                    except Exception as e:
                        print(f"❌ Error accediendo a id: {e}")
                    
                    # Convertir a dict
                    try:
                        package_dict = first_package.model_dump()
                        print(f"👤 Dict del paquete: {package_dict}")
                    except Exception as e:
                        print(f"❌ Error convirtiendo a dict: {e}")
                    
                    # Convertir a JSON
                    try:
                        package_json = first_package.model_dump_json()
                        print(f"👤 JSON del paquete: {package_json}")
                    except Exception as e:
                        print(f"❌ Error convirtiendo a JSON: {e}")
                
                # Convertir el usuario completo a dict
                try:
                    user_dict = user.model_dump()
                    print(f"\n👤 Dict completo del usuario:")
                    print(json.dumps(user_dict, indent=2, default=str))
                except Exception as e:
                    print(f"❌ Error convirtiendo usuario a dict: {e}")
                
                break  # Solo mostrar el primero que encontremos
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Debuggeando serialización en el servicio...")
    success = debug_service_serialization()
    if success:
        print("\n✅ Debug completado")
    else:
        print("\n❌ Debug falló")
        sys.exit(1) 