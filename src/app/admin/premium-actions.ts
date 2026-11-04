"use server";

import { revalidatePath } from "next/cache";
import { z } from "zod";
import { adminError, requireAdmin } from "@/lib/admin";
import type { AdminState } from "@/app/admin/actions";

const email = z.email("Adresse email invalide").trim().max(254);
const optionalEmail = z.union([z.literal(""), email]);
const duration = z
  .string()
  .regex(/^(illimite|\d{1,3})$/, "Durée invalide")
  .transform((v) => (v === "illimite" ? null : Number(v)));

// ---------------------------------------------------------------------------
// Offres et prix
// ---------------------------------------------------------------------------
const planSchema = z.object({
  id: z.enum(["free", "premium_monthly", "premium_yearly"]),
  name: z.string().trim().min(2).max(60),
  tagline: z.string().trim().max(160),
  price: z
    .string()
    .trim()
    .regex(/^\d{1,4}([.,]\d{1,2})?$/, "Prix invalide (ex. 1 ou 9,99)")
    .transform((v) => Math.round(Number(v.replace(",", ".")) * 100)),
  features: z
    .string()
    .max(3000)
    .transform((v) => v.split("\n").map((l) => l.trim()).filter(Boolean).slice(0, 20)),
  is_active: z.literal("on").optional(),
});

export async function updatePlan(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin("/admin/offres");
  const parsed = planSchema.safeParse({
    id: form.get("id"),
    name: form.get("name"),
    tagline: form.get("tagline") ?? "",
    price: form.get("price"),
    features: form.get("features") ?? "",
    is_active: form.get("is_active") ?? undefined,
  });
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const p = parsed.data;
  if (p.id === "free" && p.price !== 0) return { error: "L'offre gratuite reste à 0 €." };
  if (p.id !== "free" && p.price < 50) return { error: "Prix minimum : 0,50 € (minimum imposé par Stripe)." };
  const { error } = await supabase
    .from("plans")
    .update({ name: p.name, tagline: p.tagline, price_cents: p.price, features: p.features, is_active: p.id === "free" || Boolean(p.is_active) })
    .eq("id", p.id);
  if (error) return { error: adminError(error) };
  revalidatePath("/admin/offres");
  revalidatePath("/tarifs");
  return { message: "Offre enregistrée. Le nouveau prix s'applique aux prochains abonnements." };
}

// ---------------------------------------------------------------------------
// Codes promotionnels
// ---------------------------------------------------------------------------
const promoSchema = z.object({
  duration,
  max_redemptions: z.coerce.number().int().min(1, "Au moins 1 utilisation").max(10000),
  restricted_email: optionalEmail,
  expires_on: z.union([z.literal(""), z.iso.date("Date d'expiration invalide")]),
  note: z.string().trim().max(200),
  code: z.union([
    z.literal(""),
    z
      .string()
      .trim()
      .toUpperCase()
      .regex(/^[A-Z0-9-]{6,32}$/, "Code personnalisé : 6 à 32 caractères (lettres, chiffres, tirets)"),
  ]),
});

export async function createPromoCode(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin("/admin/codes-promo");
  const parsed = promoSchema.safeParse({
    duration: form.get("duration"),
    max_redemptions: form.get("max_redemptions") || 1,
    restricted_email: form.get("restricted_email") ?? "",
    expires_on: form.get("expires_on") ?? "",
    note: form.get("note") ?? "",
    code: form.get("code") ?? "",
  });
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const p = parsed.data;
  if (p.duration !== null && (p.duration < 1 || p.duration > 60)) return { error: "Durée : 1 à 60 mois, ou illimitée." };
  if (p.restricted_email && p.max_redemptions !== 1) return { error: "Un code personnel ne peut servir qu'une fois." };
  const expires = p.expires_on ? new Date(`${p.expires_on}T23:59:59+01:00`).toISOString() : null;
  if (expires && new Date(expires) <= new Date()) return { error: "La date d'expiration est déjà passée." };

  const { data, error } = await supabase.rpc("admin_create_promo_code", {
    p_months: p.duration,
    p_max_redemptions: p.max_redemptions,
    p_restricted_email: p.restricted_email || null,
    p_expires_at: expires,
    p_note: p.note,
    p_code: p.code || undefined,
  });
  if (error) return { error: error.code === "23505" ? "Ce code existe déjà." : adminError(error) };
  revalidatePath("/admin/codes-promo");
  return { message: `Code créé : ${data}. Transmettez-le à la personne concernée ; elle le saisira dans Mon compte → Abonnement.` };
}

export async function disablePromoCode(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin("/admin/codes-promo");
  const id = z.uuid().safeParse(form.get("id"));
  if (!id.success) return { error: "Code introuvable." };
  const { error } = await supabase.rpc("admin_disable_promo_code", { p_id: id.data });
  if (error) return { error: adminError(error) };
  revalidatePath("/admin/codes-promo");
  return { message: "Code désactivé." };
}

// ---------------------------------------------------------------------------
// Accès Premium offerts (clients fidèles)
// ---------------------------------------------------------------------------
const grantSchema = z.object({ email, duration, note: z.string().trim().max(200) });

export async function grantPremium(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin("/admin/acces");
  const parsed = grantSchema.safeParse({
    email: form.get("email"),
    duration: form.get("duration"),
    note: form.get("note") ?? "",
  });
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const { email: mail, duration: months, note } = parsed.data;
  if (months !== null && (months < 1 || months > 120)) return { error: "Durée : 1 à 120 mois, ou illimitée." };
  const { error } = await supabase.rpc("admin_grant_premium", { p_email: mail, p_months: months, p_note: note });
  if (error) {
    if (error.code === "P0002") return { error: "Aucun compte SMK Academy n'utilise cette adresse. La personne doit d'abord créer son compte." };
    return { error: adminError(error) };
  }
  revalidatePath("/admin/acces");
  return { message: `Accès Premium ${months === null ? "illimité" : `de ${months} mois`} offert à ${mail}.` };
}

export async function revokePremium(_prev: AdminState, form: FormData): Promise<AdminState> {
  const { supabase } = await requireAdmin("/admin/acces");
  const id = z.uuid().safeParse(form.get("id"));
  if (!id.success) return { error: "Accès introuvable." };
  const { error } = await supabase.rpc("admin_revoke_premium", { p_grant_id: id.data });
  if (error) return { error: adminError(error) };
  revalidatePath("/admin/acces");
  return { message: "Accès révoqué." };
}
