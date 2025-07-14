#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de filtrado de usuarios
"""

import requests
import json
from typing import Dict, Any

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

def test_filter(filter_name: str, params: Dict[str, Any], expected_min_results: int = 0):
    """Probar un filtro específico"""
    print(f"\n🔍 Probando filtro: {filter_name}")
    print(f"   Parámetros: {params}")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/", params=params, headers=headers)
    
    if response.status_code == 200:
        users = response.json()
        print(f"   ✅ Éxito: {len(users)} usuarios encontrados")
        if len(users) > 0:
            print(f"   📋 Primeros usuarios:")
            for i, user in enumerate(users[:3]):
                roles = ", ".join(user.get('roles', []))
                print(f"      {i+1}. {user.get('first_name', '')} {user.get('last_name', '')} - Roles: {roles}")
        if len(users) < expected_min_results:
            print(f"   ⚠️  Advertencia: Solo {len(users)} usuarios (esperaba al menos {expected_min_results})")
    else:
        print(f"   ❌ Error: {response.status_code} - {response.text}")

def test_combined_filters():
    """Probar combinaciones de filtros"""
    print(f"\n🔄 Probando combinaciones de filtros:")
    
    # Combinación 1: Búsqueda + Estado
    test_filter("Búsqueda + Estado Activo", {
        "search": "carlos",
        "is_active": True
    }, 1)
    
    # Combinación 2: Institución + Rol
    test_filter("Institución + Rol", {
        "institution_id": 1,
        "role": "cuidador"
    }, 1)
    
    # Combinación 3: Estado + Rol
    test_filter("Estado Activo + Rol Admin", {
        "is_active": True,
        "role": "admin"
    }, 1)

if __name__ == "__main__":
    print("🧪 Iniciando pruebas del sistema de filtrado...")
    
    try:
        # Obtener token
        token = get_auth_token()
        print(f"✅ Token obtenido correctamente")
        
        # Probar filtros individuales
        print(f"\n📊 Probando filtros individuales:")
        
        # Filtro de búsqueda
        test_filter("Búsqueda por nombre", {"search": "carlos"}, 1)
        test_filter("Búsqueda por email", {"search": "carlos.rodriguez"}, 1)
        
        # Filtro de estado
        test_filter("Usuarios activos", {"is_active": True}, 10)
        test_filter("Usuarios inactivos", {"is_active": False}, 0)
        
        # Filtro de roles
        test_filter("Rol admin", {"role": "admin"}, 1)
        test_filter("Rol cuidador", {"role": "cuidador"}, 6)
        test_filter("Rol familia", {"role": "familia"}, 5)
        
        # Filtro de institución
        test_filter("Institución ID 1", {"institution_id": 1}, 2)
        test_filter("Institución por nombre", {"institution_name": "San Martín"}, 2)
        
        # Filtro de paquetes (ahora que existen)
        test_filter("Paquete Básico", {"package": "Básico"}, 0)  # No hay usuarios con paquetes asignados
        
        # Probar combinaciones
        test_combined_filters()
        
        print(f"\n🎉 Pruebas completadas!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}") 