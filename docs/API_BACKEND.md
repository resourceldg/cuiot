# API Backend - Sistema Integral de Monitoreo

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
- Query: `skip`, `limit`, `care_type`, `mobility_level`
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
  "care_type": "self_care",
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

## Sistema de Paquetes (NUEVA ENTIDAD CENTRAL)

### Listar paquetes disponibles
**GET** `/api/v1/packages/`
- Query: `package_type`, `is_active`
- **Protegido:** Sí (JWT)

### Detalle de paquete
**GET** `/api/v1/packages/{package_id}`

### Crear paquete (Admin)
**POST** `/api/v1/packages/`
```json
{
  "package_type": "basic",
  "name": "Paquete Básico Individual",
  "description": "Monitoreo básico para 1 persona",
  "price_monthly": 3000,
  "price_yearly": 30000,
  "currency": "ARS",
  "features": {
    "monitoreo": "básico",
    "alertas": "simples",
    "reportes": "diarios",
    "dispositivos": 3,
    "usuarios": 1,
    "soporte": "email"
  },
  "limitations": {
    "max_users": 1,
    "max_devices": 3,
    "max_storage_gb": 5
  },
  "max_users": 1,
  "max_devices": 3,
  "max_storage_gb": 5,
  "support_level": "email",
  "is_active": true
}
```

### Actualizar paquete
**PUT** `/api/v1/packages/{package_id}`

### Eliminar paquete
**DELETE** `/api/v1/packages/{package_id}`

---

## Contratación de Paquetes

### Listar paquetes contratados por usuario
**GET** `/api/v1/user-packages/`
- Query: `status`, `package_type`
- **Protegido:** Sí (JWT)

### Contratar paquete
**POST** `/api/v1/user-packages/`
```json
{
  "package_id": "uuid-del-paquete",
  "start_date": "2024-01-15",
  "auto_renew": true,
  "payment_method": "credit_card"
}
```

### Actualizar suscripción
**PUT** `/api/v1/user-packages/{subscription_id}`

### Cancelar suscripción
**PATCH** `/api/v1/user-packages/{subscription_id}/cancel`

### Renovar suscripción
**PATCH** `/api/v1/user-packages/{subscription_id}/renew`

---

## Sistema de Referidos

### Generar código de referido
**POST** `/api/v1/referrals/generate-code`
```json
{
  "referrer_type": "caregiver",
  "referrer_id": "uuid-del-referente"
}
```

### Validar código de referido
**POST** `/api/v1/referrals/validate`
```json
{
  "referral_code": "ABC123",
  "referred_email": "nuevo@ejemplo.com",
  "referred_name": "Nuevo Usuario"
}
```

### Listar referidos del usuario
**GET** `/api/v1/referrals/my-referrals`
- Query: `status`, `referrer_type`
- **Protegido:** Sí (JWT)

### Estadísticas de referidos
**GET** `/api/v1/referrals/stats`
- **Protegido:** Sí (JWT)

### Actualizar estado de referido
**PATCH** `/api/v1/referrals/{referral_id}/update-status`
```json
{
  "status": "converted",
  "commission_amount": 1500.00
}
```

---

## Sistema de Comisiones

### Listar comisiones del usuario
**GET** `/api/v1/referral-commissions/my-commissions`
- Query: `status`, `commission_type`
- **Protegido:** Sí (JWT)

### Marcar comisión como pagada
**PATCH** `/api/v1/referral-commissions/{commission_id}/mark-paid`

### Estadísticas de comisiones
**GET** `/api/v1/referral-commissions/stats`
- **Protegido:** Sí (JWT)

---

## Sistema de Scoring y Reviews

### Crear review de cuidador
**POST** `/api/v1/caregiver-reviews/`
```json
{
  "caregiver_id": "uuid-del-cuidador",
  "rating": 5,
  "comment": "Excelente servicio",
  "categories": {
    "puntualidad": 5,
    "cuidado": 5,
    "comunicacion": 4
  },
  "is_recommended": true,
  "service_date": "2024-01-15",
  "service_hours": 8.0,
  "service_type": "daily"
}
```

### Listar reviews de cuidador
**GET** `/api/v1/caregiver-reviews/caregiver/{caregiver_id}`
- Query: `rating`, `is_verified`

### Crear review de institución
**POST** `/api/v1/institution-reviews/`
```json
{
  "institution_id": 1,
  "rating": 4,
  "comment": "Muy buena atención",
  "categories": {
    "calidad_medica": 4,
    "infraestructura": 5,
    "personal": 4
  },
  "is_recommended": true,
  "service_date": "2024-01-15",
  "service_type": "consultation"
}
```

### Listar reviews de institución
**GET** `/api/v1/institution-reviews/institution/{institution_id}`
- Query: `rating`, `is_verified`

### Obtener score de cuidador
**GET** `/api/v1/caregiver-scores/{caregiver_id}`

### Obtener score de institución
**GET** `/api/v1/institution-scores/{institution_id}`

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

### Estado del dispositivo
**GET** `/api/v1/devices/{device_id}/status`

### Configurar dispositivo
**PATCH** `/api/v1/devices/{device_id}/configure`
```json
{
  "settings": {
    "sensitivity": 0.9,
    "sampling_rate": 2000
  }
}
```

### Dispositivos por tipo
**GET** `/api/v1/devices/type/{device_type}/list`

### Dispositivos activos
**GET** `/api/v1/devices/active/list`

### Dispositivos con batería baja
**GET** `/api/v1/devices/low-battery/list`

---

## Eventos

### Listar eventos
**GET** `/api/v1/events/`
- Query: `skip`, `limit`, `event_type`, `severity`, `device_id`, `cared_person_id`

