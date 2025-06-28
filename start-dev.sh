#!/bin/bash

# Script para iniciar el entorno de desarrollo
echo "🚀 Iniciando entorno de desarrollo para Viejos Son Los Trapos..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor, instala Docker Compose primero."
    exit 1
fi

# Verificar si Docker está ejecutándose
if ! docker info &> /dev/null; then
    echo "❌ Docker no está ejecutándose. Por favor, inicia Docker primero."
    exit 1
fi

echo "✅ Docker y Docker Compose están disponibles"

# Detener contenedores existentes si los hay
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Limpiar recursos no utilizados
echo "🧹 Limpiando recursos no utilizados..."
docker system prune -f

# Construir y levantar todos los servicios
echo "🔨 Construyendo y levantando servicios..."
docker-compose up --build -d

# Esperar un momento para que los servicios se inicien
echo "⏳ Esperando que los servicios se inicien..."
sleep 10

# Verificar el estado de los contenedores
echo "🔍 Verificando estado de los contenedores..."
docker-compose ps

# Verificar que los servicios estén respondiendo
echo "🌐 Verificando conectividad de los servicios..."

# Verificar backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend (puerto 8000) - Funcionando"
else
    echo "❌ Backend (puerto 8000) - No responde"
fi

# Verificar frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend (puerto 3000) - Funcionando"
else
    echo "❌ Frontend (puerto 3000) - No responde"
fi

# Verificar base de datos
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Adminer (puerto 8080) - Funcionando"
else
    echo "❌ Adminer (puerto 8080) - No responde"
fi

echo ""
echo "🎉 ¡Entorno de desarrollo iniciado!"
echo ""
echo "📱 Servicios disponibles:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • Documentación API: http://localhost:8000/docs"
echo "   • Adminer (DB): http://localhost:8080"
echo "   • MQTT: localhost:1883"
echo ""
echo "📋 Comandos útiles:"
echo "   • Ver logs: docker-compose logs -f [servicio]"
echo "   • Parar servicios: docker-compose down"
echo "   • Reiniciar: docker-compose restart [servicio]"
echo ""
echo "🔧 Para desarrollo:"
echo "   • Los archivos están montados en volumen, los cambios se reflejan automáticamente"
echo "   • El frontend tiene hot-reload habilitado"
echo "   • El backend tiene auto-reload habilitado"
echo "" 