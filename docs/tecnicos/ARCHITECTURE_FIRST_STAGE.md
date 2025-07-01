# Arquitectura Primera Etapa - Sistema de Monitoreo de Cuidado Humano

---

## Resumen Ejecutivo

Este documento define la arquitectura para la **primera etapa comercial** del sistema, diseñada para servicios menores y validación de mercado. Se utiliza una **arquitectura monolítica con Docker** desplegada en **Ubuntu Server**, optimizada para costos y simplicidad operacional.

---

## 1. Arquitectura Monolítica - Primera Etapa

### 1.1 Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│                    Ubuntu Server (VPS)                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Nginx Proxy   │  │   Certbot SSL   │  │   Fail2ban   │ │
│  │   (Puerto 80/443)│  │   (Let's Encrypt)│  │   (Seguridad)│ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Docker Compose Stack                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │ │
│  │  │   Backend   │  │  Frontend   │  │   PostgreSQL    │ │ │
│  │  │  FastAPI    │  │  SvelteKit  │  │   Database      │ │ │
│  │  │  (Puerto 8000)│  │  (Puerto 3000)│  │   (Puerto 5432)│ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘ │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │ │
│  │  │    Redis    │  │   Mosquitto │  │   Prometheus    │ │ │
│  │  │   Cache     │  │   MQTT      │  │   Monitoring    │ │ │
│  │  │ (Puerto 6379)│  │ (Puerto 1883)│  │   (Puerto 9090)│ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Backup Script │  │   Log Rotation │  │   Cron Jobs  │ │
│  │   (Diario)      │  │   (Logrotate)   │  │   (Mantenimiento)│ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Especificaciones del Servidor

#### Requisitos Mínimos (Hasta 50 usuarios)
- **CPU**: 2 vCPUs
- **RAM**: 4 GB
- **Storage**: 100 GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Red**: 1 Gbps

#### Requisitos Recomendados (Hasta 200 usuarios)
- **CPU**: 4 vCPUs
- **RAM**: 8 GB
- **Storage**: 200 GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Red**: 1 Gbps

#### Requisitos Escalados (Hasta 500 usuarios)
- **CPU**: 8 vCPUs
- **RAM**: 16 GB
- **Storage**: 500 GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Red**: 1 Gbps

---

## 2. Stack Tecnológico - Primera Etapa

### 2.1 Backend (FastAPI Monolítico)
```python
# Estructura del backend monolítico
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app principal
│   ├── core/
│   │   ├── config.py           # Configuración centralizada
│   │   ├── database.py         # Conexión PostgreSQL
│   │   ├── auth.py             # Autenticación JWT
│   │   └── security.py         # Encriptación y seguridad
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── api/                    # Endpoints organizados
│   ├── services/               # Lógica de negocio
│   ├── utils/                  # Utilidades comunes
│   └── tests/                  # Tests unitarios
├── requirements.txt
├── Dockerfile
└── alembic/                    # Migraciones de BD
```

### 2.2 Frontend (SvelteKit)
```javascript
// Estructura del frontend
frontend/
├── src/
│   ├── app.html
│   ├── app.css
│   ├── lib/
│   │   ├── components/         # Componentes reutilizables
│   │   ├── stores/            # Svelte stores
│   │   ├── utils/             # Utilidades
│   │   └── api/               # Cliente API
│   ├── routes/                # Páginas SvelteKit
│   └── types/                 # TypeScript types
├── package.json
├── svelte.config.js
├── vite.config.js
└── Dockerfile
```

### 2.3 Base de Datos (PostgreSQL)
```sql
-- Configuración optimizada para primera etapa
-- PostgreSQL 15+ con extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Configuración de rendimiento
SET shared_buffers = '256MB';
SET effective_cache_size = '1GB';
SET maintenance_work_mem = '64MB';
SET checkpoint_completion_target = 0.9;
SET wal_buffers = '16MB';
SET default_statistics_target = 100;
```

---

## 3. Docker Compose - Configuración

### 3.1 docker-compose.yml
```yaml
version: '3.8'

services:
  # Base de datos
  postgres:
    image: postgres:15-alpine
    container_name: cuiot_postgres
    environment:
      POSTGRES_DB: cuiot_db
      POSTGRES_USER: cuiot_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cuiot_user -d cuiot_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache Redis
  redis:
    image: redis:7-alpine
    container_name: cuiot_redis
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  # MQTT Broker
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: cuiot_mosquitto
    volumes:
      - ./docker/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./docker/mosquitto/passwd:/mosquitto/config/passwd
      - mosquitto_data:/mosquitto/data
      - mosquitto_logs:/mosquitto/log
    ports:
      - "1883:1883"
      - "9001:9001"
    restart: unless-stopped

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: cuiot_backend
    environment:
      - DATABASE_URL=postgresql://cuiot_user:${DB_PASSWORD}@postgres:5432/cuiot_db
      - REDIS_URL=redis://redis:6379
      - MQTT_BROKER=mosquitto
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    volumes:
      - ./backend:/app
      - backend_logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: cuiot_frontend
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  # Monitoreo
  prometheus:
    image: prom/prometheus:latest
    container_name: cuiot_prometheus
    volumes:
      - ./docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: cuiot_grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./docker/grafana/provisioning:/etc/grafana/provisioning
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  mosquitto_data:
  mosquitto_logs:
  backend_logs:
  prometheus_data:
  grafana_data:
```

---

## 4. Configuración del Servidor Ubuntu

### 4.1 Script de Instalación Inicial
```bash
#!/bin/bash
# install-server.sh

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
sudo apt install -y curl wget git htop vim ufw fail2ban

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Configurar firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 1883  # MQTT
sudo ufw --force enable

# Configurar Nginx
sudo apt install -y nginx certbot python3-certbot-nginx

# Configurar logs
sudo mkdir -p /var/log/cuiot
sudo chown $USER:$USER /var/log/cuiot

# Configurar backups
sudo mkdir -p /opt/backups/cuiot
sudo chown $USER:$USER /opt/backups/cuiot

echo "Instalación básica completada. Reinicia la sesión para aplicar cambios de Docker."
```

### 4.2 Configuración Nginx
```nginx
# /etc/nginx/sites-available/cuiot
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    # SSL (configurado por Certbot)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket para tiempo real
    location /ws/ {
        proxy_pass http://localhost:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # MQTT WebSocket
    location /mqtt/ {
        proxy_pass http://localhost:9001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Monitoreo (solo acceso local)
    location /monitoring/ {
        allow 127.0.0.1;
        deny all;
        proxy_pass http://localhost:3001/;
    }

    # Logs
    access_log /var/log/nginx/cuiot_access.log;
    error_log /var/log/nginx/cuiot_error.log;
}
```

---

## 5. Costos Estimados - Primera Etapa

### 5.1 Servidor VPS (Mensual)
- **DigitalOcean**: $12-24/mes (2-4 vCPUs, 4-8 GB RAM)
- **Linode**: $10-20/mes (2-4 vCPUs, 4-8 GB RAM)
- **Vultr**: $12-24/mes (2-4 vCPUs, 4-8 GB RAM)
- **AWS EC2**: $15-30/mes (t3.medium-t3.large)

### 5.2 Dominio y SSL
- **Dominio**: $10-15/año
- **SSL**: Gratis (Let's Encrypt)
- **CDN**: $5-10/mes (opcional)

### 5.3 Servicios Externos
- **Twilio**: $1-5/mes (SMS y llamadas)
- **SendGrid**: $15/mes (email)
- **WhatsApp Business**: $5-10/mes

### 5.4 Total Estimado
- **Mínimo**: $25-35/mes (hasta 50 usuarios)
- **Recomendado**: $40-60/mes (hasta 200 usuarios)
- **Escalado**: $80-120/mes (hasta 500 usuarios)

---

## 6. Escalabilidad y Migración

### 6.1 Límites de la Arquitectura Monolítica
- **Usuarios concurrentes**: Hasta 500-1000
- **Dispositivos IoT**: Hasta 2000-3000
- **Eventos/segundo**: Hasta 100-200
- **Almacenamiento**: Hasta 500 GB

### 6.2 Señales de Escalado
- CPU > 80% por más de 5 minutos
- RAM > 90% utilizada
- Tiempo de respuesta API > 2 segundos
- Errores 5xx > 1% de requests
- Disco > 80% utilizado

### 6.3 Plan de Migración a Microservicios
1. **Fase 1**: Separar servicios críticos (alertas, notificaciones)
2. **Fase 2**: Migrar a contenedores independientes
3. **Fase 3**: Implementar load balancer
4. **Fase 4**: Migrar a Kubernetes o AWS ECS

---

## 7. Monitoreo y Mantenimiento

### 7.1 Scripts de Mantenimiento
```bash
#!/bin/bash
# maintenance.sh

# Backup diario
docker exec cuiot_postgres pg_dump -U cuiot_user cuiot_db > /opt/backups/cuiot/db_$(date +%Y%m%d).sql

# Limpiar backups antiguos (mantener 7 días)
find /opt/backups/cuiot -name "db_*.sql" -mtime +7 -delete

# Rotar logs
docker exec cuiot_backend logrotate /etc/logrotate.conf

# Verificar salud de servicios
docker-compose ps
docker exec cuiot_backend curl -f http://localhost:8000/health

# Actualizar certificados SSL
certbot renew --quiet
```

### 7.2 Alertas de Monitoreo
- CPU > 80%
- RAM > 90%
- Disco > 85%
- Servicios down
- Errores de aplicación > 5%

---

## 8. Seguridad

### 8.1 Medidas Implementadas
- **Firewall**: UFW configurado
- **Fail2ban**: Protección contra ataques
- **SSL/TLS**: Certificados automáticos
- **Docker**: Aislamiento de servicios
- **Backups**: Diarios y automáticos
- **Updates**: Automáticos de seguridad

### 8.2 Recomendaciones Adicionales
- Cambiar puertos por defecto
- Implementar rate limiting
- Monitoreo de logs de seguridad
- Auditorías regulares
- Plan de respuesta a incidentes

---

*Documento en desarrollo - Versión 1.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 