# 🏥 Reglas de Negocio - Cuidadores Freelance

## 📋 Resumen Ejecutivo

Este documento define las **nuevas reglas de negocio** implementadas en CUIOT para manejar **cuidadores freelance** que pueden trabajar con múltiples instituciones o de forma independiente.

## 🎯 Objetivo

Permitir que los cuidadores profesionales puedan:
- Trabajar con **múltiples instituciones** simultáneamente
- Operar como **freelance independientes** sin institución fija
- Mantener **flexibilidad laboral** y autonomía
- Gestionar **horarios y responsabilidades** específicas por institución

## 🏗️ Arquitectura de Datos

### Modelo CaregiverInstitution

```sql
CREATE TABLE caregiver_institutions (
    id UUID PRIMARY KEY,
    caregiver_id UUID NOT NULL REFERENCES users(id),
    institution_id UUID REFERENCES institutions(id), -- NULL para freelance
    relationship_type VARCHAR(50) NOT NULL,
    role_in_institution VARCHAR(100),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    is_primary_institution BOOLEAN DEFAULT FALSE,
    working_hours JSONB,
    responsibilities JSONB,
    compensation_info JSONB,
    contract_details JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Tipos de Relación

| Tipo | Descripción | Características |
|------|-------------|-----------------|
| `employee` | Empleado | Contrato fijo, horarios regulares |
| `contractor` | Contratista | Contrato por proyecto o tiempo |
| `volunteer` | Voluntario | Sin compensación económica |
| `freelance` | Freelance | Trabajo independiente |
| `consultant` | Consultor | Asesoría especializada |
| `temporary` | Temporal | Contrato temporal |
| `part_time` | Tiempo Parcial | Horarios reducidos |

## 📊 Reglas de Negocio

### 1. **Relaciones Múltiples**
- ✅ Un cuidador puede trabajar con **múltiples instituciones** simultáneamente
- ✅ Un cuidador puede ser **freelance** sin institución fija
- ✅ Cada relación tiene **fechas de inicio y fin** independientes
- ✅ Se mantiene **historial completo** de todas las relaciones

### 2. **Institución Principal**
- ✅ Un cuidador puede tener **una institución principal**
- ✅ Los cuidadores freelance **no tienen institución principal**
- ✅ Solo **una relación** puede ser marcada como principal
- ✅ La institución principal se usa para **reportes y facturación**

### 3. **Roles y Responsabilidades**
- ✅ Cada relación puede tener **roles diferentes** por institución
- ✅ Las **responsabilidades** son específicas por institución
- ✅ Los **horarios** se manejan independientemente
- ✅ La **compensación** puede variar por institución

### 4. **Estados de Relación**
- ✅ `active`: Relación activa y operativa
- ✅ `inactive`: Relación inactiva temporalmente
- ✅ `suspended`: Relación suspendida por problemas
- ✅ `terminated`: Relación terminada definitivamente
- ✅ `pending`: Relación pendiente de activación

### 5. **Validaciones de Negocio**
- ✅ **Fechas coherentes**: La fecha de fin debe ser posterior a la de inicio
- ✅ **Tipos válidos**: Solo se permiten tipos de relación predefinidos
- ✅ **Estados válidos**: Solo se permiten estados predefinidos
- ✅ **Institución única**: Solo una relación puede ser principal

## 🔄 Flujos de Trabajo

### Registro de Cuidador Freelance

1. **Crear usuario** con tipo `caregiver` y `is_freelance = true`
2. **Asignar roles** apropiados (cuidador, enfermero, etc.)
3. **Crear relación** sin institución (`institution_id = NULL`)
4. **Configurar horarios** y responsabilidades
5. **Establecer compensación** y detalles de contrato

### Asignación a Institución

1. **Crear nueva relación** con la institución
2. **Definir tipo** de relación (contractor, consultant, etc.)
3. **Establecer rol** específico en la institución
4. **Configurar horarios** y responsabilidades
5. **Definir compensación** y términos del contrato

### Gestión de Múltiples Instituciones

1. **Mantener relaciones separadas** por institución
2. **Gestionar conflictos** de horarios
3. **Priorizar responsabilidades** según urgencia
4. **Coordinar comunicación** entre instituciones
5. **Mantener reportes** separados por institución

## 📈 Casos de Uso

### Caso 1: Cuidador Freelance Independiente
```
María es enfermera freelance que:
- Trabaja con 3 familias diferentes
- No tiene institución fija
- Gestiona sus propios horarios
- Establece sus propias tarifas
```

### Caso 2: Cuidador con Múltiples Instituciones
```
Juan es cuidador que:
- Es empleado del Hospital San José (institución principal)
- Trabaja como consultor en Clínica Santa María
- Hace voluntariado en Hogar de Ancianos
- Mantiene horarios diferentes en cada lugar
```

### Caso 3: Transición de Empleado a Freelance
```
Ana era empleada del Centro de Cuidado:
- Terminó su contrato como empleada
- Se registró como cuidador freelance
- Mantiene relación con la institución como contratista
- Agregó nuevos clientes independientes
```

## 🔧 Implementación Técnica

### Nuevos Endpoints

```python
# Gestión de relaciones cuidador-institución
POST /api/v1/caregiver-institutions/
GET /api/v1/caregiver-institutions/
GET /api/v1/caregiver-institutions/{id}
PUT /api/v1/caregiver-institutions/{id}
DELETE /api/v1/caregiver-institutions/{id}

