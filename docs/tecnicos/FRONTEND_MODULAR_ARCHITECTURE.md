# 🏗️ ARQUITECTURA MODULAR DEL FRONTEND CUIOT

## 📋 **RESUMEN EJECUTIVO**

La arquitectura modular del frontend de CUIOT está diseñada para maximizar la reutilización de componentes, facilitar el mantenimiento y permitir el desarrollo paralelo de diferentes dashboards por rol. Cada rol tiene su propio conjunto de componentes específicos, mientras que los componentes compartidos se reutilizan en toda la aplicación.

---

## 🎯 **PRINCIPIOS DE DISEÑO**

### **1. Componentización Atómica**
- **Componentes Atómicos**: Botones, inputs, badges, avatares
- **Componentes Moleculares**: Tarjetas de métricas, tablas, listas
- **Componentes Organizadores**: Secciones de dashboard, paneles
- **Componentes de Página**: Dashboards completos por rol

### **2. Separación por Roles**
- Cada rol tiene su propio directorio de componentes
- Los componentes específicos del rol no se comparten
- Los componentes compartidos están en `/shared`

### **3. Reutilización Máxima**
- Los componentes UI base se reutilizan en todos los dashboards
- Las tablas, filtros y métricas son genéricas y configurables
- Los estilos y comportamientos son consistentes

---

## 📁 **ESTRUCTURA DE CARPETAS**

```
src/
├── components/
│   ├── dashboard/
│   │   ├── admin/                    # Dashboard del Administrador del Sistema
│   │   │   ├── AdminDashboard.svelte # Componente principal del admin
│   │   │   ├── UserTable.svelte      # Tabla de usuarios
│   │   │   ├── InstitutionTable.svelte
│   │   │   ├── PackageGrid.svelte
│   │   │   ├── DeviceTable.svelte
│   │   │   ├── AlertList.svelte
│   │   │   ├── ReportCards.svelte
│   │   │   ├── BillingCards.svelte
│   │   │   ├── SecurityPanel.svelte
│   │   │   └── SettingsPanel.svelte
│   │   ├── family/                   # Dashboard de Familiar/Tutor
│   │   │   ├── FamilyDashboard.svelte
│   │   │   ├── CaredPersonList.svelte
│   │   │   ├── AlertCenter.svelte
│   │   │   └── CommunicationHub.svelte
│   │   ├── caregiver/                # Dashboard de Cuidador Profesional
│   │   │   ├── CaregiverDashboard.svelte
│   │   │   ├── PatientList.svelte
│   │   │   ├── ScheduleManager.svelte
│   │   │   └── CareReport.svelte
│   │   ├── self_cared/               # Dashboard de Autocuidado
│   │   │   ├── SelfCaredDashboard.svelte
│   │   │   ├── HealthMonitor.svelte
│   │   │   ├── DeviceControl.svelte
│   │   │   └── EmergencyPanel.svelte
│   │   ├── institution_admin/        # Dashboard de Admin de Institución
│   │   │   ├── InstitutionAdminDashboard.svelte
│   │   │   ├── StaffManager.svelte
│   │   │   ├── ResourceAllocation.svelte
│   │   │   └── InstitutionReports.svelte
│   │   └── freelance/                # Dashboard de Cuidador Freelance
│   │       ├── FreelanceDashboard.svelte
│   │       ├── ClientManager.svelte
│   │       ├── SchedulePlanner.svelte
│   │       └── FinancialTracker.svelte
│   ├── shared/                       # Componentes compartidos
│   │   ├── ui/                       # Componentes UI base
│   │   │   ├── MetricCard.svelte     # Tarjetas de métricas
│   │   │   ├── SectionHeader.svelte  # Encabezados de sección
│   │   │   ├── FilterBar.svelte      # Barras de filtros
│   │   │   ├── Button.svelte         # Botones
│   │   │   ├── Input.svelte          # Campos de entrada
│   │   │   ├── Modal.svelte          # Modales
│   │   │   └── Toast.svelte          # Notificaciones
│   │   ├── tables/                   # Componentes de tablas
│   │   │   ├── DataTable.svelte      # Tabla de datos genérica
│   │   │   ├── Pagination.svelte     # Paginación
│   │   │   └── SortableHeader.svelte # Encabezados ordenables
│   │   ├── charts/                   # Componentes de gráficos
│   │   │   ├── LineChart.svelte      # Gráfico de líneas
│   │   │   ├── BarChart.svelte       # Gráfico de barras
│   │   │   ├── PieChart.svelte       # Gráfico circular
│   │   │   └── MetricChart.svelte    # Gráfico de métricas
│   │   └── forms/                    # Componentes de formularios
│   │       ├── FormField.svelte      # Campo de formulario
│   │       ├── FormSection.svelte    # Sección de formulario
│   │       └── FormActions.svelte    # Acciones de formulario
│   └── ProtectedRoute.svelte         # Componente de protección de rutas
├── routes/
│   └── dashboard/
│       ├── admin/                    # Rutas del admin
│       │   └── +page.svelte          # Página principal del admin
│       ├── family/                   # Rutas del familiar
│       │   └── +page.svelte
│       ├── caregiver/                # Rutas del cuidador
│       │   └── +page.svelte
│       ├── self-cared/               # Rutas de autocuidado
│       │   └── +page.svelte
│       ├── institution-admin/        # Rutas del admin de institución
│       │   └── +page.svelte
│       └── freelance/                # Rutas del cuidador freelance
│           └── +page.svelte
└── lib/
    ├── roles.js                      # Definición de roles
    ├── api.js                        # Servicios de API
    └── stores.js                     # Stores de Svelte
```

