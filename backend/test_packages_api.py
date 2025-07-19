#!/usr/bin/env python3
"""
Script para probar que los paquetes se estén mostrando correctamente en la API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.services.user import UserService
from sqlalchemy import text

def test_packages_display():
    """Probar que los paquetes se muestren correctamente"""
    
    db = next(get_db())
    
    try:
        print("🧪 Probando visualización de paquetes...")
        
        # Obtener usuarios con roles y paquetes
        users = UserService.get_users_with_roles(db, limit=10)
        
        print(f"\n📊 Total de usuarios obtenidos: {len(users)}")
        
        # Analizar usuarios por tipo de rol
        users_with_packages = 0
        users_without_packages = 0
        users_caregiver = 0
        users_family_member = 0
        users_institution_admin = 0
        
        for user in users:
            print(f"\n👤 Usuario: {user.email}")
            print(f"   Roles: {user.roles}")
            print(f"   Paquetes: {len(user.package_subscriptions)}")
            
            if user.package_subscriptions:
                users_with_packages += 1
                for package in user.package_subscriptions:
                    print(f"   📦 {package.package_name} (ID: {package.package_id})")
            else:
                users_without_packages += 1
                print(f"   ❌ Sin paquetes")
            
            # Contar por rol
            if 'caregiver' in user.roles:
                users_caregiver += 1
            if 'family_member' in user.roles:
                users_family_member += 1
            if 'institution_admin' in user.roles:
                users_institution_admin += 1
        
        print(f"\n📈 RESUMEN:")
        print(f"   Usuarios con paquetes: {users_with_packages}")
        print(f"   Usuarios sin paquetes: {users_without_packages}")
        print(f"   Usuarios caregiver: {users_caregiver}")
        print(f"   Usuarios family_member: {users_family_member}")
        print(f"   Usuarios institution_admin: {users_institution_admin}")
        
        # Verificar lógica de negocio
        print(f"\n✅ VERIFICACIÓN DE LÓGICA:")
        
        # Verificar que usuarios family_member tengan paquetes
        family_members_without_packages = 0
        for user in users:
            if 'family_member' in user.roles and not user.package_subscriptions:
                family_members_without_packages += 1
                print(f"   ⚠️  {user.email} tiene rol family_member pero no tiene paquetes")
        
        if family_members_without_packages == 0:
            print(f"   ✅ Todos los usuarios family_member tienen paquetes")
        else:
            print(f"   ❌ {family_members_without_packages} usuarios family_member sin paquetes")
        
        # Verificar que usuarios caregiver NO tengan paquetes
        caregivers_with_packages = 0
        for user in users:
            if 'caregiver' in user.roles and user.package_subscriptions:
                caregivers_with_packages += 1
                print(f"   ⚠️  {user.email} tiene rol caregiver pero tiene paquetes")
        
        if caregivers_with_packages == 0:
            print(f"   ✅ Ningún usuario caregiver tiene paquetes")
        else:
            print(f"   ❌ {caregivers_with_packages} usuarios caregiver con paquetes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando prueba de visualización de paquetes...")
    success = test_packages_display()
    if success:
        print("\n✅ Prueba completada exitosamente")
    else:
        print("\n❌ Prueba falló")
        sys.exit(1) 