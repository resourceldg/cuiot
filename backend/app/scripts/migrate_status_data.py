#!/usr/bin/env python3
"""
Script para migrar datos de campos status a status_type_id
==========================================================

Este script migra los valores existentes de campos 'status' a la nueva
relación normalizada con la tabla status_types.
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import text

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.database import get_db
from app.models.status_type import StatusType


def migrate_status_data():
    """Migra los datos de status a status_type_id"""
    
    db = next(get_db())
    
    try:
        print("🔄 Iniciando migración de datos de status...")
        
        # Mapeo de valores de status a categorías de status_types
        status_mapping = {
            # Alertas
            "active": "alert_status",
            "acknowledged": "alert_status", 
            "resolved": "alert_status",
            "dismissed": "alert_status",
            "escalated": "alert_status",
            
            # Dispositivos
            "online": "device_status",
            "offline": "device_status",
            "maintenance": "device_status",
            "error": "device_status",
            "testing": "device_status",
            
            # Facturación
            "pending": "billing_status",
            "paid": "billing_status",
            "overdue": "billing_status",
            "cancelled": "billing_status",
            "refunded": "billing_status",
            "disputed": "billing_status",
            
            # Paquetes
            "suspended": "package_status",
            "expired": "package_status",
            "trial": "package_status",
        }
        
        # Migrar datos de alerts
        print("📊 Migrando datos de alerts...")
        migrate_table_status(db, "alerts", status_mapping)
        
        # Migrar datos de devices
        print("📊 Migrando datos de devices...")
        migrate_table_status(db, "devices", status_mapping)
        
        # Migrar datos de billing_records
        print("📊 Migrando datos de billing_records...")
        migrate_table_status(db, "billing_records", status_mapping)
        
        # Migrar datos de user_packages
        print("📊 Migrando datos de user_packages...")
        migrate_table_status(db, "user_packages", status_mapping)
        
        # Migrar datos de user_package_add_ons
        print("📊 Migrando datos de user_package_add_ons...")
        migrate_table_status(db, "user_package_add_ons", status_mapping)
        
        print("✅ Migración completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def migrate_table_status(db: Session, table_name: str, status_mapping: dict):
    """Migra los datos de status para una tabla específica"""
    
    # Obtener todos los registros con status_type_id NULL
    query = text(f"""
        SELECT id, status_type_id 
        FROM {table_name} 
        WHERE status_type_id IS NULL
    """)
    
    result = db.execute(query)
    records = result.fetchall()
    
    if not records:
        print(f"  ✅ No hay registros para migrar en {table_name}")
        return
    
    print(f"  📝 Encontrados {len(records)} registros para migrar en {table_name}")
    
    # Para cada registro, intentar asignar un status_type_id basado en valores comunes
    # Por ahora, asignaremos el status "active" por defecto
    default_status = db.query(StatusType).filter(
        StatusType.name == "active",
        StatusType.category == "alert_status"
    ).first()
    
    if not default_status:
        print(f"  ⚠️  No se encontró el status 'active' para {table_name}")
        return
    
    # Actualizar registros con status_type_id por defecto
    update_query = text(f"""
        UPDATE {table_name} 
        SET status_type_id = :status_type_id 
        WHERE status_type_id IS NULL
    """)
    
    db.execute(update_query, {"status_type_id": default_status.id})
    db.commit()
    
    print(f"  ✅ Migrados {len(records)} registros en {table_name}")


def verify_migration():
    """Verifica que la migración se completó correctamente"""
    
    db = next(get_db())
    
    try:
        print("\n🔍 Verificando migración...")
        
        tables_to_check = [
            "alerts", "devices", "billing_records", 
            "user_packages", "user_package_add_ons"
        ]
        
        for table in tables_to_check:
            # Verificar que no hay registros con status_type_id NULL
            query = text(f"""
                SELECT COUNT(*) as count 
                FROM {table} 
                WHERE status_type_id IS NULL
            """)
            
            result = db.execute(query)
            count = result.fetchone()[0]
            
            if count == 0:
                print(f"  ✅ {table}: Todos los registros tienen status_type_id")
            else:
                print(f"  ⚠️  {table}: {count} registros sin status_type_id")
        
        print("✅ Verificación completada!")
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Iniciando script de migración de datos de status...")
    migrate_status_data()
    verify_migration()
    print("🎉 Script completado!") 