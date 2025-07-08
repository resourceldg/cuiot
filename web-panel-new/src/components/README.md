# 🏗️ Arquitectura Modular de Componentes - CUIOT

## 📋 Resumen

Este directorio contiene la arquitectura modular de componentes para el frontend de CUIOT, siguiendo los principios de componentización atómica y separación por roles.

## 📁 Estructura de Carpetas

```
src/components/
├── dashboard/
│   ├── admin/                    # Dashboard del Administrador del Sistema
│   │   ├── AdminDashboard.svelte # Componente principal del admin
│   │   ├── AdminKPIRow.svelte    # Fila de KPIs principales
│   │   ├── AdminNotificationsPanel.svelte # Panel de notificaciones
│   │   ├── AdminQuickActions.svelte # Acciones rápidas
│   │   ├── AdminSystemMetrics.svelte # Métricas del sistema
│   │   ├── AdminCriticalAlerts.svelte # Alertas críticas
│   │   └── AdminActivityChart.svelte # Gráfico de actividad
│   ├── family/                   # Dashboard de Familiar/Tutor (futuro)
│   ├── caregiver/                # Dashboard de Cuidador Profesional (futuro)
│   ├── self_cared/               # Dashboard de Autocuidado (futuro)
│   ├── institution_admin/        # Dashboard de Admin de Institución (futuro)
│   └── freelance/                # Dashboard de Cuidador Freelance (futuro)
└── shared/                       # Componentes compartidos
    └── ui/                       # Componentes UI base
        └── SectionHeader.svelte  # Encabezados de sección
```

## 🎯 Principios de Diseño

### 1. Componentización Atómica
- **Componentes Atómicos**: Botones, inputs, badges, avatares
- **Componentes Moleculares**: Tarjetas de métricas, tablas, listas
- **Componentes Organizadores**: Secciones de dashboard, paneles
- **Componentes de Página**: Dashboards completos por rol

### 2. Separación por Roles
- Cada rol tiene su propio directorio de componentes
- Los componentes específicos del rol no se comparten
- Los componentes compartidos están en `/shared`

### 3. Reutilización Máxima
- Los componentes UI base se reutilizan en todos los dashboards
- Las tablas, filtros y métricas son genéricas y configurables
- Los estilos y comportamientos son consistentes

## 🎨 Sistema de Diseño

### Variables CSS Globales
Todas las variables CSS están definidas en `src/app.css`:

```css
:root {
    /* Colores principales */
    --color-bg: #23272e;
    --color-accent: #00e676;
    --color-error: #ff4d6d;
    --color-success: #00e676;
    --color-warning: #f1c40f;
    
    /* Espaciado */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Border radius */
    --border-radius-sm: 4px;
    --border-radius: 8px;
    --border-radius-lg: 12px;
}
```

### Herencia de Estilos
- Todos los componentes heredan las variables CSS globales
- Los estilos específicos se definen en cada componente
- Se mantiene consistencia visual en toda la aplicación

## 🔧 Componentes del Dashboard Admin

### AdminDashboard.svelte
Componente principal que orquesta todos los subcomponentes del dashboard admin.

**Características:**
- Gestión de estados de carga y error
- Layout responsive
- Integración con todos los subcomponentes

### AdminKPIRow.svelte
Fila de KPIs principales con métricas clave del sistema.

**Métricas incluidas:**
- Paquetes activos
- Usuarios activos
- Instituciones
- Alertas críticas

### AdminNotificationsPanel.svelte
Panel de notificaciones recientes con acciones de gestión.

**Funcionalidades:**
- Lista de notificaciones
- Acciones: ver, marcar como leída, eliminar
- Filtrado por severidad

### AdminQuickActions.svelte
Acciones rápidas para navegación a secciones principales.

**Acciones incluidas:**
- Paquetes
- Usuarios
- Instituciones
- Dispositivos
- Reportes
- Configuración

