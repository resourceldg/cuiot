# Makefile para gestión de bases de datos y sincronización
.PHONY: help sync reset-test status migrate-dev migrate-test clean-test run-tests

# Variables
PYTHON = python3
ALEMBIC = alembic
DOCKER_COMPOSE = docker-compose

help:
	@echo "Comandos disponibles:"
	@echo "  sync        - Sincroniza base de datos de desarrollo con testing"
	@echo "  reset-test  - Resetea la base de datos de testing"
	@echo "  status      - Muestra el estado de las migraciones"
	@echo "  migrate-dev - Aplica migraciones a desarrollo"
	@echo "  migrate-test- Aplica migraciones a testing"
	@echo "  clean-test  - Limpia la base de datos de testing"
	@echo "  run-tests   - Ejecuta los tests"
	@echo "  help        - Muestra esta ayuda"

# Sincronización de bases de datos
sync:
	@echo "🔄 Sincronizando bases de datos..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && python3 scripts/sync_databases.py sync"

# Reset de base de datos de testing
reset-test:
	@echo "🔄 Reseteando base de datos de testing..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && python3 scripts/sync_databases.py reset-test"

# Estado de las migraciones
status:
	@echo "📊 Mostrando estado de migraciones..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && python3 scripts/sync_databases.py status"

# Migraciones para desarrollo
migrate-dev:
	@echo "🔧 Aplicando migraciones a desarrollo..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && ENVIRONMENT=development $(ALEMBIC) upgrade head"

# Migraciones para testing
migrate-test:
	@echo "🧪 Aplicando migraciones a testing..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && ENVIRONMENT=test $(ALEMBIC) upgrade head"

# Limpiar base de datos de testing
clean-test:
	@echo "🧹 Limpiando base de datos de testing..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && ENVIRONMENT=test $(ALEMBIC) downgrade base"
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && ENVIRONMENT=test $(ALEMBIC) upgrade head"

# Ejecutar tests
run-tests:
	@echo "🧪 Ejecutando tests..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && ENVIRONMENT=test pytest tests/ -v"

# Generar nueva migración
migrate-new:
	@echo "📝 Generando nueva migración..."
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && $(ALEMBIC) revision --autogenerate -m \"$(message)\""

# Mostrar historial de migraciones
history:
	@echo "📚 Historial de migraciones:"
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && $(ALEMBIC) history"

# Estado actual
current:
	@echo "📍 Estado actual:"
	$(DOCKER_COMPOSE) exec -T backend bash -c "cd /app && $(ALEMBIC) current" 