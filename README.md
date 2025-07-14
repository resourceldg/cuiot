# Sistema Integral de Monitoreo y Cuidado

Un sistema completo de monitoreo y cuidado para personas bajo cuidado que incluye dispositivos IoT, aplicación web, API backend y comunicación MQTT en tiempo real.

## 🚀 Estado del Proyecto

✅ **Funcionando correctamente**
- Backend FastAPI con PostgreSQL
- Frontend SvelteKit con TypeScript
- Base de datos PostgreSQL con migraciones completas
- Redis para cache
- MQTT Broker para IoT
- Docker Compose para desarrollo
- Sistema de debug y testing completo
- Panel de administración avanzado

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Dispositivos  │
│   SvelteKit     │◄──►│   FastAPI       │◄──►│      IoT        │
│   (Puerto 3000) │    │  (Puerto 8000)  │    │   (MQTT 1883)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   (Puerto 5432) │
                       └─────────────────┘
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos principal con JSONB
- **Redis** - Cache y sesiones
- **SQLAlchemy** - ORM avanzado
- **Alembic** - Migraciones de base de datos
- **Pydantic** - Validación de datos
- **JWT** - Autenticación segura

### Frontend
- **SvelteKit** - Framework web reactivo
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Framework CSS
- **Vite** - Build tool y dev server
- **Chart.js** - Gráficos
- **FullCalendar** - Calendario de eventos
- **Lucide Icons** - Iconografía moderna

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación
- **MQTT** - Comunicación IoT
- **Adminer** - Gestión de base de datos

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker
- Docker Compose

### Instalación y Ejecución

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd viejos_son_los_trapos
   ```

2. **Iniciar el entorno de desarrollo**
   ```bash
   ./start-dev.sh
   ```

   O manualmente:
   ```bash
   docker-compose up --build -d
   ```

3. **Acceder a los servicios**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs
   - Adminer (DB): http://localhost:8080
   - Panel Debug: http://localhost:3000/debug

## 📁 Estructura del Proyecto

```
viejos_son_los_trapos/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── core/           # Configuración y utilidades
│   │   ├── models/         # Modelos de base de datos
│   │   ├── schemas/        # Esquemas Pydantic
│   │   └── services/       # Lógica de negocio
│   ├── alembic/            # Migraciones
│   └── requirements.txt    # Dependencias Python
├── web-panel/              # Frontend SvelteKit
│   ├── src/
│   │   ├── components/     # Componentes Svelte
│   │   ├── lib/           # Utilidades y tipos
│   │   └── routes/        # Páginas de la aplicación
│   └── package.json       # Dependencias Node.js
├── docker/                 # Configuración Docker
├── docker-compose.yml      # Orquestación de servicios
└── start-dev.sh           # Script de inicio
```

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f web-panel

# Reiniciar un servicio
docker-compose restart backend

# Parar todos los servicios
docker-compose down

# Reconstruir un servicio
docker-compose build web-panel

# Ejecutar comandos dentro de un contenedor
docker-compose exec backend python -m pytest
docker-compose exec web-panel npm run test
```

### Hot Reload

- **Frontend**: Los cambios en `web-panel/src/` se reflejan automáticamente
- **Backend**: Los cambios en `backend/app/` reinician automáticamente el servidor

### Base de Datos

- **Acceso directo**: `docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db`
- **Interfaz web**: http://localhost:8080 (Adminer)
- **Migraciones**: `docker-compose exec backend alembic upgrade head`

## 📊 Funcionalidades

### 🏥 Gestión de Personas Bajo Cuidado
- Registro y edición de perfiles completos
- Información médica detallada (condiciones, medicamentos, alergias)
- Contactos de emergencia (médicos y familiares)
- Niveles de cuidado y movilidad
- Geolocalización y tracking en tiempo real

### 📱 Dispositivos IoT
- Registro y configuración avanzada de dispositivos
- Monitoreo de estado y conectividad
- Configuración de alertas personalizadas
- Soporte para múltiples tipos de sensores
- Firmware y configuración remota

### 🚨 Sistema de Alertas Avanzado
- Alertas en tiempo real con diferentes niveles de severidad
- Protocolos de emergencia configurables
- Notificaciones push y sonoras
- Escalamiento automático de alertas
- Integración con servicios de emergencia

### 📅 Eventos y Calendario
- Programación de eventos médicos y sociales
- Recordatorios de medicación inteligentes
- Visitas familiares y actividades
- Calendario integrado con FullCalendar
- Notificaciones automáticas

### 📈 Dashboard y Reportes
- Vista general del sistema con métricas en tiempo real
- Gráficos y estadísticas avanzadas
- Reportes personalizados con adjuntos (PDF, imágenes)
- Sistema de auditoría completo
- Exportación de datos

### 🧪 Sistema de Debug y Testing
- Panel de debug completo en `/debug`
- Generación automática de datos de prueba
- Simulación de eventos y alertas
- Testing de geolocalización y geofences
- Limpieza automática de datos de prueba

### 💰 Sistema de Facturación
- Gestión de suscripciones y servicios
- Registros de facturación completos
- Múltiples métodos de pago
- Estados de pago y vencimientos
- Números de factura únicos

### 🗺️ Geolocalización y Geofencing
- Tracking de ubicación en tiempo real
- Configuración de zonas seguras (geofences)
- Alertas de entrada/salida de zonas
- Historial de ubicaciones
- Integración con mapas

## 🔗 Reglas de Negocio Fundamentales

### 📦 Asociación de Dispositivos y Paquetes
**Regla Principal:** Un dispositivo siempre está asociado a un paquete, y un paquete siempre está asociado a un propietario específico.

