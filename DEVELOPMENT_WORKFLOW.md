# 🚀 Flujo de Trabajo de Desarrollo Completamente Dockerizado

Este documento describe el nuevo enfoque **100% dockerizado** para el desarrollo del sistema "Viejos Son Los Trapos".

## 🎯 Filosofía del Enfoque

**Todo se ejecuta dentro de Docker Compose** - No hay dependencias locales, no hay instalaciones manuales, no hay conflictos de versiones.

### ✅ Beneficios

- **Consistencia**: Mismo entorno en desarrollo, testing y producción
- **Aislamiento**: Cada desarrollador tiene su propio entorno
- **Simplicidad**: Un solo comando para todo
- **Portabilidad**: Funciona en cualquier máquina con Docker
- **Limpieza**: Fácil reset y limpieza completa

## 🛠️ Comandos Principales

### Inicialización (Primera vez)

```bash
# Inicializar todo el entorno de desarrollo
./scripts/dev-workflow.sh init
```

Este comando:
- Limpia cualquier entorno anterior
- Construye todas las imágenes Docker
- Levanta todos los servicios
- Aplica migraciones a ambas bases de datos
- Verifica que todo funcione correctamente

### Flujo Diario

```bash
# 1. Iniciar servicios
./scripts/dev-workflow.sh start

# 2. Después de cambios en modelos
./scripts/dev-workflow.sh migrate

# 3. Ejecutar tests
./scripts/dev-workflow.sh test

# 4. Detener servicios
./scripts/dev-workflow.sh stop
```

### Comandos Útiles

```bash
# Ver estado de todos los servicios
./scripts/dev-workflow.sh status

# Sincronizar bases de datos (desarrollo → testing)
./scripts/dev-workflow.sh sync

# Abrir shell en el contenedor backend
./scripts/dev-workflow.sh shell

# Ver logs en tiempo real
./scripts/dev-workflow.sh logs

# Limpiar todo (cuidado: elimina datos)
./scripts/dev-workflow.sh clean
```

## 🏗️ Arquitectura Docker

### Servicios

- **postgres**: Base de datos de desarrollo (puerto 5432)
- **postgres_test**: Base de datos de testing (puerto 5433)
- **backend**: API FastAPI con hot-reload
- **web-panel**: Frontend SvelteKit
- **redis**: Cache y sesiones
- **mqtt**: Broker para dispositivos IoT
- **adminer**: Interfaz web para PostgreSQL

### Volúmenes

- **postgres_data**: Datos de desarrollo
- **postgres_test_data**: Datos de testing
- **redis_data**: Cache de Redis
- **mqtt_data**: Datos de MQTT

## 🔄 Flujo de Trabajo Detallado

### 1. Desarrollo de Funcionalidades

```bash
# Iniciar entorno
./scripts/dev-workflow.sh start

# Hacer cambios en el código (hot-reload automático)
# ...

# Después de cambios en modelos SQLAlchemy
./scripts/dev-workflow.sh migrate

# Ejecutar tests
./scripts/dev-workflow.sh test
```

### 2. Trabajo con Bases de Datos

```bash
# Ver estado de migraciones
./scripts/dev-workflow.sh status

# Generar nueva migración automáticamente
./scripts/dev-workflow.sh sync

# Conectar directamente a las bases de datos
# Desarrollo: localhost:5432
# Testing: localhost:5433
# Adminer: http://localhost:8080
```

### 3. Debugging y Logs

```bash
# Ver logs de todos los servicios
./scripts/dev-workflow.sh logs

# Ver logs de un servicio específico
docker-compose logs backend

# Abrir shell en el contenedor
./scripts/dev-workflow.sh shell

# Dentro del shell:
# - ENVIRONMENT=development alembic current
# - ENVIRONMENT=test alembic current
# - pytest tests/ -v
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Ejecutar todos los tests
./scripts/dev-workflow.sh test

# Ejecutar tests específicos
docker-compose exec backend bash -c "cd /app && ENVIRONMENT=test pytest tests/test_users.py -v"

# Ejecutar tests con coverage
docker-compose exec backend bash -c "cd /app && ENVIRONMENT=test pytest tests/ --cov=app --cov-report=html"
```

