# Mapa de Vistas y Componentes: Dashboard & Overview Sysadmin

## 1. Dashboard Admin (Panel Principal)
### Secciones y Componentes
- **KPIs Principales**
  - Paquetes activos, Usuarios activos, Instituciones, Alertas críticas
  - Acciones CRUD: Ver detalle, posiblemente crear/editar desde modals
  - Modals: Detalle de KPI (opcional)
- **Alertas Críticas**
  - Lista de alertas recientes y severas
  - Acciones CRUD: Ver detalle, marcar como resuelta, eliminar
  - Modals: Detalle de alerta, Confirmar resolución/eliminación
- **Gestión Rápida**
  - Accesos directos a CRUD de entidades clave (usuarios, paquetes, instituciones, dispositivos)
  - Acciones CRUD: Crear/editar/consultar entidades
  - Modals: Crear/editar usuario, paquete, institución, dispositivo
- **Notificaciones Recientes**
  - Tabla/lista de notificaciones del sistema
  - Acciones CRUD: Ver detalle, marcar como leída, eliminar
  - Modals: Detalle de notificación
- **Actividad del Sistema (Gráfico)**
  - Gráfico de actividad de usuarios/dispositivos/alertas
  - Acciones: Ver detalle de actividad (opcional)
  - Modals: Detalle de evento/actividad (opcional)

---

## 2. Overview (Monitoreo y Estado del Sistema)
### Secciones y Componentes
- **Métricas del Sistema**
  - CPU, RAM, Disco, Uptime, Conexiones, etc.
  - Acciones: Ver histórico, ver detalle (opcional)
  - Modals: Detalle de métrica (opcional)
- **Estado de Dispositivos**
  - Lista de dispositivos IoT y su estado
  - Acciones CRUD: Ver detalle, editar, eliminar, reiniciar dispositivo
  - Modals: Detalle de dispositivo, Confirmar acción
- **Resumen de Alertas y Eventos**
  - Estadísticas y gráficos de alertas/eventos recientes
  - Acciones: Ver detalle, filtrar por tipo/severidad
  - Modals: Detalle de alerta/evento

---

## Tabla Resumen de CRUD y Modals por Sección

| Sección                | Datos Principales         | CRUD Necesario         | Modals/Flyouts Necesarios         |
|------------------------|--------------------------|------------------------|-----------------------------------|
| KPIs                   | Conteos entidades        | Ver detalle            | Detalle KPI (opcional)            |
| Alertas Críticas       | Lista alertas            | Ver, resolver, eliminar| Detalle alerta, Confirmar acción  |
| Gestión Rápida         | Accesos CRUD             | Crear, editar, eliminar| Crear/editar entidad              |
| Notificaciones         | Lista notificaciones     | Ver, marcar, eliminar  | Detalle notificación              |
| Actividad (Gráfico)    | Series de actividad      | Ver detalle (opcional) | Detalle evento/actividad          |
| Métricas del Sistema   | Stats recursos           | Ver histórico          | Detalle métrica (opcional)        |
| Estado Dispositivos    | Lista dispositivos       | Ver, editar, eliminar  | Detalle dispositivo, Confirmar     |
| Resumen Alertas/Eventos| Stats, gráficos          | Ver detalle            | Detalle alerta/evento             |

---

## Checkpoint de avance (iterativo)
1. [ ] **KPIs**: Mostrar datos mock, luego conectar a API real.
2. [ ] **Alertas Críticas**: Listar, modal de detalle, resolver/eliminar.
3. [ ] **Gestión Rápida**: Modals de alta/edición para entidades clave.
4. [ ] **Notificaciones**: Tabla, modal de detalle.
5. [ ] **Actividad (Gráfico)**: Mostrar gráfico, modal de detalle evento.
6. [ ] **Overview - Métricas**: Mostrar stats, modal de detalle.
7. [ ] **Overview - Dispositivos**: Listar, modal de detalle, CRUD.
8. [ ] **Overview - Resumen Alertas/Eventos**: Stats, gráfico, modal detalle.

---

**Este documento sirve como guía y checklist profesional para el desarrollo iterativo del dashboard y overview del sysadmin.** 