---

## 🔧 **COMPONENTES COMPARTIDOS**

### **1. MetricCard.svelte**
```javascript
// Props
export let title = '';           // Título de la métrica
export let value = '';           // Valor principal
export let subtitle = '';        // Subtítulo/descripción
export let icon = '';            // Icono (emoji o componente)
export let trend = null;         // { value: '+12%', type: 'positive' }
export let color = 'blue';       // blue, green, red, orange, purple, gray
export let size = 'medium';      // small, medium, large
```

### **2. SectionHeader.svelte**
```javascript
// Props
export let title = '';           // Título de la sección
export let subtitle = '';        // Subtítulo
export let icon = '';            // Icono
export let actions = [];         // Array de acciones
// actions: [{ label, icon, action, variant }]
```

### **3. FilterBar.svelte**
```javascript
// Props
export let filters = [];         // Array de filtros
export let searchPlaceholder = 'Buscar...';
export let showSearch = true;
export let showExport = false;

// Events
on:filterChange = (event) => { key, value }
on:search = (event) => { value }
on:export = (event) => {}
```

### **4. DataTable.svelte**
```javascript
// Props
export let columns = [];         // Definición de columnas
export let data = [];            // Datos de la tabla
export let loading = false;      // Estado de carga
export let selectable = false;   // Selección múltiple
export let sortable = true;      // Ordenamiento
export let pagination = true;    // Paginación

// Events
on:sort = (event) => { column, direction }
on:pageChange = (event) => { page }
on:selectionChange = (event) => { selectedItems }
on:action = (event) => { action, item }
```

---

## 🎨 **CONTRATOS DE COMPONENTES**

### **Definición de Columnas (DataTable)**
```javascript
const columns = [
    {
        key: 'name',              // Clave del campo
        label: 'Nombre',          // Etiqueta visible
        sortable: true,           // Permite ordenamiento
        width: '200px',           // Ancho de columna (opcional)
        render: (value, item) => `<span class="badge">${value}</span>` // Renderizado personalizado
    }
];
```

### **Definición de Filtros (FilterBar)**
```javascript
const filters = [
    {
        key: 'status',            // Clave del filtro
        label: 'Estado',          // Etiqueta
        type: 'select',           // Tipo: select, date, checkbox
        options: [                // Opciones para select
            { value: 'active', label: 'Activo' },
            { value: 'inactive', label: 'Inactivo' }
        ]
    }
];
```

### **Definición de Acciones (SectionHeader)**
```javascript
const actions = [
    {
        label: 'Nuevo Usuario',   // Texto del botón
        icon: '➕',               // Icono
        action: createUser,       // Función a ejecutar
        variant: 'primary'        // Variante: primary, secondary, danger
    }
];
```

---

## 🚀 **PATRONES DE DESARROLLO**

### **1. Crear un Nuevo Dashboard de Rol**

```javascript
// 1. Crear el directorio del rol
mkdir src/components/dashboard/nuevo_rol

// 2. Crear el dashboard principal
// src/components/dashboard/nuevo_rol/NuevoRolDashboard.svelte
<script>
    import MetricCard from '../../shared/ui/MetricCard.svelte';
    import SectionHeader from '../../shared/ui/SectionHeader.svelte';
    import DataTable from '../../shared/tables/DataTable.svelte';
    
    // Lógica específica del rol
</script>

// 3. Crear la página de ruta
// src/routes/dashboard/nuevo-rol/+page.svelte
<script>
    import ProtectedRoute from '../../../components/ProtectedRoute.svelte';
    import NuevoRolDashboard from '../../../components/dashboard/nuevo_rol/NuevoRolDashboard.svelte';
</script>

<ProtectedRoute permission="nuevo_rol.read">
    <NuevoRolDashboard />
</ProtectedRoute>
```

### **2. Crear un Nuevo Componente Compartido**

```javascript
// 1. Identificar la ubicación correcta
// src/components/shared/ui/NuevoComponente.svelte

// 2. Definir props claras
<script>
    export let prop1 = '';
    export let prop2 = null;
    export let prop3 = false;
</script>

// 3. Emitir eventos cuando sea necesario
const dispatch = createEventDispatcher();
dispatch('eventName', { data: 'value' });

// 4. Documentar el uso
// Agregar comentarios JSDoc
```

