#!/usr/bin/env python3
"""
Test específico para el filtro de usuarios sin institución
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def get_auth_token() -> str:
    """Obtener token de autenticación"""
    login_data = {
        "email": "admin@cuiot.com",
        "password": "Admin123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Error de login: {response.status_code} - {response.text}")

def test_no_institution_filter():
    """Probar el filtro de usuarios sin institución"""
    print("🧪 Probando filtro de usuarios sin institución...")
    
    try:
        token = get_auth_token()
        print("✅ Token obtenido correctamente")
        
        # Test 1: Usuarios sin institución usando no_institution=true
        print(f"\n🔍 Test 1: no_institution=true")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/", params={"no_institution": True}, headers=headers)
        
        if response.status_code == 200:
            users = response.json()
            print(f"   ✅ Éxito: {len(users)} usuarios sin institución")
            
            # Verificar que todos los usuarios devueltos no tienen institución
            all_without_institution = True
            for user in users:
                if user.get('institution_id') is not None:
                    all_without_institution = False
                    print(f"   ❌ Usuario {user.get('email')} tiene institución: {user.get('institution_id')}")
            
            if all_without_institution:
                print(f"   ✅ Todos los usuarios devueltos no tienen institución")
            else:
                print(f"   ❌ Algunos usuarios devueltos tienen institución")
            
            # Mostrar ejemplos
            if users:
                print(f"   📋 Ejemplos:")
                for i, user in enumerate(users[:3]):
                    print(f"      {i+1}. {user.get('first_name', '')} {user.get('last_name', '')} - Inst: {user.get('institution_id')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        # Test 2: Comparar con institution_id=None (debería devolver todos)
        print(f"\n🔍 Test 2: institution_id=None (comparación)")
        response2 = requests.get(f"{BASE_URL}/users/", params={"institution_id": None}, headers=headers)
        
        if response2.status_code == 200:
            users2 = response2.json()
            print(f"   📊 institution_id=None devuelve: {len(users2)} usuarios")
            print(f"   📊 no_institution=true devuelve: {len(users)} usuarios")
            
            if len(users) < len(users2):
                print(f"   ✅ El filtro no_institution está funcionando correctamente")
            else:
                print(f"   ⚠️  Ambos filtros devuelven la misma cantidad")
        else:
            print(f"   ❌ Error en comparación: {response2.status_code} - {response2.text}")
        
        # Test 3: Combinación con otros filtros
        print(f"\n🔍 Test 3: Combinación con otros filtros")
        response3 = requests.get(f"{BASE_URL}/users/", params={
            "no_institution": True,
            "is_active": True,
            "role": "cuidador"
        }, headers=headers)
        
        if response3.status_code == 200:
            users3 = response3.json()
            print(f"   ✅ Combinación exitosa: {len(users3)} usuarios sin institución, activos y con rol cuidador")
            
            if users3:
                print(f"   📋 Ejemplos:")
                for i, user in enumerate(users3[:2]):
                    roles = ", ".join(user.get('roles', []))
                    print(f"      {i+1}. {user.get('first_name', '')} {user.get('last_name', '')} - Roles: {roles} - Inst: {user.get('institution_id')}")
        else:
            print(f"   ❌ Error en combinación: {response3.status_code} - {response3.text}")
        
        print(f"\n🎉 Test completado!")
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")

if __name__ == "__main__":
    test_no_institution_filter() 