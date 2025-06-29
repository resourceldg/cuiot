# API Backend - Viejos Son Los Trapos

## Autenticación (JWT)

### Registrar usuario
**POST** `/api/v1/auth/register`
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "phone": "123456789"
}
```
**Response:** Usuario creado (200/201)

### Login
**POST** `/api/v1/auth/login`
- Form fields: `username`, `password`
**Response:**
```json
{
  "access_token": "jwt...",
  "token_type": "bearer"
}
```

### Refresh token
**POST** `/api/v1/auth/refresh`

---

## Gestión de Personas Bajo Cuidado

### Listar personas
**GET** `/api/v1/cared-persons/`
- Query: `skip`, `limit`, `care_level`, `mobility_level`
- **Protegido:** Sí (JWT)

### Detalle de persona
**GET** `/api/v1/cared-persons/{id}`

### Crear persona
**POST** `/api/v1/cared-persons/`
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "date_of_birth": "1940-05-15",
  "gender": "male",
  "phone": "123456789",
  "email": "juan@ejemplo.com",
  "emergency_contact": "María Pérez",
  "emergency_phone": "987654321",
  "medical_conditions": "Diabetes, hipertensión",
  "medications": "Insulina, metformina",
  "allergies": "Penicilina",
  "blood_type": "O+",
  "care_level": "medium",
  "mobility_level": "assisted",
  "address": "Av. Principal 123",
  "latitude": -34.6037,
  "longitude": -58.3816
}
```

### Actualizar persona
**PUT** `/api/v1/cared-persons/{id}`

### Eliminar persona
**DELETE** `/api/v1/cared-persons/{id}`

---

## Alertas

### Listar alertas
**GET** `/api/v1/alerts/`
- Query: `skip`, `limit`, `cared_person_id`, `alert_type`, `severity`, `is_resolved`
- **Protegido:** Sí (JWT)

### Detalle de alerta
**GET** `/api/v1/alerts/{alert_id}`

### Alertas por persona
**GET** `/api/v1/alerts/cared-person/{cared_person_id}`

### Crear alerta
**POST** `/api/v1/alerts/`
```json
{
  "cared_person_id": 1,
  "alert_type": "sos",
  "message": "Botón de pánico presionado",
  "severity": "high"
}
```

### Actualizar alerta
**PUT** `/api/v1/alerts/{alert_id}`

### Eliminar alerta
**DELETE** `/api/v1/alerts/{alert_id}`

### Marcar como resuelta
**PATCH** `/api/v1/alerts/{alert_id}/resolve`

### Listar no resueltas
**GET** `/api/v1/alerts/unresolved/list`

### Listar críticas
**GET** `/api/v1/alerts/critical/list`

---

## Recordatorios

### Listar recordatorios
**GET** `/api/v1/reminders/`
- Query: `skip`, `limit`, `cared_person_id`, `reminder_type`, `is_active`

### Detalle de recordatorio
**GET** `/api/v1/reminders/{reminder_id}`

### Recordatorios por persona
**GET** `/api/v1/reminders/cared-person/{cared_person_id}`

### Crear recordatorio
**POST** `/api/v1/reminders/`
```json
{
  "cared_person_id": 1,
  "title": "Tomar medicación",
  "description": "Pastilla azul",
  "reminder_type": "medication",
  "scheduled_time": "08:00:00",
  "days_of_week": [1,2,3,4,5]
}
```

### Actualizar recordatorio
**PUT** `/api/v1/reminders/{reminder_id}`

### Eliminar recordatorio
**DELETE** `/api/v1/reminders/{reminder_id}`

### Activar recordatorio
**PATCH** `/api/v1/reminders/{reminder_id}/activate`

### Desactivar recordatorio
**PATCH** `/api/v1/reminders/{reminder_id}/deactivate`

### Listar activos
**GET** `/api/v1/reminders/active/list`

### Listar por tipo
**GET** `/api/v1/reminders/type/{reminder_type}/list`

### Listar de medicación
**GET** `/api/v1/reminders/medication/list`

---

## Dispositivos IoT

### Listar dispositivos
**GET** `/api/v1/devices/`
- Query: `skip`, `limit`, `device_type`, `status`, `cared_person_id`

### Detalle de dispositivo
**GET** `/api/v1/devices/{device_id}`

### Registrar dispositivo
**POST** `/api/v1/devices/`
```json
{
  "device_id": "ESP32_001",
  "device_type": "sensor",
  "model": "ESP32 DevKit",
  "manufacturer": "Espressif",
  "serial_number": "SN123456789",
  "status": "active",
  "battery_level": 85,
  "signal_strength": 95,
  "location_description": "Sala de estar",
  "latitude": -34.6037,
  "longitude": -58.3816,
  "settings": "{\"sensitivity\": 0.8, \"sampling_rate\": 1000}",
  "firmware_version": "1.2.3",
  "hardware_version": "1.0",
  "cared_person_id": 1
}
```

