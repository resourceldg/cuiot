# 🎨 LAYOUT DEL DASHBOARD ADMIN - CUIOT

## 📐 **ESTRUCTURA VISUAL**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CUIOT ADMIN DASHBOARD                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔍 [Buscar]  📧 [Notificaciones]  👤 [Admin User]  ⚙️ [Config]  🚪 [Logout] │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │   📊 DASHBOARD  │  │   👥 USUARIOS   │  │  🏢 INSTITUCIONES│  │ 📦 PKGS │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │   MÉTRICAS  │ │  │ │   LISTADO   │ │  │ │   LISTADO   │ │  │ │LIST │ │ │
│  │ │   GLOBALES  │ │  │ │   USUARIOS  │ │  │ │ INSTITUCIONES│ │  │ │PKGS │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │   KPIs      │ │  │ │   CREAR     │ │  │ │   CREAR     │ │  │ │CREAR│ │ │
│  │ │ PRINCIPALES │ │  │ │   USUARIO   │ │  │ │ INSTITUCIÓN │ │  │ │ PKG │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │   ALERTAS   │ │  │ │   ROLES     │ │  │ │   MÉTRICAS  │ │  │ │ANALY│ │ │
│  │ │   CRÍTICAS  │ │  │ │   Y PERMISOS│ │  │ │ ESPECÍFICAS │ │  │ │ PKGS│ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────┘ │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │   📱 DISPOSITIVOS│  │   🚨 ALERTAS    │  │   📈 REPORTES   │  │ ⚙️ CONFIG│ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │  INVENTARIO │ │  │ │ CONFIGURACIÓN│ │  │ │   USUARIOS  │ │  │ │SIST │ │ │
│  │ │ DISPOSITIVOS│ │  │ │   GLOBAL    │ │  │ │             │ │  │ │     │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │ CONFIGURACIÓN│ │  │ │  REGLAS DE  │ │  │ │   NEGOCIO   │ │  │ │SEGUR│ │ │
│  │ │ DISPOSITIVOS│ │  │ │ ESCALACIÓN  │ │  │ │             │ │  │ │     │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │ MONITOREO   │ │  │ │ MONITOREO   │ │  │ │   TÉCNICOS  │ │  │ │AUDIT│ │ │
│  │ │ TIEMPO REAL │ │  │ │ DE ALERTAS  │ │  │ │             │ │  │ │     │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────┘ │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │   🔒 SEGURIDAD  │  │   💰 FACTURACIÓN│  │   📞 SOPORTE    │  │ 📋 LOGS │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │   LOGS DE   │ │  │ │   GESTIÓN   │ │  │ │   SOPORTE   │ │  │ │AUDIT│ │ │
│  │ │  AUDITORÍA  │ │  │ │ FACTURACIÓN │ │  │ │   TÉCNICO   │ │  │ │     │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │ MONITOREO   │ │  │ │  REPORTES   │ │  │ │   ESCALACIÓN│ │  │ │SYSTEM│ │ │
│  │ │  SEGURIDAD  │ │  │ │ FINANCIEROS │ │  │ │             │ │  │ │      │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────┐ │ │
│  │ │ BACKUP Y    │ │  │ │  GESTIÓN    │ │  │ │   CAPACITACIÓN│ │  │ │ERROR│ │ │
│  │ │ RECUPERACIÓN│ │  │ │   PAGOS     │ │  │ │             │ │  │ │     │ │ │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────┘ │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🧭 **NAVEGACIÓN PRINCIPAL**

### **Menú Lateral (Sidebar)**
```
┌─────────────────────────────────────┐
│           CUIOT ADMIN               │
├─────────────────────────────────────┤
│ 📊 Dashboard Global                 │
│ 👥 Gestión de Usuarios             │
│ 🏢 Gestión de Instituciones        │
│ 📦 Gestión de Paquetes             │
│ 📱 Gestión de Dispositivos         │
│ 🚨 Sistema de Alertas              │
│ 📈 Reportes y Analytics            │
│ ⚙️ Configuración del Sistema       │
│ 🔒 Seguridad y Auditoría           │
│ 💰 Facturación y Finanzas          │
│ 📞 Soporte y Contacto              │
└─────────────────────────────────────┘
```

