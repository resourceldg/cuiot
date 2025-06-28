// tests/unit/setup.js
// Configuración global para tests unitarios

import '@testing-library/jest-dom';

// Mock de SvelteKit
vi.mock('$app/navigation', () => ({
    goto: vi.fn(),
    invalidate: vi.fn(),
    invalidateAll: vi.fn()
}));

// Mock de stores
vi.mock('$lib/api.js', () => ({
    authService: {
        isAuthenticated: vi.fn(() => true),
        login: vi.fn(),
        logout: vi.fn()
    },
    authStore: {
        subscribe: vi.fn(),
        update: vi.fn()
    },
    elderlyPersonService: {
        getAll: vi.fn(),
        create: vi.fn(),
        update: vi.fn(),
        delete: vi.fn()
    },
    eventService: {
        getAll: vi.fn(),
        create: vi.fn(),
        update: vi.fn(),
        delete: vi.fn()
    },
    deviceService: {
        getAll: vi.fn(),
        create: vi.fn(),
        update: vi.fn(),
        delete: vi.fn()
    },
    alertService: {
        getAll: vi.fn(),
        getCriticalAlertsByElderlyPerson: vi.fn()
    }
})); 