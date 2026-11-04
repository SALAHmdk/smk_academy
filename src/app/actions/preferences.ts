"use server";

import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { z } from "zod";
import { createClient, getCurrentUser } from "@/lib/supabase/server";
import type { FormState } from "@/app/actions/auth";

const THEME_COOKIE = "smk-theme";

export async function setTheme(form: FormData): Promise<void> {
  const theme = z.enum(["auto", "light", "dark"]).catch("auto").parse(form.get("theme"));
  const store = await cookies();
  if (theme === "auto") store.delete(THEME_COOKIE);
  else store.set(THEME_COOKIE, theme, { path: "/", maxAge: 60 * 60 * 24 * 365, sameSite: "lax" });
  revalidatePath("/", "layout");
}

export async function updateProfile(_prev: FormState, form: FormData): Promise<FormState> {
  const user = await getCurrentUser();
  if (!user) return { error: "Session expirée : reconnectez-vous." };
  const parsed = z.string().trim().min(2, "Indiquez votre nom (2 caractères minimum)").max(120).safeParse(form.get("fullName"));
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  const supabase = await createClient();
  // Seule la colonne full_name est modifiable par l'étudiant (privilège de colonne en base).
  const { error } = await supabase.from("profiles").update({ full_name: parsed.data }).eq("id", user.id);
  if (error) return { error: "Le nom n'a pas pu être enregistré. Réessayez." };
  revalidatePath("/", "layout");
  return { message: "Nom enregistré." };
}