## 📊 **DASHBOARD GLOBAL - LAYOUT DETALLADO**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DASHBOARD GLOBAL                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │   👥 USUARIOS   │  │  📱 DISPOSITIVOS│  │   🚨 ALERTAS    │  │ 💰 INGR │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │    Total: 1,247 │  │   Activos: 892  │  │  Pendientes: 23 │  │ $45,230 │ │
│  │   Activos: 1,180│  │   Offline: 45   │  │   Críticas: 5   │  │  +12.5% │ │
│  │   Nuevos: +67   │  │   Error: 12     │  │   Resueltas: 18 │  │  vs mes │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           GRÁFICO DE ACTIVIDAD                          │ │
│  │                                                                         │ │
│  │  📈 Usuarios Activos por Día (Últimos 30 días)                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                                                                     │ │ │
│  │  │  ████████████████████████████████████████████████████████████████  │ │ │
│  │  │                                                                     │ │ │
│  │  └─────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │   ⚡ RENDIMIENTO│  │   🗄️ BASE DATOS │  │   🌐 UPTIME     │  │ 📊 KPIs │ │
│  │                 │  │                 │  │                 │  │         │ │
│  │   CPU: 45%      │  │   Conexiones:   │  │   99.98%        │  │   LTV:  │ │
│  │   RAM: 67%      │  │   1,234        │  │   Último down:   │  │  $2,450 │ │
│  │   Disco: 23%    │  │   Queries/s:    │  │   2 días        │  │   Churn:│ │
│  │                 │  │   1,567        │  │                 │  │   3.2%  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           ALERTAS CRÍTICAS                             │ │
│  │                                                                         │ │
│  │  🔴 [CRÍTICO] Dispositivo IoT offline - ID: DEV-001                     │ │
│  │  🟡 [ADVERTENCIA] Base de datos lenta - 2.3s avg response              │ │
│  │  🟢 [INFO] Backup completado exitosamente                              │ │
│  │  🔴 [CRÍTICO] Intento de acceso no autorizado - IP: 192.168.1.100      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 👥 **GESTIÓN DE USUARIOS - LAYOUT**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GESTIÓN DE USUARIOS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  🔍 [Buscar usuarios...]  📊 [Filtros]  ➕ [Crear Usuario]  📥 [Exportar] │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  FILTROS: [Rol: Todos ▼] [Estado: Activo ▼] [Institución: Todas ▼]     │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  TABLA DE USUARIOS                                                      │ │
│  │                                                                         │ │
│  │  ┌─────┬─────────────┬─────────────┬─────────┬─────────┬─────────┬─────┐ │ │
│  │  │ SEL │    NOMBRE   │    EMAIL    │   ROL   │ ESTADO  │ ÚLTIMO  │ ACC │ │ │
│  │  │     │             │             │         │         │ ACCESO  │     │ │ │
│  │  ├─────┼─────────────┼─────────────┼─────────┼─────────┼─────────┼─────┤ │ │
│  │  │ ☑️  │ Juan Pérez  │ juan@...    │ Admin   │ Activo  │ 2h ago  │ ⚙️  │ │ │
│  │  │ ☑️  │ María López │ maria@...   │ Family  │ Activo  │ 1d ago  │ ⚙️  │ │ │
│  │  │ ☑️  │ Carlos Ruiz │ carlos@...  │ Careg.  │ Inactivo│ 5d ago  │ ⚙️  │ │ │
│  │  │ ☑️  │ Ana García  │ ana@...     │ Self    │ Activo  │ 30m ago │ ⚙️  │ │ │
│  │  └─────┴─────────────┴─────────────┴─────────┴─────────┴─────────┴─────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  ACCIONES MASIVAS: [Activar] [Desactivar] [Cambiar Rol] [Enviar Email]  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  📄 Página 1 de 25 | Mostrando 1-10 de 247 usuarios                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🏢 **GESTIÓN DE INSTITUCIONES - LAYOUT**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GESTIÓN DE INSTITUCIONES                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  🔍 [Buscar instituciones...]  ➕ [Crear Institución]  📥 [Exportar]     │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  FILTROS: [Tipo: Todos ▼] [Estado: Activo ▼] [Rating: Todos ▼]         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  TABLA DE INSTITUCIONES                                                 │ │
│  │                                                                         │ │
│  │  ┌─────┬─────────────┬─────────────┬─────────┬─────────┬─────────┬─────┐ │ │
│  │  │ SEL │    NOMBRE   │     TIPO    │ USUARIOS│ RATING  │ FACTURA │ ACC │ │ │
│  │  │     │             │             │         │         │         │     │ │ │
│  │  ├─────┼─────────────┼─────────────┼─────────┼─────────┼─────────┼─────┤ │ │
│  │  │ ☑️  │ Hosp. San   │ Hospital    │   45    │ ⭐⭐⭐⭐⭐ │ $12,450 │ ⚙️  │ │ │
│  │  │ ☑️  │ Res. Golden │ Residencia  │   23    │ ⭐⭐⭐⭐  │ $8,230  │ ⚙️  │ │ │
│  │  │ ☑️  │ Clin. Vida  │ Clínica     │   67    │ ⭐⭐⭐⭐⭐ │ $15,670 │ ⚙️  │ │ │
│  │  └─────┴─────────────┴─────────────┴─────────┴─────────┴─────────┴─────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  MÉTRICAS POR INSTITUCIÓN                                               │ │
│  │                                                                         │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────┐ │ │
│  │  │   Total Inst.   │  │   Activas       │  │   Ingresos      │  │Rating│ │ │
│  │  │                 │  │                 │  │                 │  │      │ │ │
│  │  │       45        │  │       42        │  │    $156,230     │  │ 4.7  │ │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📦 **GESTIÓN DE PAQUETES - LAYOUT**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GESTIÓN DE PAQUETES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  ➕ [Crear Paquete]  📊 [Analytics]  📥 [Exportar]  ⚙️ [Configuración]   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PAQUETES DISPONIBLES                                                   │ │
│  │                                                                         │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────┐ │ │
│  │  │   🏥 BÁSICO     │  │   🏥 PREMIUM    │  │   🏥 ENTERPRISE │  │➕CUS│ │ │
│  │  │                 │  │                 │  │                 │  │     │ │ │
│  │  │   $29/mes       │  │   $79/mes       │  │   $199/mes      │  │     │ │ │
│  │  │   5 usuarios    │  │   20 usuarios   │  │   Ilimitado     │  │     │ │ │
│  │  │   Monitoreo     │  │   + Alertas     │  │   + Analytics   │  │     │ │ │
│  │  │   básico        │  │   + Reportes    │  │   + API         │  │     │ │ │
│  │  │   234 susc.     │  │   156 susc.     │  │   89 susc.      │  │     │ │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  ANALYTICS DE PAQUETES                                                  │ │
│  │                                                                         │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────┐ │ │
│  │  │   Ingresos      │  │   Suscripciones │  │   Cancelaciones │  │Satisf│ │
│  │  │   Mensuales     │  │   Nuevas        │  │   Mensuales     │  │      │ │ │
│  │  │                 │  │                 │  │                 │  │      │ │ │
│  │  │   $45,230       │  │   +67           │  │   -12           │  │ 4.8  │ │ │
│  │  │   +15.3%        │  │   +23%          │  │   -5%           │  │ ⭐⭐⭐⭐⭐│ │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🎨 **PALETA DE COLORES Y ESTILOS**

