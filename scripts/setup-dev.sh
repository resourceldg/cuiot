#!/bin/bash

# Script de setup robusto para desarrollo
# Borra la base de datos y volúmenes, recrea todo y aplica migraciones
# USO: ./scripts/setup-dev.sh [--dummy]

set -e

echo "⚠️  Este script borrará TODOS los datos de la base de datos y volúmenes de Docker."
echo "¿Deseas continuar? (s/n)"
read -r confirm
if [[ "$confirm" != "s" ]]; then
  echo "Cancelado."
  exit 1
fi

# 1. Detener y eliminar contenedores y volúmenes
echo "🧹 Deteniendo y eliminando contenedores y volúmenes..."
docker compose down -v

# 2. Levantar servicios
echo "🚀 Levantando servicios..."
docker compose up -d

# 3. Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
RETRIES=20
until docker compose exec postgres pg_isready -U viejos_trapos_user -d viejos_trapos_db; do
  sleep 2
  RETRIES=$((RETRIES-1))
  if [ $RETRIES -le 0 ]; then
    echo "❌ La base de datos no está lista. Abortando."
    exit 1
  fi
done

# 4. Aplicar migraciones Alembic
echo "🔄 Aplicando migraciones Alembic..."
docker compose exec backend alembic upgrade head

# 5. (Opcional) Cargar datos dummy
if [[ "$1" == "--dummy" ]]; then
  echo "📦 Cargando datos dummy..."
  docker compose exec backend python -m app.scripts.load_dummy_data --reset
fi

echo "✅ Entorno de desarrollo listo."

echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "🗄️  Adminer: http://localhost:8080"
echo ""
echo "🔑 Credenciales de prueba:"
echo "   📧 maria.gonzalez@example.com | 🔐 password123"
echo "   📧 carlos.rodriguez@example.com | 🔐 password123" 