# 🎨 Sistema de Diseño UX/UI - CUIOT

## 📋 Resumen Ejecutivo

Este documento define el sistema de diseño UX/UI para CUIOT, abarcando flujos de información, dashboards, modales y experiencias de usuario para cada tipo de usuario, desde el MVP hasta la evolución futura.

---

## 1. Objetivo del Diseño
- Crear una experiencia intuitiva, accesible y eficiente.
- Facilitar el cuidado y la gestión de emergencias.
- Empoderar a cuidadores, familiares e instituciones.
- Escalar desde uso individual hasta institucional.
- Mantener privacidad y seguridad de datos sensibles.

---

## 2. Roles y Privilegios

| Rol                        | Acceso a Dashboards         | Acciones Principales                        |
|----------------------------|----------------------------|---------------------------------------------|
| Familiar/Tutor             | Familiar                    | Ver estado, recibir alertas, configurar protocolos, comunicación directa |
| Cuidador Profesional       | Profesional                 | Gestionar pacientes, responder alertas, reportar eventos, ver protocolos |
| Cuidador Freelance         | Freelance                   | Gestionar múltiples instituciones/clientes, agenda, facturación, reportes |
| Admin de Institución       | Institucional               | Gestión global, métricas, personal, reportes, compliance |
| Persona bajo cuidado       | Paciente                    | Ver estado propio, pedir ayuda, configurar preferencias |
| Admin del sistema          | Global                      | Gestión de usuarios, monitoreo, soporte     |

---

## 3. Arquitectura de Información

```
CUIOT Dashboard
├── Overview (Vista General)
├── Gestión de Cuidado
│   ├── Personas Bajo Cuidado
│   ├── Cuidadores
│   └── Asignaciones
├── Dispositivos IoT
│   ├── Sensores
│   ├── Cámaras
│   └── Configuración
├── Alertas y Eventos
│   ├── Activas
│   ├── Historial
│   └── Protocolos
├── Reportes y Analytics
│   ├── Diarios
│   ├── Analytics
│   └── Exportación
├── Configuración
│   ├── Perfil
│   ├── Notificaciones
│   └── Seguridad
└── Soporte
    ├── Ayuda
    ├── Contacto
    └── Documentación
```

---

## 4. Flujos de Usuario (Wireframes Textuales)

### 4.1. Registro y Onboarding
```
Landing Page
    ↓
[Registrarse] → Selección de Tipo de Usuario
    ↓
Formulario de Registro
    ↓
Verificación de Email/Teléfono
    ↓
Configuración Inicial (según rol)
    ↓
Tutorial Interactivo
    ↓
Dashboard Principal
```

### 4.2. Alerta de Emergencia
```
Detección de Evento
    ↓
Clasificación Automática
    ↓
Activación de Protocolo
    ↓
Notificación a Cuidadores/Familia
    ↓
Dashboard de Respuesta
    ↓
Escalación si no hay respuesta
    ↓
Registro de Resolución
```

### 4.3. Gestión de Cuidadores
```
Lista de Cuidadores
    ↓
[Agregar Cuidador]
    ↓
Formulario de Registro
    ↓
Asignación de Roles y Disponibilidad
    ↓
Configuración de Protocolos
    ↓
Notificación y Activación
```

### 4.4. Configuración de Protocolos
```
Configuración de Protocolos
    ↓
Selección de Tipo de Evento
    ↓
Secuencia de Contactos y Acciones
    ↓
Prueba y Activación
```

---

## 5. Dashboards por Rol (Wireframes Textuales)

### 5.1. Familiar/Tutor
```
┌───────────────────────────────┐
│ 🏠 Panel Familiar             │
├───────────────────────────────┤
│ 👤 Nombre                     │
│ 📍 Estado: En casa            │
│ ⚡ Dispositivos: 3 activos    │
│ 🔔 Alertas: 0 pendientes      │
├───────────────────────────────┤
│ 📈 Actividad Reciente         │
│ 🚨 Protocolo Emergencia       │
│ 📱 Acciones Rápidas           │
└───────────────────────────────┘
```

### 5.2. Cuidador Profesional
```
┌───────────────────────────────┐
│ 👩‍⚕️ Panel Profesional        │
├───────────────────────────────┤
│ 👤 Nombre | 🏥 Institución     │
│ 📊 Pacientes: 8               │
│ 🔔 Alertas: 2 pendientes      │
├───────────────────────────────┤
│ 🚨 Alertas Prioritarias       │
│ 📋 Pacientes Asignados        │
│ 📊 Métricas del Turno         │
└───────────────────────────────┘
```

### 5.3. Cuidador Freelance
```
┌───────────────────────────────┐
│ 🆓 Panel Freelance            │
├───────────────────────────────┤
│ 👤 Nombre | Freelance         │
│ 📊 Clientes: 5                │
│ 💰 Ingresos mes: $2,400       │
├───────────────────────────────┤
│ 🏢 Instituciones/Clientes     │
│ 📅 Agenda Hoy                 │
│ 💰 Gestión Financiera         │
└───────────────────────────────┘
```

### 5.4. Admin Institución
```
┌───────────────────────────────┐
│ 🏢 Panel Institucional         │
├───────────────────────────────┤
│ 🏥 Institución | Admin         │
│ 📊 Pacientes: 45 | Cuidadores: 12 │
│ 🔔 Alertas: 5                  │
├───────────────────────────────┤
│ 📊 Métricas Operativas         │
│ 🚨 Alertas Institucionales     │
│ 👥 Gestión de Personal         │
│ 📈 Reportes y Analytics        │
└───────────────────────────────┘
```

---

## 6. Modales y Acciones Contextuales
- Confirmación de acciones críticas (ej: atender alerta, eliminar usuario)
- Edición rápida de datos (ej: horarios, protocolos)
- Visualización de detalles (ej: evento, paciente, dispositivo)
- Notificaciones emergentes (ej: alerta crítica, éxito, error)

---

## 7. Principios de Diseño Visual
- **Paleta**: Azul, púrpura, verde, naranja, rojo, neutros
- **Tipografía**: Inter, JetBrains Mono
- **Componentes**: Botones, tarjetas, tablas, modales, sidebar
- **Responsive**: Mobile first, breakpoints para tablet y desktop
- **Accesibilidad**: Alto contraste, texto grande, navegación por teclado

---

## 8. Roadmap Visual
- **MVP**: Dashboard familiar, alertas, registro, protocolos básicos
- **Fase 2**: Dashboard profesional, gestión de pacientes, reportes
- **Fase 3**: Dashboard institucional, métricas, compliance
- **Fase 4**: Freelance, multi-institución, facturación
- **Fase 5**: Personalización avanzada, integraciones externas

---

*Este documento se actualiza regularmente según la evolución del sistema y feedback de usuarios.* 