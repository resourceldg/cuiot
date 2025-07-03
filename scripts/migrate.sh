#!/bin/bash

# Script mejorado para gestionar migraciones con Docker Compose
# Uso: ./scripts/migrate.sh [comando]

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
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

show_help() {
    echo "Gestión de Migraciones con Docker Compose"
    echo ""
    echo "Comandos:"
    echo "  up        - Aplicar migraciones (upgrade head)"
    echo "  down      - Revertir migraciones (downgrade -1)"
    echo "  reset     - Resetear base de datos y aplicar migraciones"
    echo "  status    - Mostrar estado de migraciones"
    echo "  history   - Mostrar historial de migraciones"
    echo "  create    - Crear nueva migración (requiere mensaje)"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 up                    # Aplicar migraciones"
    echo "  $0 create 'add new table' # Crear nueva migración"
    echo "  $0 status                # Ver estado"
}

wait_for_database() {
    print_info "🔄 Esperando conexión a la base de datos..."
    
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker-compose exec -T postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db >/dev/null 2>&1; then
            print_success "✅ Base de datos lista!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        print_info "⏳ Intento $attempt/$max_attempts: Base de datos no disponible aún..."
        sleep 2
    done
    
    print_error "❌ No se pudo conectar a la base de datos después de $max_attempts intentos"
    return 1
}

ensure_backend_running() {
    if ! docker-compose ps | grep -q "backend.*Up"; then
        print_info "📦 Levantando backend para migraciones..."
        docker-compose up -d backend
        sleep 5
    fi
}

migrate_up() {
    print_info "🔧 Aplicando migraciones..."
    
    if ! wait_for_database; then
        print_error "❌ No se pudo conectar a la base de datos"
        exit 1
    fi
    
    ensure_backend_running
    
    if docker-compose exec -T backend alembic upgrade head; then
        print_success "✅ Migraciones aplicadas correctamente"
    else
        print_error "❌ Error al aplicar migraciones"
        exit 1
    fi
}

migrate_down() {
    print_warning "⚠️  Revertiendo última migración..."
    
    ensure_backend_running
    
    if docker-compose exec -T backend alembic downgrade -1; then
        print_success "✅ Migración revertida correctamente"
    else
        print_error "❌ Error al revertir migración"
        exit 1
    fi
}

migrate_reset() {
    print_warning "⚠️  Esto eliminará TODOS los datos de la base de datos"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "🧹 Reseteando base de datos..."
        
        # Detener servicios
        docker-compose down
        
        # Eliminar volúmenes
        docker-compose down -v
        
        # Levantar solo base de datos
        docker-compose up -d postgres
        
        # Esperar a que esté lista
        if ! wait_for_database; then
            print_error "❌ Error al conectar a la base de datos"
            exit 1
        fi
        
        # Aplicar migraciones
        migrate_up
        
        print_success "✅ Base de datos reseteada y migraciones aplicadas"
    else
        print_info "Operación cancelada"
    fi
}

show_status() {
    print_info "📊 Estado de migraciones:"
    echo ""
    
    ensure_backend_running
    
    docker-compose exec -T backend alembic current
    echo ""
    
    print_info "📋 Últimas migraciones:"
    docker-compose exec -T backend alembic history --verbose
}

show_history() {
    print_info "📋 Historial completo de migraciones:"
    echo ""
    
    ensure_backend_running
    
    docker-compose exec -T backend alembic history --verbose
}

create_migration() {
    if [ -z "$1" ]; then
        print_error "❌ Debes proporcionar un mensaje para la migración"
        echo "Uso: $0 create 'mensaje de la migración'"
        exit 1
    fi
    
    print_info "📝 Creando nueva migración: $1"
    
    ensure_backend_running
    
    if docker-compose exec -T backend alembic revision --autogenerate -m "$1"; then
        print_success "✅ Migración creada correctamente"
        print_info "💡 Para aplicarla, ejecuta: $0 up"
    else
        print_error "❌ Error al crear migración"
        exit 1
    fi
}

# Función principal
main() {
    case "${1:-help}" in
        "up")
            migrate_up
            ;;
        "down")
            migrate_down
            ;;
        "reset")
            migrate_reset
            ;;
        "status")
            show_status
            ;;
        "history")
            show_history
            ;;
        "create")
            create_migration "$2"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Ejecutar función principal
main "$@" 