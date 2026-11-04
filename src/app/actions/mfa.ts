"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";
import { safeNextPath } from "@/lib/learning";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export type EnrollState = { error?: string; factorId?: string; qr?: string; secret?: string; done?: boolean };

const code = z.string().trim().regex(/^\d{6}$/, "Saisissez les 6 chiffres affichés par votre application.");

/** Étape 1 : crée un facteur TOTP non vérifié et renvoie le QR code à scanner. */
export async function startTotpEnrollment(): Promise<EnrollState> {
  if (!(await getCurrentUser())) return { error: "Session expirée : reconnectez-vous." };
  const supabase = await createClient();

  // Nettoie les facteurs TOTP restés non vérifiés (tentative interrompue).
  const { data: factors } = await supabase.auth.mfa.listFactors();
  for (const f of factors?.all ?? []) {
    if (f.factor_type === "totp" && f.status === "unverified") await supabase.auth.mfa.unenroll({ factorId: f.id });
  }

  const { data, error } = await supabase.auth.mfa.enroll({
    factorType: "totp",
    friendlyName: `SMK Academy ${new Date().toISOString().slice(0, 10)}`,
    issuer: "SMK Academy",
  });
  if (error || !data) return { error: "Impossible de démarrer l'activation. Réessayez dans un instant." };
  return { factorId: data.id, qr: data.totp.qr_code, secret: data.totp.secret };
}

/** Étape 2 : vérifie le premier code ; la session passe au niveau aal2. */
export async function confirmTotpEnrollment(prev: EnrollState, form: FormData): Promise<EnrollState> {
  const parsed = code.safeParse(form.get("code"));
  const factorId = z.uuid().safeParse(form.get("factorId"));
  if (!factorId.success) return { error: "Activation expirée : recommencez." };
  if (!parsed.success) return { ...prev, error: parsed.error.issues[0].message };

  const supabase = await createClient();
  const { error } = await supabase.auth.mfa.challengeAndVerify({ factorId: factorId.data, code: parsed.data });
  if (error) return { ...prev, error: "Code incorrect ou expiré. Vérifiez l'heure de votre téléphone et réessayez." };
  revalidatePath("/compte/securite");
  return { done: true };
}

export type VerifyState = { error?: string };

/** Connexion : vérifie le code TOTP d'un compte protégé (aal1 → aal2). */
export async function verifyTotpLogin(_prev: VerifyState, form: FormData): Promise<VerifyState> {
  const parsed = code.safeParse(form.get("code"));
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  const supabase = await createClient();
  const { data: factors } = await supabase.auth.mfa.listFactors();
  const totp = factors?.totp?.find((f) => f.status === "verified");
  if (!totp) redirect("/compte/securite");

  const { error } = await supabase.auth.mfa.challengeAndVerify({ factorId: totp.id, code: parsed.data });
  if (error) return { error: "Code incorrect ou expiré." };
  redirect(safeNextPath(form.get("suite")));
}

/** Désactive un facteur (exige une session aal2 côté Supabase). */
export async function removeTotpFactor(form: FormData): Promise<void> {
  const factorId = z.uuid().parse(form.get("factorId"));
  const supabase = await createClient();
  const { data: aal } = await supabase.auth.mfa.getAuthenticatorAssuranceLevel();
  if (aal?.currentLevel !== "aal2") redirect("/connexion/verification?suite=/compte/securite");
  const { data: role } = await supabase.rpc("my_role");
  if (role === "admin") redirect("/compte/securite?erreur=admin");
  await supabase.auth.mfa.unenroll({ factorId });
  revalidatePath("/compte/securite");
  redirect("/compte/securite?retire=1");
}
