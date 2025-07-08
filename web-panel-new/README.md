# Frontend Style Architecture — SysAdmin Dashboard

## 🎨 Principios de Diseño
- **Consistencia visual:** Fondo gris semi claro verdoso (`#232a27`) en todo el dashboard.
- **Separación visual:** Líneas divisorias/bordes sutiles en gris más claro, sin cajas flotantes ni sombras innecesarias.
- **Acentos:** Verde profesional (`#00e676`) para métricas, iconos activos y detalles.
- **Tipografía:** Sans-serif moderna, tamaños y pesos definidos en variables CSS.
- **Accesibilidad:** Contraste alto, foco visible, tamaños legibles.

## 🧩 Variables CSS Globales
Definidas en `src/app.css`:
```css
:root {
  --color-bg: #232a27;
  --color-bg-card: #262e2a;
  --color-bg-sidebar: #232a27;
  --color-bg-header: #232a27;
  --color-bg-hover: #27302b;
  --color-border: #2e3531;
  --color-accent: #00e676;
  --color-danger: #ff4d6d;
  --color-success: #00e676;
  --color-warning: #f1c40f;
  --color-text: #f3f6fa;
  --color-text-secondary: #b0b8c9;
}
```

## 🗂️ Estructura de Componentes Base
Todos los componentes visuales viven en `src/lib/ui/` y heredan los estilos globales:

### UI General
- `Button.svelte` — Botón reutilizable (primary, secondary, danger, icon).
- `Input.svelte` — Campo de texto accesible.
- `Select.svelte` — Dropdown estilizado.
- `Textarea.svelte` — Área de texto.
- `Checkbox.svelte` / `Switch.svelte` — Toggle y checks.
- `Card.svelte` — Contenedor plano, border y padding personalizables.
- `Modal.svelte` — Diálogo modal reutilizable.
- `Toast.svelte` — Notificaciones flotantes.
- `Tooltip.svelte` — Ayuda contextual.

### Layout y navegación
- `SidebarNav.svelte` — Menú lateral con slots para ítems.
- `Topbar.svelte` — Cabecera superior.
- `SectionHeader.svelte` — Título de sección con icono/acento.
- `Grid.svelte` — Layout de grilla responsiva.
- `PageContainer.svelte` — Wrapper para páginas.

### Tablas y datos
- `DataTable.svelte` — Tabla profesional, sorting, paginación, etc.
- `MetricCard.svelte` — Card de métrica con icono, valor, tendencia.
- `StatusBadge.svelte` — Etiqueta de estado (success, warning, danger).

### Gráficos y monitoreo
- `Chart.svelte` — Wrapper para gráficos (línea, barra, área, donut, etc.), usando SVG puro o una librería ligera (ej: Chart.js, ApexCharts, pero estilizado con nuestras variables).
- `MonitorPanel.svelte` — Panel de monitoreo en tiempo real (con slots para widgets).
- `Gauge.svelte` — Medidor tipo velocímetro.
- `Sparkline.svelte` — Mini-gráficos de tendencia.

### Otros
- `Avatar.svelte` — Foto o iniciales de usuario.
- `Icon.svelte` — SVG inline reutilizable.
- `Loader.svelte` — Spinner o barra de carga.

### Estructura de carpetas sugerida
```
src/
  lib/
    ui/
      Button.svelte
      Input.svelte
      Select.svelte
      Card.svelte
      DataTable.svelte
      Chart.svelte
      MetricCard.svelte
      SidebarNav.svelte
      Topbar.svelte
      SectionHeader.svelte
      Toast.svelte
      Modal.svelte
      ...
    icons/
      UserIcon.svelte
      AlertIcon.svelte
      ...
```

## 📦 Ejemplo de Uso
```svelte
<script>
  import Button from '$lib/ui/Button.svelte';
  import Card from '$lib/ui/Card.svelte';
  import Input from '$lib/ui/Input.svelte';
  import Chart from '$lib/ui/Chart.svelte';
</script>
<Card>
  <SectionHeader title="Monitoreo de ventas" />
  <Chart type="line" data={data} color="var(--color-accent)" />
  <Input placeholder="Buscar..." />
  <Button>Agregar</Button>
</Card>
```

## 📊 Guía de estilos para gráficos y monitoreo
- **Colores:** Verde acento para líneas/áreas principales, transparencias para áreas bajo curvas, ejes y líneas de referencia en gris sutil.
- **Animaciones:** Suaves, no distractoras.
- **Responsividad:** Gráficos y paneles deben adaptarse a distintos tamaños de pantalla.
- **Accesibilidad:** Contraste alto, tooltips descriptivos, focus visible.

## 🧑‍💻 Principios de Componentización
- **Herencia de estilos:** Todos los componentes usan variables CSS globales.
- **Props para customización:** Padding, border, color, etc. se pasan como props.
- **Nada de estilos hardcodeados ni colores fuera de la paleta.**
- **Nada de icon libraries ni frameworks de CSS externos.**
- **Solo SVG inline y CSS puro.**

## 📐 Layout y Separación
- **Sidebar:** Ancho fijo, fondo igual al general, `border-right` sutil.
- **Header:** Fondo igual al general, `border-bottom` sutil.
- **Cards/secciones:** Fondo igual al general, `border` sutil si se requiere separación.
- **Hover/activo:** Fondo gris apenas más claro, color/acento solo en icono/texto.

## 🚦 Accesibilidad y Responsividad
- Contraste alto en todos los elementos.
- Focus visible en botones, inputs, links.
- Layout responsivo con media queries.

---

Este README es la guía de referencia para todo el equipo de frontend. Cualquier nuevo componente o sección debe seguir estos principios y reutilizar los estilos y componentes base. Si necesitas un nuevo componente, primero agrégalo aquí y define su estilo y props antes de implementarlo.
