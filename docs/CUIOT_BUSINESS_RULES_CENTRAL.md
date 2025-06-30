# CUIOT - Reglas de Negocio Centrales

## 🏥 **CUIOT: Reglas de Negocio Fundamentales**

**CUIOT** = **CUI**dar + **IOT** - Plataforma de monitoreo y gestión del cuidado usando IoT.

---

## 📋 **Índice de Reglas**

1. **[Actores y Permisos](#actores-y-permisos)**
2. **[Modelo de Negocio](#modelo-de-negocio)**
3. **[Sistema de Referidos](#sistema-de-referidos)**
4. **[Tipos de Cuidado](#tipos-de-cuidado)**
5. **[Scoring y Calificaciones](#scoring-y-calificaciones)**
6. **[Relaciones y Asignaciones](#relaciones-y-asignaciones)**
7. **[Flujos de Información](#flujos-de-información)**
8. **[Consideraciones Éticas](#consideraciones-éticas)**
9. **[Métricas y KPIs](#métricas-y-kpis)**

---

## 👥 **Actores y Permisos**

### **A. Persona Bajo Cuidado (CaredPerson)**
**Tipos**:
- **Autocuidado**: Independiente, toma decisiones propias
- **Cuidado Delegado**: Dependiente, necesita representación

**Permisos por Tipo**:

| Acción | Autocuidado | Cuidado Delegado |
|--------|-------------|------------------|
| Contratar servicios IoT | ✅ | ❌ |
| Contratar cuidador | ✅ | ❌ |
| Contratar institución | ✅ | ❌ |
| Ver costos totales | ✅ | ❌ |
| Editar perfil propio | ✅ | ❌ |
| Asignar cuidadores | ✅ | ❌ |
| Coordinar servicios | ✅ | ❌ |
| Recomendar plataforma | ✅ | ❌ |
| Recibir comisiones | ✅ | ❌ |

### **B. Familiar/Representante Legal (User: family)**
**Responsabilidades**:
- Toma de decisiones para cuidado delegado
- Pagos y contrataciones
- Consentimiento legal
- Coordinación entre cuidadores e instituciones

**Permisos**:
- ✅ Contratar servicios IoT
- ✅ Contratar cuidadores e instituciones
- ✅ Ver costos totales
- ✅ Editar perfil familiar
- ✅ Asignar cuidadores
- ✅ Coordinar servicios
- ✅ Recomendar plataforma
- ✅ Recibir comisiones

### **C. Cuidador Freelancer (User: caregiver)**
**Responsabilidades**:
- Brindar cuidado de calidad
- Cumplir horarios acordados
- Reportar incidentes
- Mantener confidencialidad

**Permisos**:
- ✅ Comprar dispositivos IoT
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

---

## 💰 **Modelo de Negocio**

### **Flujos de Ingresos**

#### **1. Venta de Dispositivos IoT**
- **Sensores de movimiento**: ARS 15,000
- **Wearables**: ARS 25,000
- **Cámaras de seguridad**: ARS 35,000
- **Sensores de temperatura**: ARS 8,000
- **GPS tracker**: ARS 12,000

#### **2. Suscripciones Mensuales**
- **Básico**: ARS 3,000/mes (1 persona, monitoreo básico)
- **Familiar**: ARS 8,000/mes (hasta 3 personas, monitoreo completo)
- **Premium**: ARS 15,000/mes (ilimitado, analytics avanzados)

#### **3. Comisiones por Gestión**
- **Cuidador**: 10% del valor del servicio
- **Institución**: 5% del valor del servicio
- **Plataforma**: 15% del valor total

#### **4. Paquetes Institucionales**
- **Básico**: ARS 5,000/mes (10 pacientes)
- **Profesional**: ARS 15,000/mes (50 pacientes)
- **Enterprise**: ARS 50,000/mes (ilimitado)

#### **5. Sistema de Referidos**
- **Comisión por referido**: 15% del primer mes
- **Comisión recurrente**: 5% mensual
- **Bonificación por volumen**: +10% después de 5 referidos

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

### **Autocuidado (Self-Care)**
**Definición**: Persona independiente que gestiona su propio cuidado

**Características**:
- Toma decisiones propias
- Compra servicios directamente
- Control total de datos
- Monitoreo personal

**Casos de Uso**:
- Adultos mayores independientes
- Personas con condiciones crónicas manejables
- Usuarios de monitoreo preventivo

### **Cuidado Delegado (Delegated Care)**
**Definición**: Persona dependiente que necesita representación

**Características**:
- Necesita representante legal
- Compra a través de familiar
- Datos compartidos con representante
- Monitoreo por terceros

**Casos de Uso**:
- Personas con demencia
- Discapacidades severas
- Menores de edad
- Incapacitados legales

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
CaredPerson → Busca servicios → Compara opciones → Compra → Usa plataforma
```

### **Flujo de Compra (Cuidado Delegado)**
```
Family → Busca cuidadores → Evalúa opciones → Contrata → Coordina servicios
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
2. **Gestión de perfiles** por tipo de usuario
3. **Sistema de referidos** con comisiones
4. **Scoring y reviews** para calidad
5. **Dashboard de métricas** para seguimiento

### **Validaciones Requeridas**
- **Capacidad legal**: Verificar edad y capacidad
- **Representación**: Validar representantes legales
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
- [ ] Modelos de datos con tipos de cuidado
- [ ] Sistema de permisos granular
- [ ] API de referidos y comisiones
- [ ] Sistema de scoring y reviews
- [ ] Validaciones de capacidad legal

### **Frontend**
- [ ] Interfaces diferenciadas por rol
- [ ] Dashboard de referidos
- [ ] Sistema de reviews
- [ ] Gestión de perfiles
- [ ] Reportes y métricas

### **Negocio**
- [ ] Flujos de pago y comisiones
- [ ] Sistema de notificaciones
- [ ] Soporte y capacitación
- [ ] Marketing de referidos
- [ ] Partnership con instituciones

---

*Documento de Reglas de Negocio Centrales - CUIOT v1.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 