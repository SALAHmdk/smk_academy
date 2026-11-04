import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { PortalButton, RedeemForm } from "@/components/billing-forms";
import { formatDate, formatPrice, type Access } from "@/lib/format";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Abonnement", robots: { index: false } };

type Props = { searchParams: Promise<{ paiement?: string }> };

const PLAN: Record<string, string> = { premium_monthly: "SMK Premium mensuel", premium_yearly: "SMK Premium annuel" };
const STATUS: Record<string, string> = {
  active: "Actif",
  trialing: "Période d'essai",
  past_due: "Paiement en attente",
  canceled: "Résilié",
  unpaid: "Impayé",
  incomplete: "En attente de paiement",
  incomplete_expired: "Paiement non abouti",
};

export default async function SubscriptionPage({ searchParams }: Props) {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion?suite=/compte/abonnement");
  const { paiement } = await searchParams;
  const supabase = await createClient();
  const [{ data: accessData }, { data: grants }, { data: payments }] = await Promise.all([
    supabase.rpc("my_access"),
    supabase.from("premium_grants").select("id, source, starts_at, ends_at, note, revoked_at").is("revoked_at", null).order("starts_at"),
    supabase.from("payments").select("id, amount_cents, status, created_at, plan_id").order("created_at", { ascending: false }).limit(24),
  ]);
  const access = (accessData ?? { premium: false }) as Access;
  const sub = access.subscription;
  const now = new Date();
  const activeGrants = (grants ?? []).filter((g) => !g.ends_at || new Date(g.ends_at) > now);

  return (
    <div className="mx-auto max-w-2xl px-5 pt-10">
      <Link href="/compte" className="text-sm text-blue">
        ← Mon compte
      </Link>
      <h1 className="t-1 mt-2">Abonnement</h1>

      {paiement === "ok" && (
        <p role="status" className="mt-6 rounded-[var(--radius-md)] bg-green-soft px-4 py-3 text-green">
          Merci ! Votre paiement est confirmé par Stripe. L&apos;activation de Premium peut prendre quelques secondes :
          actualisez la page si besoin.
        </p>
      )}

      <section aria-labelledby="offre" className="mt-8">
        <h2 id="offre" className="mb-2 px-1 text-[13px] font-medium text-ink-2">
          Votre offre
        </h2>
        <div className="surface p-6">
          <p className="text-[28px] font-bold tracking-tight">{access.premium ? "SMK Premium" : "SMK Free"}</p>
          <p className="mt-1 text-ink-2">
            {!access.premium && "Accès gratuit aux formations fondamentales, exercices, quiz et progression."}
            {access.premium && access.unlimited && "Accès Premium illimité, offert par SMK Academy."}
            {access.premium && !access.unlimited && access.until && `Premium actif jusqu'au ${formatDate(access.until)}.`}
          </p>
          {!access.premium && (
            <Link href="/tarifs" className="btn btn-primary mt-5">
              Découvrir Premium — dès 1 € / mois
            </Link>
          )}
        </div>
      </section>

      {sub && (
        <section aria-labelledby="abonnement" className="mt-8">
          <h2 id="abonnement" className="mb-2 px-1 text-[13px] font-medium text-ink-2">
            Abonnement payant
          </h2>
          <div className="surface divide-y divide-line">
            <div className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
              <span>Formule</span>
              <span className="text-ink-2">{PLAN[sub.plan_id ?? ""] ?? "SMK Premium"}</span>
            </div>
            <div className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
              <span>Statut</span>
              <span className="text-ink-2">{STATUS[sub.status] ?? sub.status}</span>
            </div>
            <div className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
              <span>{sub.cancel_at_period_end || sub.status === "canceled" ? "Se termine le" : "Prochain renouvellement"}</span>
              <span className="text-ink-2">{formatDate(sub.current_period_end)}</span>
            </div>
            {sub.provider === "stripe" && (
              <div className="p-5">
                <PortalButton />
                <p className="mt-2 text-[13px] text-ink-3">
                  Vous serez redirigé vers l&apos;espace sécurisé Stripe. Une résiliation prend effet à la fin de la
                  période payée ; votre progression est conservée.
                </p>
              </div>
            )}
          </div>
        </section>
      )}

      {activeGrants.length > 0 && (
        <section aria-labelledby="offerts" className="mt-8">
          <h2 id="offerts" className="mb-2 px-1 text-[13px] font-medium text-ink-2">
            Accès offerts
          </h2>
          <ul className="surface divide-y divide-line">
            {activeGrants.map((g) => (
              <li key={g.id} className="flex min-h-[52px] flex-wrap items-center justify-between gap-x-4 px-5 py-3">
                <span>{g.source === "promo" ? g.note || "Code promo" : "Offert par SMK Academy"}</span>
                <span className="text-ink-2">
                  {new Date(g.starts_at) > now ? `du ${formatDate(g.starts_at)} ` : ""}
                  {g.ends_at ? `jusqu'au ${formatDate(g.ends_at)}` : "sans limite"}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section aria-labelledby="code" className="mt-8">
        <h2 id="code" className="mb-2 px-1 text-[13px] font-medium text-ink-2">
          Code promo
        </h2>
        <div className="surface p-5">
          <RedeemForm />
        </div>
      </section>

      {(payments ?? []).length > 0 && (
        <section aria-labelledby="historique" className="mt-8">
          <h2 id="historique" className="mb-2 px-1 text-[13px] font-medium text-ink-2">
            Historique des paiements
          </h2>
          <ul className="surface divide-y divide-line">
            {(payments ?? []).map((p) => (
              <li key={p.id} className="flex min-h-[52px] items-center justify-between gap-4 px-5 py-3">
                <span className="text-ink-2">{formatDate(p.created_at)}</span>
                <span>
                  {formatPrice(p.amount_cents)}{" "}
                  <span className={p.status === "paid" ? "text-green" : "text-red"}>
                    · {p.status === "paid" ? "payé" : p.status === "failed" ? "échec" : "remboursé"}
                  </span>
                </span>
              </li>
            ))}
          </ul>
          <p className="mt-2 px-1 text-[13px] text-ink-3">Les factures détaillées sont disponibles dans l&apos;espace Stripe.</p>
        </section>
      )}
    </div>
  );
}
