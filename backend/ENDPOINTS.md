# Documentación de Endpoints Backend

> **NOTA:** Todos los catálogos normalizados (status, tipos, etc.) deben referenciarse por su **ID** (clave foránea), no por string. Los ejemplos de request/response muestran los campos normalizados como IDs.

Este documento describe todos los endpoints principales del backend, su funcionalidad, parámetros, respuestas, errores comunes y el servicio asociado. Cada sección sigue un formato profesional y uniforme.

---

## 1. Usuarios

### Crear usuario
- **POST** `/api/v1/users/`
- **Descripción:** Crea un nuevo usuario en el sistema.
- **Parámetros:** JSON con datos de usuario (nombre, email, contraseña, etc.)
- **Respuesta:** Usuario creado (modelo UserResponse)
- **Errores:** 400 (datos inválidos), 409 (usuario ya existe)
- **Servicio:** `UserService.create_user`
- **Ejemplo request:**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@example.com",
  "password": "12345678"
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@example.com",
  "created_at": "2024-07-04T10:00:00Z"
}
```
- **Ejemplo error:**
```json
{"detail": "El email ya está registrado"}
```

### Obtener usuario actual
- **GET** `/api/v1/users/me`
- **Descripción:** Devuelve los datos del usuario autenticado.
- **Respuesta:** UserResponse
- **Errores:** 401 (no autenticado)
- **Servicio:** `UserService.get_current_user`
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@example.com"
}
```

---

## 2. Personas bajo cuidado

### Crear persona bajo cuidado
- **POST** `/api/v1/cared-persons/`
- **Descripción:** Crea una nueva persona bajo cuidado.
- **Parámetros:** JSON con datos personales y de contexto.
- **Respuesta:** CaredPersonResponse
- **Errores:** 400, 409
- **Servicio:** `CaredPersonService.create_cared_person`
- **Ejemplo request:**
```json
{
  "first_name": "Ana",
  "last_name": "García",
  "birth_date": "1940-05-12",
  "gender": "female"
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "first_name": "Ana",
  "last_name": "García",
  "birth_date": "1940-05-12",
  "gender": "female",
  "created_at": "2024-07-04T10:10:00Z"
}
```

### Listar personas bajo cuidado
- **GET** `/api/v1/cared-persons/`
- **Descripción:** Lista todas las personas bajo cuidado asociadas al usuario.
- **Respuesta:** Lista de CaredPersonResponse
- **Errores:** 401
- **Servicio:** `CaredPersonService.get_cared_persons`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "first_name": "Ana",
    "last_name": "García"
  },
  {
    "id": "uuid2",
    "first_name": "Luis",
    "last_name": "Martínez"
  }
]
```

---

## 3. Recordatorios

### Crear recordatorio
- **POST** `/api/v1/reminders/`
- **Descripción:** Crea un recordatorio para una persona bajo cuidado.
- **Parámetros:** JSON con título, descripción, tipo, fecha/hora, etc.
- **Respuesta:** ReminderResponse
- **Errores:** 400, 404
- **Servicio:** `ReminderService.create_reminder`
- **Ejemplo request:**
```json
{
  "title": "Tomar medicación",
  "description": "Pastilla para la presión",
  "reminder_type": "medication",
  "scheduled_time": "2024-07-04T08:00:00Z",
  "elderly_person_id": "uuid-persona"
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "title": "Tomar medicación",
  "description": "Pastilla para la presión",
  "reminder_type": "medication",
  "scheduled_time": "2024-07-04T08:00:00Z",
  "elderly_person_id": "uuid-persona",
  "created_at": "2024-07-04T07:00:00Z"
}
```

### Listar recordatorios
- **GET** `/api/v1/reminders/`
- **Descripción:** Lista recordatorios con filtros por usuario, tipo, estado.
- **Respuesta:** Lista de ReminderResponse
- **Errores:** 401
- **Servicio:** `ReminderService.get_reminders`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "title": "Tomar medicación",
    "reminder_type": "medication"
  },
  {
    "id": "uuid2",
    "title": "Cita médica",
    "reminder_type": "appointment"
  }
]
```

---

## 4. Alertas

