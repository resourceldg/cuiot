# CUIOT - Documento Central de Reglas de Negocio

## 🏥 **CUIOT: Plataforma de Monitoreo y Cuidado IoT**

**CUIOT** = **CUI**dar + **IOT** - Una plataforma integral de monitoreo y gestión del cuidado para personas bajo cuidado y personas con necesidades especiales, utilizando tecnología IoT.

---

## 📋 **Índice de Documentación**

### 🎯 **Documentos Principales**
- **[ACTORES_PERMISSIONS_MATRIX.md](./ACTORS_PERMISSIONS_MATRIX.md)** - Matriz completa de actores, permisos y responsabilidades
- **[BUSINESS_MODEL.md](./BUSINESS_MODEL.md)** - Modelo de negocio detallado y flujos de ingresos
- **[BUSINESS_RULES.md](./BUSINESS_RULES.md)** - Reglas de negocio fundamentales
- **[CAREGIVER_FREELANCE_RULES.md](./CAREGIVER_FREELANCE_RULES.md)** - Sistema de scoring y freelance para cuidadores

### 🏗️ **Documentación Técnica**
- **[TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)** - Arquitectura técnica del sistema
- **[API_BACKEND.md](./API_BACKEND.md)** - Documentación de APIs y endpoints
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Guías de desarrollo y setup
- **[UML.md](./UML.md)** - Diagramas UML del sistema
- **[DER.md](./DER.md)** - Diagrama Entidad-Relación

### 🎨 **UX/UI y Diseño**
- **[UX_UI_DESIGN_SYSTEM.md](./UX_UI_DESIGN_SYSTEM.md)** - Sistema de diseño y experiencia de usuario

### 📊 **Análisis y Planificación**
- **[ARCHITECTURE_ANALYSIS.md](./ARCHITECTURE_ANALYSIS.md)** - Análisis de arquitectura
- **[ARCHITECTURE_FIRST_STAGE.md](./ARCHITECTURE_FIRST_STAGE.md)** - Primera etapa de arquitectura
- **[BACKEND_REFACTORING_FEEDBACK.md](./BACKEND_REFACTORING_FEEDBACK.md)** - Feedback del refactor del backend
- **[TECHNICAL_BACKEND_REFACTOR_PLAN.md](./TECHNICAL_BACKEND_REFACTOR_PLAN.md)** - Plan de refactor técnico
- **[INTEGRATION_SUMMARY.md](./INTEGRATION_SUMMARY.md)** - Resumen de integraciones

---

## 🎯 **Resumen Ejecutivo de CUIOT**

### **Propuesta de Valor**
CUIOT es una plataforma integral que combina:
- **Monitoreo IoT** en tiempo real
- **Gestión de cuidadores** freelance
- **Coordinación de instituciones** médicas
- **Sistema de alertas** inteligentes
- **Reportes** de salud y actividad

### **Modelo de Negocio Principal**
1. **Venta de dispositivos IoT** (sensores, wearables, cámaras)
2. **Suscripciones mensuales** por monitoreo
3. **Comisiones** por gestión de cuidadores
4. **Paquetes institucionales** para clínicas y geriátricos
5. **Sistema de referidos** con incentivos

### **Actores del Sistema**
- **Persona Bajo Cuidado**: Usuario final (autocuidado o delegado)
- **Familiar/Representante**: Responsable legal y financiero
- **Cuidador Freelancer**: Profesional independiente
- **Institución**: Centro médico, geriátrico, clínica
- **Administrador**: Gestor de la plataforma

---

## 🚀 **Estrategia de Crecimiento Basada en Referidos**

### **Cuidadores como Embajadores**
- **Comisión**: 15% del primer mes + 5% recurrente
- **Herramientas gratuitas**: App profesional, gestión de horarios
- **Perfil destacado**: Mejor posicionamiento en búsquedas
- **Capacitación**: Cursos y certificaciones gratuitas

