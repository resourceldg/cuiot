#!/usr/bin/env python3
"""
Script de inicialización de base de datos
Ejecuta migraciones automáticamente al levantar el contenedor
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def wait_for_database():
    """Espera a que la base de datos esté lista"""
    import psycopg2
    from psycopg2 import OperationalError
    
    # Obtener URL de base de datos del entorno
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "test":
        database_url = os.getenv(
            "TEST_DATABASE_URL", 
            "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres_test:5432/viejos_trapos_test_db"
        )
    else:
        database_url = os.getenv(
            "DATABASE_URL", 
            "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db"
        )
    
    print(f"🔄 Esperando conexión a la base de datos ({environment})...")
    
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            conn = psycopg2.connect(database_url)
            conn.close()
            print(f"✅ Base de datos {environment} lista!")
            return True
        except OperationalError as e:
            attempt += 1
            print(f"⏳ Intento {attempt}/{max_attempts}: Base de datos no disponible aún...")
            time.sleep(2)
    
    print(f"❌ No se pudo conectar a la base de datos después de {max_attempts} intentos")
    return False

def run_migrations():
    """Ejecuta las migraciones de Alembic"""
    print("🔧 Ejecutando migraciones...")
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir("/app")
        
        # Ejecutar migraciones
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd="/app"
        )
        
        if result.returncode == 0:
            print("✅ Migraciones aplicadas correctamente")
            return True
        else:
            print(f"❌ Error al aplicar migraciones: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {e}")
        return False

def load_initial_data():
    """Carga datos iniciales si es necesario"""
    print("📊 Verificando si se necesitan datos iniciales...")
    
    # Aquí puedes agregar lógica para cargar datos iniciales
    # Por ejemplo, roles del sistema, configuraciones por defecto, etc.
    
    print("✅ Datos iniciales verificados")

def main():
    """Función principal"""
    print("🚀 Iniciando configuración de base de datos...")
    
    # Esperar a que la base de datos esté lista
    if not wait_for_database():
        sys.exit(1)
    
    # Ejecutar migraciones
    if not run_migrations():
        sys.exit(1)
    
    # Cargar datos iniciales
    load_initial_data()
    
    print("🎉 Configuración de base de datos completada!")

if __name__ == "__main__":
    main() 