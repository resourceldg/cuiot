# 🛠️ Guía de Desarrollo - Viejos Son Los Trapos

## 📋 Prerrequisitos

- **Docker** y **Docker Compose** instalados
- **Git** para control de versiones
- **Node.js 18+** (para desarrollo local del panel web)
- **Python 3.11+** (para desarrollo local del backend)
- **Flutter SDK** (para desarrollo de la app móvil)

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd viejos_son_los_trapos
```

### 2. Iniciar entorno de desarrollo
```bash
./start-dev.sh
```

O manualmente:
```bash
docker-compose up --build -d
```

### 3. Verificar servicios
- Backend API: http://localhost:8000
- Panel Web: http://localhost:3000
- Adminer (DB): http://localhost:8080
- Documentación API: http://localhost:8000/docs
- Panel Debug: http://localhost:3000/debug

## 🏗️ Arquitectura del Proyecto

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/           # Endpoints de la API
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py              # Autenticación JWT
│   │           ├── users.py             # Gestión de usuarios
│   │           ├── cared_persons.py     # Personas bajo cuidado
│   │           ├── devices.py           # Dispositivos IoT
│   │           ├── alerts.py            # Sistema de alertas
│   │           ├── events.py            # Eventos del sistema
│   │           ├── reminders.py         # Recordatorios
│   │           ├── reports.py           # Reportes con adjuntos
│   │           ├── debug.py             # Sistema de debug
│   │           ├── health.py            # Health checks
│   │           └── admin.py             # Administración
│   ├── core/          # Configuración y utilidades
│   │   ├── config.py      # Configuración de la aplicación
│   │   ├── database.py    # Conexión a base de datos
│   │   ├── auth.py        # Autenticación y autorización
│   │   └── exceptions.py  # Manejo de excepciones
│   ├── models/        # Modelos de SQLAlchemy
│   │   ├── user.py                    # Usuarios y roles
│   │   ├── cared_person.py            # Personas bajo cuidado
│   │   ├── device.py                  # Dispositivos IoT
│   │   ├── alert.py                   # Alertas del sistema
│   │   ├── event.py                   # Eventos
│   │   ├── reminder.py                # Recordatorios
│   │   ├── report.py                  # Reportes con adjuntos
│   │   ├── emergency_protocol.py      # Protocolos de emergencia
│   │   ├── service_subscription.py    # Suscripciones de servicio
│   │   ├── billing_record.py          # Registros de facturación
│   │   ├── location_tracking.py       # Geolocalización
│   │   ├── geofence.py                # Geofencing
│   │   ├── debug_event.py             # Eventos de debug
│   │   └── audit_log.py               # Log de auditoría
│   ├── schemas/       # Esquemas Pydantic
│   └── services/      # Lógica de negocio
│       ├── auth.py        # Servicio de autenticación
│       ├── user.py        # Servicio de usuarios
│       ├── device.py      # Servicio de dispositivos
│       ├── alert.py       # Servicio de alertas
│       ├── debug.py       # Servicio de debug
│       └── audit_log.py   # Servicio de auditoría
├── alembic/           # Migraciones de base de datos
├── tests/             # Tests unitarios
└── main.py           # Punto de entrada
```

### Panel Web (Svelte)
```
web-panel/
├── src/
│   ├── components/    # Componentes reutilizables
│   │   ├── Toast.svelte               # Notificaciones
│   │   ├── ProfileCard.svelte         # Tarjeta de perfil
│   │   ├── DeviceForm.svelte          # Formulario de dispositivos
│   │   ├── EventForm.svelte           # Formulario de eventos
│   │   ├── ElderlyPersonForm.svelte   # Formulario de personas
│   │   └── PreferencesSection.svelte  # Sección de preferencias
│   ├── routes/        # Páginas de la aplicación
│   │   ├── +layout.svelte             # Layout principal
│   │   ├── +page.svelte               # Página de inicio
│   │   ├── login/                     # Autenticación
│   │   ├── register/                  # Registro
│   │   ├── debug/                     # Panel de debug
│   │   └── dashboard/                 # Dashboard principal
│   │       ├── +layout.svelte         # Layout del dashboard
│   │       ├── overview/              # Vista general
│   │       ├── human/                 # Gestión de personas
│   │       ├── devices/               # Dispositivos IoT
│   │       ├── alerts/                # Sistema de alertas
│   │       ├── events/                # Eventos
│   │       ├── reminders/             # Recordatorios
│   │       ├── reports/               # Reportes con adjuntos
│   │       ├── calendar/              # Calendario
│   │       ├── profile/               # Perfil de usuario
│   │       └── admin/                 # Administración
│   ├── lib/           # Utilidades y configuraciones
│   │   ├── api.js                     # Servicios de API
│   │   └── types/                     # Tipos TypeScript
│   └── app.css        # Estilos globales
├── static/            # Archivos estáticos
└── package.json
```

