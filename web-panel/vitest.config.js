// vitest.config.js
// Configuración para tests unitarios de componentes Svelte

import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
    plugins: [sveltekit()],
    test: {
        include: ['tests/unit/**/*.{test,spec}.{js,ts}'],
        environment: 'jsdom',
        setupFiles: ['tests/unit/setup.js'],
        globals: true
    }
}); 