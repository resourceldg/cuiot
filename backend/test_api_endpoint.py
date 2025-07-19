#!/usr/bin/env python3
"""
Script para probar el endpoint de la API directamente
"""

import requests
import json

def test_api_endpoint():
    """Probar el endpoint de la API directamente"""
    
    try:
        print("🔍 Probando endpoint de la API...")
        
        # URL del endpoint
        url = "http://localhost:8000/api/v1/users/"
        
        # Parámetros
        params = {
            "limit": 10,
            "skip": 0
        }
        
        print(f"📡 Haciendo request a: {url}")
        print(f"📋 Parámetros: {params}")
        
        # Hacer la request
        response = requests.get(url, params=params)
        
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total de usuarios: {len(data)}")
            
            # Buscar usuarios específicos
            target_emails = [
                "admin.clinica@cuiot.com",
                "paciente2@cuiot.com"
            ]
            
            for user in data:
                if user.get('email') in target_emails:
                    print(f"\n👤 Usuario encontrado: {user['email']}")
                    print(f"👤 Roles: {user.get('roles', [])}")
                    print(f"👤 package_subscriptions: {user.get('package_subscriptions', [])}")
                    
                    if user.get('package_subscriptions'):
                        first_package = user['package_subscriptions'][0]
                        print(f"👤 Primer paquete: {first_package}")
                        print(f"👤 Tipo del primer paquete: {type(first_package)}")
                        
                        if isinstance(first_package, dict):
                            print(f"👤 package_name: {first_package.get('package_name')}")
                        else:
                            print(f"👤 package_name: {first_package}")
                    
                    # Mostrar estructura completa
                    print(f"\n👤 Estructura completa:")
                    print(json.dumps(user, indent=2, default=str))
                    break
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"❌ Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Probando endpoint de la API...")
    success = test_api_endpoint()
    if success:
        print("\n✅ Prueba completada")
    else:
        print("\n❌ Prueba falló")
        import sys
        sys.exit(1) 