"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { z } from "zod";
import { env } from "@/lib/env";
import { safeNextPath } from "@/lib/learning";
import { createClient } from "@/lib/supabase/server";

export type FormState = { error?: string; message?: string; fields?: Record<string, string> };

const email = z.email("Adresse email invalide").max(254).transform((v) => v.trim().toLowerCase());
const password = z
  .string()
  .min(8, "Le mot de passe doit contenir au moins 8 caractères")
  .max(72, "Le mot de passe est trop long (72 caractères maximum)");

const signUpSchema = z.object({
  fullName: z.string().trim().min(2, "Indiquez votre nom (2 caractères minimum)").max(120),
  email,
  password,
  terms: z.literal("on", { error: "Vous devez accepter les conditions d'utilisation" }),
});

/**
 * Origine publique du site pour les liens envoyés par email.
 * Priorité à l'en-tête Origin de la requête (fonctionne aussi sur les prévisualisations Netlify) ;
 * Supabase n'accepte de toute façon que les URL déclarées dans « Redirect URLs ».
 */
async function siteOrigin(): Promise<string> {
  const origin = (await headers()).get("origin");
  if (origin && /^https?:\/\/[a-z0-9.-]+(:\d+)?$/i.test(origin)) return origin;
  return env.siteUrl;
}

function translateAuthError(message: string): string {
  const m = message.toLowerCase();
  if (m.includes("invalid login credentials")) return "Email ou mot de passe incorrect.";
  if (m.includes("email not confirmed"))
    return "Confirmez d'abord votre adresse : ouvrez le lien reçu par email.";
  if (m.includes("already registered") || m.includes("already exists"))
    return "Un compte existe déjà avec cette adresse. Connectez-vous ou réinitialisez votre mot de passe.";
  if (m.includes("rate limit") || m.includes("too many"))
    return "Trop de tentatives. Patientez quelques minutes avant de réessayer.";
  if (m.includes("weak") || m.includes("pwned"))
    return "Ce mot de passe est trop faible ou a déjà fuité. Choisissez-en un autre.";
  return "L'opération n'a pas abouti. Réessayez dans un instant.";
}

export async function signUp(_prev: FormState, form: FormData): Promise<FormState> {
  const parsed = signUpSchema.safeParse({
    fullName: form.get("fullName"),
    email: form.get("email"),
    password: form.get("password"),
    terms: form.get("terms"),
  });
  const fields = { fullName: String(form.get("fullName") ?? ""), email: String(form.get("email") ?? "") };
  if (!parsed.success) return { error: parsed.error.issues[0].message, fields };

  const next = safeNextPath(form.get("suite"));
  const supabase = await createClient();
  const { data, error } = await supabase.auth.signUp({
    email: parsed.data.email,
    password: parsed.data.password,
    options: {
      data: { full_name: parsed.data.fullName },
      emailRedirectTo: `${await siteOrigin()}/auth/confirm?suite=${encodeURIComponent(next)}`,
    },
  });
  if (error) return { error: translateAuthError(error.message), fields };

  // Confirmation d'email désactivée côté Supabase : la session existe déjà.
  if (data.session) redirect(next);

  return {
    message: `Compte créé. Un email de confirmation a été envoyé à ${parsed.data.email} : cliquez sur le lien pour activer votre compte.`,
  };
}

const signInSchema = z.object({ email, password: z.string().min(1, "Saisissez votre mot de passe").max(72) });

export async function signIn(_prev: FormState, form: FormData): Promise<FormState> {
  const parsed = signInSchema.safeParse({ email: form.get("email"), password: form.get("password") });
  const fields = { email: String(form.get("email") ?? "") };
  if (!parsed.success) return { error: parsed.error.issues[0].message, fields };

  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithPassword(parsed.data);
  if (error) return { error: translateAuthError(error.message), fields };

  redirect(safeNextPath(form.get("suite")));
}

export async function signOut(): Promise<void> {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/");
}

export async function requestPasswordReset(_prev: FormState, form: FormData): Promise<FormState> {
  const parsed = email.safeParse(form.get("email"));
  if (!parsed.success) return { error: "Adresse email invalide" };

  const supabase = await createClient();
  await supabase.auth.resetPasswordForEmail(parsed.data, {
    redirectTo: `${await siteOrigin()}/auth/confirm?suite=/compte/nouveau-mot-de-passe`,
  });
  // Réponse identique que le compte existe ou non (pas d'énumération des comptes).
  return { message: "Si un compte existe pour cette adresse, un lien de réinitialisation vient d'être envoyé." };
}

export async function updatePassword(_prev: FormState, form: FormData): Promise<FormState> {
  const parsed = z
    .object({ password, confirm: z.string() })
    .refine((v) => v.password === v.confirm, "Les deux mots de passe ne correspondent pas")
    .safeParse({ password: form.get("password"), confirm: form.get("confirm") });
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  const supabase = await createClient();
  const { error } = await supabase.auth.updateUser({ password: parsed.data.password });
  if (error) return { error: translateAuthError(error.message) };
  redirect("/tableau-de-bord?mdp=ok");
}
