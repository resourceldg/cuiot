import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import random
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.models.package import PackageAddOn, UserPackage, UserPackageAddOn
from app.models.user import User
from app.models.package import Package
from app.models.status_type import StatusType

# Sample Package Add-ons
SAMPLE_ADD_ONS = [
    # Storage add-ons
    {
        "name": "Almacenamiento Extra 50GB",
        "description": "50GB adicionales de almacenamiento para reportes y datos",
        "add_on_type": "storage",
        "price_monthly": 2000,  # 20 ARS
        "price_yearly": 20000,  # 200 ARS
        "configuration": {"storage_gb": 50},
        "limitations": {"max_quantity": 5},
        "compatible_packages": ["individual", "professional", "institutional"],
        "max_quantity": 5,
        "is_active": True
    },
    {
        "name": "Almacenamiento Extra 100GB",
        "description": "100GB adicionales de almacenamiento para reportes y datos",
        "add_on_type": "storage",
        "price_monthly": 3500,  # 35 ARS
        "price_yearly": 35000,  # 350 ARS
        "configuration": {"storage_gb": 100},
        "limitations": {"max_quantity": 3},
        "compatible_packages": ["professional", "institutional"],
        "max_quantity": 3,
        "is_active": True
    },
    # Users add-ons
    {
        "name": "Usuarios Adicionales (5)",
        "description": "5 usuarios adicionales para el paquete",
        "add_on_type": "users",
        "price_monthly": 3000,  # 30 ARS
        "price_yearly": 30000,  # 300 ARS
        "configuration": {"users_count": 5},
        "limitations": {"max_quantity": 10},
        "compatible_packages": ["professional", "institutional"],
        "max_quantity": 10,
        "is_active": True
    },
    {
        "name": "Usuarios Adicionales (10)",
        "description": "10 usuarios adicionales para el paquete",
        "add_on_type": "users",
        "price_monthly": 5000,  # 50 ARS
        "price_yearly": 50000,  # 500 ARS
        "configuration": {"users_count": 10},
        "limitations": {"max_quantity": 5},
        "compatible_packages": ["institutional"],
        "max_quantity": 5,
        "is_active": True
    },
    # Devices add-ons
    {
        "name": "Dispositivos Adicionales (10)",
        "description": "10 dispositivos adicionales para monitoreo",
        "add_on_type": "devices",
        "price_monthly": 4000,  # 40 ARS
        "price_yearly": 40000,  # 400 ARS
        "configuration": {"devices_count": 10},
        "limitations": {"max_quantity": 5},
        "compatible_packages": ["professional", "institutional"],
        "max_quantity": 5,
        "is_active": True
    },
    # Features add-ons
    {
        "name": "Analytics Avanzado",
        "description": "Análisis avanzado con machine learning y predicciones",
        "add_on_type": "features",
        "price_monthly": 8000,  # 80 ARS
        "price_yearly": 80000,  # 800 ARS
        "configuration": {"features": ["ml_analytics", "predictions", "trends"]},
        "limitations": {"requires_premium": True},
        "compatible_packages": ["professional", "institutional"],
        "max_quantity": 1,
        "is_active": True
    },
    {
        "name": "Integraciones Avanzadas",
        "description": "Integración con sistemas externos y APIs",
        "add_on_type": "features",
        "price_monthly": 6000,  # 60 ARS
        "price_yearly": 60000,  # 600 ARS
        "configuration": {"integrations": ["api_access", "webhooks", "third_party"]},
        "limitations": {"max_quantity": 3},
        "compatible_packages": ["professional", "institutional"],
        "max_quantity": 3,
        "is_active": True
    },
    # Support add-ons
    {
        "name": "Soporte Prioritario",
        "description": "Soporte técnico prioritario con respuesta en 4 horas",
        "add_on_type": "support",
        "price_monthly": 5000,  # 50 ARS
        "price_yearly": 50000,  # 500 ARS
        "configuration": {"response_time": "4h", "priority": True},
        "limitations": {"max_quantity": 1},
        "compatible_packages": ["individual", "professional", "institutional"],
        "max_quantity": 1,
        "is_active": True
    },
    {
        "name": "Soporte Dedicado",
        "description": "Soporte técnico dedicado con ingeniero asignado",
        "add_on_type": "support",
        "price_monthly": 15000,  # 150 ARS
        "price_yearly": 150000,  # 1500 ARS
        "configuration": {"dedicated_engineer": True, "response_time": "2h"},
        "limitations": {"max_quantity": 1},
        "compatible_packages": ["institutional"],
        "max_quantity": 1,
        "is_active": True
    },
    # Analytics add-ons
    {
        "name": "Analytics Básico",
        "description": "Análisis básico de datos y reportes",
        "add_on_type": "analytics",
        "price_monthly": 3000,  # 30 ARS
        "price_yearly": 30000,  # 300 ARS
        "configuration": {"analytics_level": "basic", "reports": True},
        "limitations": {"max_quantity": 1},
        "compatible_packages": ["individual", "professional", "institutional"],
        "max_quantity": 1,
        "is_active": True
    },
    # Integration add-ons
    {
        "name": "Integración API",
        "description": "Acceso completo a APIs para integración con sistemas externos",
        "add_on_type": "integration",
        "price_monthly": 7000,  # 70 ARS
        "price_yearly": 70000,  # 700 ARS
        "configuration": {"api_access": True, "webhooks": True},
        "limitations": {"max_quantity": 1},
        "compatible_packages": ["professional", "institutional"],
        "max_quantity": 1,
        "is_active": True
    }
]