### Crear alerta
- **POST** `/api/v1/alerts/`
- **Descripción:** Crea una alerta para una persona bajo cuidado o dispositivo.
- **Parámetros:** JSON con tipo, severidad, mensaje, etc.
- **Respuesta:** AlertResponse
- **Errores:** 400, 404
- **Servicio:** `AlertService.create_alert`
- **Ejemplo request:**
```json
{
  "alert_type": "fall",
  "severity": "high",
  "message": "Caída detectada en habitación 2",
  "cared_person_id": "uuid-persona"
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "alert_type": "fall",
  "severity": "high",
  "message": "Caída detectada en habitación 2",
  "created_at": "2024-07-04T09:00:00Z"
}
```

### Listar alertas
- **GET** `/api/v1/alerts/`
- **Descripción:** Lista alertas con filtros por usuario, tipo, severidad, estado.
- **Respuesta:** Lista de AlertResponse
- **Errores:** 401
- **Servicio:** `AlertService.get_alerts`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "alert_type": "fall",
    "severity": "high"
  },
  {
    "id": "uuid2",
    "alert_type": "medication_missed",
    "severity": "medium"
  }
]
```

---

## 5. Dispositivos

### Registrar dispositivo
- **POST** `/api/v1/devices/`
- **Descripción:** Registra un nuevo dispositivo en el sistema.
- **Parámetros:** JSON con datos del dispositivo.
- **Respuesta:** DeviceResponse
- **Errores:** 400, 409
- **Servicio:** `DeviceService.register_device`
- **Ejemplo request:**
```json
{
  "device_type": "sensor",
  "serial_number": "SN123456",
  "user_id": "uuid-usuario"
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "device_type": "sensor",
  "serial_number": "SN123456",
  "user_id": "uuid-usuario",
  "created_at": "2024-07-04T11:00:00Z"
}
```

### Listar dispositivos
- **GET** `/api/v1/devices/`
- **Descripción:** Lista dispositivos asociados al usuario.
- **Respuesta:** Lista de DeviceResponse
- **Errores:** 401
- **Servicio:** `DeviceService.get_devices`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "device_type": "sensor",
    "serial_number": "SN123456"
  },
  {
    "id": "uuid2",
    "device_type": "wearable",
    "serial_number": "SN654321"
  }
]
```

---

## 6. Diagnósticos

### Crear diagnóstico
- **POST** `/api/v1/diagnoses/`
- **Descripción:** Crea un diagnóstico médico para una persona bajo cuidado.
- **Parámetros:** FormData con nombre, descripción, severidad, fecha, archivos adjuntos, etc.
- **Respuesta:** DiagnosisResponse
- **Errores:** 400, 404
- **Servicio:** `DiagnosisService.create_diagnosis`
- **Ejemplo request (FormData):**
```
diagnosis_name: "Diabetes tipo 2"
description: "Diagnóstico reciente"
severity_level: "moderate"
diagnosis_date: "2024-07-01"
cared_person_id: "uuid-persona"
files: [archivo.pdf]
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "diagnosis_name": "Diabetes tipo 2",
  "description": "Diagnóstico reciente",
  "severity_level": "moderate",
  "diagnosis_date": "2024-07-01",
  "cared_person_id": "uuid-persona",
  "created_at": "2024-07-04T12:00:00Z"
}
```

### Listar diagnósticos
- **GET** `/api/v1/diagnoses/`
- **Descripción:** Lista diagnósticos médicos con filtros.
- **Respuesta:** Lista de DiagnosisResponse
- **Errores:** 401
- **Servicio:** `DiagnosisService.get_diagnoses`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "diagnosis_name": "Diabetes tipo 2"
  },
  {
    "id": "uuid2",
    "diagnosis_name": "Hipertensión"
  }
]
```

---

## 7. Reportes

### Crear reporte
- **POST** `/api/v1/reports/`
- **Descripción:** Crea un reporte asociado a un usuario o persona bajo cuidado.
- **Parámetros:** JSON con título, descripción, tipo, archivos adjuntos, etc.
- **Respuesta:** ReportResponse
- **Errores:** 400, 404
- **Servicio:** `ReportService.create_report`
- **Ejemplo request:**
```json
{
  "title": "Reporte de caída",
  "description": "Caída en el baño",
  "report_type": "incident",
  "cared_person_id": "uuid-persona",
  "attached_files": []
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "title": "Reporte de caída",
  "description": "Caída en el baño",
  "report_type": "incident",
  "cared_person_id": "uuid-persona",
  "created_at": "2024-07-04T13:00:00Z"
}
```

### Listar reportes
- **GET** `/api/v1/reports/`
- **Descripción:** Lista todos los reportes disponibles.
- **Respuesta:** Lista de ReportResponse
- **Errores:** 401
- **Servicio:** `ReportService.list_reports`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "title": "Reporte de caída"
  },
  {
    "id": "uuid2",
    "title": "Reporte de medicación"
  }
]
```

