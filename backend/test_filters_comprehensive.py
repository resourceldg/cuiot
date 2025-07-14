#!/usr/bin/env python3
"""
Test completo del sistema de filtrado de usuarios
Prueba todos los casos: individuales, combinados, negativos y validación de coherencia
"""

import requests
import json
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

BASE_URL = "http://localhost:8000/api/v1"

@dataclass
class TestResult:
    name: str
    success: bool
    users_count: int
    expected_min: int
    expected_max: int = None
    error: str = None
    users_sample: List[Dict] = None
    validation_errors: List[str] = None

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

def validate_user_filters(user: Dict, filters: Dict) -> List[str]:
    """Validar que un usuario cumple con todos los filtros aplicados"""
    errors = []
    
    # Validar búsqueda
    if 'search' in filters and filters['search']:
        search_term = filters['search'].lower()
        user_text = f"{user.get('first_name', '')} {user.get('last_name', '')} {user.get('email', '')}".lower()
        if search_term not in user_text:
            errors.append(f"Usuario no contiene término de búsqueda '{filters['search']}'")
    
    # Validar estado
    if 'is_active' in filters and filters['is_active'] is not None:
        if user.get('is_active') != filters['is_active']:
            errors.append(f"Estado incorrecto: esperaba {filters['is_active']}, obtuve {user.get('is_active')}")
    
    # Validar rol (exacto)
    if 'role' in filters and filters['role']:
        user_roles = [r.lower() for r in user.get('roles', [])]
        if filters['role'].lower() not in user_roles:
            errors.append(f"Rol '{filters['role']}' no encontrado en roles del usuario: {user_roles}")
    
    # Validar institución
    if 'institution_id' in filters and filters['institution_id'] is not None:
        if user.get('institution_id') != filters['institution_id']:
            errors.append(f"Institución incorrecta: esperaba {filters['institution_id']}, obtuve {user.get('institution_id')}")
    
    return errors

def test_filter(test_name: str, params: Dict[str, Any], expected_min: int = 0, expected_max: int = None, token: str = None) -> TestResult:
    """Probar un filtro específico con validación completa"""
    print(f"🔍 Probando: {test_name}")
    print(f"   Parámetros: {params}")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/", params=params, headers=headers)
    
    if response.status_code != 200:
        return TestResult(
            name=test_name,
            success=False,
            users_count=0,
            expected_min=expected_min,
            error=f"HTTP {response.status_code}: {response.text}"
        )
    
    users = response.json()
    success = len(users) >= expected_min
    if expected_max is not None:
        success = success and len(users) <= expected_max
    
    # Validar que cada usuario cumple con los filtros
    validation_errors = []
    for user in users:
        user_errors = validate_user_filters(user, params)
        if user_errors:
            validation_errors.extend([f"Usuario {user.get('email', 'N/A')}: {', '.join(user_errors)}"])
    
    # Tomar muestra de usuarios para mostrar
    users_sample = users[:3] if users else []
    
    result = TestResult(
        name=test_name,
        success=success and not validation_errors,
        users_count=len(users),
        expected_min=expected_min,
        expected_max=expected_max,
        users_sample=users_sample,
        validation_errors=validation_errors
    )
    
    if result.success:
        print(f"   ✅ Éxito: {len(users)} usuarios")
        if users_sample:
            print(f"   📋 Ejemplos:")
            for i, user in enumerate(users_sample):
                roles = ", ".join(user.get('roles', []))
                institution = f" (Inst: {user.get('institution_id')})" if user.get('institution_id') else " (Sin inst)"
                print(f"      {i+1}. {user.get('first_name', '')} {user.get('last_name', '')} - Roles: {roles}{institution}")
    else:
        print(f"   ❌ Falló: {len(users)} usuarios (esperaba {expected_min}-{expected_max or '∞'})")
        if validation_errors:
            print(f"   ⚠️  Errores de validación:")
            for error in validation_errors[:3]:  # Mostrar solo los primeros 3 errores
                print(f"      - {error}")
    
    return result

