#!/bin/bash

# Script para sincronizar bases de datos de desarrollo con testing
# Uso: ./scripts/sync-db.sh

set -e

# Colores
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

# Verificar que las bases de datos estén corriendo
check_databases() {
    if ! docker-compose ps | grep -q "postgres.*Up"; then
        print_error "❌ Las bases de datos no están corriendo. Ejecuta './scripts/db-manage.sh start' primero."
        exit 1
    fi
}

# Sincronizar bases de datos
sync_databases() {
    print_info "🔄 Sincronizando bases de datos..."
    
    # Verificar estado
    check_databases
    
    # Levantar backend si no está corriendo
    if ! docker-compose ps | grep -q "backend.*Up"; then
        print_info "📦 Levantando backend..."
        docker-compose up -d backend
        sleep 5
    fi
    
    # Generar nueva migración si hay cambios
    print_info "📝 Verificando cambios en modelos..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic revision --autogenerate -m 'sync_$(date +%Y%m%d_%H%M%S)'" || {
        print_warning "⚠️  No hay cambios nuevos para migrar"
    }
    
    # Aplicar migraciones a desarrollo
    print_info "🔧 Aplicando migraciones a desarrollo..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic upgrade head"
    
    # Aplicar migraciones a testing
    print_info "🧪 Aplicando migraciones a testing..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
    
    print_success "✅ Bases de datos sincronizadas correctamente"
}

# Mostrar estado de sincronización
show_sync_status() {
    print_info "📊 Estado de sincronización:"
    echo ""
    
    # Estado de desarrollo
    print_info "🔧 Base de datos de desarrollo:"
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic current" 2>/dev/null || print_error "❌ No se pudo verificar desarrollo"
    
    echo ""
    
    # Estado de testing
    print_info "🧪 Base de datos de testing:"
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic current" 2>/dev/null || print_error "❌ No se pudo verificar testing"
    
    echo ""
}

# Función principal
main() {
    case "${1:-sync}" in
        "sync")
            sync_databases
            ;;
        "status")
            show_sync_status
            ;;
        "help"|*)
            echo "Sincronización de Bases de Datos"
            echo ""
            echo "Uso: $0 [comando]"
            echo ""
            echo "Comandos:"
            echo "  sync    - Sincroniza desarrollo con testing (por defecto)"
            echo "  status  - Muestra el estado de sincronización"
            echo "  help    - Muestra esta ayuda"
            echo ""
            echo "Ejemplos:"
            echo "  $0       # Sincronizar"
            echo "  $0 sync  # Sincronizar explícitamente"
            echo "  $0 status # Ver estado"
            ;;
    esac
}

main "$@" 