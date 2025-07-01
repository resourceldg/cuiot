# CUIOT - Reglas de Negocio

> **NOTA**: Este documento ha sido actualizado. Para las reglas de negocio más completas y actualizadas, consulta **[CUIOT_BUSINESS_RULES_CENTRAL.md](./CUIOT_BUSINESS_RULES_CENTRAL.md)**

## 🏥 **CUIOT: Reglas de Negocio Fundamentales**

**CUIOT** = **CUI**dar + **IOT** - Plataforma de monitoreo y gestión del cuidado usando IoT.

---

## 📋 **Documentos Relacionados**

- **[CUIOT_BUSINESS_RULES_CENTRAL.md](./CUIOT_BUSINESS_RULES_CENTRAL.md)** - Reglas de negocio completas y actualizadas
- **[ACTORS_PERMISSIONS_MATRIX.md](./ACTORS_PERMISSIONS_MATRIX.md)** - Matriz de actores y permisos
- **[CAREGIVER_FREELANCE_RULES.md](./CAREGIVER_FREELANCE_RULES.md)** - Sistema de scoring para cuidadores
- **[BUSINESS_MODEL.md](./BUSINESS_MODEL.md)** - Modelo de negocio detallado

---

## 🎯 **Reglas Principales**

### **1. Tipos de Cuidado**
- **Autocuidado**: Persona independiente que gestiona su propio cuidado
- **Cuidado Delegado**: Persona dependiente que necesita representación

### **2. Sistema de Referidos**
- **Cuidadores**: 15% primer mes + 5% recurrente
- **Instituciones**: 10% primer mes + 3% recurrente
- **Familias**: 5% primer mes + 2% recurrente

### **3. Permisos por Rol**
- **Autocuidado**: Control total de compras y datos
- **Cuidado Delegado**: Solo a través de representante
- **Cuidadores**: Herramientas profesionales + comisiones
- **Instituciones**: Paquetes empresariales + revenue sharing

### **4. Scoring y Calidad**
- **Cuidadores**: Experiencia (30%), Calidad (25%), Confiabilidad (20%)
- **Instituciones**: Calidad médica (35%), Infraestructura (25%), Personal (20%)

### **5. Relaciones Múltiples**
- Una persona puede tener múltiples cuidadores
- Una persona puede estar en múltiples instituciones
- Coordinación centralizada a través de la plataforma

---

## 🚀 **Estrategia de Crecimiento**

### **Cuidadores como Embajadores**
- Herramientas gratuitas
- Perfil destacado
- Capacitación gratuita
- Soporte prioritario

### **Instituciones como Partners**
- Paquetes escalables
- Integración con sistemas existentes
- Revenue sharing por referidos
- Soporte dedicado

### **Experiencia de Usuario**
- Onboarding simple (< 5 minutos)
- Transparencia total en precios
- Coordinación centralizada
- Soporte 24/7

---

## 📊 **Métricas de Éxito**

### **Técnicas**
- Tiempo de onboarding: < 5 minutos
- Tasa de conversión: > 20%
- Satisfacción: > 4.7/5
- Retención: > 85%

### **Negocio**
- Crecimiento orgánico: 30% mensual
- CAC: $0 por referidos
- LTV: 24 meses promedio
- Revenue por referido: ARS 15,000

---

## 1. Diagnóstico Centralizado
- El diagnóstico de cada persona bajo cuidado debe estar registrado, actualizado y accesible para todos los actores autorizados (familiares, cuidadores, profesionales, instituciones).
- El diagnóstico incluye: condiciones médicas, características relevantes, síntomas de alarma configurables, niveles de riesgo y necesidades especiales.
- El diagnóstico debe poder ser actualizado por profesionales y notificar a los actores relevantes.

## 2. Gestión de Medicación
- Toda medicación prescrita debe estar registrada y visible para los actores autorizados.
- El sistema debe permitir configurar alertas para la toma de medicación e inyecciones.
- Debe existir confirmación y registro de la toma efectiva de la medicación (por el usuario, cuidador o profesional).
- La trazabilidad de la medicación (quién la tomó, cuándo, quién confirmó) es obligatoria.

## 3. Protocolos de Emergencia y Prevención
- Cada persona bajo cuidado debe tener protocolos de emergencia personalizables (contactos, acciones a seguir, sensores asociados).
- El sistema debe anticipar y registrar caídas/incidentes mediante sensores y alertas automáticas.
- Debe poder configurarse a quién notificar y qué acciones tomar en cada caso.

