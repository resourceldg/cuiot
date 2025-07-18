# Scripts de Población de Datos - CUIOT

## 📁 Sistema Modular de Población

Sistema profesional, idempotente y alineado a las reglas de negocio para poblar todos los datos clave del sistema CUIOT de forma eficiente y reproducible.

### Estructura Modular

```
scripts/
├── modules/
│   ├── core/                    # Datos fundamentales del sistema
│   │   ├── catalog_types.py     # Tipos de catálogos (status, relationship, care)
│   │   └── device_types.py      # Tipos de dispositivos IoT
│   ├── care/                    # Datos de cuidado y salud
│   │   ├── cared_persons.py     # Personas cuidadas
│   │   ├── caregivers.py        # Cuidadores (usuarios con rol específico)
│   │   ├── medical_data.py      # Datos médicos (diagnósticos, signos vitales, etc.)
│   │   └── care_assignments.py  # Asignaciones de cuidado
│   ├── iot/                     # Dispositivos y datos IoT
│   │   ├── devices.py           # Creación de dispositivos
│   │   ├── events.py            # Eventos de dispositivos
│   │   ├── alerts.py            # Alertas del sistema
│   │   └── tracking.py          # Seguimiento de ubicación
│   └── business/                # Datos de negocio
│       ├── institutions.py      # Instituciones
│       ├── packages.py          # Paquetes de servicios
│       ├── users.py             # Usuarios del sistema
│       ├── addons.py            # Add-ons y suscripciones
│       └── billing.py           # Facturación y pagos
│   └── monitoring/              # Datos de monitoreo
│       ├── reports.py           # Reportes normalizados
│       └── report_types.py      # Tipos de reporte
├── utils/
│   └── data_generators.py       # Generadores de datos realistas
├── run_modular_population.py    # Script principal con menú interactivo
└── README.md                    # Este archivo
```

## 🚀 Uso del Sistema

### Script Principal con Menú Interactivo

```bash
# Ejecutar desde el contenedor Docker
docker compose exec backend python3 scripts/run_modular_population.py
```

**Opciones disponibles:**
1. **Población Core** - Catálogos y tipos de dispositivos
2. **Población IoT** - Dispositivos, eventos, alertas, tracking
3. **Población Care** - Personas cuidadas, cuidadores, datos médicos
4. **Población Completa** - Todos los módulos en orden
5. **Solo corregir dispositivos sin package_id**
6. **Solo poblar dispositivos**
7. **Solo poblar eventos y alertas**
8. **Población Business: Instituciones**
9. **Población Business: Paquetes**
10. **Población Business: Usuarios**
11. **Población Business: Add-ons y Suscripciones (Completo)**
12. **Solo Add-ons de Paquetes**
13. **Solo Suscripciones de Usuario**
14. **Solo Add-ons de Usuario**
15. **Población Business: Facturación**
0. **Salir**

### Ejecución de Módulos Específicos

```bash
# Poblar solo el módulo core
docker compose exec backend python3 scripts/run_modular_population.py --module core

# Poblar solo el submódulo de personas cuidadas
docker compose exec backend python3 scripts/run_modular_population.py --module care --submodule cared_persons

# Poblar solo datos médicos
docker compose exec backend python3 scripts/run_modular_population.py --module care --submodule medical_data

# Poblar solo instituciones
 docker compose exec backend python3 -m scripts.modules.business.institutions

# Poblar solo paquetes
 docker compose exec backend python3 -m scripts.modules.business.packages

# Poblar solo usuarios
 docker compose exec backend python3 -m scripts.modules.business.users

# Poblar tipos de reporte
 docker compose exec backend python3 -m scripts.modules.monitoring.report_types

# Poblar reportes normalizados
 docker compose exec backend python3 -m scripts.modules.monitoring.reports

# Poblar add-ons y suscripciones
 docker compose exec backend python3 -m scripts.modules.business.addons

# Poblar facturación
 docker compose exec backend python3 -m scripts.modules.business.billing
```

## 🔧 Módulos Implementados

### Core - Datos Fundamentales

#### `modules/core/catalog_types.py`
**Funcionalidad:** Poblar catálogos base del sistema
- **Status Types**: Estados de entidades (activo, inactivo, pendiente, etc.)
- **Relationship Types**: Tipos de relación (familiar, legal, etc.)
- **Care Types**: Tipos de cuidado (básico, especializado, etc.)

