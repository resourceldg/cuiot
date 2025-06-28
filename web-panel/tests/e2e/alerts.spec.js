import { expect, test } from '@playwright/test';

test('Visualización de alertas críticas', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', 'testuser@example.com');
    await page.fill('input[type="password"]', 'testpassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/dashboard/);

    // Ir a sección de gestión humana (ajustar selector según UI real)
    await page.click('a:has-text("Gestión Humana")');

    // Abrir drawer de adulto mayor (ajustar selector según UI real)
    await page.click('.card-person:first-child');

    // Verificar que se visualizan alertas críticas
    await expect(page.locator('.alert-critical')).toBeVisible();
    await expect(page.locator('.led-red')).toBeVisible();
}); 