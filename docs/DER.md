# Diagrama Entidad-Relación (DER) - Sistema de Monitoreo Integral de Cuidado Humano

---

## Resumen Ejecutivo

Este documento presenta el modelo de datos completo para el sistema de monitoreo de cuidado humano, diseñado para soportar todos los tipos de usuarios, servicios, dispositivos, protocolos y funcionalidades definidas en las reglas de negocio. **Actualizado para incluir Sistema de Paquetes como unidad central del negocio.**

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
- Un usuario puede tener múltiples paquetes (PACKAGES)
- Un usuario puede hacer múltiples referidos (REFERRALS)
- Un usuario puede recibir múltiples comisiones (REFERRAL_COMMISSIONS)

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
- `user_id` (UUID, FK): Referencia al usuario (representante legal para cuidado delegado)
- `care_type` (VARCHAR(50)): Tipo de cuidado (self_care, delegated)
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
- Una persona puede pertenecer a múltiples instituciones (CARED_PERSON_INSTITUTIONS)
- Una persona puede tener múltiples paquetes (PACKAGES) - solo si es autocuidado
- Una persona puede hacer referidos (REFERRALS) - solo si es autocuidado

### 1.4 PACKAGES (Paquetes - NUEVA ENTIDAD CENTRAL)
**Descripción**: Unidad central del negocio. Paquetes de servicios que pueden ser contratados por usuarios.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `package_type` (VARCHAR(50)): Tipo de paquete (basic, familiar, premium, professional, institutional)
- `name` (VARCHAR(100)): Nombre del paquete
- `description` (TEXT): Descripción del paquete
- `price_monthly` (DECIMAL(10,2)): Precio mensual en centavos
- `price_yearly` (DECIMAL(10,2)): Precio anual en centavos
- `currency` (VARCHAR(3)): Moneda (ARS)
- `features` (JSONB): Características incluidas
- `limitations` (JSONB): Limitaciones del paquete
- `max_users` (INTEGER): Máximo número de usuarios
- `max_devices` (INTEGER): Máximo número de dispositivos
- `max_storage_gb` (INTEGER): Almacenamiento máximo en GB
- `support_level` (VARCHAR(50)): Nivel de soporte (email, chat, phone, 24/7)
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Un paquete puede ser contratado por múltiples usuarios (USER_PACKAGES)
- Un paquete puede ser contratado por múltiples instituciones (INSTITUTION_PACKAGES)
- Un paquete puede generar múltiples facturas (BILLING_RECORDS)

### 1.5 USER_PACKAGES (Paquetes de Usuarios)
**Descripción**: Relación entre usuarios y paquetes contratados.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `user_id` (UUID, FK): Usuario que contrata
- `package_id` (UUID, FK): Paquete contratado
- `start_date` (DATE): Fecha de inicio
- `end_date` (DATE): Fecha de fin (NULL para contratos continuos)
- `auto_renew` (BOOLEAN): Renovación automática
- `status` (VARCHAR(20)): Estado (active, suspended, cancelled, expired)
- `payment_method` (VARCHAR(50)): Método de pago
- `created_at` (TIMESTAMP): Fecha de contratación

### 1.6 INSTITUTIONS (Instituciones)
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
- Una institución puede tener múltiples paquetes (INSTITUTION_PACKAGES)
- Una institución puede tener múltiples dispositivos (DEVICES)
- Una institución puede hacer referidos (REFERRALS)
- Una institución puede recibir comisiones (REFERRAL_COMMISSIONS)

### 1.7 INSTITUTION_PACKAGES (Paquetes de Instituciones)
**Descripción**: Relación entre instituciones y paquetes contratados.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `institution_id` (UUID, FK): Institución que contrata
- `package_id` (UUID, FK): Paquete contratado
- `start_date` (DATE): Fecha de inicio
- `end_date` (DATE): Fecha de fin
- `auto_renew` (BOOLEAN): Renovación automática
- `status` (VARCHAR(20)): Estado
- `payment_method` (VARCHAR(50)): Método de pago
- `max_patients` (INTEGER): Máximo número de pacientes
- `created_at` (TIMESTAMP): Fecha de contratación

