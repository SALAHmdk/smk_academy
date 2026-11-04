import { defineConfig, devices } from "@playwright/test";

// Parcours étudiant de bout en bout contre un site déployé (ou local) relié à Supabase.
// E2E_BASE_URL=https://... E2E_EMAIL=... E2E_PASSWORD=... npx playwright test
export default defineConfig({
  testDir: "./e2e",
  timeout: 60_000,
  use: { baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000", trace: "retain-on-failure" },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile", use: { ...devices["iPhone 14"] } },
  ],
});