### **Instituciones como Partners**
- **Paquete Básico**: ARS 5,000/mes (10 pacientes)
- **Paquete Profesional**: ARS 15,000/mes (50 pacientes)
- **Paquete Enterprise**: ARS 50,000/mes (ilimitado)
- **Revenue sharing**: Por referidos de familias

### **Experiencia de Usuario como Driver**
- **Onboarding simple**: 5 minutos para registrarse
- **Herramientas útiles**: Calendario, pagos, comunicación
- **Transparencia total**: Reviews, precios, antecedentes
- **Soporte 24/7**: Chat, teléfono, WhatsApp

---

## 💡 **Diferenciación Clave: Autocuidado vs Cuidado Delegado**

### **Autocuidado (Self-Care)**
- **Usuario**: Adulto mayor independiente
- **Compra**: Directa de servicios IoT
- **Uso**: Monitoreo personal, alarmas, gestión propia
- **Permisos**: Control total de datos y decisiones

### **Cuidado Delegado (Delegated Care)**
- **Usuario**: Persona dependiente
- **Compra**: A través de familiar/representante
- **Uso**: Monitoreo por terceros, coordinación
- **Permisos**: Compartidos con representante legal

---

## 📊 **Métricas de Éxito**

### **Técnicas**
- Tiempo de onboarding: < 5 minutos
- Tasa de conversión: > 20% de referidos
- Satisfacción: > 4.7/5 promedio
- Retención: > 85% mensual

### **Negocio**
- Crecimiento orgánico: 30% mensual
- CAC (Costo de Adquisición): $0 por referidos
- LTV (Lifetime Value): 24 meses promedio
- Revenue por referido: ARS 15,000 promedio

### **Sociales**
- Empleo generado: 500+ cuidadores activos
- Instituciones integradas: 50+ partners
- Familias beneficiadas: 1000+ hogares
- Calidad del servicio: +40% satisfacción

---

## 🔧 **Stack Técnico**

### **Backend**
- **FastAPI** (Python) - APIs RESTful
- **PostgreSQL** - Base de datos principal
- **SQLAlchemy** - ORM
- **Alembic** - Migraciones
- **JWT** - Autenticación

### **Frontend**
- **SvelteKit** - Framework web
- **Tailwind CSS** - Estilos
- **TypeScript** - Tipado estático

### **IoT**
- **MQTT** - Protocolo de comunicación
- **Mosquitto** - Broker MQTT
- **Sensores** - Temperatura, movimiento, ubicación

### **DevOps**
- **Docker** - Containerización
- **Docker Compose** - Orquestación local
- **Git** - Control de versiones

---

## 🎯 **Próximos Pasos**

### **Inmediatos (1-2 semanas)**
1. ✅ Migración de base de datos con nuevos modelos
2. ✅ Implementación del sistema de referidos
3. ✅ Actualización de permisos por tipo de cuidado
4. ✅ Testing end-to-end del flujo completo

### **Corto Plazo (1 mes)**
1. 🎯 Dashboard de referidos y comisiones
2. 🎯 Sistema de notificaciones automáticas
3. 🎯 Integración con pasarelas de pago
4. 🎯 App móvil para cuidadores

### **Mediano Plazo (3 meses)**
1. 🎯 Integración con dispositivos IoT reales
2. 🎯 Analytics avanzados y reportes
3. 🎯 Sistema de certificaciones para cuidadores
4. 🎯 Partnership con instituciones médicas

---

## 📞 **Contacto y Soporte**

### **Desarrollo**
- **Repositorio**: [GitHub](https://github.com/your-org/cuiot)
- **Documentación**: [Docs](./)
- **API**: [Swagger UI](http://localhost:8000/docs)

### **Negocio**
- **Email**: business@cuiot.com
- **WhatsApp**: +54 9 11 1234-5678
- **Soporte**: soporte@cuiot.com

---

*Documento central de CUIOT - Versión 1.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 