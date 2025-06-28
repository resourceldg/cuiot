// playwright.config.js
// Configuración básica para tests E2E en SvelteKit

/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
    testDir: './tests/e2e',
    timeout: 30000,
    retries: 1,
    use: {
        baseURL: 'http://localhost:5173',
        headless: true,
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
};

export default config; 