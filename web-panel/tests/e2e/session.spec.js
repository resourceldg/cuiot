import { expect, test } from '@playwright/test';

test('Gestión de sesión: login y logout', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', 'testuser@example.com');
    await page.fill('input[type="password"]', 'testpassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/dashboard/);

    // Logout
    await page.click('button:has-text("Cerrar Sesión")');
    await expect(page).toHaveURL(/login/);
}); 