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

## Sistema Médico Avanzado

### Diagnósticos

#### Listar diagnósticos
**GET** `/api/v1/diagnoses/`
- Query: `cared_person_id`, `diagnosis_type`, `is_active`, `skip`, `limit`
- **Protegido:** Sí (JWT)

#### Crear diagnóstico
**POST** `/api/v1/diagnoses/`
- **Content-Type:** `multipart/form-data`
```json
{
  "cared_person_id": "uuid",
  "diagnosis_type": "medical",
  "diagnosis_date": "2024-01-15",
  "diagnosis_code": "E11.9",
  "diagnosis_name": "Diabetes mellitus tipo 2 sin complicaciones",
  "description": "Diagnóstico de diabetes mellitus tipo 2",
  "severity": "moderate",
  "symptoms": ["sed excesiva", "fatiga", "visión borrosa"],
  "treatments": ["dieta", "ejercicio", "metformina"],
  "notes": "Paciente requiere monitoreo de glucosa",
  "is_active": true,
  "file": "archivo.pdf" // opcional
}
```

#### Actualizar diagnóstico
**PUT** `/api/v1/diagnoses/{diagnosis_id}`

#### Eliminar diagnóstico
**DELETE** `/api/v1/diagnoses/{diagnosis_id}`

### Perfiles Médicos

#### Listar perfiles médicos
**GET** `/api/v1/medical-profiles/`
- Query: `cared_person_id`, `is_active`, `skip`, `limit`

#### Crear perfil médico
**POST** `/api/v1/medical-profiles/`
```json
{
  "cared_person_id": "uuid",
  "blood_type": "O+",
  "allergies": ["penicilina", "sulfas"],
  "chronic_conditions": ["diabetes", "hipertensión"],
  "emergency_contacts": [
    {
      "name": "Dr. García",
      "phone": "123456789",
      "specialty": "Cardiología"
    }
  ],
  "special_needs": ["dieta sin sal", "monitoreo de glucosa"],
  "is_active": true
}
```

#### Actualizar perfil médico
**PUT** `/api/v1/medical-profiles/{profile_id}`

#### Eliminar perfil médico
**DELETE** `/api/v1/medical-profiles/{profile_id}`

### Programas de Medicación

#### Listar programas de medicación
**GET** `/api/v1/medication-schedules/`
- Query: `cared_person_id`, `medication_name`, `is_active`, `skip`, `limit`

#### Crear programa de medicación
**POST** `/api/v1/medication-schedules/`
```json
{
  "cared_person_id": "uuid",
  "medication_name": "Metformina",
  "dosage": "500mg",
  "frequency": "twice_daily",
  "time_slots": ["08:00", "20:00"],
  "start_date": "2024-01-15",
  "end_date": "2024-12-31",
  "instructions": "Tomar con las comidas",
  "side_effects": ["náuseas", "diarrea"],
  "is_active": true
}
```

#### Actualizar programa de medicación
**PUT** `/api/v1/medication-schedules/{schedule_id}`

#### Eliminar programa de medicación
**DELETE** `/api/v1/medication-schedules/{schedule_id}`

### Registros de Medicación

#### Listar registros de medicación
**GET** `/api/v1/medication-logs/`
- Query: `cared_person_id`, `medication_schedule_id`, `status`, `date_from`, `date_to`, `skip`, `limit`

#### Registrar toma de medicación
**POST** `/api/v1/medication-logs/`
```json
{
  "medication_schedule_id": "uuid",
  "cared_person_id": "uuid",
  "administered_at": "2024-01-15T08:00:00Z",
  "dosage_given": "500mg",
  "status": "taken",
  "administered_by": "uuid",
  "notes": "Paciente tomó la medicación sin problemas"
}
```

#### Actualizar registro de medicación
**PUT** `/api/v1/medication-logs/{log_id}`

#### Eliminar registro de medicación
**DELETE** `/api/v1/medication-logs/{log_id}`

### Protocolos de Sujeción

#### Listar protocolos de sujeción
**GET** `/api/v1/restraint-protocols/`
- Query: `cared_person_id`, `protocol_type`, `is_active`, `skip`, `limit`

