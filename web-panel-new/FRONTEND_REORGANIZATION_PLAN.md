# Plan de Reorganización del Frontend - Dashboard Admin

## Análisis del Estado Actual

### ✅ Lo que está funcionando bien:
- **Arquitectura modular**: Componentes bien separados y reutilizables
- **Sistema de validaciones**: Validaciones robustas para usuarios
- **Casos de uso**: Lógica de negocio separada de la UI
- **Diseño consistente**: Sistema de diseño coherente
- **Componentización**: Formularios divididos en secciones

### ❌ Lo que necesita actualización:
- **APIs incompletas**: Solo 6 APIs de ~50+ entidades del backend
- **Navegación desactualizada**: No refleja módulos del backend
- **KPIs limitados**: Solo 4 métricas básicas
- **Falta de gestión CRUD**: No hay interfaces para la mayoría de entidades
- **Dashboard básico**: Funcionalidad limitada

## Plan de Reorganización por Módulos

### 1. **Módulo Core** (Catálogos y Tipos)
**Entidades a implementar:**
- Status Types (tipos de estado normalizados)
- Device Types (tipos de dispositivos)
- Alert Types (tipos de alertas)
- Event Types (tipos de eventos)
- Reminder Types (tipos de recordatorios)
- Emergency Protocol Types (tipos de protocolos)
- Service Types (tipos de servicios)
- Referral Types (tipos de referencias)

**APIs a crear:**
```typescript
// src/lib/api/core/
- statusTypes.ts
- deviceTypes.ts
- alertTypes.ts
- eventTypes.ts
- reminderTypes.ts
- emergencyProtocolTypes.ts
- serviceTypes.ts
- referralTypes.ts
```

**Componentes a crear:**
```svelte
// src/components/dashboard/admin/core/
- StatusTypesManager.svelte
- DeviceTypesManager.svelte
- AlertTypesManager.svelte
- EventTypesManager.svelte
- ReminderTypesManager.svelte
- EmergencyProtocolTypesManager.svelte
- ServiceTypesManager.svelte
- ReferralTypesManager.svelte
```

### 2. **Módulo Care** (Cuidados y Asignaciones)
**Entidades a implementar:**
- Cared Persons (personas cuidadas)
- Caregiver Assignments (asignaciones de cuidadores)
- Medical Profiles (perfiles médicos)
- Diagnoses (diagnósticos)
- Medications (medicamentos)
- Allergies (alergias)
- Medical Conditions (condiciones médicas)
- Shift Observations (observaciones de turno)
- Vital Signs (signos vitales)
- Restraint Protocols (protocolos de sujeción)

**APIs a crear:**
```typescript
// src/lib/api/care/
- caredPersons.ts
- caregiverAssignments.ts
- medicalProfiles.ts
- diagnoses.ts
- medications.ts
- allergies.ts
- medicalConditions.ts
- shiftObservations.ts
- vitalSigns.ts
- restraintProtocols.ts
```

**Componentes a crear:**
```svelte
// src/components/dashboard/admin/care/
- CaredPersonsManager.svelte
- CaregiverAssignmentsManager.svelte
- MedicalProfilesManager.svelte
- DiagnosesManager.svelte
- MedicationsManager.svelte
- AllergiesManager.svelte
- MedicalConditionsManager.svelte
- ShiftObservationsManager.svelte
- VitalSignsManager.svelte
- RestraintProtocolsManager.svelte
```

### 3. **Módulo IoT** (Dispositivos y Eventos)
**Entidades a implementar:**
- Devices (dispositivos)
- Device Configurations (configuraciones)
- Events (eventos)
- Alerts (alertas)
- Location Tracking (seguimiento de ubicación)
- Geofences (geocercas)
- Debug Events (eventos de depuración)

**APIs a crear:**
```typescript
// src/lib/api/iot/
- devices.ts
- deviceConfigs.ts
- events.ts
- alerts.ts
- locationTracking.ts
- geofences.ts
- debugEvents.ts
```