### AdminSystemMetrics.svelte
Métricas detalladas del sistema en tiempo real.

**Categorías:**
- Rendimiento (CPU, RAM, Disco)
- Base de Datos (Conexiones, Queries/s)
- Disponibilidad (Uptime, Último down)
- Negocio (LTV, Churn)

### AdminCriticalAlerts.svelte
Panel de alertas críticas del sistema.

**Tipos de alertas:**
- Críticas (rojo)
- Advertencias (amarillo)
- Información (azul)

### AdminActivityChart.svelte
Gráfico de actividad del sistema con datos históricos.

**Datos mostrados:**
- Usuarios activos por día
- Dispositivos conectados
- Alertas generadas

## 🚀 Patrones de Desarrollo

### Crear un Nuevo Componente
1. Identificar la ubicación correcta (específico de rol o compartido)
2. Crear el archivo con nomenclatura PascalCase
3. Definir props claras y documentadas
4. Implementar manejo de errores y estados de carga
5. Agregar estilos responsivos

### Ejemplo de Estructura de Componente
```javascript
<script>
    // 1. Imports
    import Component from './Component.svelte';
    
    // 2. Props
    export let prop1 = '';
    export let prop2 = null;
    
    // 3. Variables reactivas
    $: computedValue = prop1 + prop2;
    
    // 4. Funciones
    function handleClick() {
        // lógica
    }
</script>

<!-- 5. Template -->
<div class="component">
    <!-- contenido -->
</div>

<!-- 6. Estilos -->
<style>
    .component {
        /* estilos usando variables CSS */
    }
</style>
```

## 📱 Responsive Design

Todos los componentes incluyen:
- Breakpoints para mobile (768px)
- Adaptaciones de layout
- Optimización de contenido para pantallas pequeñas

## 🔄 Estados de Componente

### Estados Comunes
- **Loading**: Estado de carga con spinner
- **Error**: Manejo de errores con mensajes claros
- **Empty**: Estado vacío con mensajes informativos
- **Success**: Confirmación de acciones exitosas

### Ejemplo de Implementación
```javascript
{#if loading}
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>Cargando...</p>
    </div>
{:else if error}
    <div class="error-container">
        <p>Error: {error}</p>
        <button on:click={retry}>Reintentar</button>
    </div>
{:else}
    <!-- contenido normal -->
{/if}
```

## 🎯 Best Practices

### 1. Nomenclatura
- **Componentes**: PascalCase (ej: `UserTable.svelte`)
- **Props**: camelCase (ej: `userName`)
- **Eventos**: camelCase (ej: `userSelected`)

### 2. Accesibilidad
- Uso de `aria-label` para elementos interactivos
- Navegación por teclado
- Contraste adecuado
- Textos alternativos para iconos

### 3. Performance
- Lazy loading de componentes pesados
- Optimización de re-renders
- Uso eficiente de stores

## 🔗 Integración con API

Los componentes se integran con la API a través de:
- Servicios en `src/lib/api/`
- Manejo de errores consistente
- Estados de carga apropiados

## 📈 Roadmap

### Fase 1: Dashboard Admin ✅
- [x] Estructura modular
- [x] Componentes principales
- [x] Sistema de diseño
- [x] Responsive design

### Fase 2: Otros Dashboards
- [ ] Dashboard de Familiar/Tutor
- [ ] Dashboard de Cuidador Profesional
- [ ] Dashboard de Autocuidado
- [ ] Dashboard de Admin de Institución
- [ ] Dashboard de Cuidador Freelance

### Fase 3: Componentes Avanzados
- [ ] Gráficos interactivos
- [ ] Formularios dinámicos
- [ ] Modales y overlays
- [ ] Drag & drop
- [ ] Notificaciones en tiempo real

---

*Esta arquitectura modular proporciona una base sólida para el desarrollo escalable y mantenible del frontend de CUIOT.* 