### 1.8 REFERRALS (Referidos)
**Descripción**: Sistema de referidos para crecimiento orgánico.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `referral_code` (VARCHAR(20), UNIQUE): Código único de referido
- `referrer_type` (VARCHAR(20)): Tipo de referente (caregiver, institution, family, cared_person)
- `referrer_id` (UUID): ID del referente
- `referred_email` (VARCHAR(100)): Email de la persona referida
- `referred_name` (VARCHAR(100)): Nombre de la persona referida
- `referred_phone` (VARCHAR(20)): Teléfono de la persona referida
- `status` (VARCHAR(20)): Estado (pending, registered, converted, expired)
- `registered_at` (TIMESTAMP): Fecha de registro
- `converted_at` (TIMESTAMP): Fecha de conversión
- `expired_at` (TIMESTAMP): Fecha de expiración
- `commission_amount` (DECIMAL(10,2)): Monto de comisión
- `commission_paid` (BOOLEAN): Si la comisión fue pagada
- `commission_paid_at` (TIMESTAMP): Fecha de pago de comisión
- `notes` (TEXT): Notas adicionales
- `source` (VARCHAR(50)): Fuente del referido (email, whatsapp, phone, in_person)

**Relaciones**:
- Un referido puede generar múltiples comisiones (REFERRAL_COMMISSIONS)

### 1.9 REFERRAL_COMMISSIONS (Comisiones de Referidos)
**Descripción**: Tracking de comisiones por referidos.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `referral_id` (UUID, FK): Referido asociado
- `recipient_type` (VARCHAR(20)): Tipo de receptor (caregiver, institution, family)
- `recipient_id` (UUID): ID del receptor
- `amount` (DECIMAL(10,2)): Monto de la comisión
- `commission_type` (VARCHAR(20)): Tipo (first_month, recurring, bonus)
- `percentage` (DECIMAL(5,2)): Porcentaje de comisión
- `status` (VARCHAR(20)): Estado (pending, paid, cancelled)
- `paid_at` (TIMESTAMP): Fecha de pago

### 1.10 CAREGIVER_SCORES (Puntuaciones de Cuidadores)
**Descripción**: Sistema de scoring para cuidadores.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `caregiver_id` (UUID, FK): Cuidador evaluado
- `experience_score` (DECIMAL(3,2)): Puntuación por experiencia (0-5)
- `quality_score` (DECIMAL(3,2)): Puntuación por calidad (0-5)
- `reliability_score` (DECIMAL(3,2)): Puntuación por confiabilidad (0-5)
- `availability_score` (DECIMAL(3,2)): Puntuación por disponibilidad (0-5)
- `specialization_score` (DECIMAL(3,2)): Puntuación por especialización (0-5)
- `overall_score` (DECIMAL(3,2)): Puntuación general (0-5)
- `total_reviews` (INTEGER): Total de reviews
- `last_calculated` (TIMESTAMP): Última fecha de cálculo

### 1.11 CAREGIVER_REVIEWS (Reviews de Cuidadores)
**Descripción**: Reviews y calificaciones de cuidadores.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `caregiver_id` (UUID, FK): Cuidador evaluado
- `reviewer_id` (UUID, FK): Usuario que hace la review
- `cared_person_id` (UUID, FK): Persona bajo cuidado (opcional)
- `rating` (INTEGER): Calificación (1-5)
- `comment` (TEXT): Comentario
- `categories` (JSONB): Calificaciones por categorías
- `is_recommended` (BOOLEAN): Si recomendaría
- `service_date` (DATE): Fecha del servicio
- `service_hours` (DECIMAL(5,2)): Horas de servicio
- `service_type` (VARCHAR(50)): Tipo de servicio
- `is_verified` (BOOLEAN): Si está verificado
- `is_public` (BOOLEAN): Si es público

### 1.12 INSTITUTION_SCORES (Puntuaciones de Instituciones)
**Descripción**: Sistema de scoring para instituciones.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `institution_id` (UUID, FK): Institución evaluada
- `medical_quality_score` (DECIMAL(3,2)): Puntuación por calidad médica (0-5)
- `infrastructure_score` (DECIMAL(3,2)): Puntuación por infraestructura (0-5)
- `staff_score` (DECIMAL(3,2)): Puntuación por personal (0-5)
- `attention_score` (DECIMAL(3,2)): Puntuación por atención (0-5)
- `price_score` (DECIMAL(3,2)): Puntuación por precios (0-5)
- `overall_score` (DECIMAL(3,2)): Puntuación general (0-5)
- `total_reviews` (INTEGER): Total de reviews
- `last_calculated` (TIMESTAMP): Última fecha de cálculo

### 1.13 INSTITUTION_REVIEWS (Reviews de Instituciones)
**Descripción**: Reviews y calificaciones de instituciones.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `institution_id` (UUID, FK): Institución evaluada
- `reviewer_id` (UUID, FK): Usuario que hace la review
- `cared_person_id` (UUID, FK): Persona bajo cuidado (opcional)
- `rating` (INTEGER): Calificación (1-5)
- `comment` (TEXT): Comentario
- `categories` (JSONB): Calificaciones por categorías
- `is_recommended` (BOOLEAN): Si recomendaría
- `service_date` (DATE): Fecha del servicio
- `service_type` (VARCHAR(50)): Tipo de servicio
- `is_verified` (BOOLEAN): Si está verificado
- `is_public` (BOOLEAN): Si es público