def run_comprehensive_tests():
    """Ejecutar todas las pruebas de filtros"""
    print("🧪 Iniciando test completo del sistema de filtrado...")
    
    try:
        token = get_auth_token()
        print("✅ Token obtenido correctamente")
        
        results = []
        
        # === FILTROS INDIVIDUALES ===
        print(f"\n📊 FILTROS INDIVIDUALES:")
        
        # Búsqueda
        results.append(test_filter("Búsqueda por nombre", {"search": "carlos"}, 1, 5, token))
        results.append(test_filter("Búsqueda por email", {"search": "carlos.rodriguez"}, 1, 1, token))
        results.append(test_filter("Búsqueda inexistente", {"search": "usuarioinexistente"}, 0, 0, token))
        
        # Estado
        results.append(test_filter("Usuarios activos", {"is_active": True}, 10, 20, token))
        results.append(test_filter("Usuarios inactivos", {"is_active": False}, 0, 5, token))
        
        # Roles (exactos)
        results.append(test_filter("Rol admin (sysadmin)", {"role": "admin"}, 0, 2, token))
        results.append(test_filter("Rol institution_admin", {"role": "institution_admin"}, 2, 5, token))
        results.append(test_filter("Rol cuidador", {"role": "cuidador"}, 4, 8, token))
        results.append(test_filter("Rol familia", {"role": "familia"}, 3, 6, token))
        results.append(test_filter("Rol inexistente", {"role": "rolinexistente"}, 0, 0, token))
        
        # Institución
        results.append(test_filter("Institución ID 1", {"institution_id": 1}, 2, 10, token))
        results.append(test_filter("Institución ID 2", {"institution_id": 2}, 0, 5, token))
        results.append(test_filter("Institución por nombre", {"institution_name": "San Martín"}, 2, 10, token))
        results.append(test_filter("Sin institución", {"no_institution": True}, 5, 15, token))
        
        # Paquetes
        results.append(test_filter("Paquete Básico", {"package": "Básico"}, 2, 8, token))
        results.append(test_filter("Paquete Premium", {"package": "Premium"}, 2, 8, token))
        results.append(test_filter("Paquete inexistente", {"package": "PaqueteInexistente"}, 0, 0, token))
        
        # === COMBINACIONES DE 2 FILTROS ===
        print(f"\n🔄 COMBINACIONES DE 2 FILTROS:")
        
        # Búsqueda + Estado
        results.append(test_filter("Búsqueda + Activo", {"search": "carlos", "is_active": True}, 1, 3, token))
        results.append(test_filter("Búsqueda + Inactivo", {"search": "carlos", "is_active": False}, 0, 0, token))
        
        # Búsqueda + Rol
        results.append(test_filter("Búsqueda + Rol Cuidador", {"search": "carlos", "role": "cuidador"}, 0, 2, token))
        
        # Estado + Rol
        results.append(test_filter("Activo + Admin", {"is_active": True, "role": "admin"}, 0, 2, token))
        results.append(test_filter("Activo + Institution Admin", {"is_active": True, "role": "institution_admin"}, 2, 5, token))
        
        # Institución + Rol
        results.append(test_filter("Institución 1 + Cuidador", {"institution_id": 1, "role": "cuidador"}, 0, 3, token))
        results.append(test_filter("Institución 1 + Institution Admin", {"institution_id": 1, "role": "institution_admin"}, 1, 3, token))
        
        # Institución + Paquete
        results.append(test_filter("Institución 1 + Paquete Básico", {"institution_id": 1, "package": "Básico"}, 0, 5, token))
        
        # Rol + Paquete
        results.append(test_filter("Cuidador + Paquete Premium", {"role": "cuidador", "package": "Premium"}, 0, 3, token))
        
        # === COMBINACIONES DE 3 FILTROS ===
        print(f"\n🎯 COMBINACIONES DE 3 FILTROS:")
        
        results.append(test_filter("Activo + Institución 1 + Cuidador", {
            "is_active": True, "institution_id": 1, "role": "cuidador"
        }, 0, 2, token))
        
        results.append(test_filter("Activo + Institución 1 + Paquete Básico", {
            "is_active": True, "institution_id": 1, "package": "Básico"
        }, 0, 3, token))
        
        # === CASOS NEGATIVOS (no deberían devolver nada) ===
        print(f"\n🚫 CASOS NEGATIVOS:")
        
        results.append(test_filter("Inactivo + Búsqueda existente", {"is_active": False, "search": "carlos"}, 0, 0, token))
        results.append(test_filter("Institución 2 + Rol con datos en Inst 1", {"institution_id": 2, "role": "institution_admin"}, 0, 0, token))
        
        # === REPORTE FINAL ===
        print(f"\n📋 REPORTE FINAL:")
        print("=" * 60)
        
        successful_tests = [r for r in results if r.success]
        failed_tests = [r for r in results if not r.success]
        
        print(f"✅ Tests exitosos: {len(successful_tests)}/{len(results)}")
        print(f"❌ Tests fallidos: {len(failed_tests)}/{len(results)}")
        
        if failed_tests:
            print(f"\n🔍 DETALLE DE FALLOS:")
            for result in failed_tests:
                print(f"   ❌ {result.name}")
                if result.error:
                    print(f"      Error: {result.error}")
                if result.validation_errors:
                    print(f"      Validación: {', '.join(result.validation_errors[:2])}")
                print(f"      Usuarios: {result.users_count} (esperaba {result.expected_min}-{result.expected_max or '∞'})")
        
        success_rate = (len(successful_tests) / len(results)) * 100
        print(f"\n📊 TASA DE ÉXITO: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 ¡Sistema de filtrado funcionando correctamente!")
        elif success_rate >= 70:
            print("⚠️  Sistema de filtrado con algunos problemas menores")
        else:
            print("🚨 Sistema de filtrado con problemas significativos")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    run_comprehensive_tests() 