### Base de Datos de Testing

- **Aislamiento completo**: Base de datos separada
- **Limpieza automática**: Se limpia entre tests
- **Migraciones automáticas**: Se aplican al inicio de la sesión de tests
- **Sin `Base.metadata.create_all()`**: Solo migraciones de Alembic

## 🔧 Configuración

### Variables de Entorno

El sistema detecta automáticamente el entorno:

- **Desarrollo**: `ENVIRONMENT=development`
- **Testing**: `ENVIRONMENT=test`

### URLs de Base de Datos

- **Desarrollo**: `postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db`
- **Testing**: `postgresql://viejos_trapos_user:viejos_trapos_pass@postgres_test:5432/viejos_trapos_test_db`

## 🚨 Solución de Problemas

### Error: "Puerto ya en uso"

```bash
# Verificar qué está usando el puerto
sudo lsof -i :5432
sudo lsof -i :5433

# Limpiar todo y reiniciar
./scripts/dev-workflow.sh clean
./scripts/dev-workflow.sh init
```

### Error: "Migraciones fallaron"

```bash
# Verificar estado
./scripts/dev-workflow.sh status

# Resetear bases de datos
./scripts/dev-workflow.sh clean
./scripts/dev-workflow.sh init
```

### Error: "Tests fallaron"

```bash
# Verificar que la base de datos de testing esté lista
./scripts/dev-workflow.sh status

# Resetear solo testing
docker-compose exec backend bash -c "cd /app && ENVIRONMENT=test alembic downgrade base"
docker-compose exec backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
```

### Error: "Docker no está corriendo"

```bash
# Iniciar Docker Desktop
# Luego ejecutar
./scripts/dev-workflow.sh init
```

## 📊 Monitoreo

### Estado de Servicios

```bash
# Ver estado general
./scripts/dev-workflow.sh status

# Ver logs en tiempo real
./scripts/dev-workflow.sh logs

# Ver logs de un servicio específico
docker-compose logs -f backend
```

### Conectar a Bases de Datos

```bash
# Desarrollo (puerto 5432)
psql -h localhost -p 5432 -U viejos_trapos_user -d viejos_trapos_db

# Testing (puerto 5433)
psql -h localhost -p 5433 -U viejos_trapos_user -d viejos_trapos_test_db

# Adminer (interfaz web)
# http://localhost:8080
```

## 🔄 Automatización

### Git Hooks (Opcional)

```bash
# En .git/hooks/pre-commit
#!/bin/bash
./scripts/dev-workflow.sh test
```

### CI/CD

```bash
# En tu pipeline
docker-compose -f docker-compose.test.yml up -d
docker-compose exec backend bash -c "cd /app && ENVIRONMENT=test alembic upgrade head"
docker-compose exec backend bash -c "cd /app && ENVIRONMENT=test pytest tests/"
```

## 📝 Notas Importantes

1. **Nunca ejecutes comandos localmente** - Todo debe ir dentro de Docker
2. **Siempre usa `./scripts/dev-workflow.sh`** - Es la interfaz principal
3. **Las migraciones son automáticas** - No crees tablas manualmente
4. **Los tests usan base de datos separada** - No hay contaminación
5. **Hot-reload está habilitado** - Los cambios se reflejan automáticamente

## 🎯 Flujo Recomendado

### Para Nuevos Desarrolladores

1. `git clone <repo>`
2. `cd viejos_son_los_trapos`
3. `./scripts/dev-workflow.sh init`
4. `./scripts/dev-workflow.sh start`
5. ¡Listo para desarrollar!

### Para Desarrollo Diario

1. `./scripts/dev-workflow.sh start`
2. Hacer cambios en el código
3. `./scripts/dev-workflow.sh migrate` (si cambiaste modelos)
4. `./scripts/dev-workflow.sh test`
5. `./scripts/dev-workflow.sh stop`

### Para Cambios en Modelos

1. Modificar modelos en `backend/app/models/`
2. `./scripts/dev-workflow.sh sync`
3. `./scripts/dev-workflow.sh test`
4. Commit y push

Este enfoque garantiza un desarrollo **consistente, limpio y profesional** sin conflictos de dependencias o configuraciones. 