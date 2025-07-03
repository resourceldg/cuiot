#!/usr/bin/env python3
"""
Script para sincronizar bases de datos entre entornos.
Permite sincronizar la base de datos de desarrollo con la de testing.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import Settings

def run_command(command, description, cwd=None):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd or project_root
        )
        print(f"✅ {description} completado exitosamente")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida de error: {e.stderr}")
        return None

def sync_dev_to_test():
    """Sincroniza la base de datos de desarrollo con la de testing"""
    print("🚀 Iniciando sincronización de base de datos de desarrollo a testing...")
    
    # 1. Generar nueva migración desde desarrollo
    print("\n📝 Paso 1: Generando nueva migración desde desarrollo...")
    migration_result = run_command(
        "alembic revision --autogenerate -m 'sync_dev_to_test'",
        "Generando migración automática"
    )
    
    if not migration_result:
        print("❌ No se pudo generar la migración. Verifica que no haya errores en el modelo.")
        return False
    
    # 2. Aplicar migración a desarrollo
    print("\n📝 Paso 2: Aplicando migración a base de datos de desarrollo...")
    os.environ["ENVIRONMENT"] = "development"
    dev_result = run_command(
        "alembic upgrade head",
        "Aplicando migración a desarrollo"
    )
    
    if not dev_result:
        print("❌ No se pudo aplicar la migración a desarrollo.")
        return False
    
    # 3. Aplicar migración a testing
    print("\n📝 Paso 3: Aplicando migración a base de datos de testing...")
    os.environ["ENVIRONMENT"] = "test"
    test_result = run_command(
        "alembic upgrade head",
        "Aplicando migración a testing"
    )
    
    if not test_result:
        print("❌ No se pudo aplicar la migración a testing.")
        return False
    
    print("\n🎉 ¡Sincronización completada exitosamente!")
    print("✅ Base de datos de desarrollo y testing están sincronizadas")
    return True

def reset_test_database():
    """Resetea la base de datos de testing"""
    print("🔄 Reseteando base de datos de testing...")
    
    os.environ["ENVIRONMENT"] = "test"
    
    # Eliminar todas las migraciones aplicadas
    reset_result = run_command(
        "alembic downgrade base",
        "Eliminando todas las migraciones de testing"
    )
    
    if reset_result:
        # Aplicar todas las migraciones nuevamente
        upgrade_result = run_command(
            "alembic upgrade head",
            "Aplicando todas las migraciones a testing"
        )
        
        if upgrade_result:
            print("✅ Base de datos de testing reseteada exitosamente")
            return True
    
    print("❌ Error al resetear la base de datos de testing")
    return False

def show_status():
    """Muestra el estado de las migraciones en ambos entornos"""
    print("📊 Estado de las migraciones:")
    
    # Estado en desarrollo
    print("\n🔧 Entorno de Desarrollo:")
    os.environ["ENVIRONMENT"] = "development"
    run_command("alembic current", "Estado actual de desarrollo")
    run_command("alembic history", "Historial de migraciones de desarrollo")
    
    # Estado en testing
    print("\n🧪 Entorno de Testing:")
    os.environ["ENVIRONMENT"] = "test"
    run_command("alembic current", "Estado actual de testing")
    run_command("alembic history", "Historial de migraciones de testing")

def main():
    parser = argparse.ArgumentParser(description="Sincronización de bases de datos")
    parser.add_argument(
        "action",
        choices=["sync", "reset-test", "status"],
        help="Acción a realizar"
    )
    
    args = parser.parse_args()
    
    if args.action == "sync":
        sync_dev_to_test()
    elif args.action == "reset-test":
        reset_test_database()
    elif args.action == "status":
        show_status()

if __name__ == "__main__":
    main() 