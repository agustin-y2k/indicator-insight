import { expect, test } from '@playwright/test';

test('initial screen exposes loading and empty states', async ({ page }) => {
  let resolveResponse!: () => void;
  const responseAllowed = new Promise<void>((resolve) => { resolveResponse = resolve; });
  await page.route('**/api/health/ready', async (route) => {
    await responseAllowed;
    await route.fulfill({ json: { status: 'ok' } });
  });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Indicator Insight' })).toBeVisible();
  await expect(page.getByRole('status')).toHaveText('Comprobando conexión…');
  resolveResponse();
  await expect(page.getByRole('status')).toHaveText('Conexión disponible.');
  await expect(page.getByText('Aún no hay actividades disponibles.')).toBeVisible();
});

test('unavailable backend shows an actionable error', async ({ page }) => {
  await page.route('**/api/health/ready', (route) =>
    route.fulfill({ status: 503, json: { status: 'unavailable' } }),
  );
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('Recargá la página');
});

test('frontend reaches the backend and PostgreSQL through the proxy', async ({ page }) => {
  test.skip(!process.env.E2E_BASE_URL, 'Requires the running Compose environment');
  await page.goto('/');
  await expect(page.getByRole('status')).toHaveText('Conexión disponible.');
});