#### `modules/core/device_types.py`
**Funcionalidad:** Tipos de dispositivos IoT especializados
- **27 tipos** organizados por categorías
- **Categorías**: Médicos, ambientales, seguridad, asistencia, monitoreo, comunicación, control

### Care - Datos de Cuidado y Salud

#### `modules/care/cared_persons.py`
**Funcionalidad:** Personas cuidadas del sistema
- **Datos personales**: Nombre, edad, género, contacto
- **Información médica**: Diagnósticos, condiciones especiales
- **Relaciones**: Familiares, tutores legales
- **Configuración**: Preferencias de cuidado

#### `modules/care/caregivers.py`
**Funcionalidad:** Cuidadores (usuarios con rol específico)
- **Creación de usuarios** con rol de cuidador
- **Asignación de roles** via UserRole
- **Relaciones institucionales** via CaregiverInstitution
- **Datos profesionales**: Experiencia, especialidades

#### `modules/care/medical_data.py`
**Funcionalidad:** Datos médicos completos
- **Diagnósticos**: Condiciones médicas con severidad y notas
- **Shift Observations**: Observaciones de turno
- **Vital Signs**: Signos vitales asociados a observaciones
- **Medication Schedules**: Programas de medicación
- **Medication Logs**: Registros de administración

#### `modules/care/care_assignments.py`
**Funcionalidad:** Asignaciones de cuidado
- **Asignación cuidadores-personas cuidadas**
- **Horarios y turnos**
- **Responsabilidades específicas**
- **Validación de datos requeridos**

### IoT - Dispositivos y Monitoreo

#### `modules/iot/devices.py`
**Funcionalidad:** Dispositivos IoT
- **Creación con package_id obligatorio**
- **Asignación de propietarios** según tipo de paquete
- **Configuración realista** de ubicaciones y parámetros

#### `modules/iot/events.py`
**Funcionalidad:** Eventos de dispositivos
- **Eventos de temperatura, movimiento, etc.**
- **Datos JSON estructurados**
- **Timestamps realistas**

#### `modules/iot/alerts.py`
**Funcionalidad:** Alertas del sistema
- **Alertas de emergencia, mantenimiento, etc.**
- **Niveles de urgencia**
- **Asociación a dispositivos y personas**

#### `modules/iot/tracking.py`
**Funcionalidad:** Seguimiento de ubicación
- **Coordenadas GPS**
- **Precisión y fuente**
- **Historial de ubicaciones**

#### `modules/iot/geofences.py`
**Funcionalidad:** Geofences (zonas seguras, áreas restringidas, zonas médicas, etc.)
- **Geofence**: Zonas geográficas asociadas a usuarios, personas cuidadas o instituciones
- **Tipos**: safe_zone, restricted_area, home_zone, work_zone, medical_zone, danger_zone, custom_zone, monitoring_zone
- **Ubicación**: Coordenadas, radio o polígono, horarios, días de la semana
- **Alertas**: Mensajes personalizados por tipo y acción (enter, exit, both)
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar geofences
 docker compose exec backend python3 -m scripts.modules.iot.geofences

# O desde el menú interactivo:
 docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 24 (Población IoT: Geofences)

# O solo geofences:
 docker compose exec backend python3 scripts/run_modular_population.py --geofences
```

#### `modules/care/reminders.py`
**Funcionalidad:** Recordatorios del sistema de cuidado
- **Reminder**: Recordatorios asociados a personas cuidadas y usuarios
- **Tipos**: medication, appointment, exercise, meal, hygiene, social, checkup, meditation
- **Programación**: Horarios, fechas de vencimiento, patrones de repetición
- **Prioridad**: Niveles de importancia (1-10), recordatorios marcados como importantes
- **Estado**: Pendiente, completado, con timestamps de completado
- **Datos estructurados**: JSON con detalles específicos por tipo de recordatorio
- **Notas**: Instrucciones y recomendaciones personalizadas
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar recordatorios
 docker compose exec backend python3 -m scripts.modules.care.reminders

# O desde el menú interactivo:
 docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 26 (Población Care: Recordatorios)

# O solo recordatorios:
 docker compose exec backend python3 scripts/run_modular_population.py --reminders
```

