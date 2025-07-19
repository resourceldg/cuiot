#!/usr/bin/env python3
"""
Script para verificar y corregir la lógica de roles y paquetes
"""

import os
import sys
sys.path.append('/app')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.package import Package
from app.models.user_package_subscription import UserPackageSubscription
from app.core.config import settings

# Crear conexión a la base de datos
engine = create_engine(settings.get_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_roles_packages_logic():
    """Verificar la lógica de roles y paquetes"""
    db = SessionLocal()
    try:
        print("🔍 VERIFICANDO LÓGICA DE ROLES Y PAQUETES")
        print("=" * 60)
        
        # 1. Verificar usuarios con roles que pueden tener paquetes
        print("\n📋 USUARIOS CON ROLES QUE PUEDEN TENER PAQUETES:")
        
        # Roles que pueden tener paquetes individuales
        individual_package_roles = ['cared_person_self', 'caredperson', 'family', 'family_member']
        # Roles que pueden tener paquetes institucionales
        institutional_package_roles = ['institution_admin']
        
        # Consultar usuarios con roles de paquetes individuales
        query_individual = text("""
            SELECT 
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                r.name as role_name,
                COUNT(ups.id) as package_count
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            JOIN roles r ON ur.role_id = r.id AND r.is_active = true
            LEFT JOIN user_package_subscriptions ups ON u.id = ups.user_id AND ups.is_active = true
            WHERE r.name IN ('cared_person_self', 'caredperson', 'family', 'family_member')
            AND u.is_active = true
            GROUP BY u.id, u.email, u.first_name, u.last_name, r.name
            ORDER BY r.name, u.email
        """)
        
        result_individual = db.execute(query_individual)
        users_individual = result_individual.fetchall()
        
        print(f"\n👥 USUARIOS CON ROLES DE PAQUETES INDIVIDUALES:")
        role_counts = {}
        users_without_packages = []
        
        for user in users_individual:
            role_name = user.role_name
            package_count = user.package_count
            role_counts[role_name] = role_counts.get(role_name, 0) + 1
            
            if package_count == 0:
                users_without_packages.append(user)
                print(f"   ⚠️  {user.email} ({user.first_name} {user.last_name or ''}) - Rol: {role_name} - Paquetes: {package_count}")
            else:
                print(f"   ✅ {user.email} ({user.first_name} {user.last_name or ''}) - Rol: {role_name} - Paquetes: {package_count}")
        
        print(f"\n📊 ESTADÍSTICAS DE ROLES INDIVIDUALES:")
        for role_name, count in role_counts.items():
            print(f"   - {role_name}: {count} usuarios")
        
        print(f"\n⚠️  USUARIOS SIN PAQUETES: {len(users_without_packages)}")
        
        # 2. Verificar usuarios con roles institucionales
        query_institutional = text("""
            SELECT 
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                r.name as role_name,
                COUNT(ups.id) as package_count
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            JOIN roles r ON ur.role_id = r.id AND r.is_active = true
            LEFT JOIN user_package_subscriptions ups ON u.id = ups.user_id AND ups.is_active = true
            WHERE r.name IN ('institution_admin')
            AND u.is_active = true
            GROUP BY u.id, u.email, u.first_name, u.last_name, r.name
            ORDER BY r.name, u.email
        """)
        
        result_institutional = db.execute(query_institutional)
        users_institutional = result_institutional.fetchall()
        
        print(f"\n🏥 USUARIOS CON ROLES INSTITUCIONALES:")
        for user in users_institutional:
            role_name = user.role_name
            package_count = user.package_count
            if package_count == 0:
                print(f"   ⚠️  {user.email} ({user.first_name} {user.last_name or ''}) - Rol: {role_name} - Paquetes: {package_count}")
            else:
                print(f"   ✅ {user.email} ({user.first_name} {user.last_name or ''}) - Rol: {role_name} - Paquetes: {package_count}")
        
        # 3. Verificar paquetes disponibles
        print(f"\n📦 PAQUETES DISPONIBLES:")
        packages = db.query(Package).filter(Package.is_active == True).all()
        individual_packages = [p for p in packages if p.package_type == 'individual']
        institutional_packages = [p for p in packages if p.package_type == 'institutional']
        
        print(f"   - Paquetes individuales: {len(individual_packages)}")
        for pkg in individual_packages:
            print(f"     * {pkg.name} (ID: {pkg.id})")
        
        print(f"   - Paquetes institucionales: {len(institutional_packages)}")
        for pkg in institutional_packages:
            print(f"     * {pkg.name} (ID: {pkg.id})")
        
        return users_without_packages, individual_packages
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        raise
    finally:
        db.close()

def fix_users_without_packages(users_without_packages, individual_packages):
    """Asignar paquetes a usuarios que pueden tenerlos pero no los tienen"""
    if not users_without_packages or not individual_packages:
        print("✅ No hay usuarios sin paquetes que corregir o no hay paquetes disponibles")
        return
    
    db = SessionLocal()
    try:
        print(f"\n🔧 ASIGNANDO PAQUETES A USUARIOS")
        print("=" * 60)
        
        # Usar el primer paquete individual disponible como default
        default_package = individual_packages[0]
        print(f"📦 Paquete por defecto: {default_package.name}")
        
        fixed_count = 0
        for user in users_without_packages:
            # Verificar si ya existe una suscripción inactiva
            existing_subscription = db.query(UserPackageSubscription).filter(
                UserPackageSubscription.user_id == user.id,
                UserPackageSubscription.package_id == default_package.id
            ).first()
            
            if existing_subscription:
                # Reactivar suscripción existente
                existing_subscription.is_active = True
                print(f"   ✅ Reactivado paquete para: {user.email}")
            else:
                # Crear nueva suscripción
                new_subscription = UserPackageSubscription(
                    user_id=user.id,
                    package_id=default_package.id,
                    is_active=True,
                    subscription_date=db.query(text("NOW()")).scalar()
                )
                db.add(new_subscription)
                print(f"   ✅ Creado nuevo paquete para: {user.email}")
            
            fixed_count += 1
        
        db.commit()
        print(f"\n🎉 CORRECCIÓN COMPLETADA")
        print(f"   - Usuarios corregidos: {fixed_count}")
        print(f"   - Paquete asignado: {default_package.name}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la corrección: {e}")
        raise
    finally:
        db.close()

def verify_final_state():
    """Verificar el estado final después de las correcciones"""
    db = SessionLocal()
    try:
        print(f"\n🔍 VERIFICACIÓN FINAL")
        print("=" * 60)
        
        # Contar usuarios con roles de paquetes individuales
        query = text("""
            SELECT 
                r.name as role_name,
                COUNT(u.id) as user_count,
                COUNT(ups.id) as package_count
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            JOIN roles r ON ur.role_id = r.id AND r.is_active = true
            LEFT JOIN user_package_subscriptions ups ON u.id = ups.user_id AND ups.is_active = true
            WHERE r.name IN ('cared_person_self', 'caredperson', 'family', 'family_member')
            AND u.is_active = true
            GROUP BY r.name
            ORDER BY r.name
        """)
        
        result = db.execute(query)
        role_stats = result.fetchall()
        
        print(f"📊 ESTADO FINAL DE ROLES Y PAQUETES:")
        for stat in role_stats:
            role_name = stat.role_name
            user_count = stat.user_count
            package_count = stat.package_count
            coverage = (package_count / user_count * 100) if user_count > 0 else 0
            print(f"   - {role_name}: {user_count} usuarios, {package_count} paquetes ({coverage:.1f}% cobertura)")
        
        # Verificar usuarios sin paquetes restantes
        query_no_packages = text("""
            SELECT COUNT(*) as count
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
            JOIN roles r ON ur.role_id = r.id AND r.is_active = true
            LEFT JOIN user_package_subscriptions ups ON u.id = ups.user_id AND ups.is_active = true
            WHERE r.name IN ('cared_person_self', 'caredperson', 'family', 'family_member')
            AND u.is_active = true
            GROUP BY u.id
            HAVING COUNT(ups.id) = 0
        """)
        
        result_no_packages = db.execute(query_no_packages)
        users_still_without_packages = len(result_no_packages.fetchall())
        
        if users_still_without_packages == 0:
            print(f"\n✅ TODOS LOS USUARIOS CON ROLES APROPIADOS TIENEN PAQUETES")
        else:
            print(f"\n⚠️  Aún quedan {users_still_without_packages} usuarios sin paquetes")
        
    except Exception as e:
        print(f"❌ Error en verificación final: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 VERIFICANDO LÓGICA DE ROLES Y PAQUETES")
    print("=" * 60)
    
    # Verificar estado actual
    users_without_packages, individual_packages = verify_roles_packages_logic()
    
    # Preguntar si corregir
    if users_without_packages:
        print(f"\n❓ ¿Deseas asignar paquetes a {len(users_without_packages)} usuarios? (s/n): ", end="")
        response = input().strip().lower()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            fix_users_without_packages(users_without_packages, individual_packages)
            verify_final_state()
        else:
            print("❌ Corrección cancelada por el usuario")
    else:
        print("✅ No hay usuarios sin paquetes que corregir")
    
    print("\n🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 60) 