### **Colores Principales:**
- **Primario:** `#2563eb` (Azul CUIOT)
- **Secundario:** `#7c3aed` (Púrpura)
- **Éxito:** `#059669` (Verde)
- **Advertencia:** `#d97706` (Naranja)
- **Error:** `#dc2626` (Rojo)
- **Info:** `#0891b2` (Cian)

### **Estados:**
- **Activo:** `#059669` (Verde)
- **Inactivo:** `#6b7280` (Gris)
- **Pendiente:** `#d97706` (Naranja)
- **Error:** `#dc2626` (Rojo)
- **Crítico:** `#dc2626` (Rojo intenso)

### **Tipografía:**
- **Títulos:** Inter Bold, 24px
- **Subtítulos:** Inter SemiBold, 18px
- **Texto:** Inter Regular, 14px
- **Captions:** Inter Light, 12px

### **Espaciado:**
- **Padding:** 16px, 24px, 32px
- **Margin:** 8px, 16px, 24px
- **Border Radius:** 8px, 12px, 16px

---

## 📱 **RESPONSIVE DESIGN**

### **Breakpoints:**
- **Desktop:** 1200px+
- **Tablet:** 768px - 1199px
- **Mobile:** 320px - 767px

### **Adaptaciones:**
- **Sidebar:** Colapsable en tablet/mobile
- **Tablas:** Scroll horizontal en mobile
- **Cards:** Stack vertical en mobile
- **Filtros:** Dropdown en mobile

---

*Este layout proporciona una base sólida para el dashboard del administrador del sistema, con una navegación intuitiva y todas las funcionalidades necesarias para la gestión completa de CUIOT.* 