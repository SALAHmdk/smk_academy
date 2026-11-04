import { ActionForm, Field } from "@/components/admin/action-form";
import { DurationSelect } from "@/components/admin/duration-select";
import { createPromoCode, disablePromoCode } from "@/app/admin/premium-actions";
import { requireAdmin } from "@/lib/admin";
import { formatDate, formatMonths } from "@/lib/format";

function codeStatus(c: {
  disabled_at: string | null;
  expires_at: string | null;
  redemptions_count: number;
  max_redemptions: number;
}): [string, string] {
  if (c.disabled_at) return ["Désactivé", "bg-surface-2 text-ink-3"];
  if (c.expires_at && new Date(c.expires_at) <= new Date()) return ["Expiré", "bg-surface-2 text-ink-3"];
  if (c.redemptions_count >= c.max_redemptions) return ["Épuisé", "bg-surface-2 text-ink-2"];
  return ["Actif", "bg-green-soft text-green"];
}

export default async function AdminPromoCodes() {
  const { supabase } = await requireAdmin("/admin/codes-promo");
  const { data: codes } = await supabase.from("promo_codes").select("*").order("created_at", { ascending: false }).limit(300);

  return (
    <>
      <h1 className="t-1">Codes promo</h1>
      <p className="mt-2 max-w-2xl text-ink-2">
        Un code offre un accès Premium pendant la durée choisie. Il peut être <strong>personnel</strong> (réservé à une
        adresse email, une seule utilisation) ou <strong>partagé</strong> (plusieurs personnes, jusqu&apos;au nombre
        d&apos;utilisations fixé). Les mois offerts s&apos;ajoutent à l&apos;accès déjà en cours.
      </p>

      <section className="surface mt-8 p-6" aria-labelledby="nouveau-code">
        <h2 id="nouveau-code" className="t-3 mb-5">
          Générer un code
        </h2>
        <ActionForm action={createPromoCode} submitLabel="Générer le code" pendingLabel="Génération…">
          <div className="grid gap-5 sm:grid-cols-2">
            <DurationSelect max={60} />
            <Field label="Nombre d'utilisations" name="max_redemptions" type="number" defaultValue={1} inputMode="numeric" />
            <Field
              label="Réservé à l'adresse (facultatif)"
              name="restricted_email"
              type="email"
              hint="Code personnel : seule cette personne pourra l'utiliser (1 utilisation)."
            />
            <Field label="Valable jusqu'au (facultatif)" name="expires_on" type="date" hint="Date limite pour saisir le code." />
            <Field label="Note interne" name="note" maxLength={200} hint="Ex. client fidèle, partenaire, salon…" />
            <Field
              label="Code personnalisé (facultatif)"
              name="code"
              maxLength={32}
              hint="Laissez vide pour un code aléatoire sûr (SMK-XXXX-XXXX-XXXX)."
            />
          </div>
        </ActionForm>
      </section>

      <section className="mt-10" aria-labelledby="liste-codes">
        <h2 id="liste-codes" className="t-2">
          Codes créés ({codes?.length ?? 0})
        </h2>
        {(codes ?? []).length === 0 ? (
          <p className="mt-4 text-ink-2">Aucun code pour l&apos;instant.</p>
        ) : (
          <ul className="surface mt-5 divide-y divide-line overflow-hidden">
            {(codes ?? []).map((c) => {
              const [label, tone] = codeStatus(c);
              return (
                <li key={c.id} className="flex flex-wrap items-center gap-x-5 gap-y-2 px-5 py-4">
                  <span className="min-w-0 flex-1">
                    <span className="block font-mono text-[15px] font-semibold tracking-wide">{c.code}</span>
                    <span className="text-[13px] text-ink-3">
                      {formatMonths(c.months)} · {c.redemptions_count}/{c.max_redemptions} utilisation
                      {c.max_redemptions > 1 ? "s" : ""}
                      {c.restricted_email ? ` · pour ${c.restricted_email}` : " · partagé"}
                      {c.expires_at ? ` · jusqu'au ${formatDate(c.expires_at)}` : ""}
                      {c.note ? ` · ${c.note}` : ""}
                    </span>
                  </span>
                  <span className={`rounded-full px-3 py-1 text-[13px] font-medium ${tone}`}>{label}</span>
                  {label === "Actif" && (
                    <ActionForm action={disablePromoCode} submitLabel="Désactiver" className="flex items-center gap-2" subtle>
                      <input type="hidden" name="id" value={c.id} />
                    </ActionForm>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </>
  );
}