#### Crear protocolo de sujeción
**POST** `/api/v1/restraint-protocols/`
- **Content-Type:** `multipart/form-data`
```json
{
  "cared_person_id": "uuid",
  "protocol_type": "physical",
  "name": "Protocolo de sujeción para prevención de caídas",
  "description": "Protocolo para prevenir caídas durante la noche",
  "indications": ["confusión nocturna", "riesgo de caída alto"],
  "contraindications": ["úlceras por presión", "problemas circulatorios"],
  "procedures": [
    {
      "step": 1,
      "description": "Evaluar necesidad de sujeción",
      "duration": "5 minutos"
    }
  ],
  "monitoring_requirements": ["cada 2 horas", "evaluar piel"],
  "emergency_procedures": ["liberar inmediatamente si hay complicaciones"],
  "authorized_by": "Dr. García",
  "authorization_date": "2024-01-15",
  "review_date": "2024-02-15",
  "is_active": true,
  "attached_files": ["archivo.pdf"] // opcional
}
```

#### Actualizar protocolo de sujeción
**PUT** `/api/v1/restraint-protocols/{protocol_id}`

#### Eliminar protocolo de sujeción
**DELETE** `/api/v1/restraint-protocols/{protocol_id}`

### Observaciones de Turno

#### Listar observaciones de turno
**GET** `/api/v1/shift-observations/`
- Query: `cared_person_id`, `caregiver_id`, `shift_type`, `status`, `start_date`, `end_date`, `incidents_only`, `skip`, `limit`

#### Crear observación de turno
**POST** `/api/v1/shift-observations/`
```json
{
  "cared_person_id": "uuid",
  "caregiver_id": "uuid",
  "shift_type": "night",
  "shift_start": "2024-01-15T20:00:00Z",
  "shift_end": "2024-01-16T08:00:00Z",
  "observation_date": "2024-01-15T20:00:00Z",
  "physical_condition": "fair",
  "mental_state": "confused",
  "safety_concerns": "Paciente presenta confusión nocturna",
  "incidents_occurred": true,
  "incident_details": "Paciente intentó levantarse de la cama sin asistencia a las 02:30",
  "fall_risk_assessment": "high",
  "status": "draft"
}
```

#### Actualizar observación de turno
**PUT** `/api/v1/shift-observations/{observation_id}`

#### Eliminar observación de turno
**DELETE** `/api/v1/shift-observations/{observation_id}`

#### Verificar observación de turno
**PATCH** `/api/v1/shift-observations/{observation_id}/verify`
```json
{
  "verified_by": "uuid",
  "verification_notes": "Observación verificada y aprobada"
}
```

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

### Cambio de rol de usuario: exclusividad y soft delete

A partir de la versión X.X.X, al cambiar el rol de un usuario:
- El backend desactiva (soft delete) todos los roles previos del usuario.
- Solo el nuevo rol queda activo.
- Se mantiene el historial de roles previos para trazabilidad.

Esto garantiza que un usuario solo puede tener un rol activo a la vez y que el sistema cumple con la lógica de negocio de exclusividad de rol.

---

## Política de Soft Delete y Manejo de Datos Asociados a Roles

- Al cambiar el rol de un usuario, todos los datos asociados al rol anterior se marcan como **soft deleted** (no se eliminan físicamente, solo se desactivan para la operación diaria).
- Si el usuario vuelve a un rol anterior (por ejemplo, de "caregiver" a "family_member" y luego nuevamente a "caregiver"), **no se reactivan los datos soft deleted** de ciclos previos.
- En cada reasignación de rol, se crean nuevos registros asociados al nuevo ciclo del rol. Los datos soft deleted quedan como histórico y pueden ser consultados para auditoría o trazabilidad, pero no se usan en la operación normal.
- Esta política garantiza trazabilidad total, integridad histórica y cumplimiento de buenas prácticas de auditoría.

> **Nota:** Si se requiere recuperar datos previos, debe hacerse mediante un proceso manual o una restauración explícita, nunca de forma automática.

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

## Validación de datos esenciales al cambiar de rol de usuario

