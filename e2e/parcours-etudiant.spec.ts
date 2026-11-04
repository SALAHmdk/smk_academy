import { expect, test } from "@playwright/test";

// Requiert un compte étudiant confirmé (E2E_EMAIL / E2E_PASSWORD).
const email = process.env.E2E_EMAIL;
const password = process.env.E2E_PASSWORD;

test.describe("parcours étudiant", () => {
  test.skip(!email || !password, "E2E_EMAIL et E2E_PASSWORD requis");

  test("connexion, leçon, quiz noté sur 20, déconnexion et reprise", async ({ page }) => {
    await page.goto("/connexion");
    await page.getByLabel("Adresse email").fill(email!);
    await page.getByLabel("Mot de passe", { exact: true }).fill(password!);
    await page.getByRole("button", { name: "Se connecter" }).click();
    await expect(page).toHaveURL(/tableau-de-bord/);

    await page.goto("/formations/python-debutant");
    await page.getByRole("link", { name: /Découvrir Python/ }).first().click();
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Découvrir Python");
    await page.getByText("Voir la correction").first().click();

    await page.goto("/formations/python-debutant/1/quiz");
    const groups = page.locator("fieldset");
    const count = await groups.count();
    for (let i = 0; i < count; i++) await groups.nth(i).locator("input").first().check();
    await page.getByRole("button", { name: "Valider mes réponses" }).click();
    await expect(page).toHaveURL(/resultats\//);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("/20");
    await expect(page.getByText("Correction détaillée")).toBeVisible();

    await page.getByRole("button", { name: "Déconnexion" }).click();
    await page.goto("/tableau-de-bord");
    await expect(page).toHaveURL(/connexion/);

    await page.getByLabel("Adresse email").fill(email!);
    await page.getByLabel("Mot de passe", { exact: true }).fill(password!);
    await page.getByRole("button", { name: "Se connecter" }).click();
    await expect(page.getByText("Historique des quiz")).toBeVisible();
    await expect(page.locator("text=/\\d+([,.]\\d+)?\\/20/").first()).toBeVisible();
  });
});

test("les espaces privés exigent une connexion", async ({ page }) => {
  await page.goto("/tableau-de-bord");
  await expect(page).toHaveURL(/connexion\?suite=/);
});