#### `modules/care/emergency_protocols.py`
**Funcionalidad:** Protocolos de emergencia globales e institucionales
- **EmergencyProtocol**: Protocolos asociados a crisis y tipos (caídas, incendios, fugas, etc.)
- **Tipos y crisis**: Definidos en el modelo, combinados para cobertura realista
- **Pasos y contactos**: Listas de pasos y contactos de emergencia en JSON
- **Condiciones de activación**: Texto descriptivo
- **Severidad**: low, medium, high
- **Estado**: Asociado a status_type (activo)
- **Institución**: Protocolos globales (sin institución) y por institución
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar protocolos de emergencia
docker compose exec backend python3 -m scripts.modules.care.emergency_protocols

# O desde el menú interactivo:
docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 28 (Población Care: Protocolos de Emergencia)

# O solo protocolos de emergencia:
docker compose exec backend python3 scripts/run_modular_population.py --emergency-protocols
```

### Business - Datos de Negocio

#### `modules/business/institutions.py`
**Funcionalidad:** Instituciones del sistema
- **Creadas con datos realistas** (nombre, tipo, dirección, contacto, capacidad)
- **Idempotente** (no duplica instituciones)
- **Tipos**: nursing_home, clinic, day_care, etc.

#### `modules/business/packages.py`
**Funcionalidad:** Paquetes de servicios
- **6 paquetes** de los 3 tipos principales (individual, profesional, institucional)
- **Precios en centavos (ARS)**
- **Estructura JSON** para features, limitaciones, add-ons
- **Idempotente**

#### `modules/business/users.py`
**Funcionalidad:** Usuarios administrativos, familiares e institucionales
- **Admins, familiares, institucionales** con datos realistas
- **Passwords hasheados**
- **Asignación de roles** automática
- **Idempotente**

#### `modules/business/addons.py`
**Funcionalidad:** Add-ons y suscripciones de usuario a paquetes
- **PackageAddOn**: Add-ons disponibles para paquetes (almacenamiento, soporte, analytics, etc.)
- **UserPackage**: Suscripciones de usuarios a paquetes con configuración personalizada
- **UserPackageAddOn**: Add-ons asignados a suscripciones específicas
- **Datos realistas**: Precios, configuraciones, límites
- **Idempotente**

#### `modules/business/billing.py`
**Funcionalidad:** Registros de facturación y pagos
- **BillingRecord**: Facturas de suscripciones, servicios, configuración, consultoría, mantenimiento
- **Estados de pago**: pagado, pendiente, vencido
- **Métodos de pago**: tarjeta de crédito, débito, transferencia bancaria
- **Cálculo de impuestos**: IVA 21% incluido
- **Números de factura únicos**: Prefijos por tipo (SUB, SVC, SET, CON, MNT)
- **Idempotente**

#### `modules/business/scoring.py`
**Funcionalidad:** Sistema de puntuaciones y reseñas (scoring & reviews)
- **CaregiverScore**: Puntuaciones agregadas de cuidadores (calidad, experiencia, confiabilidad, disponibilidad, etc.)
- **CaregiverReview**: Reseñas individuales de cuidadores (ratings, comentarios, categorías, recomendaciones)
- **InstitutionScore**: Puntuaciones agregadas de instituciones (servicio, infraestructura, cumplimiento, reputación, etc.)
- **InstitutionReview**: Reseñas individuales de instituciones (ratings, comentarios, categorías, recomendaciones)
- **Datos realistas**: Ratings, comentarios, métricas de calidad, fechas, estadísticas
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar todo el sistema de scoring y reviews
 docker compose exec backend python3 -m scripts.modules.business.scoring

# O desde el menú interactivo:
 docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 16 (Scoring y Reviews)
```

#### `modules/care/referrals.py`
**Funcionalidad:** Sistema de referencias y derivaciones médicas
- **Referral**: Referencias generales de usuarios hacia personas externas (por email, teléfono)
- **MedicalReferral**: Derivaciones clínicas de personas cuidadas a especialistas/hospitales
- **ReferralCommission**: Comisiones asociadas a referencias exitosas
- **Datos realistas**: Códigos únicos, motivos médicos, especialidades, urgencias, fechas
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar todo el sistema de referencias y derivaciones
 docker compose exec backend python3 -m scripts.modules.care.referrals