# Consultas específicas
GET /api/v1/caregivers/{id}/institutions
GET /api/v1/institutions/{id}/caregivers
GET /api/v1/caregivers/freelance
GET /api/v1/caregiver-institutions/stats
```

### Servicios Implementados

```python
class CaregiverInstitutionService:
    def create_relationship(self, data: CaregiverInstitutionCreate)
    def get_caregiver_institutions(self, caregiver_id: UUID)
    def get_institution_caregivers(self, institution_id: UUID)
    def get_freelance_caregivers(self)
    def set_primary_institution(self, caregiver_id: UUID, institution_id: UUID)
    def update_relationship(self, id: UUID, data: CaregiverInstitutionUpdate)
    def terminate_relationship(self, id: UUID)
```

## 📊 Métricas y Reportes

### Estadísticas de Relaciones
- **Total de relaciones** activas
- **Distribución por tipo** de relación
- **Cuidadores freelance** vs institucionales
- **Rotación** de personal
- **Satisfacción** por institución

### Reportes de Negocio
- **Horas trabajadas** por institución
- **Compensación** por tipo de relación
- **Eficiencia** de cuidadores
- **Cobertura** de servicios
- **Análisis de costos** por institución

## 🔒 Consideraciones de Seguridad

### Control de Acceso
- ✅ Los cuidadores solo ven **sus propias relaciones**
- ✅ Las instituciones ven **sus cuidadores asignados**
- ✅ Los administradores ven **todas las relaciones**
- ✅ **Auditoría completa** de cambios

### Protección de Datos
- ✅ **Información sensible** encriptada
- ✅ **Acceso granular** por institución
- ✅ **Consentimiento** para compartir datos
- ✅ **Cumplimiento** con regulaciones locales

## 🚀 Beneficios del Sistema

### Para Cuidadores
- ✅ **Flexibilidad laboral** total
- ✅ **Gestión independiente** de horarios
- ✅ **Múltiples fuentes** de ingresos
- ✅ **Desarrollo profesional** continuo

### Para Instituciones
- ✅ **Acceso a talento** especializado
- ✅ **Flexibilidad** en contratación
- ✅ **Reducción de costos** fijos
- ✅ **Escalabilidad** de servicios

### Para el Sistema
- ✅ **Mayor cobertura** de servicios
- ✅ **Optimización** de recursos
- ✅ **Mejor calidad** de cuidado
- ✅ **Innovación** en modelos de negocio

## 📝 Próximos Pasos

1. **Implementar endpoints** de gestión
2. **Crear interfaces** de usuario
3. **Desarrollar reportes** y dashboards
4. **Configurar notificaciones** automáticas
5. **Implementar validaciones** avanzadas
6. **Crear documentación** de usuario

---

*Este documento se actualiza regularmente según las necesidades del negocio y la evolución del sistema.* 