import { requireAdmin } from "@/lib/admin";
import { formatDate, formatPrice } from "@/lib/format";
import { stripeStatus } from "@/lib/stripe";

type Overview = {
  payments: { id: string; email: string | null; provider: string; provider_ref: string; plan_id: string | null; amount_cents: number; status: string; created_at: string }[];
  subscriptions: { id: string; email: string; provider: string; plan_id: string | null; status: string; current_period_end: string | null; cancel_at_period_end: boolean; updated_at: string }[];
  totals: { paid_cents: number; failed: number; active_subscriptions: number; premium_members: number; free_members: number };
};

const PLAN: Record<string, string> = { premium_monthly: "Premium mensuel", premium_yearly: "Premium annuel", free: "Free" };
const PAY_STATUS: Record<string, [string, string]> = {
  paid: ["Payé", "bg-green-soft text-green"],
  failed: ["Échec", "bg-red-soft text-red"],
  refunded: ["Remboursé", "bg-surface-2 text-ink-2"],
};
const SUB_STATUS: Record<string, string> = {
  active: "Actif",
  trialing: "Essai",
  past_due: "Paiement en retard",
  canceled: "Résilié",
  unpaid: "Impayé",
  incomplete: "Incomplet",
  incomplete_expired: "Expiré",
};

export default async function AdminPayments() {
  const { supabase } = await requireAdmin("/admin/paiements");
  const { data } = await supabase.rpc("admin_payments_overview");
  const o = (data ?? { payments: [], subscriptions: [], totals: {} }) as unknown as Overview;
  const cfg = stripeStatus();
  const ready = cfg.secretKey === "test" && cfg.webhookSecret === "présente" && cfg.dbToken === "présent";

  const tiles = [
    ["Encaissé (mode test)", formatPrice(o.totals.paid_cents ?? 0)],
    ["Abonnements actifs", o.totals.active_subscriptions ?? 0],
    ["Membres Premium", o.totals.premium_members ?? 0],
    ["Étudiants Free", o.totals.free_members ?? 0],
    ["Paiements échoués", o.totals.failed ?? 0],
  ] as const;

  return (
    <>
      <h1 className="t-1">Paiements</h1>
      <p className="mt-2 max-w-2xl text-ink-2">
        Données réelles synchronisées par les webhooks Stripe signés. La plateforme est en <strong>mode test</strong> : tout
        paiement réel est refusé par la base.
      </p>

      <section
        className={`mt-6 rounded-[var(--radius-lg)] p-5 ${ready ? "bg-green-soft" : "bg-surface-2"}`}
        aria-labelledby="config-stripe"
      >
        <h2 id="config-stripe" className="font-semibold">
          {ready ? "Stripe (mode test) configuré" : "Stripe (mode test) : configuration à terminer"}
        </h2>
        <ul className="mt-2 grid gap-1 text-[14px] text-ink-2 sm:grid-cols-3">
          <li>Clé secrète : {cfg.secretKey}</li>
          <li>Secret du webhook : {cfg.webhookSecret}</li>
          <li>Jeton base de données : {cfg.dbToken}</li>
        </ul>
        {!ready && (
          <p className="mt-2 text-[14px] text-ink-2">
            Tant que ces trois réglages ne sont pas présents dans Netlify, le bouton d&apos;abonnement indique que le
            paiement en ligne arrive bientôt ; les codes promo et les accès offerts fonctionnent déjà.
          </p>
        )}
      </section>

      <dl className="mt-8 grid grid-cols-2 gap-px overflow-hidden rounded-[var(--radius-lg)] bg-line sm:grid-cols-5">
        {tiles.map(([label, value]) => (
          <div key={label} className="bg-surface p-4">
            <dt className="text-[13px] text-ink-2">{label}</dt>
            <dd className="mt-1 text-2xl font-bold tracking-tight">{value}</dd>
          </div>
        ))}
      </dl>

      <section className="mt-10" aria-labelledby="abonnements">
        <h2 id="abonnements" className="t-2">
          Abonnements ({o.subscriptions.length})
        </h2>
        {o.subscriptions.length === 0 ? (
          <p className="mt-4 text-ink-2">Aucun abonnement pour l&apos;instant.</p>
        ) : (
          <ul className="surface mt-5 divide-y divide-line overflow-hidden">
            {o.subscriptions.map((s) => (
              <li key={s.id} className="flex flex-wrap items-center gap-x-5 gap-y-1 px-5 py-4">
                <span className="min-w-0 flex-1">
                  <span className="block truncate font-medium">{s.email}</span>
                  <span className="text-[13px] text-ink-3">
                    {PLAN[s.plan_id ?? ""] ?? "Offre inconnue"} · {s.provider === "stripe" ? "Stripe" : "PayPal"} ·{" "}
                    {s.cancel_at_period_end ? "se termine" : "renouvellement"} le {formatDate(s.current_period_end)}
                  </span>
                </span>
                <span className="rounded-full bg-surface-2 px-3 py-1 text-[13px] font-medium">{SUB_STATUS[s.status] ?? s.status}</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="mt-10" aria-labelledby="transactions">
        <h2 id="transactions" className="t-2">
          Transactions ({o.payments.length})
        </h2>
        {o.payments.length === 0 ? (
          <p className="mt-4 text-ink-2">Aucune transaction pour l&apos;instant.</p>
        ) : (
          <ul className="surface mt-5 divide-y divide-line overflow-hidden">
            {o.payments.map((p) => {
              const [label, tone] = PAY_STATUS[p.status] ?? [p.status, "bg-surface-2"];
              return (
                <li key={p.id} className="flex flex-wrap items-center gap-x-5 gap-y-1 px-5 py-4">
                  <span className="w-36 shrink-0 text-[14px] text-ink-3">{formatDate(p.created_at, true)}</span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">{p.email ?? "Compte supprimé"}</span>
                    <span className="text-[13px] text-ink-3">
                      {PLAN[p.plan_id ?? ""] ?? "—"} · {p.provider_ref}
                    </span>
                  </span>
                  <span className="font-semibold">{formatPrice(p.amount_cents)}</span>
                  <span className={`rounded-full px-3 py-1 text-[13px] font-medium ${tone}`}>{label}</span>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </>
  );
}
