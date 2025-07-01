# Frontend - Sistema Integral de Monitoreo

## Arquitectura General

- **Framework:** SvelteKit
- **Estilos:** Tailwind CSS + estilos personalizados
- **Estructura modular:**
  - `components/`: Componentes reutilizables (formularios, cards, drawer, toast, etc.)
  - `routes/`: Rutas y páginas principales (dashboard, login, register, etc.)
  - `lib/`: Servicios de API y utilidades

## Flujos críticos cubiertos
- ABM de personas bajo cuidado, eventos y dispositivos.
- Drawer lateral inteligente con polling y feedback visual.
- Sincronización de estados activo/inactivo y soft delete.
- Sistema de notificaciones, toast y banners de error/success.
- Gestión de sesión y expiración con feedback visual.
- Visualización de alertas críticas y sistema de "semáforo" de estado.

## Decisiones de UX
- Diseño moderno, responsivo y accesible.
- Feedback visual inmediato tras cada acción.
- Prioridad visual para alertas críticas y advertencias.
- Validaciones en tiempo real en formularios.

## Recomendaciones para tests automáticos
- **Actualmente no hay tests automáticos.**
- Se recomienda agregar tests de integración y UI con Playwright, Cypress o Vitest + Testing Library.
- Priorizar tests para:
  - ABM de personas bajo cuidado y eventos
  - Sincronización de estados y feedback visual
  - Gestión de sesión y drawer

## Extensión y buenas prácticas
- Documentar props, eventos y lógica interna en componentes.
- Mantener la separación de lógica de negocio en servicios (`lib/api.js`).
- Usar stores para estado global y sincronización.
- Seguir patrones de diseño accesible y responsivo. 