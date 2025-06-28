#!/bin/bash

# Script de setup automático para desarrollo
# Maneja reset completo, migraciones y carga de datos

set -e  # Exit on any error

echo "🚀 Iniciando setup de desarrollo..."

# 1. Reset completo del entorno
echo "📦 Reseteando entorno Docker..."
docker-compose down -v
docker-compose up --build -d

# 2. Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 15

# 3. Aplicar migraciones
echo "🔧 Aplicando migraciones..."
docker cp docker/postgres/complete_migration.sql viejos_trapos_postgres:/tmp/complete_migration.sql
docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -f /tmp/complete_migration.sql

# 4. Cargar datos dummy
echo "📊 Cargando datos dummy..."
docker-compose exec backend python -m app.scripts.load_dummy_data

echo "✅ Setup completado exitosamente!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "🗄️  Adminer: http://localhost:8080"
echo ""
echo "🔑 Credenciales de prueba:"
echo "   📧 maria.gonzalez@example.com | 🔐 password123"
echo "   📧 carlos.rodriguez@example.com | 🔐 password123" 