import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { signOut } from "@/app/actions/auth";
import { ChevronIcon } from "@/components/icons";
import { ProfileForm } from "@/components/profile-form";
import { ThemeSwitch } from "@/components/theme-switch";
import { createClient, getCurrentUser } from "@/lib/supabase/server";
import { getTheme } from "@/lib/theme";

export const metadata: Metadata = { title: "Mon compte", robots: { index: false } };

export default async function AccountPage() {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion?suite=/compte");
  const supabase = await createClient();
  const [{ data: profile }, theme] = await Promise.all([
    supabase.from("profiles").select("full_name, plan, created_at").eq("id", user.id).single(),
    getTheme(),
  ]);

  return (
    <div className="mx-auto max-w-2xl px-5 pt-10">
      <h1 className="t-1">Mon compte</h1>

      <section aria-labelledby="profil" className="mt-8">
        <h2 id="profil" className="mb-2 px-1 text-[13px] font-medium text-ink-2">Profil</h2>
        <div className="surface divide-y divide-line">
          <div className="p-5">
            <ProfileForm fullName={profile?.full_name ?? ""} />
          </div>
          <div className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
            <span>Adresse email</span>
            <span className="truncate text-ink-2">{user.email}</span>
          </div>
          <div className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
            <span>Offre</span>
            <span className="text-ink-2">{profile?.plan === "premium" ? "SMK Premium" : "SMK Free"}</span>
          </div>
          {profile?.created_at && (
            <div className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
              <span>Membre depuis</span>
              <span className="text-ink-2">
                {new Date(profile.created_at).toLocaleDateString("fr-FR", { dateStyle: "long", timeZone: "Europe/Paris" })}
              </span>
            </div>
          )}
        </div>
      </section>

      <section aria-labelledby="apparence" className="mt-8">
        <h2 id="apparence" className="mb-2 px-1 text-[13px] font-medium text-ink-2">Apparence</h2>
        <div className="surface flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
          <span>Thème</span>
          <ThemeSwitch current={theme} />
        </div>
      </section>

      <section aria-labelledby="securite" className="mt-8">
        <h2 id="securite" className="mb-2 px-1 text-[13px] font-medium text-ink-2">Sécurité</h2>
        <div className="surface divide-y divide-line">
          <Link href="/compte/nouveau-mot-de-passe" className="flex min-h-[52px] items-center justify-between px-5 py-3 hover:bg-surface-2">
            <span>Changer de mot de passe</span>
            <ChevronIcon className="h-4 w-4 text-ink-3" />
          </Link>
          <form action={signOut}>
            <button type="submit" className="flex min-h-[52px] w-full items-center px-5 py-3 text-left text-red hover:bg-surface-2">
              Se déconnecter
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}