### App Móvil (Flutter)
```
mobile-app/
├── lib/
│   ├── models/        # Modelos de datos
│   ├── services/      # Servicios de API
│   ├── screens/       # Pantallas de la app
│   ├── widgets/       # Widgets reutilizables
│   └── utils/         # Utilidades
├── android/           # Configuración Android
├── ios/              # Configuración iOS
└── pubspec.yaml
```

## 🔧 Comandos Útiles

### Docker
```bash
# Ver logs de un servicio
docker-compose logs -f backend

# Reiniciar un servicio
docker-compose restart backend

# Detener todos los servicios
docker-compose down

# Reconstruir un servicio
docker-compose up --build backend
```

### Base de Datos
```bash
# Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Crear nueva migración
docker-compose exec backend alembic revision --autogenerate -m "descripción"

# Resetear base de datos
docker-compose down -v
docker-compose up -d
```

### Desarrollo Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Panel Web
```bash
cd web-panel
npm install
npm run dev
```

#### App Móvil
```bash
cd mobile-app
flutter pub get
flutter run
```

## 📊 Base de Datos

### Conexión
- **Host**: localhost
- **Puerto**: 5432
- **Base de datos**: viejos_trapos_db
- **Usuario**: viejos_trapos_user
- **Contraseña**: viejos_trapos_pass

### Tablas Principales
- `users` - Usuarios del sistema
- `roles` - Roles y permisos
- `user_roles` - Asignación de roles a usuarios
- `institutions` - Centros de cuidado
- `cared_persons` - Personas bajo cuidado
- `devices` - Dispositivos IoT
- `events` - Eventos del sistema
- `alerts` - Alertas del sistema
- `reminders` - Recordatorios
- `reports` - Reportes con adjuntos
- `emergency_protocols` - Protocolos de emergencia
- `service_subscriptions` - Suscripciones de servicio
- `billing_records` - Registros de facturación
- `location_tracking` - Geolocalización
- `geofences` - Zonas de seguridad
- `debug_events` - Eventos de debug
- `audit_logs` - Log de auditoría

## 🔌 MQTT

### Configuración
- **Broker**: localhost:1883
- **WebSocket**: localhost:9001
- **Tópicos principales**:
  - `viejos_trapos/+/events` - Eventos de dispositivos
  - `viejos_trapos/+/heartbeat` - Heartbeat de dispositivos
  - `viejos_trapos/+/config` - Configuración de dispositivos
  - `viejos_trapos/+/location` - Datos de geolocalización

### Ejemplo de mensaje
```json
{
  "device_id": "ESP32_001",
  "event_type": "movement",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "location": "sala_estar",
    "confidence": 0.95
  }
}
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
pytest --cov=app
```

### Panel Web
```bash
cd web-panel
npm test
```

### App Móvil
```bash
cd mobile-app
flutter test
```

### Panel de Debug
El sistema incluye un panel de debug completo en `/debug` que permite:
- Generar datos de prueba automáticamente
- Simular eventos y alertas
- Probar geolocalización y geofences
- Limpiar datos de prueba
- Ver estadísticas del sistema

## 📝 Convenciones de Código

### Python (Backend)
- Usar **Black** para formateo
- Usar **isort** para imports
- Usar **flake8** para linting
- Documentar funciones con docstrings

```python
def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Crear un nuevo usuario en el sistema.
    
    Args:
        db: Sesión de base de datos
        user_data: Datos del usuario a crear
        
    Returns:
        User: Usuario creado
        
    Raises:
        HTTPException: Si el email ya existe
    """
    # Implementación
    pass
```

### JavaScript/TypeScript (Frontend)
- Usar **Prettier** para formateo
- Usar **ESLint** para linting
- Usar **Svelte** con TypeScript
- Documentar componentes con comentarios

