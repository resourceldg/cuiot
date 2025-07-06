# Flujo de Trabajo de Bases de Datos

Este documento describe cómo trabajar con bases de datos separadas para desarrollo y testing, manteniéndolas sincronizadas automáticamente.

## 🏗️ Arquitectura

El sistema utiliza **dos bases de datos PostgreSQL separadas**:

- **Desarrollo**: `viejos_trapos_db` (puerto 5432)
- **Testing**: `viejos_trapos_test_db` (puerto 5433)

## ✅ Estado Actual

**🎉 NORMALIZACIÓN COMPLETA**: Todas las tablas han sido normalizadas exitosamente:
- ✅ Status fields → `status_types` table
- ✅ Care types → `care_types` table  
- ✅ Device types → `device_types` table
- ✅ Alert types → `alert_types` table
- ✅ Event types → `event_types` table
- ✅ Reminder types → `reminder_types` table
- ✅ Service types → `service_types` table
- ✅ Caregiver assignment types → `caregiver_assignment_types` table
- ✅ Shift observation types → `shift_observation_types` table
- ✅ Referral types → `referral_types` table
- ✅ Relationship types → `relationship_types` table

**🧪 TESTS**: 100% de tests pasando (98/98)

## 🚀 Configuración Inicial

### 1. Primera vez que configuras el proyecto

```bash
# Desde la raíz del proyecto
./scripts/setup_databases.sh init
```

Este comando:
- Levanta los servicios de Docker (postgres y postgres_test)
- Aplica todas las migraciones de Alembic a ambas bases de datos
- Inicializa los catálogos normalizados automáticamente
- Verifica que las conexiones funcionen correctamente

### 2. Verificar el estado

```bash
./scripts/setup_databases.sh status
```

## 🔄 Flujo de Trabajo Diario

### Cuando haces cambios en los modelos

1. **Modifica los modelos** en `backend/app/models/`
2. **Genera una nueva migración**:
   ```bash
   cd backend
   ENVIRONMENT=development alembic revision --autogenerate -m "descripción del cambio"
   ```
3. **Aplica la migración a desarrollo**:
   ```bash
   ENVIRONMENT=development alembic upgrade head
   ```
4. **Sincroniza con testing**:
   ```bash
   ./scripts/setup_databases.sh sync
   ```

### Comando rápido de sincronización

```bash
# Desde la raíz del proyecto
./scripts/setup_databases.sh sync
```

Este comando automáticamente:
- Detecta cambios en desarrollo
- Genera migraciones si es necesario
- Aplica cambios a testing
- Mantiene ambas bases de datos sincronizadas

## 🧪 Trabajando con Tests

### Ejecutar tests

```bash
cd backend
ENVIRONMENT=test pytest tests/ -v
```

### Resetear base de datos de testing

```bash
./scripts/setup_databases.sh reset-test
```

## 🛠️ Comandos Útiles

### Desde la raíz del proyecto

```bash
# Inicializar todo
./scripts/setup_databases.sh init

# Sincronizar cambios
./scripts/setup_databases.sh sync

# Ver estado
./scripts/setup_databases.sh status

# Resetear testing
./scripts/setup_databases.sh reset-test

# Limpiar todo (cuidado: elimina todos los datos)
./scripts/setup_databases.sh clean
```

### Desde el directorio backend

```bash
# Migraciones para desarrollo
make migrate-dev

# Migraciones para testing
make migrate-test

# Ejecutar tests
make run-tests

# Ver estado de migraciones
make status
```

## 🔧 Configuración Técnica

### Variables de Entorno

El sistema usa estas variables de entorno:

- `ENVIRONMENT`: `development` o `test`
- `DATABASE_URL`: URL de la base de datos de desarrollo
- `TEST_DATABASE_URL`: URL de la base de datos de testing

### Configuración de Alembic

Alembic está configurado para:
- Detectar automáticamente el entorno
- Usar la base de datos correcta según `ENVIRONMENT`
- Generar migraciones automáticas desde los modelos

### Docker Compose

El `docker-compose.yml` incluye:
- `postgres`: Base de datos de desarrollo (puerto 5432)
- `postgres_test`: Base de datos de testing (puerto 5433)

## 🚨 Solución de Problemas

### Error: "Base de datos no existe"

```bash
# Reinicializar todo
./scripts/setup_databases.sh clean
./scripts/setup_databases.sh init
```

### Error: "Migraciones desincronizadas"

```bash
# Resetear testing y sincronizar
./scripts/setup_databases.sh reset-test
./scripts/setup_databases.sh sync
```

### Error: "Docker no está corriendo"

```bash
# Iniciar Docker Desktop
# Luego ejecutar
./scripts/setup_databases.sh init
```

### Error: "Puerto ya en uso"

```bash
# Verificar qué está usando el puerto
sudo lsof -i :5432
sudo lsof -i :5433

# Detener servicios conflictivos
docker-compose down
```

## 📊 Monitoreo

### Ver logs de las bases de datos

```bash
# Logs de desarrollo
docker-compose logs postgres

# Logs de testing
docker-compose logs postgres_test
```

### Conectar directamente a las bases de datos

```bash
# Desarrollo (puerto 5432)
psql -h localhost -p 5432 -U viejos_trapos_user -d viejos_trapos_db

# Testing (puerto 5433)
psql -h localhost -p 5433 -U viejos_trapos_user -d viejos_trapos_test_db
```

### Usar Adminer (interfaz web)

Accede a http://localhost:8080 y conecta a:
- **Desarrollo**: `postgres:5432/viejos_trapos_db`
- **Testing**: `postgres_test:5432/viejos_trapos_test_db`

## 🔄 Automatización

### Git Hooks (Opcional)

Puedes configurar hooks de Git para sincronizar automáticamente:

```bash
# En .git/hooks/pre-commit
#!/bin/bash
./scripts/setup_databases.sh sync
```

### CI/CD

Para integración continua, usa:

```bash
# En tu pipeline
ENVIRONMENT=test alembic upgrade head
ENVIRONMENT=test pytest tests/
```

## 📝 Notas Importantes

1. **Nunca modifiques directamente la base de datos de testing** - siempre usa migraciones
2. **Siempre ejecuta `sync` después de cambios en desarrollo**
3. **Los tests usan automáticamente la base de datos de testing**
4. **Las migraciones se aplican en orden cronológico**
5. **Backup automático**: Los volúmenes de Docker preservan los datos

## 🎯 Beneficios

- ✅ **Aislamiento**: Desarrollo y testing completamente separados
- ✅ **Sincronización automática**: Cambios se propagan automáticamente
- ✅ **Consistencia**: Ambas bases de datos siempre tienen la misma estructura
- ✅ **Seguridad**: No hay riesgo de contaminar datos de producción
- ✅ **Flexibilidad**: Puedes resetear testing sin afectar desarrollo 