### **3. Extender un Componente Existente**

```javascript
// En lugar de modificar el componente base, crear una variante
// src/components/dashboard/admin/UserTableExtended.svelte
<script>
    import DataTable from '../../shared/tables/DataTable.svelte';
    
    // Configuración específica para usuarios
    const userColumns = [
        // ... columnas específicas
    ];
</script>

<DataTable 
    columns={userColumns}
    data={users}
    // ... otras props
/>
```

---

## 📊 **ESTADOS Y GESTIÓN DE DATOS**

### **1. Estados Locales**
```javascript
// Cada componente maneja su propio estado
let loading = false;
let data = [];
let error = null;
let filters = {};
```

### **2. Comunicación entre Componentes**
```javascript
// Usar eventos de Svelte
const dispatch = createEventDispatcher();

// Emitir evento
dispatch('dataLoaded', { data });

// Escuchar evento
<ChildComponent on:dataLoaded={handleDataLoaded} />
```

### **3. Stores Globales**
```javascript
// src/lib/stores.js
import { writable } from 'svelte/store';

export const userStore = writable(null);
export const notificationStore = writable([]);
export const themeStore = writable('light');
```

---

## 🎯 **BEST PRACTICES**

### **1. Nomenclatura**
- **Componentes**: PascalCase (ej: `UserTable.svelte`)
- **Archivos**: kebab-case (ej: `user-table.svelte`)
- **Props**: camelCase (ej: `userName`)
- **Eventos**: camelCase (ej: `userSelected`)

### **2. Estructura de Componentes**
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
        /* estilos */
    }
</style>
```

### **3. Manejo de Errores**
```javascript
// Siempre incluir manejo de errores
{#if error}
    <div class="error-banner">
        <p>{error}</p>
    </div>
{:else if loading}
    <div class="loading">
        <p>Cargando...</p>
    </div>
{:else}
    <!-- contenido normal -->
{/if}
```

### **4. Responsive Design**
```javascript
// Usar clases de Tailwind para responsive
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- contenido -->
</div>
```

---

## 🔄 **FLUJO DE DESARROLLO**

### **1. Desarrollo de Nuevas Funcionalidades**
1. **Identificar** si es específico de un rol o compartido
2. **Crear** el componente en la ubicación correcta
3. **Implementar** la funcionalidad usando componentes base
4. **Probar** en diferentes contextos
5. **Documentar** el uso y props

### **2. Refactoring**
1. **Identificar** código duplicado
2. **Extraer** a componente compartido
3. **Actualizar** referencias
4. **Probar** que todo funcione
5. **Documentar** cambios

### **3. Mantenimiento**
1. **Revisar** componentes regularmente
2. **Actualizar** dependencias
3. **Optimizar** rendimiento
4. **Mejorar** accesibilidad
5. **Actualizar** documentación

---

## 📈 **MÉTRICAS Y MONITOREO**

### **1. Métricas de Calidad**
- **Reutilización**: Porcentaje de componentes compartidos
- **Cohesión**: Componentes con responsabilidades claras
- **Acoplamiento**: Dependencias entre componentes
- **Mantenibilidad**: Facilidad de modificación

### **2. Métricas de Rendimiento**
- **Tiempo de carga**: Componentes individuales
- **Bundle size**: Tamaño del bundle final
- **Re-renders**: Frecuencia de re-renderizados
- **Memory usage**: Uso de memoria

---

## 🚀 **ROADMAP**

### **Fase 1: Base Modular (Completada)**
- ✅ Estructura de carpetas
- ✅ Componentes base compartidos
- ✅ Dashboard del Admin
- ✅ Documentación inicial

### **Fase 2: Dashboards por Rol**
- 🔄 Dashboard de Familiar/Tutor
- ⏳ Dashboard de Cuidador Profesional
- ⏳ Dashboard de Autocuidado
- ⏳ Dashboard de Admin de Institución
- ⏳ Dashboard de Cuidador Freelance

### **Fase 3: Componentes Avanzados**
- ⏳ Gráficos interactivos
- ⏳ Formularios dinámicos
- ⏳ Modales y overlays
- ⏳ Drag & drop
- ⏳ Notificaciones en tiempo real

### **Fase 4: Optimización**
- ⏳ Lazy loading de componentes
- ⏳ Code splitting por rol
- ⏳ Caching inteligente
- ⏳ PWA features
- ⏳ Testing automatizado

---

*Esta arquitectura modular proporciona una base sólida para el desarrollo escalable y mantenible del frontend de CUIOT, permitiendo que múltiples equipos trabajen en paralelo en diferentes dashboards mientras mantienen la consistencia y reutilización de componentes.* 