### Actualizar dispositivo
**PUT** `/api/v1/devices/{device_id}`

### Eliminar dispositivo
**DELETE** `/api/v1/devices/{device_id}`

### Configurar dispositivo
**PATCH** `/api/v1/devices/{device_id}/config`

### Estado del dispositivo
**GET** `/api/v1/devices/{device_id}/status`

---

## Eventos

### Listar eventos
**GET** `/api/v1/events/`
- Query: `skip`, `limit`, `event_type`, `severity`, `cared_person_id`

### Detalle de evento
**GET** `/api/v1/events/{event_id}`

### Crear evento
**POST** `/api/v1/events/`
```json
{
  "cared_person_id": 1,
  "event_type": "sensor_event",
  "event_subtype": "movement",
  "severity": "info",
  "message": "Movimiento detectado en sala de estar",
  "event_data": "{\"location\": \"sala_estar\", \"confidence\": 0.95}",
  "event_time": "2024-01-15T10:30:00Z"
}
```

### Actualizar evento
**PUT** `/api/v1/events/{event_id}`

### Eliminar evento
**DELETE** `/api/v1/events/{event_id}`

### Eventos por persona
**GET** `/api/v1/events/cared-person/{cared_person_id}`

### Eventos por tipo
**GET** `/api/v1/events/type/{event_type}/list`

---

## Reportes con Adjuntos

### Listar reportes
**GET** `/api/v1/reports/`
- Query: `skip`, `limit`, `report_type`, `cared_person_id`, `is_autocuidado`

### Detalle de reporte
**GET** `/api/v1/reports/{report_id}`

### Crear reporte con adjuntos
**POST** `/api/v1/reports/`
- **Content-Type:** `multipart/form-data`
- **Form fields:**
  - `title`: Título del reporte
  - `description`: Descripción (opcional)
  - `report_type`: Tipo de reporte (general, médico, incidente, etc.)
  - `is_autocuidado`: Boolean (false para reportes de otros)
  - `cared_person_id`: ID de la persona (requerido si no es autocuidado)
  - `files`: Archivos adjuntos (múltiples)

**Response:**
```json
{
  "id": 1,
  "title": "Reporte médico mensual",
  "description": "Control rutinario",
  "report_type": "médico",
  "attached_files": [
    {
      "filename": "analisis_sangre.pdf",
      "url": "/static/reports/uuid_analisis_sangre.pdf",
      "content_type": "application/pdf",
      "size": 1024000
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "cared_person_id": 1,
  "created_by_id": 1,
  "is_autocuidado": false
}
```

### Actualizar reporte
**PUT** `/api/v1/reports/{report_id}`

### Eliminar reporte
**DELETE** `/api/v1/reports/{report_id}`

### Reportes por persona
**GET** `/api/v1/reports/cared-person/{cared_person_id}`

### Reportes de autocuidado
**GET** `/api/v1/reports/autocuidado`

---

## Sistema de Debug y Testing

### Resumen de debug
**GET** `/api/v1/debug/summary`
- **Protegido:** Sí (JWT)
- **Response:** Estadísticas de datos de prueba

### Generar datos de prueba
**POST** `/api/v1/debug/generate-test-data`
- **Query:** `count` (número de registros a generar, 1-100)
- **Protegido:** Sí (JWT)
- **Response:**
```json
{
  "message": "Test data generated successfully",
  "results": {
    "users_created": 5,
    "cared_persons_created": 3,
    "devices_created": 4,
    "events_created": 8,
    "alerts_created": 6,
    "debug_events_created": 10
  }
}
```

### Limpiar datos de prueba
**POST** `/api/v1/debug/clean-test-data`
- **Protegido:** Sí (JWT)
- **Response:**
```json
{
  "message": "Test data cleaned successfully",
  "results": {
    "location_tracking_deleted": 50,
    "geofences_deleted": 5,
    "debug_events_deleted": 100,
    "cared_persons_deleted": 3,
    "devices_deleted": 4
  }
}
```

### Listar eventos de debug
**GET** `/api/v1/debug/events`
- **Query:** `skip`, `limit`, `event_type`, `severity`, `test_session`
- **Protegido:** Sí (JWT)

### Crear evento de debug
**POST** `/api/v1/debug/events`
```json
{
  "event_type": "test_event",
  "event_subtype": "simulation",
  "severity": "info",
  "message": "Evento de prueba simulado",
  "source": "test_suite",
  "test_session": "session_20240115_103000",
  "environment": "development",
  "event_time": "2024-01-15T10:30:00Z"
}
```

