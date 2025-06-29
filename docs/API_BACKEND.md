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

## Alertas

### Listar alertas
**GET** `/api/v1/alerts/`
- Query: `skip`, `limit`, `elderly_person_id`, `alert_type`, `severity`, `is_resolved`
- **Protegido:** Sí (JWT)

### Detalle de alerta
**GET** `/api/v1/alerts/{alert_id}`

### Alertas por adulto mayor
**GET** `/api/v1/alerts/elderly/{elderly_person_id}`

### Crear alerta
**POST** `/api/v1/alerts/`
```json
{
  "elderly_person_id": "uuid",
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
- Query: `skip`, `limit`, `elderly_person_id`, `reminder_type`, `is_active`

### Detalle de recordatorio
**GET** `/api/v1/reminders/{reminder_id}`

### Recordatorios por adulto mayor
**GET** `/api/v1/reminders/elderly/{elderly_person_id}`

### Crear recordatorio
**POST** `/api/v1/reminders/`
```json
{
  "elderly_person_id": "uuid",
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
  "elderly_person_id": "uuid",
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
  "elderly_person_id": "uuid",
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
  "elderly_person_id": "uuid",
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

### Ejemplos de Uso

#### Flujo típico de creación de reporte
1. Usuario autenticado (familia/empleado) crea un evento
2. Sistema asigna automáticamente `created_by_id` = usuario actual
3. Si se especifica `received_by_id`, se asigna al usuario destinatario
4. El reporte queda vinculado a ambos usuarios

#### Consulta de reportes propios
```bash
# Obtener eventos creados por el usuario actual
GET /api/v1/events/my-events/
Authorization: Bearer <token>

# Obtener alertas recibidas por el usuario actual
GET /api/v1/alerts/received/
Authorization: Bearer <token>
```

### Control de Acceso
- Los usuarios solo pueden ver reportes que han creado o recibido
- Los administradores pueden ver todos los reportes
- Se valida que el usuario tenga acceso al adulto mayor asociado

---

## Notas de uso

- Todos los endpoints protegidos requieren el header:
  ```
  Authorization: Bearer <access_token>
  ```
- Los endpoints devuelven errores claros con códigos HTTP estándar.
- Los modelos y parámetros están documentados en `/docs` (Swagger UI) y `/redoc`.

---

## Ejemplo de flujo completo

1. **Registrar usuario** → **Login** → obtener `access_token`.
2. Usar el token para crear, listar y modificar alertas y recordatorios.
3. Consultar endpoints de salud para monitoreo del sistema.

---

¿Dudas? Consulta la documentación interactiva en `/docs` o `/redoc`.

### Reportes (con adjuntos)

**Modelo:**
- id: int
- title: str
- description: str
- report_type: str
- attached_files: List[FileMeta]
- is_autocuidado: bool
- cared_person_id: int (opcional)
- created_by_id: int
- created_at, updated_at

**Endpoints:**
- POST `/api/v1/reports/` (multipart/form-data): crear reporte (con adjuntos)
- GET `/api/v1/reports/`: listar reportes
- GET `/api/v1/reports/{id}`: obtener detalle

**Notas:**
- Si `is_autocuidado` es false, `cared_person_id` es obligatorio.
- Los adjuntos se suben como archivos y se devuelven como metadatos (filename, url, etc.). 