A partir de la versión X.X.X, al cambiar el rol de un usuario mediante el endpoint correspondiente, el backend:

- Realiza un soft delete de registros asociados a roles que el usuario ya no debe tener.
- Valida y crea los registros esenciales para el nuevo rol.
- Si faltan datos obligatorios para el nuevo rol, responde con HTTP 422 y un objeto JSON con las claves:
    - `message`: Mensaje explicativo.
    - `missing_fields`: Lista de campos requeridos que faltan.

**Regla de integración frontend:**
El frontend debe interceptar este error, mostrar un modal popup explicativo con el mensaje y los campos faltantes, y bloquear la operación hasta que el usuario complete los datos requeridos. 

## Lógica de Contratación y Visualización de Paquetes

- **Solo pueden contratar paquetes:**
  - Administrador institucional (`admin_institution`, `institution_admin`)
  - Persona auto-cuidante (`self_cared_person`, `cared_person_self`)
  - Familia o familiar (`family`, `family_member`)
- **El staff institucional** (`institution_staff`) solo puede visualizar los paquetes, pero no contratarlos.
- Si un usuario con otro rol intenta contratar, la API devuelve un error claro y el frontend muestra un mensaje UX adecuado.

**Ejemplo de respuesta de error:**
```
{
  "detail": "Solo el administrador de la institución puede contratar paquetes. El staff solo puede visualizar."
}
```

Esta lógica se aplica tanto en backend (API) como en frontend (UI/UX), garantizando coherencia y cumplimiento de la regla de negocio. 

## Política de asociación de paquetes y roles

- Cada usuario puede tener solo un rol activo a la vez.
- Solo los roles habilitados pueden asociarse a paquetes (por ejemplo: caredperson, familia, selfcared person, caregiver).
- Si un usuario con un rol no habilitado (por ejemplo, staff institucional) desea adquirir un paquete, debe crear una nueva cuenta con el rol correspondiente.
- No se permite la asociación de múltiples paquetes en diferentes contextos para una misma cuenta.
- Esta política simplifica la gestión, mejora la trazabilidad y evita ambigüedades en los permisos y accesos.

> **Nota:** Si en el futuro se habilita la multi-asociación de roles o paquetes, esta política deberá ser revisada y adaptada en consecuencia. 

## Convención de nombres de roles y procedimiento de unificación

- Los nombres de roles deben ser únicos y consistentes en todo el sistema (backend, frontend y base de datos).
- Los nombres canónicos para roles clave son:
    - `institution_admin` (Administrador de institución)
    - `cared_person_self` (Persona en autocuidado)
- Se eliminaron los nombres duplicados/históricos: `admin_institution`, `self_cared_person`.
- El procedimiento de unificación consistió en:
    1. Actualizar el código y scripts para usar solo los nombres canónicos.
    2. Actualizar los registros de usuarios en la base de datos para apuntar a los roles correctos.
    3. Eliminar los roles duplicados de la tabla `roles`.
    4. Documentar la convención para evitar futuros problemas de compatibilidad.
- Si se detectan nuevos duplicados, repetir el procedimiento y mantener la documentación actualizada. 

## Política y procedimiento de población de paquetes

- **Paquetes personales**: Solo pueden ser asignados a usuarios con roles `cared_person_self`, `family`, `family_member`. Los scripts de población asignan automáticamente paquetes de tipo `individual` a estos usuarios, evitando duplicados y respetando la lógica de negocio.
- **Paquetes institucionales**: Solo pueden ser asignados a instituciones activas. Los scripts de población asignan automáticamente todos los paquetes de tipo `institutional` a todas las instituciones activas, sin mezclar con paquetes personales.
- **No se permite** la asignación cruzada (usuarios personales no pueden tener paquetes institucionales y viceversa).
- **Scripts involucrados**:
    - `backend/scripts/modules/business/addons.py` → función `populate_user_packages` (paquetes personales)
    - `backend/scripts/populate_institution_packages.py` → función `populate_institution_packages` (paquetes institucionales)
- Esta política asegura trazabilidad, consistencia y cumplimiento de las reglas de negocio en la base de datos poblada para desarrollo y pruebas. 