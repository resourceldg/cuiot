#!/bin/bash

# Script para configurar y sincronizar bases de datos
# Uso: ./scripts/setup_databases.sh [comando]

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  init        - Inicializa las bases de datos (desarrollo y testing)"
    echo "  sync        - Sincroniza desarrollo con testing"
    echo "  reset-test  - Resetea la base de datos de testing"
    echo "  status      - Muestra el estado de las migraciones"
    echo "  clean       - Limpia todos los volúmenes de Docker"
    echo "  help        - Muestra esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 init      # Primera vez que configuras el proyecto"
    echo "  $0 sync      # Después de hacer cambios en desarrollo"
    echo "  $0 status    # Ver estado actual"
}

# Función para inicializar bases de datos
init_databases() {
    print_message "🚀 Inicializando bases de datos..."
    
    # Verificar que Docker esté corriendo
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker no está corriendo. Inicia Docker primero."
        exit 1
    fi
    
    # Limpiar volúmenes existentes si existen
    print_message "🧹 Limpiando volúmenes existentes..."
    docker-compose down -v 2>/dev/null || true
    
    # Levantar servicios
    print_message "📦 Levantando servicios de Docker..."
    docker-compose up -d postgres postgres_test backend
    
    # Esperar a que las bases de datos estén listas
    print_message "⏳ Esperando a que las bases de datos estén listas..."
    sleep 15
    
    # Verificar conexión a desarrollo
    print_message "🔍 Verificando conexión a base de datos de desarrollo..."
    if ! docker-compose exec -T postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db; then
        print_error "No se pudo conectar a la base de datos de desarrollo"
        exit 1
    fi
    
    # Verificar conexión a testing
    print_message "🔍 Verificando conexión a base de datos de testing..."
    if ! docker-compose exec -T postgres_test pg_isready -U viejos_trapos_user -d viejos_trapos_test_db; then
        print_error "No se pudo conectar a la base de datos de testing"
        exit 1
    fi
    
    # Aplicar migraciones a desarrollo
    print_message "🔧 Aplicando migraciones a desarrollo..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic upgrade head"
    
    # Aplicar migraciones a testing
    print_message "🧪 Aplicando migraciones a testing..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
    
    print_success "✅ Bases de datos inicializadas correctamente"
    print_message "📊 Puedes verificar el estado con: $0 status"
}

# Función para sincronizar
sync_databases() {
    print_message "🔄 Sincronizando bases de datos..."
    
    # Verificar que las bases de datos estén corriendo
    if ! docker-compose ps | grep -q "postgres.*Up"; then
        print_error "Los servicios de base de datos no están corriendo. Ejecuta '$0 init' primero."
        exit 1
    fi
    
    # Ejecutar script de sincronización dentro del contenedor
    docker-compose exec -T backend bash -c "cd /app && python3 scripts/sync_databases.py sync"
    
    print_success "✅ Sincronización completada"
}

# Función para resetear testing
reset_test_database() {
    print_message "🔄 Reseteando base de datos de testing..."
    
    # Verificar que la base de datos de testing esté corriendo
    if ! docker-compose ps | grep -q "postgres_test.*Up"; then
        print_error "La base de datos de testing no está corriendo. Ejecuta '$0 init' primero."
        exit 1
    fi
    
    # Ejecutar reset dentro del contenedor
    docker-compose exec -T backend bash -c "cd /app && python3 scripts/sync_databases.py reset-test"
    
    print_success "✅ Base de datos de testing reseteada"
}

# Función para mostrar estado
show_status() {
    print_message "📊 Mostrando estado de las bases de datos..."
    
    # Estado de los servicios
    echo ""
    print_message "🐳 Estado de los servicios Docker:"
    docker-compose ps postgres postgres_test backend
    
    # Estado de las migraciones
    echo ""
    docker-compose exec -T backend bash -c "cd /app && python3 scripts/sync_databases.py status"
}

# Función para limpiar
clean_all() {
    print_warning "⚠️  Esto eliminará TODOS los datos de las bases de datos"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "🧹 Limpiando volúmenes de Docker..."
        docker-compose down -v
        print_success "✅ Volúmenes limpiados"
    else
        print_message "Operación cancelada"
    fi
}

# Función principal
main() {
    case "${1:-help}" in
        "init")
            init_databases
            ;;
        "sync")
            sync_databases
            ;;
        "reset-test")
            reset_test_database
            ;;
        "status")
            show_status
            ;;
        "clean")
            clean_all
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Ejecutar función principal
main "$@" 