# O desde el menú interactivo:
 docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 21 (Referencias y Derivaciones Médicas)
```

### Monitoring - Reportes y Analíticas

#### `modules/monitoring/report_types.py`
**Funcionalidad:** Poblar tipos de reporte (catálogo normalizado)
- **Tipos**: activity, health, alerts, compliance, custom
- **Idempotente**

#### `modules/monitoring/reports.py`
**Funcionalidad:** Poblar reportes normalizados y masivos
- **15 reportes** con relaciones a usuarios y personas cuidadas
- **Referencias normalizadas**: report_type_id, cared_person_id, created_by_id
- **Datos realistas y variados**
- **Idempotente**

#### `modules/iot/debug_events.py`
**Funcionalidad:** Eventos de debug para testing, desarrollo y monitoreo
- **DebugEvent**: Eventos de debug asociados a usuarios, personas cuidadas y dispositivos
- **Tipos**: test_event, debug_event, simulation, system_test, integration_test, performance_test, load_test
- **Severidad**: debug, info, warning, error, critical
- **Entornos**: development, testing, staging, production
- **Datos estructurados**: JSON con métricas, parámetros, stack traces
- **Fuentes**: test_suite, manual_test, system_test, device_monitor, etc.
- **Timestamps**: event_time, processed_at con distribución realista
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar eventos de debug
docker compose exec backend python3 -m scripts.modules.iot.debug_events

# O desde el menú interactivo:
docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 30 (Población IoT: Eventos de Debug)

# O solo eventos de debug:
docker compose exec backend python3 scripts/run_modular_population.py --debug-events
```

#### `modules/iot/device_configs.py`
**Funcionalidad:** Configuraciones personalizadas de dispositivos IoT
- **DeviceConfig**: Configuraciones asociadas a dispositivos específicos
- **Tipos**: sensor_config, alert_config, notification_config, sampling_config, threshold_config, calibration_config, network_config, security_config, power_config
- **Datos estructurados**: JSON con configuraciones específicas por tipo
- **Versiones**: Control de versiones con timestamps de aplicación
- **Estado**: Activo/inactivo, configuración por defecto
- **Aplicación**: Asociado a usuarios que aplican configuraciones
- **Idempotente**

**Ejecución manual:**
```bash
# Poblar configuraciones de dispositivos
docker compose exec backend python3 -m scripts.modules.iot.device_configs

# O desde el menú interactivo:
docker compose exec backend python3 scripts/run_modular_population.py
# Opción: 32 (Población IoT: Configuraciones de Dispositivos)

# O solo configuraciones de dispositivos:
docker compose exec backend python3 scripts/run_modular_population.py --device-configs
```

## 🔄 Flujo de Población Recomendado

### Orden de Ejecución

1. **Core** (catálogos y tipos base)
   ```bash
   docker compose exec backend python3 scripts/run_modular_population.py --module core
   ```

2. **Business** (instituciones, paquetes, usuarios, add-ons, facturación)
   ```bash
   docker compose exec backend python3 scripts/run_modular_population.py --module business
   ```

3. **Care** (personas cuidadas, cuidadores, datos médicos)
   ```bash
   docker compose exec backend python3 scripts/run_modular_population.py --module care
   ```

4. **IoT** (dispositivos, eventos, alertas, tracking)
   ```bash
   docker compose exec backend python3 scripts/run_modular_population.py --module iot
   ```

5. **Monitoring** (tipos de reporte, reportes)
   ```bash
   docker compose exec backend python3 scripts/run_modular_population.py --module monitoring
   ```

6. **Población Completa** (todos los módulos en orden)
   ```bash
   docker compose exec backend python3 scripts/run_modular_population.py
   # Seleccionar opción 4
   ```

### Validación de Datos

El sistema incluye validaciones automáticas:
- ✅ **Verificación de datos requeridos** antes de crear entidades
- ✅ **Prevención de duplicados** usando get_or_create
- ✅ **Mensajes informativos** sobre datos faltantes
- ✅ **Sugerencias de ejecución** en orden correcto

## 📊 Estadísticas de Población