**Componentes a crear:**
```svelte
// src/components/dashboard/admin/iot/
- DevicesManager.svelte
- DeviceConfigsManager.svelte
- EventsManager.svelte
- AlertsManager.svelte
- LocationTrackingManager.svelte
- GeofencesManager.svelte
- DebugEventsManager.svelte
```

### 4. **Módulo Business** (Negocio y Facturación)
**Entidades a implementar:**
- Institutions (instituciones)
- Packages (paquetes)
- Users (usuarios) - ya existe
- Add-ons (complementos)
- Billing Records (registros de facturación)
- Service Subscriptions (suscripciones)
- Referrals (referencias)
- Referral Commissions (comisiones)

**APIs a crear:**
```typescript
// src/lib/api/business/
- institutions.ts (ya existe, actualizar)
- packages.ts (ya existe, actualizar)
- users.ts (ya existe, actualizar)
- addOns.ts
- billingRecords.ts
- serviceSubscriptions.ts
- referrals.ts
- referralCommissions.ts
```

**Componentes a crear:**
```svelte
// src/components/dashboard/admin/business/
- InstitutionsManager.svelte
- PackagesManager.svelte
- UsersManager.svelte (ya existe, actualizar)
- AddOnsManager.svelte
- BillingRecordsManager.svelte
- ServiceSubscriptionsManager.svelte
- ReferralsManager.svelte
- ReferralCommissionsManager.svelte
```

### 5. **Módulo Scoring & Reviews** (Calificaciones)
**Entidades a implementar:**
- Caregiver Scores (puntuaciones de cuidadores)
- Caregiver Reviews (reseñas de cuidadores)
- Institution Scores (puntuaciones de instituciones)
- Institution Reviews (reseñas de instituciones)

**APIs a crear:**
```typescript
// src/lib/api/scoring/
- caregiverScores.ts
- caregiverReviews.ts
- institutionScores.ts
- institutionReviews.ts
```

**Componentes a crear:**
```svelte
// src/components/dashboard/admin/scoring/
- CaregiverScoresManager.svelte
- CaregiverReviewsManager.svelte
- InstitutionScoresManager.svelte
- InstitutionReviewsManager.svelte
```

### 6. **Módulo Monitoring** (Monitoreo y Reportes)
**Entidades a implementar:**
- Reports (reportes)
- Report Types (tipos de reportes)

**APIs a crear:**
```typescript
// src/lib/api/monitoring/
- reports.ts
- reportTypes.ts
```

**Componentes a crear:**
```svelte
// src/components/dashboard/admin/monitoring/
- ReportsManager.svelte
- ReportTypesManager.svelte
```

## Reorganización de la Navegación

### Nueva Estructura del Sidebar:
```javascript
const nav = [
    // Dashboard Principal
    { href: "/dashboard/overview", label: "Dashboard", icon: "dashboard" },
    
    // Módulo Admin
    { href: "/dashboard/admin", label: "Admin", icon: "admin" },
    
    // Módulo Core
    { href: "/dashboard/core", label: "Catálogos", icon: "catalog" },
    
    // Módulo Care
    { href: "/dashboard/care", label: "Cuidados", icon: "care" },
    
    // Módulo IoT
    { href: "/dashboard/iot", label: "IoT", icon: "iot" },
    { href: "/dashboard/alerts", label: "Alertas", icon: "alerts" },
    { href: "/dashboard/events", label: "Eventos", icon: "events" },
    
    // Módulo Business
    { href: "/dashboard/business", label: "Negocio", icon: "business" },
    { href: "/dashboard/users", label: "Usuarios", icon: "users" },
    { href: "/dashboard/institutions", label: "Instituciones", icon: "institutions" },
    { href: "/dashboard/packages", label: "Paquetes", icon: "packages" },
    
    // Módulo Scoring
    { href: "/dashboard/scoring", label: "Calificaciones", icon: "scoring" },
    
    // Módulo Monitoring
    { href: "/dashboard/reports", label: "Reportes", icon: "reports" },
    
    // Otros
    { href: "/dashboard/calendar", label: "Calendario", icon: "calendar" },
    { href: "/dashboard/profile", label: "Perfil", icon: "profile" },
    { href: "/dashboard/settings", label: "Configuración", icon: "settings" },
];
```

