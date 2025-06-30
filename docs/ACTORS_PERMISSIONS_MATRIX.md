# Matriz de Actores, Permisos y Responsabilidades - Versión 2.0

## 1. Definición de Actores

### A. Persona Bajo Cuidado (CaredPerson)
**Descripción**: Persona que recibe servicios de cuidado
**Tipos**:
- **Autocuidado**: Independiente, toma decisiones propias
- **Cuidado Delegado**: Dependiente, necesita representación
**Capacidad Legal**: Variable según tipo
**Representación**: Propia (autocuidado) o Familiar (delegado)

### B. Familiar/Representante Legal (User: family)
**Descripción**: Persona responsable legal y financieramente (solo para cuidado delegado)
**Capacidad Legal**: Completa
**Responsabilidad**: Toma de decisiones, pagos, consentimiento

### C. Cuidador Freelancer (User: caregiver)
**Descripción**: Profesional independiente que brinda cuidado
**Capacidad Legal**: Completa
**Responsabilidad**: Calidad del servicio, cumplimiento de horarios
**Rol Adicional**: Embajador de la plataforma

### D. Institución (Institution)
**Descripción**: Centro médico, geriátrico, clínica, etc.
**Capacidad Legal**: Completa (persona jurídica)
**Responsabilidad**: Servicios médicos, compliance legal
**Rol Adicional**: Partner de la plataforma

### E. Administrador del Sistema (User: admin)
**Descripción**: Gestor de la plataforma
**Capacidad Legal**: Completa
**Responsabilidad**: Operación del sistema, soporte

## 2. Matriz de Permisos Actualizada

| Acción | CaredPerson (Autocuidado) | CaredPerson (Delegado) | Family | Caregiver | Institution | Admin |
|--------|---------------------------|------------------------|--------|-----------|-------------|-------|
| **COMPRAS** |
| Contratar servicios IoT | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Contratar cuidador | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Contratar institución | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Comprar dispositivos IoT | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Suscripción premium | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **REPORTES** |
| Reportar cuidador | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Reportar institución | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Reportar incidente | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reporte médico | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **VISIBILIDAD** |
| Ver perfil propio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver perfil familiar | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Ver cuidadores asignados | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Ver instituciones | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Ver costos totales | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Ver reviews | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **GESTIÓN** |
| Editar perfil propio | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Editar perfil familiar | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Asignar cuidadores | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Coordinar servicios | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **RECOMENDACIONES** |
| Recomendar plataforma | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Recibir comisiones | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **ADMINISTRACIÓN** |
| Gestionar usuarios | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver reportes del sistema | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Configurar sistema | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

## 3. Modelo de Negocio Basado en Recomendaciones

### A. Cuidadores como Embajadores

#### Incentivos para Cuidadores
- **Comisión por referido**: 15% del primer mes de suscripción
- **Comisión recurrente**: 5% de suscripciones continuas
- **Herramientas gratuitas**: App profesional, gestión de horarios
- **Perfil destacado**: Mejor posicionamiento en búsquedas
- **Capacitación gratuita**: Cursos y certificaciones
- **Soporte prioritario**: Atención preferencial

#### Flujo de Recomendación
```
1. Cuidador brinda servicio de calidad
2. Cuidador recomienda plataforma a familia
3. Familia se registra con código del cuidador
4. Sistema asigna comisión automáticamente
5. Cuidador recibe pago mensual
```

### B. Instituciones como Partners

#### Paquetes Institucionales
- **Básico** (ARS 5,000/mes):
  - Monitoreo básico para 10 pacientes
  - Reportes semanales
  - Soporte por email

- **Profesional** (ARS 15,000/mes):
  - Monitoreo completo para 50 pacientes
  - Gestión de cuidadores externos
  - Analytics y reportes avanzados
  - Soporte telefónico

- **Enterprise** (ARS 50,000/mes):
  - Monitoreo ilimitado
  - API completa
  - Integración con sistemas existentes
  - Account manager dedicado
  - Revenue sharing por referidos

#### Flujo de Partnership
```
1. Institución implementa paquete
2. Institución recomienda a familias
3. Familias contratan servicios
4. Institución recibe revenue sharing
5. Plataforma gana nuevos usuarios
```

## 4. Experiencia de Usuario como Driver

### A. Para Cuidadores (Embajadores)

#### Onboarding Simple
- **Registro en 5 minutos**: Solo datos esenciales
- **Verificación rápida**: Proceso automatizado
- **Perfil atractivo**: Templates profesionales
- **Primera asignación**: En 24 horas

#### Herramientas Útiles
- **Calendario inteligente**: Gestión de horarios
- **Pagos automáticos**: Sin intermediarios
- **Comunicación integrada**: Chat con familias
- **Dashboard de ganancias**: Tiempo real

#### Incentivos Visibles
- **Comisiones claras**: Cuánto gana por referido
- **Progreso visible**: Hacia metas de ganancia
- **Reconocimiento**: Badges y certificaciones
- **Crecimiento profesional**: Cursos y networking

