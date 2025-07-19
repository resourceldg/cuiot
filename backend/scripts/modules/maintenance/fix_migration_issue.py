#!/usr/bin/env python3
"""
Script para verificar y corregir el problema de migración con la tabla devices
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import ProgrammingError

def check_database_state():
    """Verificar el estado actual de la base de datos"""
    database_url = os.getenv("DATABASE_URL", "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db")
    engine = create_engine(database_url)
    
    print("🔍 Verificando estado de la base de datos...")
    
    with engine.connect() as conn:
        # Verificar si la tabla devices existe
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'devices'
            );
        """))
        devices_exists = result.scalar()
        print(f"📋 Tabla 'devices' existe: {devices_exists}")
        
        if devices_exists:
            # Verificar columnas de la tabla devices
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'devices' 
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            print(f"📋 Columnas en tabla 'devices':")
            for col in columns:
                print(f"   - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
            
            # Verificar si package_id existe
            package_id_exists = any(col[0] == 'package_id' for col in columns)
            print(f"📋 Columna 'package_id' existe: {package_id_exists}")
            
            if package_id_exists:
                # Verificar si package_id es nullable
                package_id_nullable = next(col[2] for col in columns if col[0] == 'package_id')
                print(f"📋 Columna 'package_id' es nullable: {package_id_nullable}")
                
                if package_id_nullable == 'YES':
                    print("⚠️  La columna package_id es nullable, pero la migración intenta hacerla NOT NULL")
                    return "nullable_package_id"
                else:
                    print("✅ La columna package_id ya es NOT NULL")
                    return "already_not_null"
            else:
                print("❌ La columna package_id no existe")
                return "missing_package_id"
        else:
            print("❌ La tabla devices no existe")
            return "missing_table"

def fix_migration_issue():
    """Corregir el problema de migración"""
    database_url = os.getenv("DATABASE_URL", "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db")
    engine = create_engine(database_url)
    
    print("🔧 Corrigiendo problema de migración...")
    
    with engine.connect() as conn:
        try:
            # Verificar si la migración problemática ya se aplicó
            result = conn.execute(text("""
                SELECT version_num FROM alembic_version;
            """))
            current_version = result.scalar()
            print(f"📋 Versión actual de Alembic: {current_version}")
            
            # Si estamos en la versión problemática, hacer downgrade
            if current_version == "00f6cee5362d":
                print("⚠️  Detectada versión problemática, haciendo downgrade...")
                conn.execute(text("UPDATE alembic_version SET version_num = '7720cbe232ed';"))
                conn.commit()
                print("✅ Downgrade completado")
                return True
            else:
                print("✅ No se detectó la versión problemática")
                return False
                
        except Exception as e:
            print(f"❌ Error al corregir migración: {e}")
            return False

def main():
    """Función principal"""
    print("🔄 Iniciando verificación y corrección de migración...")
    
    # Verificar estado actual
    state = check_database_state()
    
    if state == "nullable_package_id":
        print("\n💡 Problema detectado: package_id es nullable pero la migración intenta hacerla NOT NULL")
        print("🔧 Aplicando corrección...")
        
        if fix_migration_issue():
            print("✅ Corrección aplicada exitosamente")
            print("\n💡 Próximos pasos:")
            print("   1. Ejecutar: docker-compose exec backend alembic upgrade head")
            print("   2. Verificar que las migraciones se aplican correctamente")
            print("   3. Ejecutar tests para confirmar que todo funciona")
        else:
            print("❌ No se pudo aplicar la corrección")
    elif state == "already_not_null":
        print("✅ La columna package_id ya está configurada correctamente")
    elif state == "missing_package_id":
        print("❌ La columna package_id no existe, necesitas revisar las migraciones")
    elif state == "missing_table":
        print("❌ La tabla devices no existe, necesitas revisar las migraciones")
    else:
        print(f"❓ Estado desconocido: {state}")

if __name__ == "__main__":
    main() 