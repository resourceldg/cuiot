#!/usr/bin/env python3
"""
Script para asignar paquetes a usuarios con rol cared_person_self que no los tengan
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

def assign_cared_person_packages():
    """Asignar paquetes a usuarios cared_person_self sin paquetes"""
    
    db = next(get_db())
    
    try:
        print("👴 Asignando paquetes a usuarios cared_person_self...")
        
        # Obtener el rol cared_person_self
        cared_person_role = db.query(Role).filter(Role.name == "cared_person_self").first()
        if not cared_person_role:
            print("❌ No se encontró el rol cared_person_self")
            return False
        
        # Obtener usuarios con rol cared_person_self
        user_roles = db.query(UserRole).filter(
            and_(
                UserRole.role_id == cared_person_role.id,
                UserRole.is_active == True
            )
        ).all()
        
        cared_person_users = []
        for user_role in user_roles:
            user = db.query(User).filter(User.id == user_role.user_id).first()
            if user:
                cared_person_users.append(user)
        
        print(f"👥 Encontrados {len(cared_person_users)} usuarios cared_person_self")
        
        # Obtener el paquete individual por defecto
        individual_package = db.query(Package).filter(
            Package.package_type == "individual"
        ).first()
        
        if not individual_package:
            print("❌ No se encontró ningún paquete individual")
            return False
        
        print(f"📦 Paquete individual encontrado: {individual_package.name}")
        
        # Obtener el status_type_id para "active"
        active_status = db.query(StatusType).filter(StatusType.name == "active").first()
        if not active_status:
            print("❌ No se encontró el status_type 'active'")
            return False
        
        # Verificar qué usuarios cared_person_self no tienen paquetes
        users_without_packages = []
        for user in cared_person_users:
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
            print("✅ Todos los usuarios cared_person_self ya tienen paquetes")
            return True
        
        print(f"\n📦 Asignando paquetes a {len(users_without_packages)} usuarios...")
        
        # Asignar paquetes
        for user in users_without_packages:
            # Calcular next_billing_date (30 días desde hoy)
            next_billing_date = datetime.now() + timedelta(days=30)
            
            user_package = UserPackage(
                user_id=user.id,
                package_id=individual_package.id,
                start_date=datetime.now(),
                auto_renew=True,
                billing_cycle="monthly",
                current_amount=individual_package.price_monthly or 0,
                next_billing_date=next_billing_date,
                status_type_id=active_status.id,
                selected_features={},
                custom_configuration={}
            )
            
            db.add(user_package)
            print(f"   ✅ Asignado paquete a {user.email}")
        
        db.commit()
        print(f"\n✅ Se asignaron paquetes individuales a {len(users_without_packages)} usuarios")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando asignación de paquetes para cared_person_self...")
    success = assign_cared_person_packages()
    if success:
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Proceso falló")
        sys.exit(1) 