### 1.14 DEVICES (Dispositivos)
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
- Un dispositivo debe estar asociado a un paquete (USER_PACKAGES o INSTITUTION_PACKAGES)
- Un dispositivo puede estar asociado a una persona (CARED_PERSONS) o institución (INSTITUTIONS)
- Un dispositivo puede generar múltiples eventos (EVENTS)

### 1.15 EVENTS (Eventos)
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

### 1.16 ALERTS (Alertas)
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

### 1.17 BILLING_RECORDS (Registros de Facturación)
**Descripción**: Registros de facturación y pagos.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `invoice_number` (VARCHAR(50), UNIQUE): Número de factura único
- `billing_type` (VARCHAR(50)): Tipo de facturación (subscription, service, usage, etc.)
- `description` (TEXT): Descripción
- `amount` (INTEGER): Monto en centavos
- `currency` (VARCHAR(3)): Moneda
- `tax_amount` (INTEGER): Monto de impuestos en centavos
- `total_amount` (INTEGER): Monto total en centavos
- `billing_date` (DATE): Fecha de facturación
- `due_date` (DATE): Fecha de vencimiento
- `paid_date` (DATE): Fecha de pago
- `status` (VARCHAR(20)): Estado (pending, paid, overdue, cancelled)
- `payment_method` (VARCHAR(50)): Método de pago
- `transaction_id` (VARCHAR(100)): ID de transacción

**Relaciones**:
- Una factura puede estar asociada a un paquete (USER_PACKAGES o INSTITUTION_PACKAGES)
- Una factura puede estar asociada a un usuario (USERS) o institución (INSTITUTIONS)

---

## 2. Reglas de Negocio Críticas

### 2.1 Capacidad Legal y Representación
- **Autocuidado**: Puede contratar paquetes directamente
- **Cuidado Delegado**: DEBE tener representante legal vinculado
- **Validación**: Verificar edad y capacidad legal antes de permitir contrataciones

### 2.2 Sistema de Paquetes
- **Unidad Central**: Los paquetes son la unidad central del negocio
- **Contratación**: Solo usuarios con capacidad legal pueden contratar
- **Límites**: Verificar límites de usuarios/dispositivos según paquete
- **Renovación**: Sistema de renovación automática configurable

### 2.3 Sistema de Referidos
- **Comisiones Automáticas**: Cálculo automático según tipo de referente
- **Expiración**: Referidos expiran después de 30 días
- **Bonificaciones**: Bonificaciones por volumen de referidos
- **Tracking**: Seguimiento completo del ciclo de vida del referido

### 2.4 Scoring y Reviews
- **Cálculo Automático**: Scores calculados automáticamente basados en reviews
- **Verificación**: Solo usuarios reales pueden hacer reviews
- **Moderación**: Reviews verificadas por administradores
- **Categorías**: Reviews por categorías específicas

---

## 3. Relaciones Principales

### 3.1 Jerarquía de Usuarios
```
USERS (1) ←→ (N) USER_ROLES
USERS (1) ←→ (N) CARED_PERSONS (como representante)
USERS (1) ←→ (N) USER_PACKAGES
USERS (1) ←→ (N) REFERRALS (como referente)
USERS (1) ←→ (N) REFERRAL_COMMISSIONS (como receptor)
```

### 3.2 Sistema de Paquetes
```
PACKAGES (1) ←→ (N) USER_PACKAGES
PACKAGES (1) ←→ (N) INSTITUTION_PACKAGES
USER_PACKAGES (1) ←→ (N) BILLING_RECORDS
INSTITUTION_PACKAGES (1) ←→ (N) BILLING_RECORDS
```

### 3.3 Sistema de Referidos
```
REFERRALS (1) ←→ (N) REFERRAL_COMMISSIONS
USERS (1) ←→ (N) REFERRALS (como referente)
USERS (1) ←→ (N) REFERRAL_COMMISSIONS (como receptor)
```

### 3.4 Sistema de Scoring
```
USERS (1) ←→ (1) CAREGIVER_SCORES
USERS (1) ←→ (N) CAREGIVER_REVIEWS (como cuidador)
USERS (1) ←→ (N) CAREGIVER_REVIEWS (como reviewer)
INSTITUTIONS (1) ←→ (1) INSTITUTION_SCORES
INSTITUTIONS (1) ←→ (N) INSTITUTION_REVIEWS
```

---

*Diagrama Entidad-Relación - CUIOT v2.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 