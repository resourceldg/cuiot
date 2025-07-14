#!/bin/bash

set -e

# Script de población automatizada para CUIOT (Docker)
echo "\n🚀 Iniciando población completa de datos para CUIOT..."

# 1. Poblar datos core
echo "\n🔧 Poblando datos core y catálogos..."
docker-compose exec -T backend python scripts/run_modular_population.py --core

# 2. Poblar instituciones
echo "\n🏢 Poblando instituciones..."
docker-compose exec -T backend python scripts/run_modular_population.py --institutions

# 3. Poblar paquetes
echo "\n📦 Poblando paquetes..."
docker-compose exec -T backend python scripts/run_modular_population.py --packages

# 4. Poblar usuarios
echo "\n👥 Poblando usuarios..."
docker-compose exec -T backend python scripts/run_modular_population.py --users

# 5. Poblar add-ons y suscripciones
echo "\n🎯 Poblando add-ons y suscripciones..."
docker-compose exec -T backend python scripts/run_modular_population.py --addons

# 6. Poblar facturación
echo "\n💰 Poblando facturación..."
docker-compose exec -T backend python scripts/run_modular_population.py --billing

# 7. Poblar scoring y reviews
echo "\n🏆 Poblando scoring y reviews..."
docker-compose exec -T backend python scripts/run_modular_population.py --scoring

# 8. Poblar referencias y derivaciones médicas
echo "\n📋 Poblando referencias y derivaciones médicas..."
docker-compose exec -T backend python scripts/run_modular_population.py --referrals

# 9. Poblar geofences
echo "\n📍 Poblando geofences (zonas seguras, áreas restringidas, etc.)..."
docker-compose exec -T backend python scripts/run_modular_population.py --geofences

# 10. Poblar recordatorios
echo "\n🔔 Poblando recordatorios (medicación, citas, ejercicio, etc.)..."
docker-compose exec -T backend python scripts/run_modular_population.py --reminders

# 11. Poblar protocolos de emergencia
echo "\n🚨 Poblando protocolos de emergencia (globales e institucionales)..."
docker-compose exec -T backend python scripts/run_modular_population.py --emergency-protocols

# 12. Poblar eventos de debug
echo "\n🐛 Poblando eventos de debug (testing, desarrollo, monitoreo)..."
docker-compose exec -T backend python scripts/run_modular_population.py --debug-events

# 13. Poblar configuraciones de dispositivos
echo "\n⚙️ Poblando configuraciones de dispositivos (personalización IoT)..."
docker-compose exec -T backend python scripts/run_modular_population.py --device-configs

# 14. Verificación final
if [ -f backend/verify_system.py ]; then
  echo "\n🔎 Verificando integridad del sistema..."
  docker-compose exec -T backend python verify_system.py
else
  echo "\n⚠️  Script de verificación no encontrado. Verifica manualmente si es necesario."
fi

echo "\n✅ Población automatizada completada con éxito.\n" 