### B. Para Familias

#### Búsqueda Intuitiva
- **Filtros inteligentes**: Ubicación, especialización, precio
- **Comparación fácil**: Side-by-side de cuidadores
- **Reviews verificadas**: Solo de usuarios reales
- **Precios transparentes**: Sin sorpresas

#### Coordinación Centralizada
- **Un solo lugar**: Todos los servicios integrados
- **Calendario unificado**: Cuidadores e instituciones
- **Pagos consolidados**: Una factura mensual
- **Comunicación centralizada**: Chat grupal

#### Paz Mental
- **Monitoreo 24/7**: Alertas en tiempo real
- **Backup automático**: Si un cuidador no puede
- **Reportes detallados**: Actividad y salud
- **Soporte inmediato**: Emergencias y consultas

### C. Para Instituciones

#### Implementación Rápida
- **Setup en 48 horas**: Sin interrumpir operaciones
- **Migración de datos**: Automática desde sistemas existentes
- **Capacitación incluida**: Para todo el personal
- **Soporte dedicado**: Durante la transición

#### ROI Visible
- **Reportes de eficiencia**: Ahorros de tiempo y costos
- **Analytics avanzados**: Tendencias y predicciones
- **Comparación con benchmarks**: Industria y región
- **ROI calculado**: Retorno de inversión mensual

## 5. Flujos de Información Optimizados

### Flujo de Compra (Autocuidado)
```
CaredPerson → Busca servicios → Compara opciones → Compra → Usa plataforma
```

### Flujo de Compra (Cuidado Delegado)
```
Family → Busca cuidadores → Evalúa opciones → Contrata → Coordina servicios
```

### Flujo de Recomendación
```
Cuidador/Institución → Recomienda → Familia se registra → Comisión automática
```

### Flujo de Reportes
```
Cualquier actor → Reporta → Sistema analiza → Notifica apropiados → Acción
```

## 6. Consideraciones Éticas Actualizadas

### Privacidad por Tipo de Usuario
- **Autocuidado**: Control total de sus datos
- **Cuidado Delegado**: Compartido con representante legal
- **Cuidadores**: Solo información profesional relevante
- **Instituciones**: Información médica necesaria

### Transparencia en Recomendaciones
- **Disclosure obligatorio**: Cuidadores deben revelar comisiones
- **Reviews independientes**: No influenciadas por incentivos
- **Calidad verificada**: Recomendaciones basadas en resultados
- **Sin spam**: Límites en frecuencia de recomendaciones

### Consentimiento Informado
- **Autocuidado**: Consentimiento directo
- **Cuidado Delegado**: Consentimiento del representante legal
- **Menores**: Consentimiento de padres/tutores
- **Incapacitados**: Consentimiento de representante legal

## 7. Implementación Técnica

### Roles en el Sistema
```python
ROLES = {
    "admin": "Administrador del sistema",
    "family": "Familiar/Representante legal",
    "caregiver": "Cuidador freelancer",
    "institution": "Institución médica",
    "cared_person_self": "Persona en autocuidado",
    "cared_person_delegated": "Persona con cuidado delegado"
}
```

### Sistema de Referidos
```python
REFERRAL_SYSTEM = {
    "caregiver_commission": 0.15,  # 15% del primer mes
    "institution_commission": 0.10,  # 10% del primer mes
    "recurring_commission": 0.05,  # 5% mensual
    "min_referrals_for_bonus": 5,  # Bonificación por volumen
    "referral_expiry_days": 30  # Expiración de referidos
}
```

### Permisos por Endpoint
```python
PERMISSIONS = {
    "/services/contract": ["cared_person_self", "family"],
    "/caregivers/contract": ["cared_person_self", "family"],
    "/institutions/contract": ["cared_person_self", "family"],
    "/referrals/create": ["caregiver", "institution", "family"],
    "/referrals/commission": ["caregiver", "institution"],
    "/reports/create": ["cared_person_self", "cared_person_delegated", "family", "caregiver", "institution", "admin"],
    "/admin/*": ["admin"]
}
```

## 8. Métricas de Éxito

### Técnicas
- **Tiempo de onboarding**: < 5 minutos para cuidadores
- **Tasa de conversión**: > 20% de referidos a contrataciones
- **Satisfacción**: > 4.7/5 en calificaciones promedio
- **Retención**: > 85% de clientes recurrentes

### Negocio
- **Crecimiento orgánico**: 30% mensual por referidos
- **CAC (Costo de Adquisición)**: $0 por referidos orgánicos
- **LTV (Lifetime Value)**: 24 meses promedio
- **Revenue por referido**: ARS 15,000 promedio

### Sociales
- **Empleo generado**: 500+ cuidadores activos en 12 meses
- **Instituciones integradas**: 50+ partners en 12 meses
- **Familias beneficiadas**: 1000+ hogares con mejor cuidado
- **Calidad del servicio**: Mejora del 40% en satisfacción

---

*Documento en desarrollo - Versión 2.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 