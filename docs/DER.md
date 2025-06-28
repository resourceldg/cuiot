# Diagrama Entidad-Relación (DER) - Sistema de Monitoreo Integral de Cuidado Humano

---

## Resumen Ejecutivo

Este documento presenta el modelo de datos completo para el sistema de monitoreo de cuidado humano, diseñado para soportar todos los tipos de usuarios, servicios, dispositivos, protocolos y funcionalidades definidas en las reglas de negocio.

---

## 1. Entidades Principales

### 1.1 USERS (Usuarios)
**Descripción**: Tabla central de usuarios del sistema con diferentes roles y capacidades.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único del usuario
- `email` (VARCHAR(255), UNIQUE): Email único del usuario
- `phone` (VARCHAR(20)): Teléfono de contacto
- `first_name` (VARCHAR(100)): Nombre
- `last_name` (VARCHAR(100)): Apellido
- `date_of_birth` (DATE): Fecha de nacimiento
- `is_active` (BOOLEAN): Estado activo/inactivo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de última actualización

**Relaciones**:
- Un usuario puede tener múltiples roles (USER_ROLES)
- Un usuario puede ser cuidador de múltiples personas (CAREGIVER_ASSIGNMENTS)
- Un usuario puede ser persona bajo cuidado (CARED_PERSONS)
- Un usuario puede pertenecer a múltiples instituciones (USER_INSTITUTIONS)

### 1.2 ROLES (Roles)
**Descripción**: Roles disponibles en el sistema.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único del rol
- `name` (VARCHAR(50)): Nombre del rol (admin, caregiver, family, patient, etc.)
- `description` (TEXT): Descripción del rol
- `permissions` (JSONB): Permisos específicos del rol

### 1.3 CARED_PERSONS (Personas Bajo Cuidado)
**Descripción**: Personas que reciben cuidado, independientemente de su edad o condición.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `user_id` (UUID, FK): Referencia al usuario
- `care_type` (VARCHAR(50)): Tipo de cuidado (elderly, disability, autism, medical, recovery)
- `disability_type` (VARCHAR(100)): Tipo de discapacidad si aplica
- `medical_conditions` (JSONB): Condiciones médicas
- `medications` (JSONB): Medicamentos y horarios
- `emergency_contacts` (JSONB): Contactos de emergencia
- `care_preferences` (JSONB): Preferencias de cuidado
- `accessibility_needs` (JSONB): Necesidades de accesibilidad
- `guardian_info` (JSONB): Información del tutor legal
- `is_self_care` (BOOLEAN): Si es autocuidado

**Relaciones**:
- Una persona bajo cuidado debe tener al menos un cuidador (CAREGIVER_ASSIGNMENTS)
- Una persona puede tener múltiples dispositivos (DEVICES)
- Una persona puede pertenecer a una institución (INSTITUTION_ASSIGNMENTS)
- Una persona puede tener múltiples servicios (SERVICE_SUBSCRIPTIONS)

### 1.4 INSTITUTIONS (Instituciones)
**Descripción**: Centros de cuidado, escuelas especiales, geriátricos, etc.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `name` (VARCHAR(200)): Nombre de la institución
- `institution_type` (VARCHAR(50)): Tipo (geriatric, day_center, special_school, rehabilitation)
- `address` (TEXT): Dirección completa
- `phone` (VARCHAR(20)): Teléfono
- `email` (VARCHAR(255)): Email
- `capacity` (INTEGER): Capacidad total
- `current_occupancy` (INTEGER): Ocupación actual
- `staff_count` (INTEGER): Cantidad de personal
- `services_offered` (JSONB): Servicios ofrecidos
- `operating_hours` (JSONB): Horarios de operación
- `emergency_protocols` (JSONB): Protocolos de emergencia
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Una institución puede tener múltiples usuarios (USER_INSTITUTIONS)
- Una institución puede tener múltiples servicios (SERVICE_SUBSCRIPTIONS)
- Una institución puede tener múltiples dispositivos (DEVICES)

