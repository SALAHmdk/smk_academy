import { createHmac } from "node:crypto";
import { afterEach, describe, expect, it } from "vitest";
import { stripeConfig, toForm, verifyStripeSignature } from "./stripe";
import { formatMonths, formatPlanPrice } from "./format";

const secret = "whsec_test_secret";
const payload = JSON.stringify({ id: "evt_1", type: "invoice.paid" });
const sign = (t: number, body = payload, key = secret) => createHmac("sha256", key).update(`${t}.${body}`).digest("hex");

describe("verifyStripeSignature", () => {
  const now = 1_800_000_000;

  it("accepte une signature valide", async () => {
    expect(await verifyStripeSignature(payload, `t=${now},v1=${sign(now)}`, secret, 300, now)).toBe(true);
  });
  it("refuse un contenu modifié", async () => {
    expect(await verifyStripeSignature(payload.replace("evt_1", "evt_2"), `t=${now},v1=${sign(now)}`, secret, 300, now)).toBe(false);
  });
  it("refuse une autre clé", async () => {
    expect(await verifyStripeSignature(payload, `t=${now},v1=${sign(now, payload, "whsec_autre")}`, secret, 300, now)).toBe(false);
  });
  it("refuse un horodatage trop ancien (rejeu)", async () => {
    const old = now - 600;
    expect(await verifyStripeSignature(payload, `t=${old},v1=${sign(old)}`, secret, 300, now)).toBe(false);
  });
  it("refuse un en-tête absent ou malformé", async () => {
    expect(await verifyStripeSignature(payload, null, secret, 300, now)).toBe(false);
    expect(await verifyStripeSignature(payload, "v1=abc", secret, 300, now)).toBe(false);
  });
  it("accepte si l'une des signatures v1 correspond (rotation de secret)", async () => {
    expect(await verifyStripeSignature(payload, `t=${now},v1=deadbeef,v1=${sign(now)}`, secret, 300, now)).toBe(true);
  });
});

describe("stripeConfig", () => {
  const saved = { ...process.env };
  afterEach(() => {
    process.env = { ...saved };
  });
  it("refuse une clé de production", () => {
    process.env.STRIPE_SECRET_KEY = "sk_live_xxx";
    process.env.STRIPE_WEBHOOK_SECRET = "whsec_x";
    process.env.PAYMENTS_WEBHOOK_TOKEN = "x".repeat(40);
    expect(stripeConfig()).toBeNull();
  });
  it("accepte une configuration de test complète", () => {
    process.env.STRIPE_SECRET_KEY = "sk_test_xxx";
    process.env.STRIPE_WEBHOOK_SECRET = "whsec_x";
    process.env.PAYMENTS_WEBHOOK_TOKEN = "x".repeat(40);
    expect(stripeConfig()?.secretKey).toBe("sk_test_xxx");
  });
});

describe("toForm", () => {
  it("encode les objets imbriqués à la manière de Stripe", () => {
    const f = toForm({ line_items: [{ price_data: { unit_amount: 100, recurring: { interval: "month" } } }] });
    expect(f.get("line_items[0][price_data][unit_amount]")).toBe("100");
    expect(f.get("line_items[0][price_data][recurring][interval]")).toBe("month");
  });
});

describe("formats", () => {
  it("affiche les prix des offres", () => {
    expect(formatPlanPrice(100, "month")).toBe("1 € / mois");
    expect(formatPlanPrice(1000, "year")).toBe("10 € / an");
    expect(formatPlanPrice(0, null)).toBe("0 €");
    expect(formatPlanPrice(999, "month")).toMatch(/^9,99\s€ \/ mois$/);
  });
  it("affiche les durées", () => {
    expect(formatMonths(null)).toBe("Illimité");
    expect(formatMonths(3)).toBe("3 mois");
    expect(formatMonths(12)).toBe("1 an");
    expect(formatMonths(24)).toBe("2 ans");
  });
});
