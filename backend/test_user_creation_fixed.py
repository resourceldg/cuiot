#!/usr/bin/env python3
"""
Script de prueba para verificar la creación de usuarios
Después de las correcciones implementadas
"""

import requests
import json
import sys
import os

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def get_auth_token():
    """Obtener token de autenticación"""
    try:
        login_data = {
            "email": "admin@cuiot.com",
            "password": "admin123"
        }
        
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error obteniendo token: {e}")
        return None

def test_user_creation():
    """Probar la creación de usuarios"""
    
    print("🔧 Iniciando prueba de creación de usuarios...")
    
    # Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Datos de prueba para diferentes roles
    test_users = [
        {
            "name": "Test Caregiver",
            "email": "test.caregiver@example.com",
            "first_name": "Test",
            "last_name": "Caregiver",
            "phone": "+54 11 1234-5678",
            "is_active": True,
            "professional_license": "LIC123456",
            "specialization": "Cuidado de adultos mayores",
            "experience_years": 5,
            "is_freelance": False
        },
        {
            "name": "Test Family",
            "email": "test.family@example.com", 
            "first_name": "Test",
            "last_name": "Family",
            "phone": "+54 11 2345-6789",
            "is_active": True
        },
        {
            "name": "Test Institution Admin",
            "email": "test.institution@example.com",
            "first_name": "Test",
            "last_name": "Institution",
            "phone": "+54 11 3456-7890",
            "is_active": True,
            "institution_id": 1  # Asumiendo que existe una institución con ID 1
        }
    ]
    
    success_count = 0
    total_count = len(test_users)
    
    for i, user_data in enumerate(test_users, 1):
        print(f"\n🔧 Probando usuario {i}/{total_count}: {user_data['email']}")
        
        try:
            # Crear usuario
            response = requests.post(f"{API_BASE}/users/", json=user_data, headers=headers)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                user_result = response.json()
                user_id = user_data.get("id") or user_result.get("id")
                
                print(f"✅ Usuario creado exitosamente")
                print(f"   ID: {user_id}")
                print(f"   Email: {user_data['email']}")
                
                # Asignar rol según el tipo de usuario
                role = None
                if "professional_license" in user_data:
                    role = "caregiver"
                elif "institution_id" in user_data:
                    role = "institution_admin"
                else:
                    role = "family_member"
                
                if role and user_id:
                    print(f"🔧 Asignando rol: {role}")
                    role_response = requests.post(
                        f"{API_BASE}/users/{user_id}/roles/{role}",
                        headers=headers
                    )
                    
                    if role_response.status_code == 200:
                        print(f"✅ Rol {role} asignado exitosamente")
                        success_count += 1
                    else:
                        print(f"⚠️ Error asignando rol: {role_response.status_code}")
                        print(f"   Respuesta: {role_response.text}")
                        success_count += 1  # Usuario creado, solo falló la asignación de rol
                else:
                    success_count += 1
                    
            else:
                print(f"❌ Error creando usuario: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
    
    print(f"\n📊 Resultados:")
    print(f"   Usuarios creados exitosamente: {success_count}/{total_count}")
    print(f"   Tasa de éxito: {(success_count/total_count)*100:.1f}%")
    
    return success_count == total_count

def test_roles_availability():
    """Verificar que los roles están disponibles"""
    
    print("\n🔧 Verificando disponibilidad de roles...")
    
    token = get_auth_token()
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{API_BASE}/users/roles", headers=headers)
        
        if response.status_code == 200:
            roles = response.json()
            print(f"✅ Roles disponibles: {len(roles)}")
            
            for role in roles:
                status = "✅ Activo" if role.get("is_active", True) else "❌ Inactivo"
                print(f"   - {role['name']}: {status}")
            
            return len(roles) > 0
        else:
            print(f"❌ Error obteniendo roles: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando roles: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de creación de usuarios")
    print("=" * 50)
    
    # Verificar que el backend esté funcionando
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Backend no está respondiendo correctamente")
            return False
        print("✅ Backend funcionando correctamente")
    except Exception as e:
        print(f"❌ No se puede conectar al backend: {e}")
        return False
    
    # Verificar roles
    roles_ok = test_roles_availability()
    
    # Probar creación de usuarios
    creation_ok = test_user_creation()
    
    print("\n" + "=" * 50)
    print("📋 Resumen de pruebas:")
    print(f"   Roles disponibles: {'✅' if roles_ok else '❌'}")
    print(f"   Creación de usuarios: {'✅' if creation_ok else '❌'}")
    
    if roles_ok and creation_ok:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 