### 1.5 SERVICES (Servicios)
**Descripción**: Planes y servicios contratados por usuarios o instituciones.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `name` (VARCHAR(100)): Nombre del servicio
- `service_type` (VARCHAR(50)): Tipo (basic, premium, institutional, specialized)
- `description` (TEXT): Descripción del servicio
- `price_monthly` (DECIMAL(10,2)): Precio mensual
- `features` (JSONB): Características incluidas
- `device_limit` (INTEGER): Límite de dispositivos
- `user_limit` (INTEGER): Límite de usuarios
- `storage_limit_gb` (INTEGER): Límite de almacenamiento
- `is_active` (BOOLEAN): Estado activo

### 1.6 DEVICES (Dispositivos)
**Descripción**: Dispositivos IoT y sensores del sistema.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `device_id` (VARCHAR(100), UNIQUE): ID único del dispositivo
- `name` (VARCHAR(100)): Nombre del dispositivo
- `device_type` (VARCHAR(50)): Tipo (motion_sensor, camera, panic_button, wearable, etc.)
- `model` (VARCHAR(100)): Modelo del dispositivo
- `manufacturer` (VARCHAR(100)): Fabricante
- `firmware_version` (VARCHAR(50)): Versión de firmware
- `config` (JSONB): Configuración específica
- `location` (VARCHAR(100)): Ubicación del dispositivo
- `battery_level` (INTEGER): Nivel de batería (0-100)
- `last_maintenance` (TIMESTAMP): Último mantenimiento
- `warranty_expiry` (TIMESTAMP): Vencimiento de garantía
- `accessibility_features` (JSONB): Características de accesibilidad
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Un dispositivo debe estar asociado a un servicio (SERVICE_SUBSCRIPTIONS)
- Un dispositivo puede estar asociado a una persona (CARED_PERSONS) o institución (INSTITUTIONS)
- Un dispositivo puede generar múltiples eventos (EVENTS)

### 1.7 PROTOCOLS (Protocolos)
**Descripción**: Protocolos configurables para diferentes tipos de crisis y eventos.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `name` (VARCHAR(100)): Nombre del protocolo
- `protocol_type` (VARCHAR(50)): Tipo (fall, seizure, wandering, autism_crisis, etc.)
- `description` (TEXT): Descripción del protocolo
- `contact_sequence` (JSONB): Secuencia de contactos
- `escalation_times` (JSONB): Tiempos de escalación
- `automatic_actions` (JSONB): Acciones automáticas
- `is_active` (BOOLEAN): Estado activo
- `created_by` (UUID, FK): Usuario que creó el protocolo

**Relaciones**:
- Un protocolo puede estar asociado a múltiples usuarios (USER_PROTOCOLS)
- Un protocolo puede estar asociado a múltiples instituciones (INSTITUTION_PROTOCOLS)

### 1.8 EVENTS (Eventos)
**Descripción**: Eventos generados por dispositivos o usuarios.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `event_type` (VARCHAR(50)): Tipo de evento
- `severity` (VARCHAR(20)): Severidad (low, medium, high, critical)
- `device_id` (VARCHAR(100)): Dispositivo que generó el evento
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `location_data` (JSONB): Datos de ubicación
- `sensor_data` (JSONB): Datos del sensor
- `timestamp` (TIMESTAMP): Timestamp del evento
- `processed` (BOOLEAN): Si fue procesado
- `notes` (TEXT): Notas adicionales

**Relaciones**:
- Un evento puede generar múltiples alertas (ALERTS)
- Un evento está asociado a una persona bajo cuidado (CARED_PERSONS)

