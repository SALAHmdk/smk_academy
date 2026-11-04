import "server-only";

/**
 * Accès minimal à l'API Stripe (sans SDK) — MODE TEST UNIQUEMENT.
 * Une clé « sk_live_ » est refusée : aucune transaction réelle sans autorisation explicite.
 */
const API = "https://api.stripe.com/v1";

export type StripeConfig = { secretKey: string; webhookSecret: string; dbToken: string };

export function stripeStatus() {
  const key = process.env.STRIPE_SECRET_KEY ?? "";
  return {
    secretKey: key.startsWith("sk_test_") ? "test" : key ? "refusée (clé non test)" : "absente",
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET?.startsWith("whsec_") ? "présente" : "absente",
    dbToken: (process.env.PAYMENTS_WEBHOOK_TOKEN ?? "").length >= 32 ? "présent" : "absent",
  };
}

export function stripeConfig(): StripeConfig | null {
  const secretKey = process.env.STRIPE_SECRET_KEY ?? "";
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET ?? "";
  const dbToken = process.env.PAYMENTS_WEBHOOK_TOKEN ?? "";
  if (!secretKey.startsWith("sk_test_") || !webhookSecret.startsWith("whsec_") || dbToken.length < 32) return null;
  return { secretKey, webhookSecret, dbToken };
}

/** Encodage application/x-www-form-urlencoded avec la notation à crochets de Stripe. */
export function toForm(data: Record<string, unknown>, prefix = ""): URLSearchParams {
  const out = new URLSearchParams();
  const walk = (value: unknown, key: string) => {
    if (value === undefined || value === null) return;
    if (Array.isArray(value)) value.forEach((v, i) => walk(v, `${key}[${i}]`));
    else if (typeof value === "object") for (const [k, v] of Object.entries(value)) walk(v, key ? `${key}[${k}]` : k);
    else out.append(key, String(value));
  };
  walk(data, prefix);
  return out;
}

export async function stripeRequest<T>(
  secretKey: string,
  method: "GET" | "POST",
  path: string,
  body?: Record<string, unknown>,
  idempotencyKey?: string,
): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${secretKey}`,
      "Content-Type": "application/x-www-form-urlencoded",
      ...(idempotencyKey ? { "Idempotency-Key": idempotencyKey } : {}),
    },
    body: body ? toForm(body).toString() : undefined,
    cache: "no-store",
  });
  const json = (await res.json()) as T & { error?: { message?: string } };
  if (!res.ok) throw new Error(json.error?.message ?? `Stripe ${res.status}`);
  return json;
}

/**
 * Vérifie l'en-tête Stripe-Signature (HMAC-SHA256 « t.payload », tolérance 5 min, comparaison à temps constant).
 * https://docs.stripe.com/webhooks#verify-manually
 */
export async function verifyStripeSignature(
  payload: string,
  header: string | null,
  secret: string,
  toleranceSeconds = 300,
  now = Math.floor(Date.now() / 1000),
): Promise<boolean> {
  if (!header) return false;
  const parts = header.split(",").map((p) => p.trim().split("=") as [string, string]);
  const t = Number(parts.find(([k]) => k === "t")?.[1]);
  const signatures = parts.filter(([k]) => k === "v1").map(([, v]) => v);
  if (!Number.isFinite(t) || signatures.length === 0) return false;
  if (Math.abs(now - t) > toleranceSeconds) return false;

  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${t}.${payload}`));
  const expected = Array.from(new Uint8Array(mac), (b) => b.toString(16).padStart(2, "0")).join("");
  return signatures.some((sig) => timingSafeEqual(sig, expected));
}

function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
