📁 Documentación CUIOT Organizada

## 📚 Estructura de Documentación

La documentación del sistema CUIOT está organizada en tres categorías principales:

### 🏗️ [Documentos Técnicos](./tecnicos/)
- Arquitectura del sistema
- APIs y endpoints
- Modelos de datos
- Guías de desarrollo
- Diagramas UML y DER

### 💼 [Documentos Comerciales](./comerciales/)
- Modelo de negocio
- Reglas de negocio
- Casos de uso
- Matriz de permisos
- Reglas para cuidadores

### 📖 [Manuales](./manuales/)
- Guías de usuario
- Documentación general
- Correcciones y versiones

---

## 🚀 Inicio Rápido

### Para Desarrolladores
1. 📖 [README General](./manuales/README.md)
2. 🏗️ [Arquitectura Técnica](./tecnicos/TECHNICAL_ARCHITECTURE.md)
3. 🔧 [Guía de Desarrollo](./tecnicos/DEVELOPMENT.md)
4. 📚 [API Backend](./tecnicos/API_BACKEND.md)

### Para Stakeholders
1. 💼 [Modelo de Negocio](./comerciales/BUSINESS_MODEL.md)
2. 📋 [Reglas de Negocio](./comerciales/BUSINESS_RULES.md)
3. 👥 [Casos de Uso](./comerciales/USE_CASES_BY_ROLE.md)

### Para Arquitectos
1. 🏗️ [Arquitectura Técnica](./tecnicos/TECHNICAL_ARCHITECTURE.md)
2. 📊 [Diagrama Entidad-Relación](./tecnicos/DER.md)
3. 🔄 [Diagramas UML](./tecnicos/UML.md)

---

## 🏥 Entidades Médicas Implementadas

El sistema incluye un módulo médico completo con las siguientes entidades:

- **Diagnósticos** - Con códigos CIE-10 y archivos adjuntos
- **Perfiles Médicos** - Información médica integral
- **Programas de Medicación** - Horarios y dosis específicas
- **Registros de Medicación** - Trazabilidad completa
- **Protocolos de Sujeción** - Prevención de incidentes
- **Observaciones de Turno** - Reportes clínicos detallados

📚 **Documentación técnica**: [API Médica](./tecnicos/API_BACKEND.md#sistema-médico-avanzado)
📊 **Modelo de datos**: [DER Médico](./tecnicos/DER.md)

## 🔗 Reglas de Negocio Fundamentales

### 📦 Asociación de Dispositivos y Paquetes
**Regla Principal:** Un dispositivo siempre está asociado a un paquete, y un paquete siempre está asociado a un propietario específico.

**Flujo de Asociación:**
```
Dispositivo → Paquete → Propietario
```

**Tipos de Propietarios:**
- **🏥 Institución** (paquetes profesionales/institucionales)
- **👨‍👩‍👧‍👦 Familiar/Responsable Legal** (paquetes individuales)
- **👴 Persona Cuidada** (tipo autocuidado)

### 👥 Roles del Sistema
**Roles Principales:**
- **admin** - Administrador del sistema (Sysadmin)
- **admin_institution** - Administrador de institución
- **caregiver** - Cuidador profesional
- **family_member** - Familiar de persona cuidada
- **caredperson** - Persona bajo cuidado
- **medical_staff** - Personal médico
- **freelance_caregiver** - Cuidador freelance
- **institution_staff** - Personal de institución

### 🏥 Tipos de Cuidado
**Categorías:**
- **self_care** - Autocuidado (persona independiente)
- **delegated_care** - Cuidado delegado (necesita representación)

### 🔄 Flujo de Datos IoT
**Secuencia de Eventos:**
1. **Dispositivo** detecta evento/condición
2. **Evento** se registra en el sistema
3. **Alerta** se genera si es necesario
4. **Notificación** se envía a usuarios relevantes
5. **Acción** se toma según protocolos configurados

📋 **Documentación detallada**: [Reglas de Negocio](./comerciales/BUSINESS_RULES.md)

---

## 🔗 **Enlaces Útiles**

- **Repositorio**: [GitHub](https://github.com/your-org/cuiot)
- **API Docs**: [Swagger UI](http://localhost:8000/docs)
- **Frontend**: [Web Panel](http://localhost:3000)
- **Base de Datos**: [PostgreSQL](http://localhost:5432)

---

## 📞 **Contacto**

Para preguntas sobre la documentación o el sistema:
- **Email**: tech@cuiot.com
- **Slack**: #cuiot-dev
- **Jira**: [Proyecto CUIOT](https://jira.company.com/cuiot)

---

*Última actualización: Julio 2024 - Documentación organizada por categorías*

---

