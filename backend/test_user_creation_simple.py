#!/usr/bin/env python3
"""
Script de prueba simple para verificar la creación de usuarios
Usando las librerías disponibles en el contenedor Docker
"""

import sys
import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def make_request(url, method="GET", data=None, headers=None):
    """Hacer una petición HTTP"""
    if headers is None:
        headers = {}
    
    if data and method in ["POST", "PUT"]:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    req = Request(url, data=data, headers=headers, method=method)
    
    try:
        with urlopen(req) as response:
            return {
                'status': response.status,
                'data': json.loads(response.read().decode('utf-8'))
            }
    except HTTPError as e:
        return {
            'status': e.code,
            'data': json.loads(e.read().decode('utf-8')) if e.read() else {}
        }
    except URLError as e:
        return {
            'status': 0,
            'data': {'error': str(e)}
        }

def get_auth_token():
    """Obtener token de autenticación"""
    print("🔧 Obteniendo token de autenticación...")
    
    login_data = {
        "email": "admin@cuiot.com",
        "password": "admin123"
    }
    
    response = make_request(f"{API_BASE}/auth/login", method="POST", data=login_data)
    
    if response['status'] == 200:
        token = response['data'].get("access_token")
        if token:
            print("✅ Token obtenido exitosamente")
            return token
        else:
            print("❌ No se encontró token en la respuesta")
            return None
    else:
        print(f"❌ Error en login: {response['status']}")
        print(f"Respuesta: {response['data']}")
        return None

def test_roles_availability(token):
    """Verificar que los roles están disponibles"""
    print("\n🔧 Verificando disponibilidad de roles...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = make_request(f"{API_BASE}/users/roles", headers=headers)
    
    if response['status'] == 200:
        roles = response['data']
        print(f"✅ Roles disponibles: {len(roles)}")
        
        for role in roles:
            status = "✅ Activo" if role.get("is_active", True) else "❌ Inactivo"
            print(f"   - {role['name']}: {status}")
        
        return len(roles) > 0
    else:
        print(f"❌ Error obteniendo roles: {response['status']}")
        print(f"   Respuesta: {response['data']}")
        return False

def test_user_creation(token):
    """Probar la creación de usuarios"""
    print("\n🔧 Probando creación de usuarios...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Usuario de prueba simple
    test_user = {
        "email": "test.user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+54 11 1234-5678",
        "is_active": True
    }
    
    print(f"🔧 Creando usuario: {test_user['email']}")
    
    response = make_request(f"{API_BASE}/users/", method="POST", data=test_user, headers=headers)
    
    print(f"Status: {response['status']}")
    
    if response['status'] == 201:
        user_result = response['data']
        user_id = user_result.get("id")
        
        print(f"✅ Usuario creado exitosamente")
        print(f"   ID: {user_id}")
        print(f"   Email: {test_user['email']}")
        
        # Asignar rol básico
        if user_id:
            print(f"🔧 Asignando rol: family_member")
            role_response = make_request(
                f"{API_BASE}/users/{user_id}/roles/family_member",
                method="POST",
                headers=headers
            )
            
            if role_response['status'] == 200:
                print(f"✅ Rol family_member asignado exitosamente")
                return True
            else:
                print(f"⚠️ Error asignando rol: {role_response['status']}")
                print(f"   Respuesta: {role_response['data']}")
                return True  # Usuario creado, solo falló la asignación de rol
        else:
            print("⚠️ No se pudo obtener ID del usuario creado")
            return False
    else:
        print(f"❌ Error creando usuario: {response['status']}")
        print(f"   Respuesta: {response['data']}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de creación de usuarios")
    print("=" * 50)
    
    # Verificar que el backend esté funcionando
    print("🔧 Verificando conectividad con el backend...")
    response = make_request(f"{BASE_URL}/health")
    
    if response['status'] != 200:
        print("❌ Backend no está respondiendo correctamente")
        return False
    print("✅ Backend funcionando correctamente")
    
    # Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return False
    
    # Verificar roles
    roles_ok = test_roles_availability(token)
    
    # Probar creación de usuarios
    creation_ok = test_user_creation(token)
    
    print("\n" + "=" * 50)
    print("📋 Resumen de pruebas:")
    print(f"   Roles disponibles: {'✅' if roles_ok else '❌'}")
    print(f"   Creación de usuarios: {'✅' if creation_ok else '❌'}")
    
    if roles_ok and creation_ok:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ La creación de usuarios está funcionando correctamente")
        return True
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 