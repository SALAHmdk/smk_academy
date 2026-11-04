import "server-only";
import { notFound, redirect } from "next/navigation";
import { cache } from "react";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

/**
 * Garde d'accès à l'administration (défense en profondeur : la base exige aussi rôle admin + aal2).
 * - non connecté → connexion ;
 * - non administrateur → 404 (on ne révèle pas l'existence de l'espace) ;
 * - administrateur sans double authentification vérifiée → activation ou saisie du code.
 */
export const requireAdmin = cache(async (next = "/admin") => {
  const user = await getCurrentUser();
  if (!user) redirect(`/connexion?suite=${encodeURIComponent(next)}`);

  const supabase = await createClient();
  const [{ data: role }, { data: aal }] = await Promise.all([
    supabase.rpc("my_role"),
    supabase.auth.mfa.getAuthenticatorAssuranceLevel(),
  ]);
  if (role !== "admin") notFound();
  if (aal?.currentLevel !== "aal2") {
    if (aal?.nextLevel === "aal2") redirect(`/connexion/verification?suite=${encodeURIComponent(next)}`);
    redirect("/compte/securite?admin=1");
  }
  return { user, supabase };
});

export const STATUS_LABEL: Record<string, string> = {
  draft: "Brouillon",
  coming_soon: "Bientôt disponible",
  published: "Publié",
};

/** Transforme un titre en identifiant d'URL (minuscules, sans accents, tirets). */
export function slugify(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
}

/** Message lisible pour les erreurs Postgres renvoyées aux administrateurs. */
export function adminError(error: { code?: string; message?: string } | null): string {
  if (!error) return "";
  if (error.code === "23505") return "Cet identifiant d'URL (slug) existe déjà. Choisissez-en un autre.";
  if (error.code === "42501") return "Action refusée : droits d'administration et double authentification requis.";
  if (error.code === "23503") return "Élément lié introuvable ou encore utilisé.";
  if (error.code === "23514") return "Une valeur ne respecte pas les règles (longueur, format ou valeur autorisée).";
  if (error.code === "P0001" || error.code === "22023") return error.message ?? "Opération refusée.";
  return "L'enregistrement a échoué. Vérifiez les champs et réessayez.";
}