### 1.9 ALERTS (Alertas)
**Descripción**: Alertas generadas por eventos según protocolos.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `event_id` (UUID, FK): Evento que generó la alerta
- `alert_type` (VARCHAR(50)): Tipo de alerta
- `severity` (VARCHAR(20)): Severidad
- `status` (VARCHAR(20)): Estado (pending, sent, acknowledged, resolved)
- `recipients` (JSONB): Destinatarios de la alerta
- `sent_at` (TIMESTAMP): Fecha de envío
- `acknowledged_at` (TIMESTAMP): Fecha de reconocimiento
- `resolved_at` (TIMESTAMP): Fecha de resolución
- `escalation_level` (INTEGER): Nivel de escalación actual

**Relaciones**:
- Una alerta está asociada a un evento (EVENTS)
- Una alerta puede tener múltiples notificaciones (NOTIFICATIONS)

### 1.10 LOCATION_TRACKING (Seguimiento de Ubicación)
**Descripción**: Datos de geolocalización de usuarios.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `device_id` (VARCHAR(100)): Dispositivo de tracking
- `latitude` (DECIMAL(10,8)): Latitud
- `longitude` (DECIMAL(11,8)): Longitud
- `accuracy` (FLOAT): Precisión en metros
- `timestamp` (TIMESTAMP): Timestamp de la ubicación
- `location_type` (VARCHAR(50)): Tipo (home, center, outdoor, unknown)

**Relaciones**:
- Un registro de ubicación está asociado a una persona (CARED_PERSONS)

### 1.11 GEOFENCES (Geofences)
**Descripción**: Áreas seguras para monitoreo de ubicación.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `name` (VARCHAR(100)): Nombre del geofence
- `center_latitude` (DECIMAL(10,8)): Latitud del centro
- `center_longitude` (DECIMAL(11,8)): Longitud del centro
- `radius_meters` (INTEGER): Radio en metros
- `alert_on_exit` (BOOLEAN): Alertar al salir
- `alert_on_enter` (BOOLEAN): Alertar al entrar
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Un geofence está asociado a una persona (CARED_PERSONS)

---

## 2. Tablas de Relación

### 2.1 USER_ROLES
**Descripción**: Relación muchos a muchos entre usuarios y roles.

**Atributos**:
- `user_id` (UUID, FK): Usuario
- `role_id` (UUID, FK): Rol
- `assigned_at` (TIMESTAMP): Fecha de asignación

### 2.2 CAREGIVER_ASSIGNMENTS
**Descripción**: Asignación de cuidadores a personas bajo cuidado.

**Atributos**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `caregiver_user_id` (UUID, FK): Usuario cuidador
- `relationship` (VARCHAR(50)): Relación (family, professional, guardian)
- `is_primary` (BOOLEAN): Si es cuidador principal
- `availability_hours` (JSONB): Horarios de disponibilidad
- `assigned_at` (TIMESTAMP): Fecha de asignación

### 2.3 SERVICE_SUBSCRIPTIONS
**Descripción**: Suscripciones de usuarios o instituciones a servicios.

**Atributos**:
- `id` (UUID, PK): Identificador único
- `user_id` (UUID, FK, NULL): Usuario (NULL si es institucional)
- `institution_id` (UUID, FK, NULL): Institución (NULL si es individual)
- `service_id` (UUID, FK): Servicio contratado
- `status` (VARCHAR(20)): Estado (active, suspended, cancelled, pending)
- `start_date` (DATE): Fecha de inicio
- `end_date` (DATE): Fecha de fin
- `billing_cycle` (VARCHAR(20)): Ciclo de facturación
- `price` (DECIMAL(10,2)): Precio acordado
- `modules` (JSONB): Módulos adicionales contratados

### 2.4 USER_INSTITUTIONS
**Descripción**: Relación entre usuarios e instituciones.

**Atributos**:
- `user_id` (UUID, FK): Usuario
- `institution_id` (UUID, FK): Institución
- `role_in_institution` (VARCHAR(50)): Rol en la institución
- `start_date` (DATE): Fecha de inicio
- `end_date` (DATE): Fecha de fin (NULL si activo)

### 2.5 USER_PROTOCOLS
**Descripción**: Protocolos asignados a usuarios específicos.

