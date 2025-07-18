# Diagrama Entidad-Relación (DER) - Sistema de Monitoreo Integral de Cuidado Humano

---

## Resumen Ejecutivo

Este documento presenta el modelo de datos completo para el sistema de monitoreo de cuidado humano, diseñado para soportar todos los tipos de usuarios, servicios, dispositivos, protocolos y funcionalidades definidas en las reglas de negocio. **Actualizado para incluir Sistema de Paquetes como unidad central del negocio, entidades médicas avanzadas y normalización completa de catálogos.**

**🎉 NORMALIZACIÓN COMPLETA**: Todos los campos string de catálogo han sido normalizados a claves foráneas. Se mantienen propiedades legacy para compatibilidad.

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
- Un usuario puede crear múltiples diagnósticos (DIAGNOSES)
- Un usuario puede crear múltiples protocolos de sujeción (RESTRAINT_PROTOCOLS)
- Un usuario puede verificar múltiples observaciones de turno (SHIFT_OBSERVATIONS)

### 1.2 ROLES (Roles)
**Descripción**: Roles disponibles en el sistema.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único del rol
- `name` (VARCHAR(50)): Nombre del rol (admin, caregiver, family, caredperson, etc.)
- `description` (TEXT): Descripción del rol
- `permissions` (JSONB): Permisos específicos del rol

### 1.3 CARED_PERSONS (Personas Bajo Cuidado)
**Descripción**: Personas que reciben cuidado, independientemente de su edad o condición.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `user_id` (UUID, FK): Referencia al usuario (representante legal para cuidado delegado)
- `care_type_id` (INTEGER, FK): Referencia a tabla normalizada de tipos de cuidado
- `first_name` (VARCHAR(100)): Nombre
- `last_name` (VARCHAR(100)): Apellido
- `date_of_birth` (DATE): Fecha de nacimiento
- `gender` (VARCHAR(20)): Género
- `identification_number` (VARCHAR(50)): Número de identificación
- `phone` (VARCHAR(20)): Teléfono
- `email` (VARCHAR(100)): Email
- `emergency_contact` (VARCHAR(100)): Contacto de emergencia
- `emergency_phone` (VARCHAR(20)): Teléfono de emergencia
- `blood_type` (VARCHAR(10)): Tipo de sangre
- `care_level` (VARCHAR(50)): Nivel de cuidado (low, medium, high, critical)
- `special_needs` (TEXT): Necesidades especiales
- `mobility_level` (VARCHAR(50)): Nivel de movilidad
- `address` (TEXT): Dirección
- `latitude` (FLOAT): Latitud
- `longitude` (FLOAT): Longitud
- `institution_id` (INTEGER, FK): Institución principal (legacy)
- `medical_contact_name` (VARCHAR(100)): Nombre del contacto médico
- `medical_contact_phone` (VARCHAR(20)): Teléfono del contacto médico
- `family_contact_name` (VARCHAR(100)): Nombre del contacto familiar
- `family_contact_phone` (VARCHAR(20)): Teléfono del contacto familiar
- `medical_notes` (TEXT): Notas médicas

**Relaciones**:
- Una persona bajo cuidado debe tener al menos un cuidador (CAREGIVER_ASSIGNMENTS)
- Una persona puede tener múltiples dispositivos (DEVICES)
- Una persona puede pertenecer a múltiples instituciones (CARED_PERSON_INSTITUTIONS)
- Una persona puede tener múltiples paquetes (PACKAGES) - solo si es autocuidado
- Una persona puede hacer referidos (REFERRALS) - solo si es autocuidado
- Una persona puede tener un perfil médico (MEDICAL_PROFILES)
- Una persona puede tener múltiples diagnósticos (DIAGNOSES)
- Una persona puede tener múltiples programas de medicación (MEDICATION_SCHEDULES)
- Una persona puede tener múltiples registros de medicación (MEDICATION_LOGS)
- Una persona puede tener múltiples protocolos de sujeción (RESTRAINT_PROTOCOLS)
- Una persona puede tener múltiples observaciones de turno (SHIFT_OBSERVATIONS)