```typescript
/**
 * Componente para mostrar información de una persona bajo cuidado
 * @param {Object} person - Datos de la persona
 * @param {string} person.name - Nombre completo
 * @param {number} person.age - Edad
 */
```

## 🔒 Seguridad

### Autenticación
- JWT tokens con refresh
- Tokens expiran en 30 minutos
- Refresh tokens expiran en 7 días
- Logout invalida tokens

### Autorización
- Roles granulares (admin, family, employee, caregiver)
- Permisos por funcionalidad
- Validación en endpoints y servicios

### Validación de Datos
- Pydantic schemas en backend
- Validación en frontend
- Sanitización de inputs

## 📊 Monitoreo y Logs

### Logs del Sistema
- **Backend**: Structlog con formato JSON
- **Frontend**: Console logs en desarrollo
- **Docker**: Logs de contenedores

### Métricas
- Health checks automáticos
- Métricas de base de datos
- Estadísticas de uso

## 🚀 Deployment

### Desarrollo
```bash
./start-dev.sh
```

### Staging
```bash
docker-compose -f docker-compose.staging.yml up -d
```

### Producción
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Configuración

### Variables de Entorno
```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
SECRET_KEY=your-secret-key
ENVIRONMENT=development

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Configuración de Base de Datos
- PostgreSQL 15+
- Extensión JSONB habilitada
- Índices en campos de búsqueda
- Backup automático configurado

## 📚 Recursos Adicionales

### Documentación
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Herramientas
- [Adminer](http://localhost:8080) - Gestión de base de datos
- [Swagger UI](http://localhost:8000/docs) - Documentación de API
- [Panel Debug](http://localhost:3000/debug) - Testing y debug

## 🆘 Solución de Problemas

### Problemas Comunes

#### Backend no inicia
```bash
# Verificar logs
docker-compose logs backend

# Reconstruir contenedor
docker-compose up --build backend
```

#### Base de datos no conecta
```bash
# Verificar estado de PostgreSQL
docker-compose ps postgres

# Reiniciar base de datos
docker-compose restart postgres
```

#### Frontend no carga
```bash
# Verificar logs
docker-compose logs web-panel

# Limpiar cache
docker-compose exec web-panel npm run build
```

### Debug y Testing
- Usar el panel de debug en `/debug`
- Generar datos de prueba automáticamente
- Simular diferentes escenarios
- Limpiar datos cuando sea necesario

## 🤝 Contribución

### Flujo de Trabajo
1. Crear rama desde `main`
2. Desarrollar funcionalidad
3. Agregar tests
4. Actualizar documentación
5. Crear Pull Request

### Estándares de Código
- Seguir convenciones establecidas
- Agregar tests para nuevas funcionalidades
- Documentar cambios importantes
- Mantener compatibilidad con APIs existentes

## Workflows de desarrollo optimizados

### 🚀 Setup inicial o reset completo
```bash
# Ejecuta todo el ciclo: reset, migraciones, datos dummy
sudo chmod +x scripts/setup-dev.sh
sudo ./scripts/setup-dev.sh
```

### 🔧 Migración rápida (cambios menores)
```bash
# Para agregar columnas o cambios menores sin reset completo
sudo chmod +x scripts/quick-migrate.sh
sudo ./scripts/quick-migrate.sh
```

### 📝 Agregar nuevas columnas/campos
1. **Actualizar el modelo** en `backend/app/models/`
2. **Agregar la migración** en `docker/postgres/complete_migration.sql`
3. **Ejecutar migración rápida**:
   ```bash
   sudo ./scripts/quick-migrate.sh
   ```

### 🔄 Ciclo de desarrollo recomendado
1. **Desarrollo normal**: Usar `quick-migrate.sh` para cambios menores
2. **Cambios mayores**: Usar `setup-dev.sh` para reset completo
3. **Validación**: Verificar que no hay errores en logs de Docker

## Troubleshooting y buenas prácticas de integridad de datos

### Errores comunes y soluciones rápidas

#### 1. Error de Enum en alertas
- **Síntoma**: Error 500 en `/api/v1/alerts/` relacionado con valor inválido de Enum
- **Causa**: Hay valores inválidos en la columna `alert_type` de la tabla `alerts`
- **Solución**: 
  ```bash
  # Limpiar alertas inválidas
  sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -c "DELETE FROM alerts WHERE alert_type NOT IN ('no_movement', 'sos', 'temperature', 'medication', 'fall', 'heart_rate', 'blood_pressure');"
  
  # Recargar datos dummy
  sudo docker-compose exec backend python -m app.scripts.load_dummy_data
  ```

#### 2. Adultos mayores no visibles en el frontend
- **Síntoma**: La sección "Gestión Humana" está vacía
- **Causa**: Campo `is_deleted` en `true` o error de validación JSON
- **Solución**:
  ```bash
  # Verificar estado de adultos mayores
  sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -c "SELECT id, first_name, last_name, is_deleted FROM elderly_persons;"
  
  # Si hay problemas, recargar datos
  sudo docker-compose exec backend python -m app.scripts.load_dummy_data
  ```

#### 3. Sincronización de modelos y datos
- **Síntoma**: Errores de validación Pydantic o campos faltantes
- **Causa**: Desincronización entre modelo ORM y base de datos
- **Solución**:
  ```bash
  # Aplicar migración completa
  sudo docker cp docker/postgres/complete_migration.sql viejos_trapos_postgres:/tmp/complete_migration.sql
  sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -f /tmp/complete_migration.sql
  
  # Reiniciar servicios
  sudo docker-compose restart backend web-panel
  
  # Recargar datos dummy
  sudo docker-compose exec backend python -m app.scripts.load_dummy_data
  ```

#### 4. Logs y diagnóstico
- **Ver logs del backend**:
  ```bash
  sudo docker-compose logs --tail=100 backend
  ```
- **Ver logs del frontend**:
  ```bash
  sudo docker-compose logs --tail=100 web-panel
  ```
- **Probar API desde contenedor**:
  ```bash
  sudo docker-compose exec web-panel wget -qO- http://backend:8000/api/v1/elderly-persons/
  ```

#### 5. Usuarios y credenciales
- **Credenciales por defecto**:
  - `maria.gonzalez@example.com` / `password123`
  - `carlos.rodriguez@example.com` / `password123`
  - `lucia.martinez@example.com` / `password123`
- **Si no funciona login**: Recargar datos dummy para regenerar hashes

### Validación de integridad de datos

#### Comandos útiles para diagnóstico
```bash
# Verificar estado de la base de datos
sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -c "SELECT * FROM validate_data_integrity();"

