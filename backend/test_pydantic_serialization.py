#!/usr/bin/env python3
"""
Script para probar la serialización de Pydantic específicamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.schemas.user import UserPackageResponse, UserWithRoles
import json

def test_pydantic_serialization():
    """Probar la serialización de Pydantic"""
    
    try:
        print("🧪 Probando serialización de Pydantic...")
        
        # Crear un objeto UserPackageResponse
        package_response = UserPackageResponse(
            id="test-id",
            package_id="test-package-id",
            package_name="Test Package",
            status_type_id=1,
            is_active=True
        )
        
        print(f"📦 UserPackageResponse creado: {package_response}")
        print(f"📦 Tipo: {type(package_response)}")
        print(f"📦 package_name: {package_response.package_name}")
        
        # Convertir a dict
        package_dict = package_response.model_dump()
        print(f"📦 Dict: {package_dict}")
        
        # Convertir a JSON
        package_json = package_response.model_dump_json()
        print(f"📦 JSON: {package_json}")
        
        # Crear una lista de paquetes
        packages = [package_response]
        print(f"📦 Lista de paquetes: {packages}")
        print(f"📦 Tipo de lista: {type(packages)}")
        print(f"📦 Primer elemento: {packages[0]}")
        print(f"📦 Tipo del primer elemento: {type(packages[0])}")
        
        # Crear un UserWithRoles
        from datetime import datetime
        from uuid import uuid4
        
        user_with_roles = UserWithRoles(
            id=uuid4(),
            email="test@example.com",
            first_name="Test",
            last_name="User",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            roles=["institution_admin"],
            package_subscriptions=packages
        )
        
        print(f"👤 UserWithRoles creado: {user_with_roles}")
        print(f"👤 Tipo: {type(user_with_roles)}")
        print(f"👤 package_subscriptions: {user_with_roles.package_subscriptions}")
        print(f"👤 Tipo de package_subscriptions: {type(user_with_roles.package_subscriptions)}")
        
        if user_with_roles.package_subscriptions:
            first_package = user_with_roles.package_subscriptions[0]
            print(f"👤 Primer paquete: {first_package}")
            print(f"👤 Tipo del primer paquete: {type(first_package)}")
            print(f"👤 package_name del primer paquete: {first_package.package_name}")
        
        # Convertir a dict
        user_dict = user_with_roles.model_dump()
        print(f"👤 Dict completo: {json.dumps(user_dict, indent=2, default=str)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Probando serialización de Pydantic...")
    success = test_pydantic_serialization()
    if success:
        print("\n✅ Prueba completada exitosamente")
    else:
        print("\n❌ Prueba falló")
        sys.exit(1) 