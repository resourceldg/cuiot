#!/bin/bash

# Script de inicio para desarrollo
# Levanta todos los servicios y ejecuta migraciones automáticamente

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

echo "🚀 Iniciando entorno de desarrollo..."

# 1. Levantar bases de datos
print_info "📦 Levantando bases de datos..."
docker-compose up -d postgres postgres_test

# 2. Esperar a que las bases de datos estén listas
print_info "⏳ Esperando que las bases de datos estén listas..."
sleep 15

# 3. Verificar que las bases de datos estén funcionando
print_info "🔍 Verificando conexiones a bases de datos..."

if docker-compose exec -T postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db >/dev/null 2>&1; then
    print_success "✅ Base de datos de desarrollo lista"
else
    print_error "❌ Error en base de datos de desarrollo"
    exit 1
fi

if docker-compose exec -T postgres_test pg_isready -U viejos_trapos_user -d viejos_trapos_test_db >/dev/null 2>&1; then
    print_success "✅ Base de datos de testing lista"
else
    print_error "❌ Error en base de datos de testing"
    exit 1
fi

# 4. Levantar Redis
print_info "📦 Levantando Redis..."
docker-compose up -d redis

# 5. Ejecutar migraciones automáticamente
print_info "🔧 Ejecutando migraciones automáticamente..."
if ./scripts/migrate.sh up; then
    print_success "✅ Migraciones aplicadas correctamente"
else
    print_error "❌ Error al aplicar migraciones"
    exit 1
fi

# 6. Levantar backend (con migraciones automáticas)
print_info "📦 Levantando backend..."
docker-compose up -d backend

# 7. Levantar panel web
print_info "📦 Levantando panel web..."
docker-compose up -d web-panel

# 8. Levantar servicios adicionales
print_info "📦 Levantando servicios adicionales..."
docker-compose up -d mqtt adminer

# 9. Mostrar estado final
print_success "🎉 Entorno de desarrollo iniciado correctamente!"
echo ""
print_info "📊 Servicios disponibles:"
echo "  🌐 Panel Web:     http://localhost:3000"
echo "  🔧 API Backend:   http://localhost:8000"
echo "  📊 Adminer:       http://localhost:8080"
echo "  📚 API Docs:      http://localhost:8000/docs"
echo "  🗄️  PostgreSQL:    localhost:5432"
echo "  🧪 PostgreSQL Test: localhost:5433"
echo "  📡 MQTT:          localhost:1883"
echo ""
print_info "🔧 Comandos útiles:"
echo "  ./scripts/migrate.sh status    # Ver estado de migraciones"
echo "  ./scripts/migrate.sh create 'mensaje'  # Crear nueva migración"
echo "  docker-compose logs -f backend  # Ver logs del backend"
echo "  docker-compose down            # Detener todos los servicios"
echo ""
print_success "¡Listo para desarrollar! 🚀" 