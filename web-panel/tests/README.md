# Tests - Frontend

## Estructura de Tests

### Tests E2E (End-to-End)
Ubicados en `tests/e2e/` usando Playwright:
- **elderly-persons.spec.js:** ABM completo de adultos mayores
- **events.spec.js:** ABM completo de eventos
- **devices.spec.js:** ABM completo de dispositivos
- **session.spec.js:** Login, logout y gestión de sesión
- **alerts.spec.js:** Visualización de alertas críticas
- **personas-bajo-cuidado.spec.js:** ABM completo de personas bajo cuidado

### Tests Unitarios
Ubicados en `tests/unit/` usando Vitest + Testing Library:
- **components/:** Tests de componentes Svelte
  - `ElderlyPersonForm.test.js`
  - `EventForm.test.js`
  - `Toast.test.js`
- **services/:** Tests de servicios de API
  - `api.test.js`
- **utils/:** Tests de utilidades
  - `dateUtils.test.js`

## Configuración

### Playwright (E2E)
- Configuración en `playwright.config.js`
- Base URL: `http://localhost:5173`
- Screenshots y videos en fallos
- Timeout: 30 segundos

### Vitest (Unitarios)
- Configuración en `vitest.config.js`
- Ambiente: jsdom
- Setup global en `tests/unit/setup.js`
- Mocks de SvelteKit y servicios

## Comandos

```bash
# Instalar dependencias
npm install

# Tests E2E
npm run test:e2e

# Tests unitarios
npm run test:ui

# Tests unitarios en modo watch
npm run test:ui:watch

# Instalar navegadores para Playwright
npx playwright install
```

## Cobertura

### E2E
- Flujos críticos de usuario
- ABM de entidades principales
- Gestión de sesión
- Feedback visual y validaciones

### Unitarios
- Renderizado de componentes
- Validaciones de formularios
- Eventos y callbacks
- Servicios de API
- Utilidades de fecha

## Extensión

Para agregar nuevos tests:
1. **E2E:** Crear archivo `.spec.js` en `tests/e2e/`
2. **Unitarios:** Crear archivo `.test.js` en `tests/unit/`
3. Seguir patrones de Testing Library para accesibilidad
4. Usar mocks para dependencias externas 