### Health check de debug
**GET** `/api/v1/debug/health`

---

## Geolocalización y Geofencing

### Tracking de ubicación
**POST** `/api/v1/location/track`
```json
{
  "cared_person_id": 1,
  "latitude": -34.6037,
  "longitude": -58.3816,
  "altitude": 25.5,
  "accuracy": 5.0,
  "speed": 0.0,
  "heading": 180.0,
  "location_name": "Casa",
  "address": "Av. Principal 123",
  "place_type": "home",
  "tracking_method": "gps",
  "battery_level": 85,
  "signal_strength": 95,
  "recorded_at": "2024-01-15T10:30:00Z"
}
```

### Historial de ubicaciones
**GET** `/api/v1/location/history/{cared_person_id}`
- **Query:** `start_date`, `end_date`, `limit`

### Ubicación actual
**GET** `/api/v1/location/current/{cared_person_id}`

### Crear geofence
**POST** `/api/v1/geofences/`
```json
{
  "name": "Zona segura - Casa",
  "geofence_type": "safe_zone",
  "description": "Zona segura alrededor de la casa",
  "center_latitude": -34.6037,
  "center_longitude": -58.3816,
  "radius": 100.0,
  "trigger_action": "exit",
  "alert_message": "Persona ha salido de la zona segura",
  "is_active": true,
  "start_time": "2024-01-15T00:00:00Z",
  "end_time": "2024-01-15T23:59:59Z",
  "days_of_week": "1,2,3,4,5,6,7",
  "cared_person_id": 1
}
```

### Listar geofences
**GET** `/api/v1/geofences/`
- **Query:** `cared_person_id`, `geofence_type`, `is_active`

### Actualizar geofence
**PUT** `/api/v1/geofences/{geofence_id}`

### Eliminar geofence
**DELETE** `/api/v1/geofences/{geofence_id}`

---

## Protocolos de Emergencia

### Listar protocolos
**GET** `/api/v1/emergency-protocols/`
- **Query:** `protocol_type`, `crisis_type`, `institution_id`, `is_active`

### Detalle de protocolo
**GET** `/api/v1/emergency-protocols/{protocol_id}`

### Crear protocolo
**POST** `/api/v1/emergency-protocols/`
```json
{
  "name": "Protocolo de Caída",
  "protocol_type": "medical",
  "crisis_type": "fall",
  "description": "Protocolo para manejo de caídas",
  "steps": "[\"Evaluar consciencia\", \"Verificar lesiones\", \"Contactar médico\"]",
  "contacts": "[\"Dr. García: 123456789\", \"Ambulancia: 911\"]",
  "trigger_conditions": "{\"severity\": \"high\", \"location\": \"bathroom\"}",
  "severity_threshold": "high",
  "is_active": true,
  "is_default": false,
  "institution_id": 1
}
```

### Actualizar protocolo
**PUT** `/api/v1/emergency-protocols/{protocol_id}`

### Eliminar protocolo
**DELETE** `/api/v1/emergency-protocols/{protocol_id}`

### Activar protocolo
**PATCH** `/api/v1/emergency-protocols/{protocol_id}/activate`

### Desactivar protocolo
**PATCH** `/api/v1/emergency-protocols/{protocol_id}/deactivate`

---

## Servicios y Suscripciones

### Listar suscripciones
**GET** `/api/v1/service-subscriptions/`
- **Query:** `subscription_type`, `status`, `user_id`, `institution_id`

### Detalle de suscripción
**GET** `/api/v1/service-subscriptions/{subscription_id}`

### Crear suscripción
**POST** `/api/v1/service-subscriptions/`
```json
{
  "subscription_type": "premium",
  "service_name": "Monitoreo Premium",
  "description": "Servicio de monitoreo avanzado con IA",
  "features": "[\"Monitoreo 24/7\", \"Alertas IA\", \"Reportes avanzados\"]",
  "limitations": "[\"Máximo 5 personas\", \"Sin videovigilancia\"]",
  "price_per_month": 6000,
  "price_per_year": 60000,
  "currency": "ARS",
  "start_date": "2024-01-15",
  "end_date": "2025-01-15",
  "auto_renew": true,
  "status": "active",
  "user_id": 1
}
```

### Actualizar suscripción
**PUT** `/api/v1/service-subscriptions/{subscription_id}`

### Cancelar suscripción
**PATCH** `/api/v1/service-subscriptions/{subscription_id}/cancel`

---

## Facturación

### Listar facturas
**GET** `/api/v1/billing-records/`
- **Query:** `billing_type`, `status`, `user_id`, `institution_id`

### Detalle de factura
**GET** `/api/v1/billing-records/{billing_id}`