# Verificar alertas válidas
sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -c "SELECT alert_type, COUNT(*) FROM alerts GROUP BY alert_type;"

# Verificar dispositivos con estados válidos
sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -c "SELECT status, type, COUNT(*) FROM devices GROUP BY status, type;"
```

### Prevención de errores

#### 1. Script de datos dummy robusto
- **Validación automática**: Solo genera valores válidos según enums
- **Manejo de errores**: Rollback automático si algo falla
- **Validación de integridad**: Verifica que todos los datos sean consistentes

#### 2. Migración con constraints
- **Constraints de base de datos**: Previenen valores inválidos
- **Triggers de validación**: Validan datos antes de insertar
- **Función de validación**: Verifica integridad completa

#### 3. Workflow seguro
- **Siempre usar scripts**: No ejecutar comandos manuales
- **Validar después de cambios**: Verificar que todo funciona
- **Logs detallados**: Revisar logs para detectar problemas temprano

### Comandos de administración

#### Reinicio completo del entorno
```bash
# Parar y limpiar todo
sudo docker-compose down -v

# Reconstruir y levantar
sudo docker-compose up --build -d

# Esperar a que estén listos
sleep 15

# Aplicar migraciones
sudo docker cp docker/postgres/complete_migration.sql viejos_trapos_postgres:/tmp/complete_migration.sql
sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -f /tmp/complete_migration.sql

# Cargar datos dummy
sudo docker-compose exec backend python -m app.scripts.load_dummy_data
```

#### Verificación rápida
```bash
# Verificar que todos los servicios están corriendo
sudo docker-compose ps

# Verificar que la API responde
sudo docker-compose exec web-panel wget -qO- http://backend:8000/api/v1/health

# Verificar que hay datos
sudo docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db -c "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM elderly_persons;"
```

### Recomendaciones para desarrollo

1. **Siempre usar los scripts**: `setup-dev.sh` y `quick-migrate.sh`
2. **Revisar logs después de cambios**: Detectar problemas temprano
3. **Validar datos después de migraciones**: Usar `validate_data_integrity()`
4. **Mantener enums sincronizados**: Backend, frontend y base de datos
5. **Documentar cambios**: Actualizar esta documentación cuando sea necesario 