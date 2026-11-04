import type { Metadata } from "next";
import Link from "next/link";
import { CheckoutButton } from "@/components/billing-forms";
import { CheckIcon } from "@/components/icons";
import { formatPlanPrice, formatPrice, type Access } from "@/lib/format";
import { stripeConfig } from "@/lib/stripe";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = {
  title: "Tarifs",
  description: "SMK Free gratuit, SMK Premium à 1 € par mois ou 10 € par an. Sans engagement, votre progression est toujours conservée.",
};

type Props = { searchParams: Promise<{ paiement?: string }> };

export default async function PricingPage({ searchParams }: Props) {
  const { paiement } = await searchParams;
  const supabase = await createClient();
  const user = await getCurrentUser();
  const [{ data: plans }, { count: premiumCourses }, { data: accessData }] = await Promise.all([
    supabase.from("plans").select("*").eq("is_active", true).order("position"),
    supabase.from("courses").select("id", { count: "exact", head: true }).eq("status", "published").eq("is_premium", true),
    user ? supabase.rpc("my_access") : Promise.resolve({ data: null }),
  ]);
  const access = (accessData ?? { premium: false }) as Access;
  const paymentsOpen = stripeConfig() !== null;
  const monthly = plans?.find((p) => p.id === "premium_monthly");
  const yearly = plans?.find((p) => p.id === "premium_yearly");
  const saving = monthly && yearly ? monthly.price_cents * 12 - yearly.price_cents : 0;

  return (
    <div className="mx-auto max-w-6xl px-5 pt-12">
      <header className="mx-auto max-w-2xl text-center">
        <p className="eyebrow">Tarifs</p>
        <h1 className="t-display mt-2">Apprendre, sans se ruiner.</h1>
        <p className="subhead mt-4">
          Commencez gratuitement. Passez à Premium quand vous le souhaitez, sans engagement : votre progression et vos
          notes vous appartiennent, même après une résiliation.
        </p>
      </header>

      {paiement === "annule" && (
        <p role="status" className="mx-auto mt-8 max-w-xl rounded-[var(--radius-md)] bg-surface-2 px-4 py-3 text-center">
          Paiement annulé : aucun montant n&apos;a été prélevé.
        </p>
      )}

      {(premiumCourses ?? 0) === 0 && (
        <p className="mx-auto mt-8 max-w-2xl rounded-[var(--radius-md)] bg-blue-soft px-4 py-3 text-center text-[15px]">
          Aujourd&apos;hui, toutes les formations publiées sont accessibles gratuitement. Les contenus Premium (parcours
          avancés, examens blancs, projets) sont en cours de rédaction et seront signalés dans le catalogue dès leur
          publication.
        </p>
      )}

      <div className="mt-12 grid gap-5 lg:grid-cols-3">
        {(plans ?? []).map((p) => {
          const featured = p.id === "premium_monthly";
          return (
            <section
              key={p.id}
              aria-labelledby={`offre-${p.id}`}
              className={`surface relative flex flex-col p-7 ${featured ? "ring-2 ring-[var(--smk-blue)]" : ""}`}
            >
              {featured && (
                <span className="absolute -top-3 left-7 rounded-full bg-blue px-3 py-1 text-[12px] font-semibold text-white">
                  Recommandé
                </span>
              )}
              <h2 id={`offre-${p.id}`} className="t-3">
                {p.name}
              </h2>
              <p className="mt-1 min-h-[3em] text-[15px] text-ink-2">{p.tagline}</p>
              <p className="mt-5 text-[44px] font-bold leading-none tracking-tight">
                {formatPrice(p.price_cents)}
                {p.billing_interval && (
                  <span className="text-[17px] font-medium text-ink-2"> TTC / {p.billing_interval === "year" ? "an" : "mois"}</span>
                )}
              </p>
              {p.id === "premium_yearly" && saving > 0 && (
                <p className="mt-2 text-[14px] font-medium text-green">Soit {formatPrice(saving)} d&apos;économie sur un an</p>
              )}
              <ul className="mt-6 grid flex-1 content-start gap-2.5 text-[15px]">
                {p.features.map((f) => (
                  <li key={f} className="flex gap-2.5">
                    <CheckIcon className="mt-0.5 h-5 w-5 shrink-0 text-green" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-7">
                {p.id === "free" ? (
                  user ? (
                    <Link href="/formations" className="btn btn-secondary w-full">
                      Continuer gratuitement
                    </Link>
                  ) : (
                    <Link href="/inscription" className="btn btn-secondary w-full">
                      Créer un compte gratuit
                    </Link>
                  )
                ) : access.premium ? (
                  <Link href="/compte/abonnement" className="btn btn-secondary w-full">
                    Vous êtes Premium
                  </Link>
                ) : !user ? (
                  <Link href="/inscription?suite=/tarifs" className={`btn w-full ${featured ? "btn-primary" : "btn-secondary"}`}>
                    Créer un compte pour s&apos;abonner
                  </Link>
                ) : paymentsOpen ? (
                  <CheckoutButton
                    plan={p.id}
                    primary={featured}
                    label={`S'abonner — ${formatPlanPrice(p.price_cents, p.billing_interval)}`}
                  />
                ) : (
                  <button type="button" disabled className="btn btn-secondary w-full">
                    Paiement en ligne bientôt disponible
                  </button>
                )}
              </div>
            </section>
          );
        })}
      </div>

      <section className="mx-auto mt-14 grid max-w-4xl gap-8 sm:grid-cols-2" aria-label="Questions fréquentes">
        <div>
          <h2 className="font-semibold">Vous avez un code promo ?</h2>
          <p className="mt-1 text-ink-2">
            Saisissez-le dans{" "}
            <Link href={user ? "/compte/abonnement" : "/connexion?suite=/compte/abonnement"} className="text-blue">
              Mon compte → Abonnement
            </Link>
            . Les mois offerts s&apos;ajoutent à votre accès en cours.
          </p>
        </div>
        <div>
          <h2 className="font-semibold">Comment résilier ?</h2>
          <p className="mt-1 text-ink-2">
            En deux clics depuis Mon compte → Abonnement. Premium reste actif jusqu&apos;à la fin de la période payée, puis
            vous repassez à SMK Free sans rien perdre.
          </p>
        </div>
        <div>
          <h2 className="font-semibold">Le paiement est-il sécurisé ?</h2>
          <p className="mt-1 text-ink-2">
            Le paiement est confié à Stripe (carte, Apple Pay, Google Pay selon votre appareil). SMK Academy ne voit ni ne
            stocke jamais vos données bancaires.
          </p>
        </div>
        <div>
          <h2 className="font-semibold">Le renouvellement est-il automatique ?</h2>
          <p className="mt-1 text-ink-2">
            Oui : chaque mois pour l&apos;offre mensuelle, chaque année pour l&apos;offre annuelle. La date du prochain
            prélèvement est toujours affichée dans votre compte.
          </p>
        </div>
      </section>
    </div>
  );
}
