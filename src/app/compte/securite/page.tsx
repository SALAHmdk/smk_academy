import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { removeTotpFactor } from "@/app/actions/mfa";
import { TotpEnrollment } from "@/components/mfa-forms";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Sécurité du compte", robots: { index: false } };

type Props = { searchParams: Promise<{ admin?: string; retire?: string; erreur?: string }> };

export default async function SecurityPage({ searchParams }: Props) {
  if (!(await getCurrentUser())) redirect("/connexion?suite=/compte/securite");
  const params = await searchParams;
  const supabase = await createClient();
  const [{ data: factors }, { data: aal }, { data: role }] = await Promise.all([
    supabase.auth.mfa.listFactors(),
    supabase.auth.mfa.getAuthenticatorAssuranceLevel(),
    supabase.rpc("my_role"),
  ]);
  const verified = (factors?.totp ?? []).filter((f) => f.status === "verified");
  const isAdmin = role === "admin";

  return (
    <div className="mx-auto max-w-2xl px-5 pt-10">
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/compte" className="hover:text-ink">
          Mon compte
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>Sécurité</span>
      </nav>
      <h1 className="t-1 mt-4">Sécurité</h1>

      {params.admin && (
        <p role="status" className="mt-6 rounded-[var(--radius-md)] bg-blue-soft px-4 py-3 text-ink">
          L&apos;espace administrateur exige la double authentification. Activez-la ci-dessous pour continuer.
        </p>
      )}
      {params.retire && (
        <p role="status" className="mt-6 rounded-[var(--radius-md)] bg-surface-2 px-4 py-3 text-ink-2">
          Double authentification désactivée.
        </p>
      )}
      {params.erreur === "admin" && (
        <p role="alert" className="mt-6 rounded-[var(--radius-md)] bg-red-soft px-4 py-3 text-red">
          Un compte administrateur doit conserver sa double authentification.
        </p>
      )}

      <section aria-labelledby="mfa" className="surface mt-8 p-6">
        <h2 id="mfa" className="t-3">
          Double authentification (application TOTP)
        </h2>
        <p className="mt-2 text-ink-2">
          En plus du mot de passe, un code temporaire généré par votre téléphone sera demandé à la connexion.
          {isAdmin ? " Obligatoire pour les administrateurs." : " Facultative, mais fortement recommandée."}
        </p>

        <div className="mt-6">
          {verified.length > 0 ? (
            <ul className="divide-y divide-line rounded-[var(--radius-md)] border border-line">
              {verified.map((f) => (
                <li key={f.id} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3">
                  <div>
                    <p className="font-medium">{f.friendly_name || "Application d'authentification"}</p>
                    <p className="text-sm text-green">Active depuis le {new Date(f.created_at).toLocaleDateString("fr-FR", { timeZone: "Europe/Paris" })}</p>
                  </div>
                  {!isAdmin && (
                    <form action={removeTotpFactor}>
                      <input type="hidden" name="factorId" value={f.id} />
                      <button type="submit" className="btn btn-plain text-red">
                        Désactiver
                      </button>
                    </form>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <TotpEnrollment />
          )}
        </div>

        {verified.length > 0 && aal?.currentLevel !== "aal2" && (
          <p className="mt-4 text-sm text-ink-2">
            Cette session n&apos;est pas encore vérifiée.{" "}
            <Link href="/connexion/verification?suite=/compte/securite" className="font-medium text-blue">
              Saisir un code
            </Link>
          </p>
        )}
      </section>

      <section aria-labelledby="mdp" className="surface mt-6 p-6">
        <h2 id="mdp" className="t-3">
          Mot de passe
        </h2>
        <p className="mt-2 text-ink-2">Utilisez un mot de passe unique, que vous n&apos;utilisez sur aucun autre site.</p>
        <Link href="/compte/nouveau-mot-de-passe" className="btn btn-secondary mt-4">
          Changer de mot de passe
        </Link>
      </section>
    </div>
  );
}