---

## 8. Paquetes y suscripciones

### Listar paquetes
- **GET** `/api/v1/packages/`
- **Descripción:** Lista paquetes disponibles, con filtros por tipo y destacados.
- **Respuesta:** Lista de PackageResponse
- **Errores:** 401
- **Servicio:** `PackageService.get_available_packages`
- **Ejemplo response:**
```json
[
  {
    "id": "uuid1",
    "name": "Básico",
    "price_monthly": 1000
  },
  {
    "id": "uuid2",
    "name": "Premium",
    "price_monthly": 2000
  }
]
```

### Suscribirse a paquete
- **POST** `/api/v1/packages/user/subscriptions`
- **Descripción:** Suscribe al usuario a un paquete.
- **Parámetros:** JSON con datos de suscripción.
- **Respuesta:** UserPackageResponse
- **Errores:** 400, 409
- **Servicio:** `PackageService.subscribe_user_package`
- **Ejemplo request:**
```json
{
  "package_id": "uuid-paquete",
  "user_id": "uuid-usuario"
}
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "package_id": "uuid-paquete",
  "user_id": "uuid-usuario",
  "status": "active"
}
```

---

## 9. Protocolos de sujeción

### Crear protocolo
- **POST** `/api/v1/restraint-protocols/`
- **Descripción:** Crea un protocolo de sujeción para una persona bajo cuidado.
- **Parámetros:** FormData con tipo, título, justificación, fechas, archivos, etc.
- **Respuesta:** RestraintProtocolResponse
- **Errores:** 400, 404
- **Servicio:** `RestraintProtocolService.create_restraint_protocol`
- **Ejemplo request (FormData):**
```
protocol_type: "physical"
title: "Sujeción por riesgo de caída"
justification: "Prevención de caídas"
start_date: "2024-07-04"
cared_person_id: "uuid-persona"
files: [protocolo.pdf]
```
- **Ejemplo response:**
```json
{
  "id": "uuid",
  "protocol_type": "physical",
  "title": "Sujeción por riesgo de caída",
  "justification": "Prevención de caídas",
  "cared_person_id": "uuid-persona",
  "created_at": "2024-07-04T14:00:00Z"
}
```

### Resumen de protocolos
- **GET** `/api/v1/restraint-protocols/summary/overview`
- **Descripción:** Obtiene un resumen estadístico de protocolos activos, por tipo y estado.
- **Respuesta:** RestraintProtocolSummary
- **Errores:** 401
- **Servicio:** `RestraintProtocolService.get_protocol_summary`
- **Ejemplo response:**
```json
{
  "total": 5,
  "active": 3,
  "by_type": {"physical": 2, "chemical": 1},
  "by_status": {"active": 3, "completed": 2}
}
```

---

## 10. Otros recursos

- **Enumeraciones:** `/api/v1/enumeration-types/`
- **Eventos:** `/api/v1/events/`
- **Observaciones de turno:** `/api/v1/shift-observations/`
- **Puntajes y reviews de cuidadores:** `/api/v1/caregiver-scores/`, `/api/v1/caregiver-reviews/`
- **Perfiles médicos, logs de medicación, etc.**

---

> Para cada endpoint, consulta el código fuente para ver los modelos de entrada/salida exactos y los servicios asociados. Esta documentación resume la funcionalidad y el flujo de negocio según el estado actual del backend y la base de datos, con ejemplos representativos. 