**Atributos**:
- `user_id` (UUID, FK): Usuario
- `protocol_id` (UUID, FK): Protocolo
- `is_active` (BOOLEAN): Estado activo
- `assigned_at` (TIMESTAMP): Fecha de asignación

### 2.6 INSTITUTION_PROTOCOLS
**Descripción**: Protocolos estándar de instituciones.

**Atributos**:
- `institution_id` (UUID, FK): Institución
- `protocol_id` (UUID, FK): Protocolo
- `is_active` (BOOLEAN): Estado activo
- `assigned_at` (TIMESTAMP): Fecha de asignación

---

## 3. Diagrama Visual (Representación Textual)

```
USERS (1) ←→ (N) USER_ROLES (N) ←→ (1) ROLES
USERS (1) ←→ (N) CARED_PERSONS (1) ←→ (N) CAREGIVER_ASSIGNMENTS (N) ←→ (1) USERS
USERS (N) ←→ (M) USER_INSTITUTIONS (M) ←→ (N) INSTITUTIONS
USERS (1) ←→ (N) SERVICE_SUBSCRIPTIONS (N) ←→ (1) SERVICES
INSTITUTIONS (1) ←→ (N) SERVICE_SUBSCRIPTIONS (N) ←→ (1) SERVICES

CARED_PERSONS (1) ←→ (N) DEVICES (N) ←→ (1) SERVICE_SUBSCRIPTIONS
INSTITUTIONS (1) ←→ (N) DEVICES (N) ←→ (1) SERVICE_SUBSCRIPTIONS

DEVICES (1) ←→ (N) EVENTS (1) ←→ (N) ALERTS
CARED_PERSONS (1) ←→ (N) EVENTS (1) ←→ (N) ALERTS

CARED_PERSONS (1) ←→ (N) LOCATION_TRACKING
CARED_PERSONS (1) ←→ (N) GEOFENCES

USERS (1) ←→ (N) USER_PROTOCOLS (N) ←→ (1) PROTOCOLS
INSTITUTIONS (1) ←→ (N) INSTITUTION_PROTOCOLS (N) ←→ (1) PROTOCOLS
```

---

## 4. Reglas de Negocio Implementadas

### 4.1 Validaciones de Integridad
- Un usuario debe tener al menos un rol (USER_ROLES)
- Una persona bajo cuidado debe tener al menos un cuidador (CAREGIVER_ASSIGNMENTS)
- Un servicio debe estar asociado a al menos un dispositivo (DEVICES)
- Un dispositivo debe estar asociado a un servicio activo (SERVICE_SUBSCRIPTIONS)

### 4.2 Estados y Transiciones
- Los servicios pueden estar en estados: active, suspended, cancelled, pending
- Las alertas pueden estar en estados: pending, sent, acknowledged, resolved
- Los dispositivos pueden estar: online, offline, maintenance, error

### 4.3 Configuraciones JSONB
- `medical_conditions`: Condiciones médicas específicas
- `medications`: Horarios y dosis de medicamentos
- `emergency_contacts`: Secuencia de contactos de emergencia
- `care_preferences`: Preferencias de cuidado personalizadas
- `accessibility_needs`: Necesidades de accesibilidad
- `protocols`: Configuración de protocolos específicos

---

## 5. Consideraciones de Implementación

### 5.1 Índices Recomendados
- `users.email` (UNIQUE)
- `devices.device_id` (UNIQUE)
- `events.timestamp` (para consultas temporales)
- `location_tracking.timestamp` (para consultas de ubicación)
- `alerts.status` (para consultas de alertas pendientes)

### 5.2 Particionamiento
- `events` por fecha (mensual)
- `location_tracking` por fecha (mensual)
- `alerts` por fecha (mensual)

### 5.3 Encriptación
- Datos médicos en `medical_conditions`
- Contactos de emergencia en `emergency_contacts`
- Configuraciones sensibles en `config` de dispositivos

---

*Documento en desarrollo - Versión 1.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 