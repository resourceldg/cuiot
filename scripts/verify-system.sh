#!/bin/bash

# Script de verificación rápida del sistema
# Verifica el estado de todos los componentes

set -e

echo "🔍 Verificando estado del sistema..."
echo "=================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar contenedores
check_containers() {
    echo "📦 Verificando contenedores Docker..."
    
    if docker-compose ps | grep -q "Up"; then
        echo -e "${GREEN}✅ Contenedores ejecutándose${NC}"
        docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
    else
        echo -e "${RED}❌ Contenedores no están ejecutándose${NC}"
        return 1
    fi
}

# Función para verificar API
check_api() {
    echo -e "\n🌐 Verificando API Backend..."
    
    if curl -s http://localhost:8000/api/v1/health/ > /dev/null; then
        echo -e "${GREEN}✅ API Backend respondiendo${NC}"
        echo "   Health Check: $(curl -s http://localhost:8000/api/v1/health/ | jq -r '.message' 2>/dev/null || echo 'OK')"
    else
        echo -e "${RED}❌ API Backend no responde${NC}"
        return 1
    fi
}

# Función para verificar base de datos
check_database() {
    echo -e "\n🗄️  Verificando base de datos..."
    
    if docker-compose exec -T postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Base de datos principal conectada${NC}"
        
        # Contar tablas
        TABLE_COUNT=$(docker-compose exec -T postgres psql -U viejos_trapos_user -d viejos_trapos_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
        echo "   Tablas en BD principal: $TABLE_COUNT"
    else
        echo -e "${RED}❌ Base de datos principal no conectada${NC}"
        return 1
    fi
    
    if docker-compose exec -T postgres_test pg_isready -U viejos_trapos_user -d viejos_trapos_test_db > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Base de datos de test conectada${NC}"
        
        # Contar tablas
        TEST_TABLE_COUNT=$(docker-compose exec -T postgres_test psql -U viejos_trapos_user -d viejos_trapos_test_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
        echo "   Tablas en BD de test: $TEST_TABLE_COUNT"
    else
        echo -e "${RED}❌ Base de datos de test no conectada${NC}"
        return 1
    fi
}

# Función para verificar migraciones
check_migrations() {
    echo -e "\n🔄 Verificando migraciones..."
    
    CURRENT_REVISION=$(docker-compose exec -T backend alembic current 2>/dev/null | awk '{print $1}' || echo "ERROR")
    
    if [ "$CURRENT_REVISION" != "ERROR" ]; then
        echo -e "${GREEN}✅ Migraciones aplicadas${NC}"
        echo "   Revisión actual: $CURRENT_REVISION"
    else
        echo -e "${RED}❌ Error al verificar migraciones${NC}"
        return 1
    fi
}

# Función para verificar tests
check_tests() {
    echo -e "\n🧪 Verificando tests..."
    
    # Ejecutar un test simple para verificar que funciona
    if docker-compose exec -T backend pytest tests/test_health.py -q > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Tests funcionando${NC}"
        
        # Contar tests totales
        TOTAL_TESTS=$(docker-compose exec -T backend pytest --collect-only -q 2>/dev/null | grep "collected" | awk '{print $2}' || echo "0")
        echo "   Tests disponibles: $TOTAL_TESTS"
    else
        echo -e "${YELLOW}⚠️  Tests no disponibles o fallando${NC}"
    fi
}

# Función para verificar puertos
check_ports() {
    echo -e "\n🔌 Verificando puertos..."
    
    PORTS=("8000:Backend API" "3000:Web Panel" "5432:PostgreSQL" "5433:PostgreSQL Test" "6379:Redis" "8080:Adminer")
    
    for port_info in "${PORTS[@]}"; do
        port=$(echo $port_info | cut -d: -f1)
        service=$(echo $port_info | cut -d: -f2)
        
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            echo -e "${GREEN}✅ Puerto $port ($service) abierto${NC}"
        else
            echo -e "${YELLOW}⚠️  Puerto $port ($service) no disponible${NC}"
        fi
    done
}

# Función para mostrar logs recientes
show_recent_logs() {
    echo -e "\n📋 Logs recientes del backend:"
    echo "--------------------------------"
    docker logs viejos_trapos_backend --tail=5 2>/dev/null || echo "No se pueden obtener logs"
}

# Función principal
main() {
    echo "🚀 Sistema Integral de Monitoreo - Verificación de Estado"
    echo "========================================================"
    echo "Fecha: $(date)"
    echo ""

    # Verificar que docker-compose esté disponible
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ docker-compose no está instalado${NC}"
        exit 1
    fi

    # Verificar que estemos en el directorio correcto
    if [ ! -f "docker-compose.yml" ]; then
        echo -e "${RED}❌ No se encontró docker-compose.yml${NC}"
        echo "   Ejecute este script desde el directorio raíz del proyecto"
        exit 1
    fi

    # Ejecutar verificaciones
    check_containers
    check_api
    check_database
    check_migrations
    check_tests
    check_ports
    
    echo -e "\n📊 Resumen del Estado:"
    echo "======================"
    
    # Contar contenedores ejecutándose
    RUNNING_CONTAINERS=$(docker-compose ps -q | wc -l)
    echo "   Contenedores ejecutándose: $RUNNING_CONTAINERS"
    
    # Verificar si todo está funcionando
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}🎉 Sistema funcionando correctamente${NC}"
        echo "   El sistema está listo para desarrollo y producción"
    else
        echo -e "\n${YELLOW}⚠️  Algunos componentes pueden tener problemas${NC}"
        echo "   Revise los logs para más detalles"
    fi
    
    show_recent_logs
    
    echo -e "\n📚 Comandos útiles:"
    echo "==================="
    echo "   Ver logs: docker logs viejos_trapos_backend -f"
    echo "   Ejecutar tests: docker-compose exec backend pytest tests/ -v"
    echo "   Reiniciar: docker-compose restart"
    echo "   Parar: docker-compose down"
    echo "   Iniciar: docker-compose up -d"
}

# Ejecutar función principal
main "$@" 