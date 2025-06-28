# Backend - Viejos Son Los Trapos

## Arquitectura General

- **Framework:** FastAPI
- **Base de datos:** PostgreSQL
- **ORM:** SQLAlchemy
- **Autenticación:** JWT
- **Estructura modular:**
  - `models/`: Modelos de datos y relaciones.
  - `schemas/`: Esquemas Pydantic para validación y serialización.
  - `services/`: Lógica de negocio y acceso a datos.
  - `api/`: Endpoints RESTful organizados por recurso.
  - `core/`: Configuración, base de datos y utilidades.
  - `scripts/`: Scripts de carga y utilidades.

## Modelos principales
- **User:** Usuario familiar, autenticación y relación con adultos mayores.
- **ElderlyPerson:** Adulto mayor, con soft delete (`is_deleted`) y estado (`is_active`).
- **Device:** Dispositivo IoT asociado a adulto mayor.
- **Event:** Evento de calendario o sensor.
- **Alert:** Alerta crítica, con severidad y resolución.
- **Reminder:** Recordatorio programado, con días de la semana y activación/desactivación.
- **DeviceConfig:** Configuración avanzada de dispositivos.

## Flujos críticos cubiertos
- ABM de usuarios, adultos mayores, dispositivos, eventos, alertas y recordatorios.
- Soft delete profesional y gestión de estados activos/inactivos.
- Sincronización de estados con el frontend.
- Endpoints de health check y monitoreo.
- Autenticación y autorización JWT.

## Pruebas automáticas
- Ubicadas en `../tests/`.
- Cobertura para: usuarios, autenticación, alertas, recordatorios y health check.
- Uso de fixtures para clientes asíncronos y autenticación.
- **Recomendación:** Agregar tests para dispositivos y eventos para cobertura total.

## Decisiones de negocio
- Soft delete (`is_deleted`) para evitar pérdida de datos.
- Estado `is_active` separado para lógica de negocio.
- Relaciones y constraints estrictos para integridad referencial.

## Extensión y buenas prácticas
- Seguir estructura modular para nuevos módulos.
- Documentar nuevos endpoints y servicios con docstrings.
- Mantener tests automáticos para cada flujo de negocio.
- Revisar y actualizar migraciones ante cambios en modelos.

## Troubleshooting: Integridad de datos y sincronización backend/frontend

### Error: 500 Internal Server Error en /api/v1/alerts/ por Enum inválido
- **Síntoma:** El backend devuelve un error 500 y el log muestra un mensaje como:
  > Input should be 'no_movement', 'sos', 'temperature', 'medication', 'fall', 'heart_rate' or 'blood_pressure' [type=enum, input_value='health', input_type=str]
- **Causa:** Hay un valor inválido en la columna `alert_type` de la tabla `alerts`.
- **Solución:**
  1. Identifica el usuario y base de datos de PostgreSQL (ver variables de entorno en el contenedor postgres).
  2. Ejecuta:
     ```sh
     sudo docker-compose exec postgres psql -U <usuario> -d <db> -c "UPDATE alerts SET alert_type = 'medication' WHERE alert_type = 'health';"
     ```
  3. Reintenta la carga de la vista en el frontend.

### Error: No se muestran adultos mayores en la vista "Humans"
- **Síntoma:** La sección de gestión humana aparece vacía aunque hay datos en la base.
- **Causa:** El frontend filtra por `is_deleted = false` en la tabla `elderly_persons`.
- **Solución:**
  1. Verifica los registros con:
     ```sh
     sudo docker-compose exec postgres psql -U <usuario> -d <db> -c "SELECT id, first_name, last_name, is_deleted FROM elderly_persons;"
     ```
  2. Si hay registros con `is_deleted = true`, actualízalos:
     ```sh
     sudo docker-compose exec postgres psql -U <usuario> -d <db> -c "UPDATE elderly_persons SET is_deleted = false WHERE is_deleted = true;"
     ```
  3. Refresca el frontend.

### Notas generales
- Siempre verifica los logs de backend y frontend con:
  ```sh
  sudo docker-compose logs --tail=100 backend
  sudo docker-compose logs --tail=100 web-panel
  ```
- Si hay cambios de modelo, asegúrate de alinear la base de datos y recargar los datos dummy si es necesario. 