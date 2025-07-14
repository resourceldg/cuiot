#!/usr/bin/env python3
"""
Módulo IoT: Gestión de Dispositivos
Consolida la funcionalidad para crear, gestionar y corregir dispositivos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import get_db
from app.models.device import Device
from app.models.device_type import DeviceType
from app.models.package import Package
from app.models.institution import Institution
from app.models.cared_person import CaredPerson
from app.models.user import User
from scripts.utils.data_generators import DataGenerator
from sqlalchemy.orm import Session
import random

class DeviceManager:
    """Gestor de dispositivos IoT"""
    
    @classmethod
    def populate_devices(cls, db: Session = None, devices_per_type: int = 3):
        """Poblar la base de datos con dispositivos de diferentes tipos"""
        if db is None:
            db = next(get_db())
        
        try:
            print("📱 POBLANDO DISPOSITIVOS IoT")
            print("=" * 50)
            
            # Obtener todos los tipos de dispositivos
            device_types = db.query(DeviceType).filter(DeviceType.is_active == True).all()
            print(f"📊 Tipos de dispositivos disponibles: {len(device_types)}")
            
            # Obtener paquetes disponibles
            packages = db.query(Package).filter(Package.is_active == True).all()
            if not packages:
                print("❌ No hay paquetes disponibles")
                return
            
            print(f"📦 Paquetes disponibles: {len(packages)}")
            
            # Obtener instituciones, usuarios y personas cuidadas para asignación
            institutions = db.query(Institution).filter(Institution.is_active == True).all()
            users = db.query(User).filter(User.is_active == True).all()
            cared_persons = db.query(CaredPerson).filter(CaredPerson.is_active == True).all()
            
            print(f"🏢 Instituciones: {len(institutions)}")
            print(f"👥 Usuarios: {len(users)}")
            print(f"👴 Personas cuidadas: {len(cared_persons)}")
            
            # Crear dispositivos por categoría
            devices_created = 0
            devices_by_category = {}
            
            for device_type in device_types:
                print(f"\n🔧 Creando dispositivos tipo: {device_type.name} ({device_type.category})")
                
                # Determinar cuántos dispositivos crear por tipo
                num_devices = random.randint(1, devices_per_type)
                
                category_devices = []
                for i in range(num_devices):
                    # Seleccionar paquete aleatorio
                    package = random.choice(packages)
                    
                    # Determinar propietario según el tipo de paquete
                    owner_type = "institution"  # Por defecto
                    owner_id = None
                    
                    if package.package_type == "family":
                        if users:
                            owner_type = "user"
                            owner_id = random.choice(users).id
                    elif package.package_type == "self_care":
                        if cared_persons:
                            owner_type = "cared_person"
                            owner_id = random.choice(cared_persons).id
                    elif package.package_type == "institution":
                        if institutions:
                            owner_type = "institution"
                            owner_id = random.choice(institutions).id
                    
                    # Generar datos del dispositivo
                    device_data = DataGenerator.generate_device_data(
                        device_type_id=device_type.id,
                        package_id=package.id
                    )
                    
                    # Asignar propietario
                    if owner_type == "institution":
                        device_data["institution_id"] = owner_id
                    elif owner_type == "cared_person":
                        device_data["cared_person_id"] = owner_id
                    elif owner_type == "user":
                        device_data["user_id"] = owner_id
                    
                    # Verificar si ya existe
                    existing_device = db.query(Device).filter(
                        Device.name == device_data["name"],
                        Device.package_id == package.id
                    ).first()
                    
                    if existing_device:
                        print(f"   ⚠️  {device_data['name']} ya existe")
                        continue
                    
                    # Crear dispositivo
                    device = Device(**device_data)
                    db.add(device)
                    db.flush()  # Para obtener el ID
                    
                    print(f"   ✅ {device.name} → {package.name} ({owner_type})")
                    category_devices.append(device)
                    devices_created += 1
                
                devices_by_category[device_type.category] = devices_by_category.get(device_type.category, 0) + len(category_devices)
            
            db.commit()
            print(f"\n✅ Se crearon {devices_created} nuevos dispositivos")
            
            # Mostrar resumen por categoría
            print("\n📋 DISPOSITIVOS POR CATEGORÍA:")
            for category, count in devices_by_category.items():
                print(f"   - {category}: {count} dispositivos")
            
            # Mostrar total de dispositivos
            total_devices = db.query(Device).count()
            print(f"\n📊 Total de dispositivos en la base de datos: {total_devices}")
            
            return devices_created
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.rollback()
            raise
        finally:
            if db is not None:
                db.close()
    
    @classmethod
    def fix_devices_without_package(cls, db: Session = None):
        """Corregir dispositivos sin package_id y luego eliminarlos"""
        if db is None:
            db = next(get_db())
        
        try:
            print("🔧 CORRIGIENDO DISPOSITIVOS SIN PACKAGE_ID")
            print("=" * 50)
            
            # Buscar dispositivos sin package_id
            devices_without_package = db.query(Device).filter(Device.package_id == None).all()
            
            if not devices_without_package:
                print("✅ No hay dispositivos sin package_id")
                return 0
            
            print(f"📊 Dispositivos sin package_id encontrados: {len(devices_without_package)}")
            
            # Mostrar dispositivos que serán eliminados
            print("\n🗑️  DISPOSITIVOS A ELIMINAR:")
            for device in devices_without_package:
                print(f"   - {device.name} (ID: {device.id})")
            
            # Eliminar dispositivos sin package_id
            for device in devices_without_package:
                db.delete(device)
            
            db.commit()
            print(f"\n✅ Se eliminaron {len(devices_without_package)} dispositivos sin package_id")
            
            # Verificar que no queden dispositivos sin package_id
            remaining = db.query(Device).filter(Device.package_id == None).count()
            print(f"📊 Dispositivos sin package_id restantes: {remaining}")
            
            if remaining == 0:
                print("✅ Todos los dispositivos ahora tienen package_id asignado")
            
            return len(devices_without_package)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.rollback()
            raise
        finally:
            if db is not None:
                db.close()
    
    @classmethod
    def get_devices_summary(cls, db: Session = None):
        """Obtener resumen de dispositivos por categoría"""
        if db is None:
            db = next(get_db())
        
        try:
            # Obtener dispositivos con sus tipos
            devices = db.query(Device).join(DeviceType).filter(Device.is_active == True).all()
            
            summary = {}
            for device in devices:
                category = device.device_type.category
                if category not in summary:
                    summary[category] = []
                summary[category].append(device)
            
            return summary
            
        finally:
            if db is not None:
                db.close()

def main():
    """Función principal para ejecutar desde línea de comandos"""
    print("🔧 GESTOR DE DISPOSITIVOS IoT")
    print("=" * 40)
    print("1. Corregir dispositivos sin package_id")
    print("2. Poblar dispositivos")
    print("3. Mostrar resumen")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == "1":
        DeviceManager.fix_devices_without_package()
    elif choice == "2":
        devices_per_type = int(input("Dispositivos por tipo (1-5): ") or "3")
        DeviceManager.populate_devices(devices_per_type=devices_per_type)
    elif choice == "3":
        summary = DeviceManager.get_devices_summary()
        print("\n📊 RESUMEN DE DISPOSITIVOS:")
        for category, devices in summary.items():
            print(f"   - {category}: {len(devices)} dispositivos")
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    main() 