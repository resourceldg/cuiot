#!/bin/bash

# Script de entrada para el contenedor backend
# Ejecuta migraciones automáticamente antes de iniciar la aplicación

set -e

echo "🚀 Iniciando contenedor backend..."

# Función para esperar a que la base de datos esté lista
wait_for_database() {
    echo "🔄 Esperando conexión a la base de datos..."
    
    # Obtener URL de base de datos del entorno
    if [ "$ENVIRONMENT" = "test" ]; then
        DB_URL="$TEST_DATABASE_URL"
        DB_HOST="postgres_test"
    else
        DB_URL="$DATABASE_URL"
        DB_HOST="postgres"
    fi
    
    # Extraer credenciales de la URL
    DB_USER=$(echo $DB_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
    DB_PASS=$(echo $DB_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
    DB_NAME=$(echo $DB_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
    
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if pg_isready -h $DB_HOST -U $DB_USER -d $DB_NAME >/dev/null 2>&1; then
            echo "✅ Base de datos lista!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo "⏳ Intento $attempt/$max_attempts: Base de datos no disponible aún..."
        sleep 2
    done
    
    echo "❌ No se pudo conectar a la base de datos después de $max_attempts intentos"
    return 1
}

# Función para ejecutar migraciones
run_migrations() {
    echo "🔧 Ejecutando migraciones..."
    
    if alembic upgrade head; then
        echo "✅ Migraciones aplicadas correctamente"
        return 0
    else
        echo "❌ Error al aplicar migraciones"
        return 1
    fi
}

# Función para cargar datos iniciales
load_initial_data() {
    echo "📊 Verificando datos iniciales..."
    
    # Aquí puedes agregar lógica para cargar datos iniciales
    # Por ejemplo, ejecutar scripts de carga de datos
    
    echo "✅ Datos iniciales verificados"
}

# Función principal
main() {
    # Cambiar al directorio del proyecto
    cd /app
    
    # Esperar a que la base de datos esté lista
    if ! wait_for_database; then
        echo "❌ Error: No se pudo conectar a la base de datos"
        exit 1
    fi
    
    # Ejecutar migraciones
    if ! run_migrations; then
        echo "❌ Error: No se pudieron aplicar las migraciones"
        exit 1
    fi
    
    # Cargar datos iniciales
    load_initial_data
    
    echo "🎉 Configuración completada, iniciando aplicación..."
    
    # Ejecutar el comando original (uvicorn)
    exec "$@"
}

# Ejecutar función principal con todos los argumentos
main "$@" 