**Flujo de Asociación:**
```
Dispositivo → Paquete → Propietario
```

**Tipos de Propietarios:**
- **🏥 Institución** (paquetes profesionales/institucionales)
- **👨‍👩‍👧‍👦 Familiar/Responsable Legal** (paquetes individuales)
- **👴 Persona Cuidada** (tipo autocuidado)

**Características del Paquete:**
- Número máximo de dispositivos permitidos
- Número máximo de usuarios
- Funcionalidades disponibles (monitoreo, alertas, reportes)
- Nivel de soporte técnico

### 👥 Roles del Sistema
**Roles Principales:**
- **admin** - Administrador del sistema (Sysadmin)
- **admin_institution** - Administrador de institución
- **caregiver** - Cuidador profesional
- **family_member** - Familiar de persona cuidada
- **caredperson** - Persona bajo cuidado
- **medical_staff** - Personal médico
- **freelance_caregiver** - Cuidador freelance
- **institution_staff** - Personal de institución

### 🏥 Tipos de Cuidado
**Categorías:**
- **self_care** - Autocuidado (persona independiente)
- **delegated_care** - Cuidado delegado (necesita representación)

### 📊 Estados del Sistema
**Categorías de Estados:**
- **general** - Estados generales (activo, inactivo, pendiente, etc.)
- **device** - Estados de dispositivos (online, offline, mantenimiento, error)
- **billing** - Estados de facturación (pagado, no pagado, vencido)
- **alert** - Estados de alertas (reconocido, resuelto, escalado)

### 🔄 Flujo de Datos IoT
**Secuencia de Eventos:**
1. **Dispositivo** detecta evento/condición
2. **Evento** se registra en el sistema
3. **Alerta** se genera si es necesario
4. **Notificación** se envía a usuarios relevantes
5. **Acción** se toma según protocolos configurados
- Zonas de seguridad configurables (geofences)
- Alertas automáticas de ubicación
- Historial de movimientos
- Múltiples fuentes de ubicación (GPS, WiFi, manual)

### 👥 Gestión de Usuarios y Roles
- Sistema de roles flexible (admin, family, employee, caregiver)
- Usuarios freelance con tarifas por hora
- Gestión de instituciones y centros de cuidado
- Permisos granulares por funcionalidad
- Autenticación JWT segura

### 🏢 Gestión Institucional
- Centros de cuidado y residencias
- Personal médico y administrativo
- Protocolos institucionales
- Reportes institucionales
- Integración con sistemas externos

## 🔒 Seguridad

- Autenticación JWT con refresh tokens
- Validación de datos con Pydantic
- CORS configurado
- Variables de entorno para configuración
- Sistema de auditoría completo
- Roles y permisos granulares

## 🧪 Testing

```bash
# Tests del backend
docker-compose exec backend python -m pytest

# Tests del frontend
docker-compose exec web-panel npm run test:ui
docker-compose exec web-panel npm run test:e2e

# Panel de debug para testing manual
# Acceder a: http://localhost:3000/debug
```

## 📝 API Documentation

La documentación completa de la API está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### Autenticación
- `POST /api/v1/auth/register` - Registro de usuarios
- `POST /api/v1/auth/login` - Login con JWT
- `POST /api/v1/auth/refresh` - Refresh de tokens

#### Gestión de Personas
- `GET /api/v1/cared-persons/` - Listar personas bajo cuidado
- `POST /api/v1/cared-persons/` - Crear nueva persona
- `PUT /api/v1/cared-persons/{id}` - Actualizar persona
- `DELETE /api/v1/cared-persons/{id}` - Eliminar persona

#### Dispositivos IoT
- `GET /api/v1/devices/` - Listar dispositivos
- `POST /api/v1/devices/` - Registrar dispositivo
- `PUT /api/v1/devices/{id}` - Actualizar dispositivo
- `DELETE /api/v1/devices/{id}` - Eliminar dispositivo

#### Alertas y Eventos
- `GET /api/v1/alerts/` - Listar alertas
- `POST /api/v1/alerts/` - Crear alerta
- `GET /api/v1/events/` - Listar eventos
- `POST /api/v1/events/` - Crear evento

#### Reportes
- `GET /api/v1/reports/` - Listar reportes
- `POST /api/v1/reports/` - Crear reporte con adjuntos
- `PUT /api/v1/reports/{id}` - Actualizar reporte
- `DELETE /api/v1/reports/{id}` - Eliminar reporte

#### Debug y Testing
- `GET /api/v1/debug/summary` - Resumen de datos de debug
- `POST /api/v1/debug/generate-test-data` - Generar datos de prueba
- `POST /api/v1/debug/clean-test-data` - Limpiar datos de prueba

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📋 Roadmap

### ✅ Completado
- [x] Backend FastAPI completo
- [x] Frontend SvelteKit funcional
- [x] Sistema de autenticación JWT
- [x] Gestión de personas bajo cuidado
- [x] Sistema de alertas básico
- [x] Panel de debug y testing
- [x] Sistema de reportes con adjuntos
- [x] Geolocalización y geofencing
- [x] Sistema de facturación
- [x] Protocolos de emergencia

### 🔄 En Desarrollo
- [ ] App móvil Flutter
- [ ] Integración con servicios de emergencia
- [ ] Análisis de IA para detección de patrones
- [ ] Notificaciones push avanzadas

### 📅 Próximas Funcionalidades
- [ ] Integración con dispositivos IoT físicos
- [ ] Sistema de videovigilancia
- [ ] Análisis de comportamiento avanzado
- [ ] Integración con sistemas de salud
- [ ] Certificaciones de accesibilidad 