#!/usr/bin/env python3
"""
Script para verificar usuarios específicos que aparecen en las imágenes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.user import User
from app.models.package import Package, UserPackage
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.status_type import StatusType
from sqlalchemy import and_

def check_specific_users():
    """Verificar usuarios específicos que aparecen en las imágenes"""
    
    db = next(get_db())
    
    try:
        print("🔍 Verificando usuarios específicos...")
        
        # Usuarios específicos de las imágenes
        specific_emails = [
            "admin.clinica@cuiot.com",
            "carmen.reyes.20250715141707336212@cuiot.com", 
            "paciente2@cuiot.com"
        ]
        
        for email in specific_emails:
            print(f"\n👤 Verificando: {email}")
            
            # Buscar usuario
            user = db.query(User).filter(User.email == email).first()
            if not user:
                print(f"   ❌ Usuario no encontrado")
                continue
            
            print(f"   ✅ Usuario encontrado: {user.first_name} {user.last_name}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔄 Activo: {user.is_active}")
            
            # Verificar roles
            user_roles = db.query(UserRole).filter(
                and_(
                    UserRole.user_id == user.id,
                    UserRole.is_active == True
                )
            ).all()
            
            roles = []
            for user_role in user_roles:
                role = db.query(Role).filter(Role.id == user_role.role_id).first()
                if role:
                    roles.append(role.name)
            
            print(f"   🏷️  Roles: {roles}")
            
            # Verificar paquetes
            active_status = db.query(StatusType).filter(StatusType.name == "active").first()
            if active_status:
                user_packages = db.query(UserPackage).filter(
                    and_(
                        UserPackage.user_id == user.id,
                        UserPackage.status_type_id == active_status.id
                    )
                ).all()
                
                if user_packages:
                    print(f"   📦 Paquetes encontrados: {len(user_packages)}")
                    for i, user_package in enumerate(user_packages):
                        package = db.query(Package).filter(Package.id == user_package.package_id).first()
                        if package:
                            print(f"      {i+1}. {package.name} (ID: {package.id})")
                            print(f"         Tipo: {package.package_type}")
                            print(f"         Status: {user_package.status_type_id}")
                else:
                    print(f"   ❌ Sin paquetes")
                    
                    # Verificar si debería tener paquetes
                    should_have_packages = any(role in ["family_member", "institution_admin", "cared_person_self"] for role in roles)
                    if should_have_packages:
                        print(f"   ⚠️  DEBERÍA tener paquetes según sus roles")
                    else:
                        print(f"   ✅ No requiere paquetes según sus roles")
            else:
                print(f"   ❌ No se pudo obtener status_type 'active'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Verificando usuarios específicos...")
    success = check_specific_users()
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Verificación falló")
        sys.exit(1) 