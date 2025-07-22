# Matriz de Actores, Permisos y Responsabilidades - Versión 3.0

## 🎯 **RESUMEN EJECUTIVO**

Este documento define la matriz completa de permisos para el sistema CUIOT, incluyendo operaciones CRUD detalladas y acciones específicas por entidad. La estructura está diseñada para proporcionar control granular sobre las funcionalidades del sistema.

---

## 📋 **ÍNDICE**

1. **[Definición de Actores](#1-definición-de-actores)**
2. **[Estructura de Permisos](#2-estructura-de-permisos)**
3. **[Matriz de Permisos Detallada](#3-matriz-de-permisos-detallada)**
4. **[Roles del Sistema](#4-roles-del-sistema)**
5. **[Alcances de Permisos](#5-alcances-de-permisos)**
6. **[Implementación Técnica](#6-implementación-técnica)**
7. **[Reglas de Negocio](#7-reglas-de-negocio)**

---

## 1. DEFINICIÓN DE ACTORES

### **A. Administrador del Sistema (admin)**
**Descripción**: Gestor completo de la plataforma
**Alcance**: Global
**Responsabilidades**: Operación del sistema, configuración, soporte técnico
**Capacidad Legal**: Completa

### **B. Administrador de Institución (institution_admin)**
**Descripción**: Gestor de una institución específica
**Alcance**: Institución propia
**Responsabilidades**: Gestión de personal, protocolos, facturación
**Capacidad Legal**: Completa (dentro de su institución)

### **C. Personal de Institución (institution_staff)**
**Descripción**: Personal operativo de la institución
**Alcance**: Institución propia
**Responsabilidades**: Operaciones diarias, atención a usuarios
**Capacidad Legal**: Limitada

### **D. Personal Médico (medical_staff)**
**Descripción**: Personal médico de la institución
**Alcance**: Institución propia
**Responsabilidades**: Atención médica, protocolos clínicos
**Capacidad Legal**: Profesional

### **E. Cuidador Profesional (caregiver)**
**Descripción**: Profesional independiente que brinda cuidado
**Alcance**: Personas asignadas
**Responsabilidades**: Calidad del servicio, cumplimiento de horarios
**Capacidad Legal**: Completa
**Rol Adicional**: Embajador de la plataforma

### **F. Cuidador Freelance (freelance_caregiver)**
**Descripción**: Cuidador independiente con tarifa por hora
**Alcance**: Personas asignadas
**Responsabilidades**: Servicios profesionales, facturación
**Capacidad Legal**: Completa

### **G. Familiar/Representante (family_member)**
**Descripción**: Familiar o representante legal
**Alcance**: Personas bajo su representación
**Responsabilidades**: Toma de decisiones, pagos, consentimiento
**Capacidad Legal**: Completa

### **H. Persona en Autocuidado (cared_person_self)**
**Descripción**: Persona independiente que gestiona su propio cuidado
**Alcance**: Propio
**Responsabilidades**: Autogestión, contratación de servicios
**Capacidad Legal**: Completa

### **I. Persona con Cuidado Delegado (caredperson)**
**Descripción**: Persona dependiente que necesita representación
**Alcance**: Propio (limitado)
**Responsabilidades**: Seguir protocolos de cuidado
**Capacidad Legal**: Limitada

---

## 2. ESTRUCTURA DE PERMISOS

### **Operaciones CRUD**
- **CREATE**: Crear nuevos registros
- **READ**: Leer/ver información
- **UPDATE**: Modificar registros existentes
- **DELETE**: Eliminar registros

### **Alcances de Permisos**

#### **Definición de Alcances**
- **OWN**: Propio (solo del usuario)
- **ASSIGNED**: Asignado (personas bajo cuidado asignadas)
- **INSTITUTION**: Institución (usuarios de la misma institución)
- **FAMILY**: Familiar (personas bajo representación legal)
- **ALL**: Todos (acceso global)
- **NONE**: Sin acceso

#### **Mapeo de Roles a Alcances**

| Rol | Alcance Principal | Alcance Secundario | Restricciones |
|-----|-------------------|-------------------|---------------|
| **admin** | ALL | - | Ninguna |
| **institution_admin** | INSTITUTION | OWN | Solo su institución |
| **institution_staff** | INSTITUTION | OWN | Solo lectura institucional |
| **medical_staff** | INSTITUTION | OWN | Acceso médico especial |
| **caregiver** | ASSIGNED | OWN | Solo personas asignadas |
| **freelance_caregiver** | ASSIGNED | OWN | Solo personas asignadas |
| **family_member** | FAMILY | OWN | Solo representación legal |
| **cared_person_self** | OWN | - | Solo gestión propia |
| **caredperson** | OWN | - | Limitado, requiere representante |

### **Entidades del Sistema**
1. **Users**: Usuarios del sistema
2. **Cared Persons**: Personas bajo cuidado
3. **Institutions**: Instituciones médicas
4. **Devices**: Dispositivos IoT
5. **Alerts**: Alertas del sistema
6. **Events**: Eventos registrados
7. **Reports**: Reportes y analíticas
8. **Packages**: Paquetes de servicios
9. **Roles**: Roles y permisos
10. **System**: Configuración del sistema

---

## 3. MATRIZ DE PERMISOS DETALLADA

### **Interpretación de la Matriz**

**Símbolos utilizados:**
- ✅ **Permitido**: El rol tiene acceso completo a esta funcionalidad
- ❌ **Denegado**: El rol no tiene acceso a esta funcionalidad
- ⚠️ **Limitado**: El rol tiene acceso limitado (solo lectura, solo propio, etc.)

**Ejemplos de interpretación:**
- `read_own_profile: ✅` = Puede leer su propio perfil
- `read_institution_users: ✅` = Puede leer usuarios de su institución
- `read_all_users: ❌` = No puede leer todos los usuarios del sistema
- `update_assigned_persons: ✅` = Puede actualizar personas asignadas a su cuidado

**Alcances implícitos en los permisos:**
- `read_own_*` = Alcance OWN
- `read_assigned_*` = Alcance ASSIGNED  
- `read_institution_*` = Alcance INSTITUTION
- `read_all_*` = Alcance ALL
- `read_family_*` = Alcance FAMILY

### **3.1 USUARIOS (Users)**

**Alcances por Rol:**
- **admin**: ALL (acceso global)
- **institution_admin**: OWN + INSTITUTION
- **institution_staff**: OWN + INSTITUTION (solo lectura)
- **medical_staff**: OWN + INSTITUTION (solo lectura)
- **caregiver**: OWN + ASSIGNED
- **freelance_caregiver**: OWN + ASSIGNED
- **family_member**: OWN + FAMILY
- **cared_person_self**: OWN
- **caredperson**: OWN (limitado)

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_admin | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_institution_admin | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_caregiver | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_family_member | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| create_cared_person | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **READ** |
| read_own_profile | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| read_institution_users | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_assigned_users | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| read_all_users | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_user_activity | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_own_profile | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| update_institution_users | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_assigned_users | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| update_all_users | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_user_roles | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_account | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| delete_institution_users | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_users | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| reset_user_password | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| lock_unlock_user | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| verify_user_identity | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### **3.2 PERSONAS BAJO CUIDADO (Cared Persons)**

**Alcances por Rol:**
- **admin**: ALL (acceso global)
- **institution_admin**: OWN + INSTITUTION
- **institution_staff**: OWN + INSTITUTION (solo lectura)
- **medical_staff**: OWN + INSTITUTION (acceso médico)
- **caregiver**: OWN + ASSIGNED
- **freelance_caregiver**: OWN + ASSIGNED
- **family_member**: OWN + FAMILY
- **cared_person_self**: OWN
- **caredperson**: OWN (limitado)

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_self_care | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| create_delegated_care | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| create_medical_profile | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **READ** |
| read_own_profile | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| read_assigned_persons | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| read_institution_persons | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_persons | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_care_history | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **UPDATE** |
| update_own_profile | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| update_assigned_persons | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| update_institution_persons | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_persons | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_profile | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| delete_assigned_persons | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_institution_persons | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_persons | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| assign_caregivers | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| manage_medications | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| create_emergency_protocols | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

### **3.3 INSTITUCIONES (Institutions)**

**Alcances por Rol:**
- **admin**: ALL (acceso global)
- **institution_admin**: OWN (solo su institución)
- **institution_staff**: OWN (solo su institución, lectura)
- **medical_staff**: OWN (solo su institución, lectura)
- **caregiver**: NONE (no acceso a instituciones)
- **freelance_caregiver**: NONE (no acceso a instituciones)
- **family_member**: NONE (no acceso a instituciones)
- **cared_person_self**: NONE (no acceso a instituciones)
- **caredperson**: NONE (no acceso a instituciones)

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_institution | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_branch | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_own_institution | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_institutions | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_institution_stats | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_own_institution | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_institutions | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_institution | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_institutions | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| manage_staff | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| manage_billing | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| view_analytics | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### **3.4 DISPOSITIVOS IoT (Devices)**

**Alcances por Rol:**
- **admin**: ALL (acceso global)
- **institution_admin**: OWN + INSTITUTION
- **institution_staff**: OWN + INSTITUTION (solo lectura)
- **medical_staff**: OWN + INSTITUTION (solo lectura)
- **caregiver**: OWN + ASSIGNED
- **freelance_caregiver**: OWN + ASSIGNED
- **family_member**: OWN + FAMILY
- **cared_person_self**: OWN
- **caredperson**: OWN (limitado)

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| register_device | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| create_device_group | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_own_devices | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| read_assigned_devices | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| read_institution_devices | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_devices | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_telemetry_data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **UPDATE** |
| update_own_devices | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| update_assigned_devices | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| update_institution_devices | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_devices | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_devices | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| delete_assigned_devices | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_institution_devices | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_devices | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| troubleshoot_device | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| configure_alerts | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| remote_control | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |

### **3.5 ALERTAS (Alerts)**

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_manual_alert | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| create_alert_template | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_own_alerts | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| read_assigned_alerts | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| read_institution_alerts | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_alerts | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_own_alerts | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| update_assigned_alerts | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| update_institution_alerts | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_alerts | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_alerts | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| delete_assigned_alerts | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| delete_institution_alerts | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_alerts | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| acknowledge_alert | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| escalate_alert | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| configure_alert_rules | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### **3.6 EVENTOS (Events)**

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_event | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| create_event_category | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_own_events | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| read_assigned_events | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| read_institution_events | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_events | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_own_events | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| update_assigned_events | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| update_institution_events | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_events | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_events | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| delete_assigned_events | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| delete_institution_events | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_events | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| categorize_event | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| add_event_notes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| export_event_data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### **3.7 REPORTES (Reports)**

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_custom_report | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_report_template | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_own_reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| read_assigned_reports | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| read_institution_reports | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_reports | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_own_reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| update_assigned_reports | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| update_institution_reports | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_reports | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| delete_assigned_reports | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| delete_institution_reports | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_reports | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| schedule_reports | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| export_reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| share_reports | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### **3.8 PAQUETES (Packages)**

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_package | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_addon | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_own_packages | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| read_institution_packages | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_all_packages | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_own_packages | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| update_institution_packages | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_all_packages | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_own_packages | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| delete_institution_packages | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_all_packages | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| subscribe_package | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| manage_billing | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| upgrade_downgrade | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |

### **3.9 ROLES (Roles)**

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_role | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_role_template | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_roles | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_role_permissions | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_roles | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_role_permissions | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| assign_roles | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_roles | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| clone_role | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| archive_role | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### **3.10 SISTEMA (System)**

| Permiso | admin | institution_admin | institution_staff | medical_staff | caregiver | freelance_caregiver | family_member | cared_person_self | caredperson |
|---------|-------|-------------------|-------------------|---------------|-----------|-------------------|---------------|-------------------|-------------|
| **CREATE** |
| create_backup | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| create_maintenance_window | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **READ** |
| read_system_config | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_system_logs | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_performance_metrics | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| read_audit_logs | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **UPDATE** |
| update_system_config | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| update_security_settings | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DELETE** |
| delete_system_data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| delete_logs | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **ACCIONES ESPECÍFICAS** |
| perform_maintenance | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| monitor_system | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| troubleshoot_system | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 4. ROLES DEL SISTEMA

### **Definición de Roles Activos**

```typescript
const SYSTEM_ROLES = {
    admin: {
        name: "Administrador del Sistema",
        description: "Control total del sistema",
        scope: "global",
        can_create_roles: ["institution_admin", "caregiver", "family_member", "cared_person_self", "caredperson"],
        restrictions: "Ninguna"
    },
    
    institution_admin: {
        name: "Administrador de Institución",
        description: "Gestión de institución específica",
        scope: "institution",
        can_create_roles: ["caregiver", "family_member", "cared_person_self", "caredperson"],
        restrictions: "Solo dentro de su institución"
    },
    
    institution_staff: {
        name: "Personal de Institución",
        description: "Personal operativo",
        scope: "institution",
        can_create_roles: [],
        restrictions: "Solo lectura y operaciones básicas"
    },
    
    medical_staff: {
        name: "Personal Médico",
        description: "Personal médico de la institución",
        scope: "institution",
        can_create_roles: [],
        restrictions: "Acceso médico y protocolos clínicos"
    },
    
    caregiver: {
        name: "Cuidador Profesional",
        description: "Profesional independiente",
        scope: "assigned",
        can_create_roles: ["family_member", "cared_person_self", "caredperson"],
        restrictions: "Solo como parte de referidos"
    },
    
    freelance_caregiver: {
        name: "Cuidador Freelance",
        description: "Cuidador con tarifa por hora",
        scope: "assigned",
        can_create_roles: ["family_member", "cared_person_self", "caredperson"],
        restrictions: "Solo como parte de referidos"
    },
    
    family_member: {
        name: "Familiar/Representante",
        description: "Representante legal",
        scope: "family",
        can_create_roles: ["caredperson"],
        restrictions: "Solo personas bajo su representación"
    },
    
    cared_person_self: {
        name: "Persona en Autocuidado",
        description: "Autogestión del cuidado",
        scope: "own",
        can_create_roles: [],
        restrictions: "Solo gestión propia"
    },
    
    caredperson: {
        name: "Persona con Cuidado Delegado",
        description: "Cuidado delegado",
        scope: "own",
        can_create_roles: [],
        restrictions: "Requiere representante legal"
    }
}
```

---

## 5. ALCANCES DE PERMISOS

### **Definición de Alcances**

```typescript
const PERMISSION_SCOPES = {
    own: {
        description: "Propio - Solo del usuario",
        applies_to: ["profile", "data", "devices", "reports"],
        examples: ["read_own_profile", "update_own_devices"]
    },
    
    assigned: {
        description: "Asignado - Personas bajo cuidado asignadas",
        applies_to: ["cared_persons", "devices", "alerts", "events"],
        examples: ["read_assigned_persons", "update_assigned_devices"]
    },
    
    family: {
        description: "Familiar - Personas bajo representación",
        applies_to: ["cared_persons", "devices", "alerts", "events"],
        examples: ["read_family_persons", "update_family_devices"]
    },
    
    institution: {
        description: "Institución - Usuarios de la misma institución",
        applies_to: ["users", "cared_persons", "devices", "reports"],
        examples: ["read_institution_users", "update_institution_persons"]
    },
    
    all: {
        description: "Todos - Acceso global",
        applies_to: ["all_entities"],
        examples: ["read_all_users", "update_all_system"]
    }
}
```

---

## 6. IMPLEMENTACIÓN TÉCNICA

### **Estructura de Permisos en Base de Datos**

```sql
-- Tabla de roles
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB NOT NULL DEFAULT '{}',
    is_system BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ejemplo de permisos JSONB
{
    "users": {
        "create": ["admin"],
        "read_own": ["all"],
        "read_institution": ["institution_admin", "institution_staff", "medical_staff"],
        "read_all": ["admin"],
        "update_own": ["all"],
        "update_institution": ["institution_admin"],
        "update_all": ["admin"],
        "delete_own": ["all"],
        "delete_institution": ["institution_admin"],
        "delete_all": ["admin"]
    },
    "cared_persons": {
        "create": ["admin", "institution_admin", "caregiver", "family_member"],
        "read_own": ["all"],
        "read_assigned": ["caregiver", "freelance_caregiver"],
        "read_institution": ["institution_admin", "institution_staff", "medical_staff"],
        "read_all": ["admin"],
        "update_own": ["cared_person_self", "family_member"],
        "update_assigned": ["caregiver", "freelance_caregiver"],
        "update_institution": ["institution_admin", "medical_staff"],
        "update_all": ["admin"],
        "delete_own": ["cared_person_self", "family_member"],
        "delete_assigned": [],
        "delete_institution": ["institution_admin"],
        "delete_all": ["admin"]
    }
}
```

### **Validación de Permisos**

```python
class PermissionService:
    @staticmethod
    def has_permission(user: User, permission: str, scope: str = None) -> bool:
        """
        Verificar si un usuario tiene un permiso específico
        
        Args:
            user: Usuario a verificar
            permission: Permiso requerido (ej: "users.read_own")
            scope: Alcance específico (opcional)
            
        Returns:
            bool: True si tiene el permiso, False en caso contrario
        """
        for user_role in user.user_roles:
            if not user_role.is_active:
                continue
                
            role_permissions = user_role.role.permissions
            if isinstance(role_permissions, str):
                role_permissions = json.loads(role_permissions)
                
            # Verificar permiso específico
            if PermissionService._check_permission(role_permissions, permission, scope):
                return True
                
        return False
    
    @staticmethod
    def _check_permission(role_permissions: dict, permission: str, scope: str = None) -> bool:
        """Verificar permiso en el contexto del rol"""
        entity, action = permission.split('.', 1)
        
        if entity not in role_permissions:
            return False
            
        entity_permissions = role_permissions[entity]
        
        # Verificar acción específica
        if action in entity_permissions:
            allowed_roles = entity_permissions[action]
            return "all" in allowed_roles or user.role.name in allowed_roles
            
        return False
```

---

## 7. REGLAS DE NEGOCIO

### **Principios Fundamentales**

1. **Principio de Menor Privilegio**: Los usuarios solo tienen los permisos mínimos necesarios
2. **Separación de Responsabilidades**: Cada rol tiene responsabilidades específicas
3. **Auditoría Completa**: Todas las acciones son registradas y auditables
4. **Escalabilidad**: La estructura permite agregar nuevos roles y permisos fácilmente

### **Reglas Específicas**

#### **Autocuidado vs Cuidado Delegado**
- **Autocuidado**: Puede gestionar completamente su perfil y contratar servicios
- **Cuidado Delegado**: Requiere representante legal para acciones importantes

#### **Jerarquía de Roles**
- **admin** > **institution_admin** > **institution_staff** > **medical_staff**
- **caregiver** = **freelance_caregiver** (mismos permisos, diferente modelo de negocio)
- **family_member** > **caredperson** (representación legal)

#### **Permisos por Institución**
- Los permisos institucionales solo aplican a usuarios de la misma institución
- Los administradores de institución no pueden gestionar otras instituciones
- El personal médico tiene permisos especiales para información médica

#### **Gestión de Dispositivos**
- Los dispositivos pueden ser propios, asignados o institucionales
- Solo los propietarios pueden eliminar dispositivos
- Los cuidadores pueden configurar dispositivos asignados

#### **Alertas y Eventos**
- Todos los roles pueden crear alertas y eventos
- Los alcances determinan qué alertas/eventos pueden ver/editar
- Las alertas críticas se escalan automáticamente

### **Casos de Uso Específicos**

#### **Creación de Usuarios**
1. **admin**: Puede crear cualquier tipo de usuario
2. **institution_admin**: Puede crear cuidadores, familiares y personas bajo cuidado
3. **caregiver**: Puede crear familiares y personas bajo cuidado como referidos
4. **family_member**: Puede crear personas bajo cuidado delegado

#### **Gestión de Dispositivos**
1. **admin**: Control total sobre todos los dispositivos
2. **institution_admin**: Gestión de dispositivos institucionales
3. **caregiver**: Configuración de dispositivos asignados
4. **family_member**: Gestión de dispositivos familiares

#### **Reportes y Analíticas**
1. **admin**: Acceso completo a todos los reportes
2. **institution_admin**: Reportes institucionales
3. **caregiver**: Reportes de personas asignadas
4. **family_member**: Reportes familiares

---

## 📊 **RESUMEN DE CAMBIOS - VERSIÓN 3.0**

### **Mejoras Implementadas**

1. **CRUD Completo**: Create, Read, Update, Delete para cada entidad
2. **Acciones Específicas**: Funcionalidades especiales por entidad
3. **Alcances Claros**: Own, Assigned, Institution, All
4. **Matriz Detallada**: 10 entidades × 9 roles = 90 combinaciones
5. **Implementación Técnica**: Código SQL y Python incluido
6. **Reglas de Negocio**: Principios y casos de uso específicos

### **Beneficios**

- **Control Granular**: Permisos específicos por acción
- **Escalabilidad**: Fácil agregar nuevos roles y permisos
- **Seguridad**: Principio de menor privilegio
- **Auditoría**: Trazabilidad completa de acciones
- **Flexibilidad**: Adaptable a diferentes tipos de instituciones

---

*Documento actualizado: Enero 2025*
*Versión: 3.0*
*Autor: Equipo CUIOT* 