### 1.4 MEDICAL_PROFILES (Perfiles Médicos)
**Descripción**: Perfil médico completo de cada persona bajo cuidado.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `blood_type` (VARCHAR(10)): Tipo de sangre
- `allergies` (JSONB): Lista de alergias
- `chronic_conditions` (JSONB): Condiciones crónicas
- `emergency_contacts` (JSONB): Contactos médicos de emergencia
- `special_needs` (JSONB): Necesidades especiales
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Un perfil médico pertenece a una persona bajo cuidado (CARED_PERSONS)

### 1.5 DIAGNOSES (Diagnósticos)
**Descripción**: Diagnósticos médicos de cada persona bajo cuidado.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `diagnosis_type` (VARCHAR(50)): Tipo de diagnóstico (medical, psychological, etc.)
- `diagnosis_date` (DATE): Fecha del diagnóstico
- `diagnosis_code` (VARCHAR(20)): Código de diagnóstico (CIE-10)
- `diagnosis_name` (VARCHAR(200)): Nombre del diagnóstico
- `description` (TEXT): Descripción detallada
- `severity` (VARCHAR(20)): Severidad (mild, moderate, severe)
- `symptoms` (JSONB): Síntomas asociados
- `treatments` (JSONB): Tratamientos prescritos
- `notes` (TEXT): Notas adicionales
- `attached_files` (JSONB): Archivos adjuntos
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Un diagnóstico pertenece a una persona bajo cuidado (CARED_PERSONS)
- Un diagnóstico puede ser creado por un usuario (USERS)

### 1.6 MEDICATION_SCHEDULES (Programas de Medicación)
**Descripción**: Programas de medicación prescritos para cada persona.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `medication_name` (VARCHAR(100)): Nombre del medicamento
- `dosage` (VARCHAR(50)): Dosis prescrita
- `frequency` (VARCHAR(20)): Frecuencia (daily, twice_daily, etc.)
- `time_slots` (JSONB): Horarios de administración
- `start_date` (DATE): Fecha de inicio
- `end_date` (DATE): Fecha de fin
- `instructions` (TEXT): Instrucciones de administración
- `side_effects` (JSONB): Efectos secundarios
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Un programa de medicación pertenece a una persona bajo cuidado (CARED_PERSONS)
- Un programa de medicación puede tener múltiples registros (MEDICATION_LOGS)

### 1.7 MEDICATION_LOGS (Registros de Medicación)
**Descripción**: Registro de cada administración de medicación.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `medication_schedule_id` (UUID, FK): Programa de medicación
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `administered_at` (TIMESTAMP): Fecha y hora de administración
- `dosage_given` (VARCHAR(50)): Dosis administrada
- `status` (VARCHAR(20)): Estado (taken, missed, refused)
- `administered_by` (UUID, FK): Usuario que administró
- `notes` (TEXT): Notas adicionales
- `side_effects_observed` (JSONB): Efectos secundarios observados
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Un registro de medicación pertenece a un programa de medicación (MEDICATION_SCHEDULES)
- Un registro de medicación pertenece a una persona bajo cuidado (CARED_PERSONS)
- Un registro de medicación puede ser administrado por un usuario (USERS)

### 1.8 RESTRAINT_PROTOCOLS (Protocolos de Sujeción)
**Descripción**: Protocolos de sujeción para prevención de incidentes.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `protocol_type` (VARCHAR(50)): Tipo de protocolo (physical, chemical, environmental)
- `name` (VARCHAR(200)): Nombre del protocolo
- `description` (TEXT): Descripción detallada
- `indications` (JSONB): Indicaciones para uso
- `contraindications` (JSONB): Contraindicaciones
- `procedures` (JSONB): Procedimientos paso a paso
- `monitoring_requirements` (JSONB): Requisitos de monitoreo
- `emergency_procedures` (JSONB): Procedimientos de emergencia
- `authorized_by` (VARCHAR(100)): Autorizado por
- `authorization_date` (DATE): Fecha de autorización
- `review_date` (DATE): Fecha de revisión
- `attached_files` (JSONB): Archivos adjuntos
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Un protocolo de sujeción pertenece a una persona bajo cuidado (CARED_PERSONS)
- Un protocolo de sujeción puede ser creado por un usuario (USERS)

