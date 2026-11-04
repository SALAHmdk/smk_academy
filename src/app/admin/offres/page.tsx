import { ActionForm, Field, TextArea } from "@/components/admin/action-form";
import { updatePlan } from "@/app/admin/premium-actions";
import { requireAdmin } from "@/lib/admin";
import { formatDate, formatPlanPrice } from "@/lib/format";

export default async function AdminPlans() {
  const { supabase } = await requireAdmin("/admin/offres");
  const { data: plans } = await supabase.from("plans").select("*").order("position");

  return (
    <>
      <h1 className="t-1">Offres et prix</h1>
      <p className="mt-2 max-w-2xl text-ink-2">
        Les prix sont lus en base au moment du paiement : le navigateur ne peut jamais imposer un montant. Un changement
        de prix s&apos;applique aux nouveaux abonnements ; les abonnements en cours gardent leur prix.
      </p>

      <div className="mt-8 grid gap-6">
        {(plans ?? []).map((p) => (
          <section key={p.id} className="surface p-6" aria-labelledby={`plan-${p.id}`}>
            <div className="mb-5 flex flex-wrap items-baseline justify-between gap-2">
              <h2 id={`plan-${p.id}`} className="t-3">
                {p.name} — {formatPlanPrice(p.price_cents, p.billing_interval)}
              </h2>
              <span className="text-[13px] text-ink-3">Modifiée le {formatDate(p.updated_at, true)}</span>
            </div>
            <ActionForm action={updatePlan} submitLabel="Enregistrer l'offre">
              <input type="hidden" name="id" value={p.id} />
              <div className="grid gap-5 sm:grid-cols-[1fr_180px]">
                <Field label="Nom affiché" name="name" defaultValue={p.name} required maxLength={60} />
                {p.id === "free" ? (
                  <Field label="Prix (€)" name="price" defaultValue="0" hint="Offre gratuite : toujours 0 €." />
                ) : (
                  <Field
                    label={`Prix TTC (€ / ${p.billing_interval === "year" ? "an" : "mois"})`}
                    name="price"
                    defaultValue={(p.price_cents / 100).toString().replace(".", ",")}
                    inputMode="text"
                    required
                  />
                )}
              </div>
              <Field label="Accroche" name="tagline" defaultValue={p.tagline} maxLength={160} />
              <TextArea
                label="Avantages (un par ligne)"
                name="features"
                defaultValue={p.features.join("\n")}
                rows={6}
                hint="Affichés tels quels sur la page Tarifs. N'annoncez que ce qui existe réellement."
              />
              {p.id !== "free" && (
                <label className="flex items-center gap-3 text-[15px]">
                  <input type="checkbox" name="is_active" defaultChecked={p.is_active} className="h-5 w-5 accent-[var(--smk-blue)]" />
                  Offre proposée à la vente
                </label>
              )}
            </ActionForm>
          </section>
        ))}
      </div>
    </>
  );
}