## 4. Reportes y Observaciones Diarias
- Los cuidadores y profesionales deben registrar reportes diarios de higiene, alimentación, evacuación, conducta y estado de ánimo.
- Los reportes deben estar asociados a turnos y ser accesibles para los actores relevantes.
- La trazabilidad y comunicación entre turnos es fundamental.

## 5. Protocolos de Sujeción y Prevención de Incidentes
- Deben registrarse protocolos de sujeción y sensores asociados (sillas de ruedas, etc.).
- El sistema debe alertar y prevenir caídas o incidentes relacionados.

## 6. Seguimiento de Condiciones Específicas
- El sistema debe permitir el registro y seguimiento de condiciones como deterioro cognitivo, incontinencia, inestabilidad y otras relevantes.
- Debe poder configurarse la periodicidad y responsables del seguimiento.

## 7. Roles y Permisos
- El acceso a información sensible (diagnóstico, medicación, reportes) debe estar controlado por roles y permisos.
- Familiares, cuidadores, profesionales e instituciones tienen diferentes niveles de acceso y edición.
- Toda acción relevante debe quedar registrada para trazabilidad y auditoría.

## 8. Integración y Personalización
- El sistema debe ser interoperable con sensores IoT y dispositivos médicos.
- La personalización de síntomas de alarma, protocolos y reportes es clave para la calidad del cuidado.

*Para reglas completas y actualizadas, consulta el documento central.*

---

## Diagrama de Casos de Uso (Visual)

### Código Mermaid (para copiar en [Mermaid Live Editor](https://mermaid.live/))

```mermaid
usecaseDiagram
  actor Familiar
  actor Cuidador
  actor Institucion
  actor PersonaBajoCuidado

  Familiar --> (Ver diagnóstico)
  Familiar --> (Ver medicación)
  Familiar --> (Recibir alertas)
  Familiar --> (Ver reportes diarios)

  Cuidador --> (Registrar diagnóstico)
  Cuidador --> (Actualizar diagnóstico)
  Cuidador --> (Registrar toma de medicación)
  Cuidador --> (Recibir alertas)
  Cuidador --> (Registrar reportes diarios)
  Cuidador --> (Registrar incidentes/caídas)
  Cuidador --> (Configurar protocolos de emergencia)
  Cuidador --> (Registrar observaciones de turno)

  Institucion --> (Ver y auditar toda la información)
  Institucion --> (Configurar roles y permisos)
  Institucion --> (Gestionar protocolos de sujeción)
  Institucion --> (Gestionar integración con sensores)

  PersonaBajoCuidado --> (Ver diagnóstico propio)
  PersonaBajoCuidado --> (Ver medicación propia)
  PersonaBajoCuidado --> (Confirmar toma de medicación)
```

### Tabla de Casos de Uso (compatible con GitHub)

| Actor                  | Casos de Uso principales                                                                 |
|------------------------|----------------------------------------------------------------------------------------|
| Familiar/Representante | Ver diagnóstico, Ver medicación, Recibir alertas, Ver reportes diarios                  |
| Cuidador/Profesional   | Registrar/Actualizar diagnóstico, Registrar/Confirmar medicación, Recibir alertas,      |
|                        | Registrar reportes diarios, Registrar incidentes/caídas, Configurar protocolos,         |
|                        | Registrar observaciones de turno                                                        |
| Institución            | Ver y auditar información, Configurar roles y permisos, Protocolos de sujeción,         |
|                        | Integración con sensores                                                                |
| Persona Bajo Cuidado   | Ver diagnóstico propio, Ver medicación propia, Confirmar toma de medicación             |

```mermaid
usecase
  actor Family as Familiar
  actor Caregiver as Cuidador
  actor Institution as Institucion
  actor CaredPerson as PersonaBajoCuidado

  Family --> (Ver diagnóstico)
  Family --> (Ver medicación)
  Family --> (Recibir alertas)
  Family --> (Ver reportes diarios)

  Caregiver --> (Registrar diagnóstico)
  Caregiver --> (Actualizar diagnóstico)
  Caregiver --> (Registrar toma de medicación)
  Caregiver --> (Recibir alertas)
  Caregiver --> (Registrar reportes diarios)
  Caregiver --> (Registrar incidentes/caídas)
  Caregiver --> (Configurar protocolos de emergencia)
  Caregiver --> (Registrar observaciones de turno)

  Institution --> (Ver y auditar toda la información)
  Institution --> (Configurar roles y permisos)
  Institution --> (Gestionar protocolos de sujeción)
  Institution --> (Gestionar integración con sensores)

  CaredPerson --> (Ver diagnóstico propio)
  CaredPerson --> (Ver medicación propia)
  CaredPerson --> (Confirmar toma de medicación)
``` 