def populate_package_add_ons():
    """Poblar add-ons disponibles para paquetes"""
    db = next(get_db())
    created = 0
    
    for data in SAMPLE_ADD_ONS:
        addon = db.query(PackageAddOn).filter_by(name=data["name"]).first()
        if not addon:
            addon = PackageAddOn(**data)
            db.add(addon)
            created += 1
    
    db.commit()
    print(f"✅ Package Add-ons creados: {created} (idempotente)")
    db.close()

def populate_user_packages():
    """Poblar suscripciones de usuario a paquetes personales (solo roles permitidos)"""
    db = next(get_db())
    created = 0
    # Obtener usuarios y paquetes existentes
    users = db.query(User).filter(User.is_active == True).all()
    # Solo paquetes personales
    packages = db.query(Package).filter(Package.is_active == True, Package.package_type == 'individual').all()
    status_types = db.query(StatusType).filter(StatusType.category == "subscription").all()
    if not users:
        print("⚠️  No hay usuarios disponibles. Ejecuta populate_users primero.")
        db.close()
        return
    if not packages:
        print("⚠️  No hay paquetes personales disponibles. Ejecuta populate_packages primero.")
        db.close()
        return
    if not status_types:
        print("⚠️  No hay status types de suscripción. Ejecuta populate_core primero.")
        db.close()
        return
    # Mapear status types
    status_map = {st.name: st.id for st in status_types}
    active_status_id = status_map.get("active", status_types[0].id)
    # Roles permitidos para paquetes personales
    allowed_roles = {"cared_person_self", "family", "family_member"}
    for user in users:
        # Obtener roles activos del usuario
        user_roles = [r.name for r in user.roles if getattr(r, 'is_active', True)]
        if not set(user_roles) & allowed_roles:
            continue
        # Asignar 1-2 paquetes personales por usuario
        num_packages = random.randint(1, min(2, len(packages)))
        selected_packages = random.sample(packages, num_packages)
        for package in selected_packages:
            existing = db.query(UserPackage).filter_by(user_id=user.id, package_id=package.id).first()
            if existing:
                continue
            start_date = date.today() - timedelta(days=random.randint(0, 365))
            billing_cycle = random.choice(["monthly", "yearly"])
            if billing_cycle == "monthly":
                current_amount = package.price_monthly
                next_billing = start_date + timedelta(days=30)
            else:
                current_amount = (package.price_yearly or package.price_monthly * 12)
                next_billing = start_date + timedelta(days=365)
            # Asegurar que features es una lista
            features = list(package.features) if package.features else []
            user_package = UserPackage(
                user_id=user.id,
                package_id=package.id,
                start_date=start_date,
                end_date=None,
                auto_renew=True,
                billing_cycle=billing_cycle,
                current_amount=current_amount,
                next_billing_date=next_billing,
                status_type_id=active_status_id,
                custom_configuration={
                    "selected_features": random.sample(features, min(3, len(features)))
                },
                selected_features=random.sample(features, min(3, len(features))),
                legal_capacity_verified=random.choice([True, False]),
                referral_code_used=None
            )
            db.add(user_package)
            created += 1
    db.commit()
    print(f"✅ User Packages personales creados: {created} (solo roles permitidos)")
    db.close()