### 1.9 SHIFT_OBSERVATIONS (Observaciones de Turno)
**Descripción**: Observaciones clínicas detalladas por turno de cuidado.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `cared_person_id` (UUID, FK): Persona bajo cuidado
- `caregiver_id` (UUID, FK): Cuidador responsable
- `shift_type` (VARCHAR(20)): Tipo de turno (morning, afternoon, night)
- `shift_start` (TIMESTAMP): Inicio del turno
- `shift_end` (TIMESTAMP): Fin del turno
- `observation_date` (TIMESTAMP): Fecha de observación
- `physical_condition` (VARCHAR(20)): Condición física
- `mobility_level` (VARCHAR(20)): Nivel de movilidad
- `pain_level` (INTEGER): Nivel de dolor (0-10)
- `vital_signs` (JSONB): Signos vitales
- `skin_condition` (VARCHAR(50)): Condición de la piel
- `hygiene_status` (VARCHAR(50)): Estado de higiene
- `mental_state` (VARCHAR(50)): Estado mental
- `mood` (VARCHAR(50)): Estado de ánimo
- `behavior_notes` (TEXT): Notas de comportamiento
- `cognitive_function` (VARCHAR(50)): Función cognitiva
- `communication_ability` (VARCHAR(50)): Capacidad de comunicación
- `appetite` (VARCHAR(50)): Apetito
- `food_intake` (JSONB): Ingesta de alimentos
- `fluid_intake` (JSONB): Ingesta de líquidos
- `swallowing_difficulty` (BOOLEAN): Dificultad para tragar
- `special_diet_notes` (TEXT): Notas de dieta especial
- `bowel_movement` (VARCHAR(50)): Movimiento intestinal
- `urinary_output` (VARCHAR(50)): Producción urinaria
- `incontinence_episodes` (INTEGER): Episodios de incontinencia
- `catheter_status` (VARCHAR(50)): Estado de catéter
- `medications_taken` (JSONB): Medicamentos tomados
- `medications_missed` (JSONB): Medicamentos omitidos
- `side_effects_observed` (TEXT): Efectos secundarios observados
- `medication_notes` (TEXT): Notas de medicación
- `activities_participated` (JSONB): Actividades en las que participó
- `social_interaction` (VARCHAR(50)): Interacción social
- `exercise_performed` (BOOLEAN): Ejercicio realizado
- `exercise_details` (TEXT): Detalles del ejercicio
- `safety_concerns` (TEXT): Preocupaciones de seguridad
- `incidents_occurred` (BOOLEAN): Incidentes ocurridos
- `incident_details` (TEXT): Detalles de incidentes
- `fall_risk_assessment` (VARCHAR(20)): Evaluación de riesgo de caída
- `restraint_used` (BOOLEAN): Sujeción utilizada
- `restraint_details` (TEXT): Detalles de sujeción
- `family_contact` (BOOLEAN): Contacto con familia
- `family_notes` (TEXT): Notas de contacto familiar
- `doctor_contact` (BOOLEAN): Contacto con médico
- `doctor_notes` (TEXT): Notas de contacto médico
- `handover_notes` (TEXT): Notas de entrega de turno
- `attached_files` (JSONB): Archivos adjuntos
- `status` (VARCHAR(20)): Estado (draft, completed, verified)
- `is_verified` (BOOLEAN): Verificado
- `verified_by` (UUID, FK): Verificado por
- `verified_at` (TIMESTAMP): Fecha de verificación
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Una observación de turno pertenece a una persona bajo cuidado (CARED_PERSONS)
- Una observación de turno es realizada por un cuidador (USERS)
- Una observación de turno puede ser verificada por un usuario (USERS)

### 1.10 PACKAGES (Paquetes - NUEVA ENTIDAD CENTRAL)
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

### 1.11 USER_PACKAGES (Paquetes de Usuarios)
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

### 1.12 INSTITUTIONS (Instituciones)
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

### 1.13 INSTITUTION_PACKAGES (Paquetes de Instituciones)
**Descripción**: Relación entre instituciones y paquetes contratados.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `institution_id` (INTEGER, FK): Institución que contrata
- `package_id` (UUID, FK): Paquete contratado
- `start_date` (DATE): Fecha de inicio
- `end_date` (DATE): Fecha de fin (NULL para contratos continuos)
- `status_type_id` (INTEGER, FK): Estado normalizado
- `created_at` (TIMESTAMP): Fecha de contratación