### Crear factura
**POST** `/api/v1/billing-records/`
```json
{
  "invoice_number": "FAC-2024-001",
  "billing_type": "subscription",
  "description": "Suscripción Premium - Enero 2024",
  "amount": 6000,
  "currency": "ARS",
  "tax_amount": 1260,
  "total_amount": 7260,
  "billing_date": "2024-01-15",
  "due_date": "2024-01-31",
  "status": "pending",
  "payment_method": "credit_card",
  "user_id": 1,
  "service_subscription_id": 1
}
```

### Actualizar factura
**PUT** `/api/v1/billing-records/{billing_id}`

### Marcar como pagada
**PATCH** `/api/v1/billing-records/{billing_id}/mark-paid`

### Facturas vencidas
**GET** `/api/v1/billing-records/overdue`

---

## Salud y Estadísticas

### Estado básico
**GET** `/api/v1/health/`

### Estado de base de datos
**GET** `/api/v1/health/db`

### Estado del sistema
**GET** `/api/v1/health/system`

### Estadísticas
**GET** `/api/v1/health/stats`

### Chequeo completo
**GET** `/api/v1/health/full`

### Ping
**GET** `/api/v1/health/ping`

---

## Vinculación de Reportes con Usuarios

### Descripción
El sistema implementa una regla de negocio que vincula todos los reportes (eventos, alertas y recordatorios) con los usuarios que los crean y reciben. Solo los usuarios con roles de familia o empleado pueden crear reportes.

### Campos de Vinculación
Todos los reportes incluyen los siguientes campos:
- `created_by_id`: ID del usuario que creó el reporte (obligatorio)
- `received_by_id`: ID del usuario que recibe/recibió el reporte (opcional)

### Validaciones
- Solo usuarios con roles `family` o `employee` pueden crear reportes
- El usuario autenticado se asigna automáticamente como `created_by_id`
- Se valida que el usuario tenga permisos para acceder al adulto mayor asociado

### Eventos

#### Crear evento (actualizado)
**POST** `/api/v1/events/`
```json
{
  "cared_person_id": 1,
  "event_type": "visit",
  "title": "Visita médica",
  "description": "Control rutinario",
  "event_date": "2024-01-15T10:00:00",
  "received_by_id": "uuid-opcional"
}
```
**Nota:** `created_by_id` se asigna automáticamente al usuario autenticado.

#### Listar eventos del usuario
**GET** `/api/v1/events/my-events/`
- Lista todos los eventos creados por el usuario autenticado

#### Listar eventos recibidos
**GET** `/api/v1/events/received/`
- Lista todos los eventos donde el usuario es `received_by_id`

### Alertas

#### Crear alerta (actualizado)
**POST** `/api/v1/alerts/`
```json
{
  "cared_person_id": 1,
  "alert_type": "sos",
  "message": "Botón de pánico presionado",
  "severity": "high",
  "received_by_id": "uuid-opcional"
}
```

#### Listar alertas del usuario
**GET** `/api/v1/alerts/my-alerts/`
- Lista todas las alertas creadas por el usuario autenticado

#### Listar alertas recibidas
**GET** `/api/v1/alerts/received/`
- Lista todas las alertas donde el usuario es `received_by_id`

### Recordatorios

#### Crear recordatorio (actualizado)
**POST** `/api/v1/reminders/`
```json
{
  "cared_person_id": 1,
  "title": "Tomar medicación",
  "description": "Pastilla azul",
  "reminder_type": "medication",
  "scheduled_time": "08:00:00",
  "days_of_week": [1,2,3,4,5],
  "received_by_id": "uuid-opcional"
}
```

#### Listar recordatorios del usuario
**GET** `/api/v1/reminders/my-reminders/`
- Lista todos los recordatorios creados por el usuario autenticado

#### Listar recordatorios recibidos
**GET** `/api/v1/reminders/received/`
- Lista todos los recordatorios donde el usuario es `received_by_id`

---

## Códigos de Error

### Errores de Autenticación
- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: Usuario sin permisos para la operación

### Errores de Validación
- `400 Bad Request`: Datos de entrada inválidos
- `422 Unprocessable Entity`: Error de validación de esquema

### Errores de Recurso
- `404 Not Found`: Recurso no encontrado
- `409 Conflict`: Conflicto de datos (ej: email duplicado)

### Errores del Servidor
- `500 Internal Server Error`: Error interno del servidor
- `503 Service Unavailable`: Servicio temporalmente no disponible

---

## Ejemplos de Respuesta

### Respuesta de Error
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "Email inválido"
    }
  ]
}
```

### Respuesta de Lista Paginada
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

### Respuesta de Creación
```json
{
  "id": 1,
  "message": "Recurso creado exitosamente",
  "created_at": "2024-01-15T10:30:00Z"
}
``` 