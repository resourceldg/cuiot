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

## 🏗️ Arquitectura del Proyecto

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/           # Endpoints de la API
│   ├── core/          # Configuración y utilidades
│   ├── models/        # Modelos de SQLAlchemy
│   ├── schemas/       # Esquemas Pydantic
│   └── services/      # Lógica de negocio
├── alembic/           # Migraciones de base de datos
├── tests/             # Tests unitarios
└── main.py           # Punto de entrada
```

### Panel Web (Svelte)
```
web-panel/
├── src/
│   ├── components/    # Componentes reutilizables
│   ├── pages/         # Páginas de la aplicación
│   ├── stores/        # Stores de Svelte
│   └── lib/           # Utilidades y configuraciones
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
- `users` - Usuarios (familiares)
- `elderly_persons` - Adultos mayores
- `devices` - Dispositivos IoT
- `events` - Eventos de sensores
- `alerts` - Alertas del sistema
- `reminders` - Recordatorios

## 🔌 MQTT

### Configuración
- **Broker**: localhost:1883
- **WebSocket**: localhost:9001
- **Tópicos principales**:
  - `viejos_trapos/+/events` - Eventos de dispositivos
  - `viejos_trapos/+/heartbeat` - Heartbeat de dispositivos
  - `viejos_trapos/+/config` - Configuración de dispositivos

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

## 📝 Convenciones de Código

### Python (Backend)
- Usar **Black** para formateo
- Usar **isort** para imports
- Usar **flake8** para linting
- Documentar funciones con docstrings

### JavaScript/TypeScript (Panel Web)
- Usar **Prettier** para formateo
- Usar **ESLint** para linting
- Usar **TypeScript** estrictamente

### Dart (App Móvil)
- Seguir las convenciones de Flutter
- Usar **flutter_lints**
- Documentar clases y métodos

## 🚀 Deploy

### Desarrollo
```bash
./start-dev.sh
```

### Producción
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🐛 Debugging

### Backend
- Logs en `docker-compose logs -f backend`
- Debugger en VS Code con configuración Python

### Panel Web
- DevTools del navegador
- Logs en consola del navegador

### App Móvil
- Flutter Inspector
- Logs en `flutter logs`

## 📚 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Svelte Documentation](https://svelte.dev/docs)
- [Flutter Documentation](https://flutter.dev/docs)
- [Docker Documentation](https://docs.docker.com/)
- [MQTT Documentation](https://mqtt.org/documentation)

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