**Relaciones**:
- Un paquete puede ser contratado por múltiples instituciones (INSTITUTION_PACKAGES)
- Una institución puede tener múltiples paquetes (INSTITUTION_PACKAGES)

### 1.14 REFERRALS (Referidos)
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

### 1.15 REFERRAL_COMMISSIONS (Comisiones de Referidos)
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

### 1.16 CAREGIVER_SCORES (Puntuaciones de Cuidadores)
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

### 1.17 CAREGIVER_REVIEWS (Reviews de Cuidadores)
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

### 1.18 INSTITUTION_SCORES (Puntuaciones de Instituciones)
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

### 1.19 INSTITUTION_REVIEWS (Reviews de Instituciones)
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

### 1.20 DEVICES (Dispositivos)
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

### 1.21 EVENTS (Eventos)
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

### 1.22 ALERTS (Alertas)
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

### 1.23 BILLING_RECORDS (Registros de Facturación)
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
- `status_type_id` (INTEGER, FK): Estado normalizado
- `payment_method` (VARCHAR(50)): Método de pago
- `transaction_id` (VARCHAR(100)): ID de transacción
- `user_id` (UUID, FK): Usuario asociado
- `institution_id` (INTEGER, FK): Institución asociada
- `service_subscription_id` (INTEGER, FK): Suscripción de servicio
- `user_package_id` (UUID, FK): Paquete de usuario

**Relaciones**:
- Una factura puede estar asociada a un paquete (USER_PACKAGES)
- Una factura puede estar asociada a un usuario (USERS) o institución (INSTITUTIONS)
- Una factura puede estar asociada a una suscripción de servicio (SERVICE_SUBSCRIPTIONS)

---

## 1.24 - 1.38 TABLAS DE CATÁLOGO NORMALIZADAS

### 1.24 STATUS_TYPES (Tipos de Estado)
**Descripción**: Catálogo normalizado para todos los estados del sistema.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del estado
- `description` (TEXT): Descripción del estado
- `category` (VARCHAR(50)): Categoría (alert_status, billing_status, device_status, etc.)
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por múltiples entidades para estados normalizados

### 1.25 CARE_TYPES (Tipos de Cuidado)
**Descripción**: Catálogo de tipos de cuidado disponibles.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de cuidado
- `description` (VARCHAR(255)): Descripción
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por CARED_PERSONS (care_type_id)

### 1.26 DEVICE_TYPES (Tipos de Dispositivo)
**Descripción**: Catálogo de tipos de dispositivos IoT.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de dispositivo
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría (sensor, tracker, camera, wearable, etc.)
- `icon_name` (VARCHAR(50)): Nombre del icono para UI
- `color_code` (VARCHAR(7)): Código de color hex para UI
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por DEVICES (device_type_id)

### 1.27 ALERT_TYPES (Tipos de Alerta)
**Descripción**: Catálogo de tipos de alertas del sistema.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de alerta
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría (health, security, system, etc.)
- `icon_name` (VARCHAR(50)): Nombre del icono para UI
- `color_code` (VARCHAR(7)): Código de color hex para UI
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por ALERTS (alert_type_id)

### 1.28 EVENT_TYPES (Tipos de Evento)
**Descripción**: Catálogo de tipos de eventos del sistema.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de evento
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría (sensor_event, system_event, user_action, etc.)
- `icon_name` (VARCHAR(50)): Nombre del icono para UI
- `color_code` (VARCHAR(7)): Código de color hex para UI
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por EVENTS (event_type_id)

### 1.29 REMINDER_TYPES (Tipos de Recordatorio)
**Descripción**: Catálogo de tipos de recordatorios.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de recordatorio
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría (medication, appointment, task, etc.)
- `icon_name` (VARCHAR(50)): Nombre del icono para UI
- `color_code` (VARCHAR(7)): Código de color hex para UI
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por REMINDERS (reminder_type_id)

### 1.30 SERVICE_TYPES (Tipos de Servicio)
**Descripción**: Catálogo de tipos de servicios ofrecidos.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de servicio
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría (healthcare, caregiving, emergency, etc.)
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por SERVICE_SUBSCRIPTIONS (service_type_id)
- Referenciado por CARED_PERSON_INSTITUTIONS (service_type_id)
- Referenciado por CAREGIVER_REVIEWS (service_type_id)
- Referenciado por INSTITUTION_REVIEWS (service_type_id)

