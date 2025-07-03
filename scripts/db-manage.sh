#!/bin/bash

# Script simple para gestionar bases de datos con Docker Compose
# Uso: ./scripts/db-manage.sh [comando]

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

show_help() {
    echo "Gestión de Bases de Datos con Docker Compose"
    echo ""
    echo "Comandos:"
    echo "  start     - Inicia las bases de datos"
    echo "  stop      - Detiene las bases de datos"
    echo "  restart   - Reinicia las bases de datos"
    echo "  migrate   - Aplica migraciones a ambas bases de datos"
    echo "  reset     - Resetea las bases de datos (elimina datos)"
    echo "  status    - Muestra el estado"
    echo "  logs      - Muestra logs de las bases de datos"
    echo "  shell     - Abre shell en el contenedor backend"
    echo "  help      - Muestra esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 start   # Primera vez"
    echo "  $0 migrate # Después de cambios"
    echo "  $0 status  # Ver estado"
}

start_databases() {
    print_info "🚀 Iniciando bases de datos..."
    
    # Levantar solo las bases de datos
    docker-compose up -d postgres postgres_test
    
    print_info "⏳ Esperando que las bases de datos estén listas..."
    sleep 10
    
    # Verificar conexiones
    if docker-compose exec -T postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db; then
        print_success "✅ Base de datos de desarrollo lista"
    else
        print_error "❌ Error en base de datos de desarrollo"
        exit 1
    fi
    
    if docker-compose exec -T postgres_test pg_isready -U viejos_trapos_user -d viejos_trapos_test_db; then
        print_success "✅ Base de datos de testing lista"
    else
        print_error "❌ Error en base de datos de testing"
        exit 1
    fi
    
    print_success "🎉 Bases de datos iniciadas correctamente"
}

stop_databases() {
    print_info "🛑 Deteniendo bases de datos..."
    docker-compose stop postgres postgres_test
    print_success "✅ Bases de datos detenidas"
}

restart_databases() {
    print_info "🔄 Reiniciando bases de datos..."
    docker-compose restart postgres postgres_test
    print_success "✅ Bases de datos reiniciadas"
}

migrate_databases() {
    print_info "🔧 Aplicando migraciones..."
    
    # Verificar que las bases de datos estén corriendo
    if ! docker-compose ps | grep -q "postgres.*Up"; then
        print_error "❌ Las bases de datos no están corriendo. Ejecuta '$0 start' primero."
        exit 1
    fi
    
    # Levantar backend temporalmente para migraciones
    print_info "📦 Levantando backend para migraciones..."
    docker-compose up -d backend
    
    # Esperar a que el backend esté listo
    sleep 5
    
    # Migrar desarrollo
    print_info "🔧 Migrando base de datos de desarrollo..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic upgrade head"
    
    # Migrar testing
    print_info "🧪 Migrando base de datos de testing..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
    
    # Detener backend (opcional, comentar si quieres que siga corriendo)
    docker-compose stop backend
    
    print_success "✅ Migraciones aplicadas correctamente"
}

reset_databases() {
    print_warning "⚠️  Esto eliminará TODOS los datos de las bases de datos"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "🧹 Reseteando bases de datos..."
        docker-compose down -v
        docker-compose up -d postgres postgres_test
        sleep 10
        print_success "✅ Bases de datos reseteadas"
    else
        print_info "Operación cancelada"
    fi
}

show_status() {
    print_info "📊 Estado de las bases de datos:"
    echo ""
    docker-compose ps postgres postgres_test
    echo ""
    
    # Verificar conexiones
    print_info "🔍 Verificando conexiones..."
    if docker-compose exec -T postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db 2>/dev/null; then
        print_success "✅ Desarrollo: Conectado"
    else
        print_error "❌ Desarrollo: No conectado"
    fi
    
    if docker-compose exec -T postgres_test pg_isready -U viejos_trapos_user -d viejos_trapos_test_db 2>/dev/null; then
        print_success "✅ Testing: Conectado"
    else
        print_error "❌ Testing: No conectado"
    fi
}

show_logs() {
    print_info "📋 Logs de las bases de datos:"
    echo ""
    docker-compose logs postgres postgres_test
}

open_shell() {
    print_info "🐚 Abriendo shell en el contenedor backend..."
    
    # Levantar backend si no está corriendo
    if ! docker-compose ps | grep -q "backend.*Up"; then
        docker-compose up -d backend
        sleep 3
    fi
    
    docker-compose exec backend bash
}

# Función principal
main() {
    case "${1:-help}" in
        "start")
            start_databases
            ;;
        "stop")
            stop_databases
            ;;
        "restart")
            restart_databases
            ;;
        "migrate")
            migrate_databases
            ;;
        "reset")
            reset_databases
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "shell")
            open_shell
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

main "$@" 