## Actualización del Dashboard Admin

### Nuevos KPIs a implementar:
```javascript
const kpis = [
    // Métricas Core
    { title: "Tipos de Estado", value: statusTypesCount, icon: "status" },
    { title: "Tipos de Dispositivos", value: deviceTypesCount, icon: "device" },
    { title: "Tipos de Alertas", value: alertTypesCount, icon: "alert" },
    
    // Métricas Care
    { title: "Personas Cuidadas", value: caredPersonsCount, icon: "care" },
    { title: "Asignaciones Activas", value: assignmentsCount, icon: "assignment" },
    { title: "Observaciones Hoy", value: observationsToday, icon: "observation" },
    
    // Métricas IoT
    { title: "Dispositivos Activos", value: activeDevicesCount, icon: "device" },
    { title: "Eventos Hoy", value: eventsToday, icon: "event" },
    { title: "Alertas Críticas", value: criticalAlertsCount, icon: "alert" },
    
    // Métricas Business
    { title: "Instituciones", value: institutionsCount, icon: "institution" },
    { title: "Paquetes Activos", value: activePackagesCount, icon: "package" },
    { title: "Usuarios Activos", value: activeUsersCount, icon: "user" },
    { title: "Facturación Mensual", value: monthlyBilling, icon: "billing" },
    
    // Métricas Scoring
    { title: "Calificaciones Promedio", value: avgScore, icon: "score" },
    { title: "Reseñas Pendientes", value: pendingReviews, icon: "review" },
    
    // Métricas Monitoring
    { title: "Reportes Generados", value: reportsGenerated, icon: "report" },
];
```

## Plan de Implementación por Fases

### Fase 1: APIs y Tipos (Semana 1)
1. Crear todas las APIs faltantes
2. Definir interfaces TypeScript para todas las entidades
3. Actualizar el archivo index.ts de APIs

### Fase 2: Componentes Core (Semana 2)
1. Implementar componentes del módulo Core
2. Crear rutas para catálogos
3. Actualizar navegación

### Fase 3: Componentes Care (Semana 3)
1. Implementar componentes del módulo Care
2. Crear rutas para cuidados
3. Integrar con APIs

### Fase 4: Componentes IoT (Semana 4)
1. Implementar componentes del módulo IoT
2. Actualizar dashboard con métricas IoT
3. Mejorar visualización de eventos

### Fase 5: Componentes Business (Semana 5)
1. Implementar componentes del módulo Business
2. Actualizar KPIs con métricas de negocio
3. Integrar facturación

### Fase 6: Componentes Scoring & Monitoring (Semana 6)
1. Implementar componentes de calificaciones
2. Implementar componentes de monitoreo
3. Finalizar dashboard completo

## Beneficios de la Reorganización

### 1. **Alineación con Backend**
- Todas las entidades del backend tendrán su representación en el frontend
- APIs consistentes y tipadas
- Validaciones alineadas con el modelo de datos

### 2. **Escalabilidad**
- Arquitectura modular permite agregar nuevas entidades fácilmente
- Componentes reutilizables
- Separación clara de responsabilidades

### 3. **Mantenibilidad**
- Código organizado por módulos de negocio
- APIs centralizadas y tipadas
- Componentes con responsabilidades específicas

### 4. **UX Mejorada**
- Dashboard más completo con métricas relevantes
- Navegación intuitiva por módulos
- Interfaces CRUD completas para todas las entidades

### 5. **Profesionalismo**
- Sistema completo y robusto
- Interfaces consistentes
- Funcionalidad empresarial completa

## Próximos Pasos

1. **Crear estructura de carpetas** para nuevos módulos
2. **Implementar APIs faltantes** siguiendo el patrón existente
3. **Crear componentes base** para cada módulo
4. **Actualizar navegación** con nueva estructura
5. **Implementar KPIs completos** en el dashboard
6. **Crear rutas** para cada módulo
7. **Integrar y probar** toda la funcionalidad

Este plan asegura que el frontend esté completamente alineado con el backend refactorizado y proporcione una experiencia de usuario profesional y completa. 