### 1.31 CAREGIVER_ASSIGNMENT_TYPES (Tipos de Asignación de Cuidador)
**Descripción**: Catálogo de tipos de asignación de cuidadores.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de asignación
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por CAREGIVER_ASSIGNMENTS (caregiver_assignment_type_id)

### 1.32 SHIFT_OBSERVATION_TYPES (Tipos de Observación de Turno)
**Descripción**: Catálogo de tipos de observaciones de turno.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de observación
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por SHIFT_OBSERVATIONS (shift_observation_type_id)

### 1.33 REFERRAL_TYPES (Tipos de Referido)
**Descripción**: Catálogo de tipos de referidos.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de referido
- `description` (VARCHAR(255)): Descripción
- `category` (VARCHAR(50)): Categoría
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por REFERRALS (referral_type_id)

### 1.34 RELATIONSHIP_TYPES (Tipos de Relación)
**Descripción**: Catálogo de tipos de relación entre entidades.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de relación
- `description` (VARCHAR(255)): Descripción
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por CAREGIVER_INSTITUTIONS (relationship_type_id)

### 1.35 REPORT_TYPES (Tipos de Reporte)
**Descripción**: Catálogo de tipos de reportes.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del tipo de reporte
- `description` (VARCHAR(255)): Descripción
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por REPORTS (report_type_id)

### 1.36 ACTIVITY_TYPES (Tipos de Actividad)
**Descripción**: Catálogo de tipos de actividades.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `type_name` (VARCHAR(100), UNIQUE): Nombre del tipo de actividad
- `description` (TEXT): Descripción
- `requirements` (JSONB): Requisitos (equipamiento, habilidades, etc.)
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Referenciado por ACTIVITIES (activity_type_id)

### 1.37 DIFFICULTY_LEVELS (Niveles de Dificultad)
**Descripción**: Catálogo de niveles de dificultad para actividades.

**Atributos Clave**:
- `id` (INTEGER, PK): Identificador único
- `name` (VARCHAR(50), UNIQUE): Nombre del nivel de dificultad
- `description` (VARCHAR(255)): Descripción
- `color_code` (VARCHAR(7)): Código de color hex para UI
- `is_active` (BOOLEAN): Estado activo
- `created_at` (TIMESTAMP): Fecha de creación
- `updated_at` (TIMESTAMP): Fecha de actualización

**Relaciones**:
- Referenciado por ACTIVITIES (difficulty_level_id)

### 1.38 ENUMERATION_TYPES (Tipos de Enumeración)
**Descripción**: Sistema de enumeraciones dinámicas del sistema.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `type_name` (VARCHAR(100), UNIQUE): Nombre del tipo de enumeración
- `description` (TEXT): Descripción
- `is_system` (BOOLEAN): Si es enumeración del sistema
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Referenciado por ENUMERATION_VALUES (enumeration_type_id)

### 1.39 ENUMERATION_VALUES (Valores de Enumeración)
**Descripción**: Valores específicos para cada tipo de enumeración.

**Atributos Clave**:
- `id` (UUID, PK): Identificador único
- `enumeration_type_id` (UUID, FK): Tipo de enumeración
- `value_name` (VARCHAR(100)): Nombre del valor
- `description` (TEXT): Descripción
- `sort_order` (INTEGER): Orden de clasificación
- `is_default` (BOOLEAN): Si es valor por defecto
- `is_active` (BOOLEAN): Estado activo

**Relaciones**:
- Referenciado por ENUMERATION_TYPES (enumeration_type_id)

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

## 4. Normalización de Datos

### 4.1 Catálogos Normalizados
El sistema utiliza **15 tablas de catálogo normalizadas** para eliminar redundancias y mejorar la integridad de datos:

**Estados y Tipos:**
- `STATUS_TYPES`: Estados normalizados para todas las entidades
- `CARE_TYPES`: Tipos de cuidado (self_care, delegated)
- `DEVICE_TYPES`: Tipos de dispositivos IoT
- `ALERT_TYPES`: Tipos de alertas del sistema
- `EVENT_TYPES`: Tipos de eventos
- `REMINDER_TYPES`: Tipos de recordatorios
- `