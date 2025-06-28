#!/bin/bash

# Script de migración rápida para desarrollo
# Para cambios menores en el esquema sin reset completo

set -e

echo "🔧 Aplicando migración rápida..."

# 1. Aplicar migraciones
echo "📝 Ejecutando migraciones SQL..."
docker cp docker/postgres/complete_migration.sql viejos_trapos_postgres:/tmp/complete_migration.sql
docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -f /tmp/complete_migration.sql

# 2. Reiniciar servicios para sincronizar
echo "🔄 Reiniciando servicios..."
docker-compose restart backend
docker-compose restart web-panel

# 3. Recargar datos si es necesario
read -p "¿Recargar datos dummy? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Recargando datos dummy..."
    docker-compose exec backend python -m app.scripts.load_dummy_data
fi

echo "✅ Migración rápida completada!" 