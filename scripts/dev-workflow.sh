#!/bin/bash

# Flujo de trabajo completo para desarrollo con Docker Compose
# Uso: ./scripts/dev-workflow.sh [comando]

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
    echo "🚀 Flujo de Trabajo de Desarrollo con Docker Compose"
    echo ""
    echo "Comandos:"
    echo "  init      - Inicializa todo el entorno de desarrollo"
    echo "  start     - Inicia todos los servicios"
    echo "  stop      - Detiene todos los servicios"
    echo "  restart   - Reinicia todos los servicios"
    echo "  migrate   - Aplica migraciones a ambas bases de datos"
    echo "  sync      - Sincroniza desarrollo con testing"
    echo "  test      - Ejecuta los tests"
    echo "  shell     - Abre shell en el contenedor backend"
    echo "  logs      - Muestra logs de todos los servicios"
    echo "  clean     - Limpia todo (volúmenes, contenedores, redes)"
    echo "  status    - Muestra el estado de todos los servicios"
    echo "  help      - Muestra esta ayuda"
    echo ""
    echo "Flujo típico:"
    echo "  1. $0 init    # Primera vez"
    echo "  2. $0 start   # Iniciar desarrollo"
    echo "  3. $0 migrate # Después de cambios en modelos"
    echo "  4. $0 test    # Ejecutar tests"
    echo "  5. $0 stop    # Detener cuando termines"
}

# Inicializar todo el entorno
init_environment() {
    print_info "🚀 Inicializando entorno completo de desarrollo..."
    
    # Verificar Docker
    if ! docker info > /dev/null 2>&1; then
        print_error "❌ Docker no está corriendo"
        exit 1
    fi
    
    # Limpiar todo primero
    print_info "🧹 Limpiando entorno anterior..."
    docker-compose down -v 2>/dev/null || true
    
    # Construir imágenes
    print_info "🔨 Construyendo imágenes..."
    docker-compose build
    
    # Levantar servicios
    print_info "📦 Levantando servicios..."
    docker-compose up -d
    
    # Esperar a que las bases de datos estén listas
    print_info "⏳ Esperando que las bases de datos estén listas..."
    sleep 15
    
    # Verificar conexiones
    print_info "🔍 Verificando conexiones..."
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
    
    # Aplicar migraciones
    print_info "🔧 Aplicando migraciones..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic upgrade head"
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
    
    print_success "🎉 Entorno de desarrollo inicializado correctamente"
    print_info "📊 Puedes verificar el estado con: $0 status"
}

# Iniciar servicios
start_services() {
    print_info "🚀 Iniciando servicios..."
    docker-compose up -d
    print_success "✅ Servicios iniciados"
}

# Detener servicios
stop_services() {
    print_info "🛑 Deteniendo servicios..."
    docker-compose stop
    print_success "✅ Servicios detenidos"
}

# Reiniciar servicios
restart_services() {
    print_info "🔄 Reiniciando servicios..."
    docker-compose restart
    print_success "✅ Servicios reiniciados"
}

# Aplicar migraciones
migrate_databases() {
    print_info "🔧 Aplicando migraciones..."
    
    # Verificar que los servicios estén corriendo
    if ! docker-compose ps | grep -q "postgres.*Up"; then
        print_error "❌ Los servicios no están corriendo. Ejecuta '$0 start' primero."
        exit 1
    fi
    
    # Migrar desarrollo
    print_info "🔧 Migrando base de datos de desarrollo..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic upgrade head"
    
    # Migrar testing
    print_info "🧪 Migrando base de datos de testing..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
    
    print_success "✅ Migraciones aplicadas correctamente"
}

# Sincronizar bases de datos
sync_databases() {
    print_info "🔄 Sincronizando bases de datos..."
    
    # Verificar que los servicios estén corriendo
    if ! docker-compose ps | grep -q "postgres.*Up"; then
        print_error "❌ Los servicios no están corriendo. Ejecuta '$0 start' primero."
        exit 1
    fi
    
    # Generar nueva migración si hay cambios
    print_info "📝 Verificando cambios en modelos..."
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic revision --autogenerate -m 'sync_$(date +%Y%m%d_%H%M%S)'" || {
        print_warning "⚠️  No hay cambios nuevos para migrar"
    }
    
    # Aplicar migraciones
    migrate_databases
    
    print_success "✅ Bases de datos sincronizadas"
}

# Ejecutar tests
run_tests() {
    print_info "🧪 Ejecutando tests..."
    
    # Verificar que los servicios estén corriendo
    if ! docker-compose ps | grep -q "postgres_test.*Up"; then
        print_error "❌ Los servicios no están corriendo. Ejecuta '$0 start' primero."
        exit 1
    fi
    
    # Ejecutar tests
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test pytest tests/ -v"
    
    print_success "✅ Tests completados"
}

# Abrir shell
open_shell() {
    print_info "🐚 Abriendo shell en el contenedor backend..."
    
    # Verificar que el backend esté corriendo
    if ! docker-compose ps | grep -q "backend.*Up"; then
        print_info "📦 Levantando backend..."
        docker-compose up -d backend
        sleep 3
    fi
    
    docker-compose exec backend bash
}

# Mostrar logs
show_logs() {
    print_info "📋 Mostrando logs de todos los servicios..."
    docker-compose logs -f
}

# Limpiar todo
clean_all() {
    print_warning "⚠️  Esto eliminará TODOS los datos y contenedores"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "🧹 Limpiando todo..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "✅ Todo limpiado"
    else
        print_info "Operación cancelada"
    fi
}

# Mostrar estado
show_status() {
    print_info "📊 Estado de todos los servicios:"
    echo ""
    docker-compose ps
    echo ""
    
    # Verificar conexiones de bases de datos
    print_info "🔍 Verificando conexiones de bases de datos..."
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
    
    echo ""
    
    # Mostrar estado de migraciones
    print_info "📋 Estado de migraciones:"
    echo ""
    print_info "🔧 Desarrollo:"
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=development alembic current" 2>/dev/null || print_error "❌ No se pudo verificar"
    echo ""
    print_info "🧪 Testing:"
    docker-compose exec -T backend bash -c "cd /app && ENVIRONMENT=test alembic current" 2>/dev/null || print_error "❌ No se pudo verificar"
}

# Función principal
main() {
    case "${1:-help}" in
        "init")
            init_environment
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            restart_services
            ;;
        "migrate")
            migrate_databases
            ;;
        "sync")
            sync_databases
            ;;
        "test")
            run_tests
            ;;
        "shell")
            open_shell
            ;;
        "logs")
            show_logs
            ;;
        "clean")
            clean_all
            ;;
        "status")
            show_status
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

main "$@" 