### Core
- **Status Types**: 4 tipos base
- **Relationship Types**: 6 tipos de relación
- **Care Types**: 3 tipos de cuidado
- **Device Types**: 27 tipos especializados

### Care
- **Cared Persons**: 15 personas cuidadas
- **Caregivers**: 10 cuidadores con roles
- **Diagnósticos**: 5 tipos comunes
- **Medical Records**: Registros médicos completos

### IoT
- **Devices**: 1-3 por tipo de dispositivo
- **Events**: 8 por dispositivo
- **Alerts**: 4 por dispositivo
- **Tracking**: 8 registros por persona

### Business
- **Instituciones**: 3 creadas
- **Paquetes**: 6 creados
- **Usuarios**: 5 creados (admins, familiares, institucionales)
- **Add-ons**: 8 tipos disponibles
- **Suscripciones**: Configuradas según usuarios y paquetes
- **Facturación**: 30+ registros de facturación realistas

### Monitoring
- **Tipos de reporte**: 5 creados
- **Reportes**: 15 creados, normalizados y asociados a entidades

## 🔒 Reglas de Negocio Implementadas

### Integridad de Datos
1. **Package ID Obligatorio**: Todos los dispositivos deben tener package_id
2. **Roles de Usuario**: Cuidadores son usuarios con rol específico
3. **Relaciones Institucionales**: Cuidadores vinculados a instituciones
4. **Campos Requeridos**: Validación de timestamps y campos obligatorios

### Idempotencia
- ✅ **get_or_create** en todas las entidades
- ✅ **Verificación de existencia** antes de crear
- ✅ **Manejo de duplicados** automático

### Robustez
- ✅ **Mensajes informativos** si faltan datos previos
- ✅ **Sugerencias de ejecución** en orden correcto
- ✅ **No falla abruptamente** si faltan dependencias

## 🛠️ Mantenimiento y Verificación

### Verificación de Integridad

```bash
# Verificar dispositivos sin package_id
docker compose exec backend python3 -c "
from app.core.database import get_db
from app.models.device import Device
db = next(get_db())
count = db.query(Device).filter(Device.package_id == None).count()
print(f'Dispositivos sin package_id: {count}')
db.close()
"

# Verificar cuidadores con roles
docker compose exec backend python3 -c "
from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
db = next(get_db())
caregivers = db.query(User).join(UserRole).filter(UserRole.role_id == 3).count()
print(f'Cuidadores con rol: {caregivers}')
db.close()
"
```

### Limpieza de Datos

```bash
# Eliminar dispositivos sin package_id (si es necesario)
docker compose exec backend python3 -c "
from app.core.database import get_db
from app.models.device import Device
db = next(get_db())
db.query(Device).filter(Device.package_id == None).delete()
db.commit()
print('Dispositivos sin package_id eliminados')
db.close()
"
```

## 📝 Estado Actual del Proyecto

### ✅ Completado
- **Sistema modular** completamente funcional
- **Módulos Core, Business, Care, IoT y Monitoring** implementados y probados
- **Add-ons y suscripciones** completamente funcionales
- **Sistema de facturación** con registros realistas
- **Validaciones y reglas de negocio** implementadas
- **Idempotencia** garantizada en todos los módulos
- **Mensajes informativos** y robustez del sistema
- **Automatización completa** con script bash
- **Sistema de recordatorios** con datos realistas e idempotencia
- **Sistema de protocolos de emergencia** con datos realistas e idempotencia
- **Sistema de eventos de debug** para testing y desarrollo

### 🔄 En Desarrollo
- **Módulo Monitoring**: Reportes y análisis
- **Validaciones adicionales** según necesidades específicas

### 📋 Próximos Pasos
1. **Implementar módulo Monitoring** si es requerido
2. **Agregar más validaciones** según reglas de negocio específicas
3. **Implementar logs detallados** para auditoría
4. **Crear scripts de rollback** para casos de error

## 🚨 Notas Importantes

### Entorno Docker
- Todos los scripts deben ejecutarse dentro del contenedor backend
- Las dependencias (SQLAlchemy, psycopg2) están instaladas en el contenedor
- Usar `docker compose exec backend` para ejecutar comandos

### Base de Datos
- El sistema asume que las migraciones están aplicadas
- Las tablas deben existir antes de ejecutar los scripts
- Verificar la conectividad a la base de datos antes de ejecutar