def populate_user_package_add_ons():
    """Poblar add-ons asignados a suscripciones de usuario"""
    db = next(get_db())
    created = 0
    
    # Obtener datos necesarios
    user_packages = db.query(UserPackage).all()
    add_ons = db.query(PackageAddOn).filter(PackageAddOn.is_active == True).all()
    status_types = db.query(StatusType).filter(StatusType.category == "subscription").all()
    
    if not user_packages:
        print("⚠️  No hay user packages disponibles. Ejecuta populate_user_packages primero.")
        db.close()
        return
    
    if not add_ons:
        print("⚠️  No hay add-ons disponibles. Ejecuta populate_package_add_ons primero.")
        db.close()
        return
    
    if not status_types:
        print("⚠️  No hay status types de suscripción. Ejecuta populate_core primero.")
        db.close()
        return
    
    # Mapear status types
    status_map = {st.name: st.id for st in status_types}
    active_status_id = status_map.get("active", status_types[0].id)
    
    # Asignar add-ons a suscripciones
    for user_package in user_packages:
        # Verificar compatibilidad del paquete con add-ons
        package = user_package.package
        compatible_add_ons = []
        
        for addon in add_ons:
            if (addon.compatible_packages and 
                package.package_type in addon.compatible_packages):
                compatible_add_ons.append(addon)
        
        if not compatible_add_ons:
            continue
        
        # Asignar 0-3 add-ons por suscripción
        num_addons = random.randint(0, min(3, len(compatible_add_ons)))
        selected_addons = random.sample(compatible_add_ons, num_addons)
        
        for addon in selected_addons:
            # Verificar si ya existe la asignación
            existing = db.query(UserPackageAddOn).filter_by(
                user_package_id=user_package.id,
                add_on_id=addon.id
            ).first()
            
            if existing:
                continue
            
            # Generar cantidad y configuración
            quantity = random.randint(1, min(3, addon.max_quantity or 3))
            billing_cycle = random.choice(["monthly", "yearly"])
            
            # Calcular precio según ciclo de facturación
            if billing_cycle == "monthly":
                current_amount = addon.price_monthly * quantity
            else:
                current_amount = (addon.price_yearly or addon.price_monthly * 12) * quantity
            
            # Crear asignación de add-on
            user_addon = UserPackageAddOn(
                user_package_id=user_package.id,
                add_on_id=addon.id,
                quantity=quantity,
                custom_configuration={
                    "quantity": quantity,
                    "billing_cycle": billing_cycle
                },
                current_amount=current_amount,
                billing_cycle=billing_cycle,
                status_type_id=active_status_id,
                added_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            
            db.add(user_addon)
            created += 1
    
    db.commit()
    print(f"✅ User Package Add-ons creados: {created} (idempotente)")
    db.close()

def populate_addons_complete():
    """Poblar todo el sistema de add-ons y suscripciones"""
    print("🚀 Iniciando población de add-ons y suscripciones...")
    
    print("\n1️⃣  Poblando Package Add-ons...")
    populate_package_add_ons()
    
    print("\n2️⃣  Poblando User Packages...")
    populate_user_packages()
    
    print("\n3️⃣  Poblando User Package Add-ons...")
    populate_user_package_add_ons()
    
    print("\n✅ Población de add-ons y suscripciones completada!")

if __name__ == "__main__":
    populate_addons_complete() 