### Detalle de evento
**GET** `/api/v1/events/{event_id}`

### Eventos por dispositivo
**GET** `/api/v1/events/device/{device_id}`

### Eventos por persona
**GET** `/api/v1/events/cared-person/{cared_person_id}`

### Crear evento
**POST** `/api/v1/events/`
```json
{
  "event_type": "motion_detected",
  "severity": "low",
  "device_id": "ESP32_001",
  "cared_person_id": 1,
  "location_data": {
    "latitude": -34.6037,
    "longitude": -58.3816
  },
  "sensor_data": {
    "motion_level": 0.8,
    "temperature": 22.5
  }
}
```

### Actualizar evento
**PUT** `/api/v1/events/{event_id}`

### Eliminar evento
**DELETE** `/api/v1/events/{event_id}`

### Eventos críticos
**GET** `/api/v1/events/critical/list`

### Eventos por tipo
**GET** `/api/v1/events/type/{event_type}/list`

### Eventos no procesados
**GET** `/api/v1/events/unprocessed/list`

---

## Usuarios

### Listar usuarios
**GET** `/api/v1/users/`
- Query: `skip`, `limit`, `role`, `is_active`
- **Protegido:** Sí (JWT, Admin)

### Detalle de usuario
**GET** `/api/v1/users/{user_id}`

### Crear usuario
**POST** `/api/v1/users/`
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "phone": "123456789",
  "role": "family"
}
```

### Actualizar usuario
**PUT** `/api/v1/users/{user_id}`

### Eliminar usuario
**DELETE** `/api/v1/users/{user_id}`

### Perfil del usuario actual
**GET** `/api/v1/users/me`

### Actualizar perfil
**PUT** `/api/v1/users/me`

### Cambiar contraseña
**PATCH** `/api/v1/users/me/change-password`
```json
{
  "current_password": "contraseña_actual",
  "new_password": "nueva_contraseña"
}
```

### Usuarios por rol
**GET** `/api/v1/users/role/{role}/list`

### Usuarios activos
**GET** `/api/v1/users/active/list`

---

## Suscripciones de Servicio

### Listar suscripciones
**GET** `/api/v1/service-subscriptions/`
- Query: `subscription_type`, `status`, `user_id`, `institution_id`

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
Los reportes están vinculados a usuarios específicos para mantener trazabilidad y control de acceso.

### Endpoints de Reportes
- **GET** `/api/v1/reports/` - Listar reportes del usuario
- **POST** `/api/v1/reports/` - Crear nuevo reporte
- **GET** `/api/v1/reports/{report_id}` - Detalle de reporte
- **PUT** `/api/v1/reports/{report_id}` - Actualizar reporte
- **DELETE** `/api/v1/reports/{report_id}` - Eliminar reporte

### Ejemplo de Reporte
```json
{
  "title": "Reporte Mensual - Enero 2024",
  "description": "Análisis completo de actividad y salud",
  "report_type": "monthly",
  "cared_person_id": 1,
  "content": {
    "activity_summary": "Actividad normal",
    "health_metrics": {
      "steps": 8500,
      "sleep_hours": 7.5,
      "medication_adherence": 95
    },
    "alerts_summary": {
      "total": 3,
      "resolved": 3,
      "pending": 0
    }
  },
  "attachments": [
    {
      "filename": "reporte_enero_2024.pdf",
      "url": "/uploads/reports/reporte_enero_2024.pdf",
      "size": 1024000
    }
  ]
}
```

---

## Validaciones de Capacidad Legal

### Verificar capacidad legal
**POST** `/api/v1/legal-capacity/verify`
```json
{
  "user_id": "uuid-del-usuario",
  "care_type": "self_care",
  "date_of_birth": "1940-05-15",
  "legal_status": "competent"
}
```

### Validar representante legal
**POST** `/api/v1/legal-capacity/validate-representative`
```json
{
  "cared_person_id": "uuid-de-la-persona",
  "representative_id": "uuid-del-representante",
  "relationship": "family",
  "legal_document": "power_of_attorney"
}
```

### Obtener representante legal
**GET** `/api/v1/legal-capacity/representative/{cared_person_id}`

---

## Administración

### Dashboard de métricas
**GET** `/api/v1/admin/dashboard`
- **Protegido:** Sí (JWT, Admin)

### Estadísticas de usuarios
**GET** `/api/v1/admin/users/stats`

### Estadísticas de paquetes
**GET** `/api/v1/admin/packages/stats`

### Estadísticas de referidos
**GET** `/api/v1/admin/referrals/stats`

### Estadísticas de comisiones
**GET** `/api/v1/admin/commissions/stats`

### Configuración del sistema
**GET** `/api/v1/admin/config`

### Actualizar configuración
**PUT** `/api/v1/admin/config`

---

## Códigos de Error

### Errores de Autenticación
- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: Sin permisos para el recurso

### Errores de Validación
- `422 Unprocessable Entity`: Datos inválidos
- `400 Bad Request`: Parámetros incorrectos

### Errores de Negocio
- `409 Conflict`: Conflicto de datos (ej: email duplicado)
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error interno del servidor

### Errores Específicos
- `CAPACITY_LEGAL_REQUIRED`: Se requiere validación de capacidad legal
- `REPRESENTATIVE_REQUIRED`: Se requiere representante legal para cuidado delegado
- `PACKAGE_LIMIT_EXCEEDED`: Límite del paquete excedido
- `REFERRAL_EXPIRED`: Código de referido expirado
- `INSUFFICIENT_PERMISSIONS`: Permisos insuficientes para la acción

---

*Documentación API - CUIOT v2.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 