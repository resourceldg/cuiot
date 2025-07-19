#!/usr/bin/env python3
"""
Script para asignar paquetes institucionales a usuarios institution_admin que no los tengan
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
from datetime import datetime, timedelta
from sqlalchemy import and_

def assign_institutional_packages():
    """Asignar paquetes institucionales a usuarios institution_admin sin paquetes"""
    
    db = next(get_db())
    
    try:
        print("🏢 Asignando paquetes institucionales...")
        
        # Obtener el rol institution_admin
        institution_admin_role = db.query(Role).filter(Role.name == "institution_admin").first()
        if not institution_admin_role:
            print("❌ No se encontró el rol institution_admin")
            return False
        
        # Obtener usuarios con rol institution_admin
        user_roles = db.query(UserRole).filter(
            and_(
                UserRole.role_id == institution_admin_role.id,
                UserRole.is_active == True
            )
        ).all()
        
        institution_admin_users = []
        for user_role in user_roles:
            user = db.query(User).filter(User.id == user_role.user_id).first()
            if user:
                institution_admin_users.append(user)
        
        print(f"👥 Encontrados {len(institution_admin_users)} usuarios institution_admin")
        
        # Obtener el paquete institucional por defecto
        institutional_package = db.query(Package).filter(
            Package.package_type == "institutional"
        ).first()
        
        if not institutional_package:
            print("❌ No se encontró ningún paquete institucional")
            return False
        
        print(f"📦 Paquete institucional encontrado: {institutional_package.name}")
        
        # Obtener el status_type_id para "active"
        active_status = db.query(StatusType).filter(StatusType.name == "active").first()
        if not active_status:
            print("❌ No se encontró el status_type 'active'")
            return False
        
        # Verificar qué usuarios institution_admin no tienen paquetes
        users_without_packages = []
        for user in institution_admin_users:
            existing_package = db.query(UserPackage).filter(
                and_(
                    UserPackage.user_id == user.id,
                    UserPackage.status_type_id == active_status.id
                )
            ).first()
            
            if not existing_package:
                users_without_packages.append(user)
                print(f"   ⚠️  {user.email} no tiene paquete")
            else:
                print(f"   ✅ {user.email} ya tiene paquete")
        
        if not users_without_packages:
            print("✅ Todos los usuarios institution_admin ya tienen paquetes")
            return True
        
        print(f"\n📦 Asignando paquetes a {len(users_without_packages)} usuarios...")
        
        # Asignar paquetes
        for user in users_without_packages:
            # Calcular next_billing_date (30 días desde hoy)
            next_billing_date = datetime.now() + timedelta(days=30)
            
            user_package = UserPackage(
                user_id=user.id,
                package_id=institutional_package.id,
                start_date=datetime.now(),
                auto_renew=True,
                billing_cycle="monthly",
                current_amount=institutional_package.price_monthly or 0,
                next_billing_date=next_billing_date,
                status_type_id=active_status.id,
                selected_features={},
                custom_configuration={}
            )
            
            db.add(user_package)
            print(f"   ✅ Asignado paquete a {user.email}")
        
        db.commit()
        print(f"\n✅ Se asignaron paquetes institucionales a {len(users_without_packages)} usuarios")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando asignación de paquetes institucionales...")
    success = assign_institutional_packages()
    if success:
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Proceso falló")
        sys.exit(1) 