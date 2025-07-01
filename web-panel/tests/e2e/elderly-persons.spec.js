import { expect, test } from '@playwright/test';

test('ABM de personas bajo cuidado', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', 'testuser@example.com');
    await page.fill('input[type="password"]', 'testpassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/dashboard/);

    // Abrir formulario de alta
    await page.click('button:has-text("Agregar Adulto Mayor")');
    await page.fill('input#first_name', 'Juan');
    await page.fill('input#last_name', 'Pérez');
    await page.click('button:has-text("Crear")');
    await expect(page.locator('.form-success')).toHaveText(/creado con éxito/i);

    // Editar
    await page.click('button:has-text("Editar")');
    await page.fill('input#first_name', 'Juan Editado');
    await page.click('button:has-text("Actualizar")');
    await expect(page.locator('.form-success')).toHaveText(/editado con éxito/i);

    // Eliminar
    await page.click('button:has-text("Eliminar")');
    await page.click('button:has-text("Confirmar")');
    await expect(page.locator('.form-success')).toHaveText(/eliminado con éxito/i);
}); 