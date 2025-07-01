# 📚 Documentación Técnica - CUIOT

> Documentación técnica completa del sistema CUIOT para desarrolladores, arquitectos e ingenieros.

---

## 🏗️ **Arquitectura del Sistema**

### **Arquitectura General**
- **[TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)** - Arquitectura técnica completa del sistema
- **[ARCHITECTURE_ANALYSIS.md](./ARCHITECTURE_ANALYSIS.md)** - Análisis detallado de la arquitectura
- **[ARCHITECTURE_FIRST_STAGE.md](./ARCHITECTURE_FIRST_STAGE.md)** - Primera etapa de arquitectura
- **[BACKEND_REFACTORING_FEEDBACK.md](./BACKEND_REFACTORING_FEEDBACK.md)** - Feedback del refactoring del backend
- **[TECHNICAL_BACKEND_REFACTOR_PLAN.md](./TECHNICAL_BACKEND_REFACTOR_PLAN.md)** - Plan de refactoring técnico

### **Modelos de Datos**
- **[DER.md](./DER.md)** - Diagrama Entidad-Relación completo con entidades médicas
- **[UML.md](./UML.md)** - Diagramas UML del sistema

---

## 🔧 **Desarrollo y APIs**

### **APIs y Endpoints**
- **[API_BACKEND.md](./API_BACKEND.md)** - Documentación completa de la API REST
  - Autenticación JWT
  - Gestión de personas bajo cuidado
  - **Sistema Médico Avanzado** (Diagnósticos, Perfiles, Medicación, Protocolos, Observaciones)
  - Sistema de paquetes y suscripciones
  - Sistema de referidos y comisiones

### **Guías de Desarrollo**
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Guía completa de desarrollo
- **[INTEGRATION_SUMMARY.md](./INTEGRATION_SUMMARY.md)** - Resumen de integraciones

### **Diseño y UX**
- **[UX_UI_DESIGN_SYSTEM.md](./UX_UI_DESIGN_SYSTEM.md)** - Sistema de diseño y UX

---

## 🏥 **Módulo Médico Técnico**

### **Entidades Implementadas**
1. **Diagnósticos** (`DIAGNOSES`)
   - Códigos CIE-10
   - Archivos adjuntos (PDF, imágenes)
   - Historial de versiones
   - Notificaciones automáticas

2. **Perfiles Médicos** (`MEDICAL_PROFILES`)
   - Información médica integral
   - Estructura JSONB flexible
   - Contactos de emergencia

3. **Programas de Medicación** (`MEDICATION_SCHEDULES`)
   - Horarios específicos
   - Dosis y frecuencia
   - Efectos secundarios

4. **Registros de Medicación** (`MEDICATION_LOGS`)
   - Trazabilidad completa
   - Confirmación de administración
   - Tracking de efectos secundarios

5. **Protocolos de Sujeción** (`RESTRAINT_PROTOCOLS`)
   - Validación profesional
   - Procedimientos detallados
   - Monitoreo continuo

6. **Observaciones de Turno** (`SHIFT_OBSERVATIONS`)
   - Reportes clínicos detallados
   - Sistema de verificación
   - Comunicación entre turnos

### **Endpoints Médicos**
- `GET/POST/PUT/DELETE /api/v1/diagnoses/`
- `GET/POST/PUT/DELETE /api/v1/medical-profiles/`
- `GET/POST/PUT/DELETE /api/v1/medication-schedules/`
- `GET/POST/PUT/DELETE /api/v1/medication-logs/`
- `GET/POST/PUT/DELETE /api/v1/restraint-protocols/`
- `GET/POST/PUT/DELETE /api/v1/shift-observations/`

---

## 🚀 **Inicio Rápido para Desarrolladores**

### **1. Configuración del Entorno**
```bash
# Clonar repositorio
git clone [repository-url]
cd viejos_son_los_trapos

# Configurar Docker
docker-compose up -d

# Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Ejecutar tests
docker-compose exec backend python -m pytest
```

### **2. Estructura del Proyecto**
```
backend/
├── app/
│   ├── api/v1/endpoints/     # Endpoints de la API
│   ├── models/               # Modelos SQLAlchemy
│   ├── schemas/              # Esquemas Pydantic
│   ├── services/             # Lógica de negocio
│   └── core/                 # Configuración central
├── tests/                    # Tests de integración
└── alembic/                  # Migraciones de BD
```

### **3. Tecnologías Utilizadas**
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: SvelteKit + Tailwind CSS
- **Base de Datos**: PostgreSQL con UUIDs
- **Autenticación**: JWT
- **Documentación**: Swagger/OpenAPI
- **Testing**: Pytest + Docker

---

## 📊 **Estado de Implementación**

### **✅ Completado**
- ✅ Arquitectura base del sistema
- ✅ Sistema de autenticación y autorización
- ✅ CRUD completo para todas las entidades
- ✅ **Módulo médico completo** con 6 entidades
- ✅ Sistema de archivos adjuntos
- ✅ Validaciones robustas
- ✅ Tests de integración
- ✅ Migraciones Alembic

### **🔄 En Desarrollo**
- 🔄 Dashboard de analytics médicos
- 🔄 Integración con dispositivos IoT
- 🔄 Sistema de notificaciones avanzado

### **📋 Pendiente**
- 📋 Machine Learning para predicciones
- 📋 Integración con sistemas externos
- 📋 App móvil nativa

---

## 🔗 **Enlaces Útiles**

- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Repositorio**: [GitHub](https://github.com/your-org/cuiot)
- **Base de Datos**: [PostgreSQL](http://localhost:5432)
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Documentación Comercial**: [../comerciales/](../comerciales/)
- **Manuales**: [../manuales/](../manuales/)

---

## 📞 **Soporte Técnico**

- **Email**: tech@cuiot.com
- **Slack**: #cuiot-dev
- **Jira**: [Proyecto CUIOT](https://jira.company.com/cuiot)

---

*Documentación Técnica CUIOT - Julio 2024* 