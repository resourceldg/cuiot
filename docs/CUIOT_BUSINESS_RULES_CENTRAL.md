# CUIOT - Reglas de Negocio Centrales

## 🏥 **CUIOT: Reglas de Negocio Fundamentales**

**CUIOT** = **CUI**dar + **IOT** - Plataforma de monitoreo y gestión del cuidado usando IoT.

---

## 📋 **Índice de Reglas**

1. **[Actores y Permisos](#actores-y-permisos)**
2. **[Modelo de Negocio](#modelo-de-negocio)**
3. **[Sistema de Paquetes](#sistema-de-paquetes)**
4. **[Sistema de Referidos](#sistema-de-referidos)**
5. **[Tipos de Cuidado](#tipos-de-cuidado)**
6. **[Scoring y Calificaciones](#scoring-y-calificaciones)**
7. **[Relaciones y Asignaciones](#relaciones-y-asignaciones)**
8. **[Flujos de Información](#flujos-de-información)**
9. **[Consideraciones Éticas](#consideraciones-éticas)**
10. **[Métricas y KPIs](#métricas-y-kpis)**

---

## 👥 **Actores y Permisos**

### **A. Persona Bajo Cuidado (CaredPerson)**
**Tipos**:
- **Autocuidado (self_care)**: Independiente, toma decisiones propias
- **Cuidado Delegado (delegated)**: Dependiente, necesita representación

**Permisos por Tipo**:

| Acción | Autocuidado | Cuidado Delegado |
|--------|-------------|------------------|
| Contratar paquetes | ✅ | ❌ |
| Contratar cuidador | ✅ | ❌ |
| Contratar institución | ✅ | ❌ |
| Ver costos totales | ✅ | ❌ |
| Editar perfil propio | ✅ | ❌ |
| Asignar cuidadores | ✅ | ❌ |
| Coordinar servicios | ✅ | ❌ |
| Recomendar plataforma | ✅ | ❌ |
| Recibir comisiones | ✅ | ❌ |
| Gestionar dispositivos IoT | ✅ | ❌ |

**Regla Crítica**: Persona bajo cuidado delegado **DEBE** tener un representante legal (familiar, tutor) vinculado.

### **B. Familiar/Representante Legal (User: family)**
**Responsabilidades**:
- Toma de decisiones para cuidado delegado
- Pagos y contrataciones
- Consentimiento legal
- Coordinación entre cuidadores e instituciones

**Permisos**:
- ✅ Contratar paquetes para representado
- ✅ Contratar cuidadores e instituciones
- ✅ Ver costos totales del representado
- ✅ Editar perfil familiar
- ✅ Asignar cuidadores al representado
- ✅ Coordinar servicios
- ✅ Recomendar plataforma
- ✅ Recibir comisiones
- ✅ Gestionar dispositivos IoT del representado

### **C. Cuidador Freelancer (User: caregiver)**
**Responsabilidades**:
- Brindar cuidado de calidad
- Cumplir horarios acordados
- Reportar incidentes
- Mantener confidencialidad

**Permisos**:
- ✅ Comprar dispositivos IoT
- ✅ Contratar paquetes profesionales
- ✅ Suscripción premium
- ✅ Reportar instituciones
- ✅ Reportar incidentes
- ✅ Ver perfil propio
- ✅ Editar perfil propio
- ✅ Coordinar servicios
- ✅ Recomendar plataforma
- ✅ Recibir comisiones

**Rol Adicional**: Embajador de la plataforma

### **D. Institución (Institution)**
**Responsabilidades**:
- Brindar servicios médicos
- Cumplir normativas legales
- Mantener estándares de calidad
- Coordinar con cuidadores externos

**Permisos**:
- ✅ Comprar dispositivos IoT
- ✅ Contratar paquetes institucionales
- ✅ Suscripción premium
- ✅ Reportar cuidadores
- ✅ Reportar incidentes
- ✅ Reporte médico
- ✅ Ver perfil propio
- ✅ Editar perfil propio
- ✅ Coordinar servicios
- ✅ Recomendar plataforma
- ✅ Recibir comisiones

**Rol Adicional**: Partner de la plataforma

### **E. Administrador (User: admin)**
**Responsabilidades**:
- Operar la plataforma
- Mantener seguridad de datos
- Proporcionar soporte técnico
- Gestionar disputas

**Permisos**:
- ✅ Gestionar usuarios
- ✅ Ver reportes del sistema
- ✅ Configurar sistema
- ✅ Actualizar estados de referidos
- ✅ Pagar comisiones
- ✅ Expirar referidos antiguos
- ✅ Gestionar paquetes
- ✅ Configurar precios

---

## 💰 **Modelo de Negocio**

### **Flujos de Ingresos**

#### **1. Venta de Dispositivos IoT**
- **Sensores de movimiento**: ARS 15,000
- **Wearables**: ARS 25,000
- **Cámaras de seguridad**: ARS 35,000
- **Sensores de temperatura**: ARS 8,000
- **GPS tracker**: ARS 12,000

#### **2. Paquetes de Servicios (NUEVA ENTIDAD CENTRAL)**
- **Básico Individual**: ARS 3,000/mes (1 persona, monitoreo básico)
- **Familiar**: ARS 8,000/mes (hasta 3 personas, monitoreo completo)
- **Premium**: ARS 15,000/mes (ilimitado, analytics avanzados)
- **Profesional**: ARS 12,000/mes (cuidadores, herramientas avanzadas)
- **Institucional Básico**: ARS 5,000/mes (10 pacientes)
- **Institucional Profesional**: ARS 15,000/mes (50 pacientes)
- **Institucional Enterprise**: ARS 50,000/mes (ilimitado)

#### **3. Comisiones por Gestión**
- **Cuidador**: 10% del valor del servicio
- **Institución**: 5% del valor del servicio
- **Plataforma**: 15% del valor total

#### **4. Sistema de Referidos**
- **Comisión por referido**: 15% del primer mes
- **Comisión recurrente**: 5% mensual
- **Bonificación por volumen**: +10% después de 5 referidos

---

## 📦 **Sistema de Paquetes (NUEVA ENTIDAD CENTRAL)**

### **Definición**
Los **Paquetes** son la unidad central del negocio que pueden ser contratados por cualquier tipo de usuario excepto personas bajo cuidado delegado (que deben contratar a través de su representante legal).

### **Tipos de Paquetes**

#### **Paquetes Individuales**
| Paquete | Precio | Usuarios | Dispositivos | Características |
|---------|--------|----------|--------------|-----------------|
| **Básico** | ARS 3,000/mes | 1 | 3 | Monitoreo básico, alertas simples |
| **Familiar** | ARS 8,000/mes | 3 | 10 | Monitoreo completo, reportes |
| **Premium** | ARS 15,000/mes | Ilimitado | Ilimitado | Analytics avanzados, IA |

#### **Paquetes Profesionales**
| Paquete | Precio | Usuarios | Dispositivos | Características |
|---------|--------|----------|--------------|-----------------|
| **Profesional** | ARS 12,000/mes | 1 | 15 | Herramientas de gestión, agenda |
| **Profesional Plus** | ARS 20,000/mes | 1 | 30 | Analytics, reportes avanzados |

#### **Paquetes Institucionales**
| Paquete | Precio | Pacientes | Dispositivos | Características |
|---------|--------|-----------|--------------|-----------------|
| **Institucional Básico** | ARS 5,000/mes | 10 | 30 | Monitoreo básico institucional |
| **Institucional Profesional** | ARS 15,000/mes | 50 | 150 | Gestión completa, reportes |
| **Institucional Enterprise** | ARS 50,000/mes | Ilimitado | Ilimitado | API completa, integración |

### **Reglas de Contratación**

#### **Quién Puede Contratar**
- ✅ **Autocuidado**: Puede contratar directamente
- ✅ **Familiar/Representante**: Puede contratar para representado
- ✅ **Cuidador Freelancer**: Puede contratar paquetes profesionales
- ✅ **Institución**: Puede contratar paquetes institucionales
- ❌ **Cuidado Delegado**: NO puede contratar directamente (debe ser por representante)

#### **Validaciones Obligatorias**
1. **Capacidad Legal**: Verificar edad y capacidad del contratante
2. **Representación**: Para cuidado delegado, validar representante legal
3. **Límites**: Verificar límites de usuarios/dispositivos según paquete
4. **Pago**: Validar método de pago y capacidad financiera

### **Características de los Paquetes**

#### **Funcionalidades por Nivel**
```json
{
  "básico": {
    "monitoreo": "básico",
    "alertas": "simples",
    "reportes": "diarios",
    "dispositivos": 3,
    "usuarios": 1,
    "soporte": "email"
  },
  "familiar": {
    "monitoreo": "completo",
    "alertas": "avanzadas",
    "reportes": "semanal",
    "dispositivos": 10,
    "usuarios": 3,
    "soporte": "chat"
  },
  "premium": {
    "monitoreo": "24/7",
    "alertas": "IA",
    "reportes": "personalizados",
    "dispositivos": "ilimitado",
    "usuarios": "ilimitado",
    "soporte": "24/7"
  }
}
```

---

## 🚀 **Sistema de Referidos**

### **Comisiones por Tipo de Referente**

| Referente | Primer Mes | Recurrente | Bonificación |
|-----------|------------|------------|--------------|
| Cuidador | 15% | 5% | 10% |
| Institución | 10% | 3% | 5% |
| Familia | 5% | 2% | 3% |
| Autocuidado | 5% | 2% | 3% |

### **Flujo de Referido**
```
1. Referente brinda servicio de calidad
2. Referente recomienda CUIOT
3. Nuevo usuario se registra con código
4. Sistema asigna comisión automáticamente
5. Referente recibe pago mensual
```

### **Incentivos para Referentes**
- **Herramientas gratuitas**: App profesional, gestión de horarios
- **Perfil destacado**: Mejor posicionamiento en búsquedas
- **Capacitación gratuita**: Cursos y certificaciones
- **Soporte prioritario**: Atención preferencial

---

## 🏥 **Tipos de Cuidado**

### **Autocuidado (self_care)**
**Definición**: Persona independiente que gestiona su propio cuidado

**Características**:
- Toma decisiones propias
- Compra paquetes directamente
- Control total de datos
- Monitoreo personal
- Puede recibir comisiones por referidos

**Casos de Uso**:
- Personas mayores independientes
- Personas con condiciones crónicas manejables
- Usuarios de monitoreo preventivo

### **Cuidado Delegado (delegated)**
**Definición**: Persona dependiente que necesita representación

**Características**:
- Necesita representante legal OBLIGATORIO
- Compra a través de familiar/representante
- Datos compartidos con representante
- Monitoreo por terceros
- NO puede contratar paquetes directamente

**Casos de Uso**:
- Personas con demencia
- Discapacidades severas
- Menores de edad
- Incapacitados legales

**Regla Crítica**: Persona bajo cuidado delegado **DEBE** tener un representante legal vinculado en el sistema.

---

## ⭐ **Scoring y Calificaciones**

### **Factores de Evaluación**

#### **Para Cuidadores**
1. **Experiencia** (30%): Años de experiencia, certificaciones
2. **Calidad** (25%): Reviews de familias, cumplimiento
3. **Confiabilidad** (20%): Puntualidad, disponibilidad
4. **Disponibilidad** (15%): Horarios, flexibilidad
5. **Especialización** (10%): Áreas de expertise

#### **Para Instituciones**
1. **Calidad médica** (35%): Certificaciones, estándares
2. **Infraestructura** (25%): Instalaciones, equipamiento
3. **Personal** (20%): Calificación del staff
4. **Atención** (15%): Tiempo de respuesta, trato
5. **Precios** (5%): Competitividad

### **Sistema de Reviews**
- **Escala**: 1-5 estrellas
- **Categorías**: Calidad, puntualidad, comunicación, precio
- **Verificación**: Solo usuarios reales pueden review
- **Moderación**: Reviews verificadas por admin

---

## 🔗 **Relaciones y Asignaciones**

### **Múltiples Cuidadores por Persona**
- **Cuidado 24/7**: Múltiples turnos
- **Especializaciones**: Diferentes áreas de expertise
- **Backup**: Cuidadores de respaldo
- **Coordinación**: Calendario unificado

### **Múltiples Instituciones por Persona**
- **Especialidades**: Diferentes áreas médicas
- **Ubicación**: Instituciones cercanas
- **Servicios**: Complementarios
- **Coordinación**: Información compartida

### **Asignaciones de Cuidadores**
- **Tipo**: Full-time, part-time, on-call
- **Horarios**: Definidos y flexibles
- **Pago**: Por hora, por día, por mes
- **Evaluación**: Periódica de rendimiento

---

## 📊 **Flujos de Información**

### **Flujo de Compra (Autocuidado)**
```
CaredPerson → Busca paquetes → Compara opciones → Compra → Usa plataforma
```

### **Flujo de Compra (Cuidado Delegado)**
```
Family → Busca paquetes → Evalúa opciones → Contrata para representado → Coordina servicios
```

### **Flujo de Referido**
```
Cuidador/Institución → Recomienda → Familia se registra → Comisión automática
```

### **Flujo de Reportes**
```
Cualquier actor → Reporta → Sistema analiza → Notifica apropiados → Acción
```

---

## ⚖️ **Consideraciones Éticas**

### **Privacidad por Tipo de Usuario**
- **Autocuidado**: Control total de sus datos
- **Cuidado Delegado**: Compartido con representante legal
- **Cuidadores**: Solo información profesional relevante
- **Instituciones**: Información médica necesaria

### **Transparencia en Recomendaciones**
- **Disclosure obligatorio**: Referentes deben revelar comisiones
- **Reviews independientes**: No influenciadas por incentivos
- **Calidad verificada**: Recomendaciones basadas en resultados
- **Sin spam**: Límites en frecuencia de recomendaciones

### **Consentimiento Informado**
- **Autocuidado**: Consentimiento directo
- **Cuidado Delegado**: Consentimiento del representante legal
- **Menores**: Consentimiento de padres/tutores
- **Incapacitados**: Consentimiento de representante legal

---

## 📈 **Métricas y KPIs**

### **Técnicos**
- **Tiempo de onboarding**: < 5 minutos para cuidadores
- **Tasa de conversión**: > 20% de referidos a contrataciones
- **Satisfacción**: > 4.7/5 en calificaciones promedio
- **Retención**: > 85% de clientes recurrentes

### **Negocio**
- **Crecimiento orgánico**: 30% mensual por referidos
- **CAC (Costo de Adquisición)**: $0 por referidos orgánicos
- **LTV (Lifetime Value)**: 24 meses promedio
- **Revenue por referido**: ARS 15,000 promedio

### **Sociales**
- **Empleo generado**: 500+ cuidadores activos en 12 meses
- **Instituciones integradas**: 50+ partners en 12 meses
- **Familias beneficiadas**: 1000+ hogares con mejor cuidado
- **Calidad del servicio**: Mejora del 40% en satisfacción

---

## 🎯 **Reglas de Implementación**

### **Prioridades de Desarrollo**
1. **Sistema de autenticación** con roles diferenciados
2. **Gestión de paquetes** como unidad central del negocio
3. **Validación de capacidad legal** por tipo de usuario
4. **Sistema de referidos** con comisiones
5. **Scoring y reviews** para calidad
6. **Dashboard de métricas** para seguimiento

### **Validaciones Requeridas**
- **Capacidad legal**: Verificar edad y capacidad
- **Representación**: Validar representantes legales para cuidado delegado
- **Certificaciones**: Verificar credenciales profesionales
- **Antecedentes**: Chequear historial criminal

### **Compliance Legal**
- **Ley de Protección de Datos**: RGPD argentino
- **Ley de Salud**: Normativas médicas
- **Ley de Trabajo**: Relaciones laborales freelance
- **Ley de Consumidor**: Derechos del consumidor

---

## 📋 **Checklist de Implementación**

### **Backend**
- [x] Modelos de datos con tipos de cuidado
- [x] Sistema de permisos granular
- [x] API de referidos y comisiones
- [x] Sistema de scoring y reviews
- [ ] Validaciones de capacidad legal
- [ ] Sistema de paquetes como entidad central
- [ ] Validación de representación legal

### **Frontend**
- [ ] Interfaces diferenciadas por rol
- [ ] Dashboard de referidos
- [ ] Sistema de reviews
- [ ] Gestión de perfiles
- [ ] Reportes y métricas
- [ ] Gestión de paquetes

### **Negocio**
- [ ] Flujos de pago y comisiones
- [ ] Sistema de notificaciones
- [ ] Soporte y capacitación
- [ ] Marketing de referidos
- [ ] Partnership con instituciones

---

*Documento de Reglas de Negocio Centrales - CUIOT v2.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 