### Desarrollo Colaborativo
- Los scripts son idempotentes y seguros para ejecutar múltiples veces
- Cada módulo puede ejecutarse independientemente
- El sistema informa claramente si faltan dependencias

## 🚀 Futuras Extensiones

- **Analytics y métricas:** Submódulos para poblar métricas agregadas, dashboards y logs de eventos para pruebas de analítica avanzada.
- **Rollback y limpieza:** Scripts para revertir la población o limpiar datos de prueba, útil para testing automatizado y CI/CD.
- **Logs y auditoría:** Mejorar la trazabilidad de operaciones y agregar logs detallados para auditoría y debugging.
- **Tests automáticos de integridad:** Scripts que validen la integridad y consistencia de los datos después de la población.
- **Carga de datos personalizados:** Permitir la carga de datos desde archivos externos (CSV, JSON) para escenarios de pruebas específicas.
- **Integración con pipelines CI/CD:** Automatizar la población y validación de datos en entornos de integración continua.

## 🛠️ Fixes y Mantenimiento Integrados

El sistema modular incluye fixes profesionales para corregir y migrar datos críticos. Puedes ejecutarlos desde el menú interactivo o mediante flags CLI.

### Opciones de Fix en el Menú

- **34. Fix: Corregir permisos y rol admin**
  - Asegura que el rol admin tenga permisos completos y el usuario admin esté activo y sin expiración.
- **35. Fix: Corregir roles y género de usuarios**
  - Asigna género por defecto y rol 'family_member' a usuarios que no lo tengan.
- **36. Fix: Corregir campos de paquetes (list->dict)**
  - Convierte campos de lista a dict en los paquetes para mantener la integridad de datos.
- **37. Fix: Migrar campos de paquetes (list->dict)**
  - Migra los campos de lista a dict en la tabla packages (features, limitations, customizable_options, add_ons_available).

### Flags CLI para Fixes

Puedes ejecutar cualquier fix directamente:

```bash
# Corregir permisos y rol admin
docker compose exec backend python3 scripts/run_modular_population.py --fix-admin-role

# Corregir roles y género de usuarios
docker compose exec backend python3 scripts/run_modular_population.py --fix-users-roles

# Corregir campos de paquetes (list->dict)
docker compose exec backend python3 scripts/run_modular_population.py --fix-package-fields

# Migrar campos de paquetes (list->dict)
docker compose exec backend python3 scripts/run_modular_population.py --migrate-package-fields
```

### ¿Cuándo usar cada fix?
- **Fix admin**: Si el usuario admin pierde permisos o el rol admin está desactivado.
- **Fix usuarios/roles**: Si hay usuarios sin género o sin rol asignado.
- **Fix paquetes**: Si los campos de paquetes están en formato lista y deben ser dict.
- **Migrar paquetes**: Para migraciones masivas de estructura de datos en paquetes.

Todos los fixes son idempotentes y seguros para ejecutar múltiples veces.

---

## 🧑‍💻 Enfoque profesional: eficiencia + eficacia

Como equipo de arquitectura y desarrollo, buscamos siempre el equilibrio entre:
- **Eficiencia:** hacer las cosas bien, de forma óptima y con recursos adecuados.
- **Eficacia:** hacer lo correcto, alineado a la lógica de negocio y los objetivos del sistema.

El profesionalismo es lograr ambas: soluciones correctas, alineadas al negocio, y construidas de manera óptima y sostenible.

---

## 🎯 Mapeo de roles permitidos para paquetes (lógica de negocio)

Para poblar suscripciones a paquetes, se debe respetar la siguiente lógica:

- **Paquetes individuales:**
  - Roles permitidos: `cared_person_self`, `caredperson`, `family`, `family_member`
- **Paquetes institucionales:**
  - Roles permitidos: `institution_admin`
- **Paquetes profesionales:**
  - (Actualmente no hay roles profesionales independientes definidos. Si se agregan, documentar aquí)

> **Nota:** Si en el futuro se agregan roles como `doctor`, `staff`, etc., actualizar este mapeo y la lógica de los scripts.

Este mapeo debe ser consistente entre backend, scripts y frontend.

---

**Sistema de Población Modular CUIOT** - Listo para desarrollo, testing y producción. 