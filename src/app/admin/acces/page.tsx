import { ActionForm, Field } from "@/components/admin/action-form";
import { DurationSelect } from "@/components/admin/duration-select";
import { grantPremium, revokePremium } from "@/app/admin/premium-actions";
import { requireAdmin } from "@/lib/admin";
import { formatDate } from "@/lib/format";

export default async function AdminGrants() {
  const { supabase } = await requireAdmin("/admin/acces");
  const { data: grants } = await supabase.rpc("admin_premium_members");
  const now = new Date();

  return (
    <>
      <h1 className="t-1">Accès offerts</h1>
      <p className="mt-2 max-w-2xl text-ink-2">
        Offrez directement un accès Premium gratuit à un client fidèle, pour une durée donnée ou sans limite. La personne
        doit déjà avoir un compte SMK Academy. Chaque attribution et chaque révocation sont inscrites au journal.
      </p>

      <section className="surface mt-8 p-6" aria-labelledby="offrir">
        <h2 id="offrir" className="t-3 mb-5">
          Offrir un accès Premium
        </h2>
        <ActionForm action={grantPremium} submitLabel="Offrir l'accès">
          <div className="grid gap-5 sm:grid-cols-2">
            <Field label="Email du compte" name="email" type="email" required />
            <DurationSelect max={120} defaultValue="illimite" />
          </div>
          <Field label="Note interne" name="note" maxLength={200} hint="Ex. client fidèle depuis 2024." />
        </ActionForm>
      </section>

      <section className="mt-10" aria-labelledby="liste-acces">
        <h2 id="liste-acces" className="t-2">
          Accès Premium attribués ({grants?.length ?? 0})
        </h2>
        <p className="mt-1 text-sm text-ink-2">Accès offerts par l&apos;administration et obtenus avec un code promo.</p>
        {(grants ?? []).length === 0 ? (
          <p className="mt-4 text-ink-2">Aucun accès offert pour l&apos;instant.</p>
        ) : (
          <ul className="surface mt-5 divide-y divide-line overflow-hidden">
            {(grants ?? []).map((g) => {
              const ended = g.revoked_at || (g.ends_at && new Date(g.ends_at) <= now);
              const upcoming = !ended && new Date(g.starts_at) > now;
              const [label, tone] = g.revoked_at
                ? ["Révoqué", "bg-surface-2 text-ink-3"]
                : ended
                  ? ["Terminé", "bg-surface-2 text-ink-3"]
                  : upcoming
                    ? ["À venir", "bg-blue-soft text-blue"]
                    : ["Actif", "bg-green-soft text-green"];
              return (
                <li key={g.grant_id} className="flex flex-wrap items-center gap-x-5 gap-y-2 px-5 py-4">
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">{g.email}</span>
                    <span className="text-[13px] text-ink-3">
                      {g.source === "promo" ? "Code promo" : "Offert par l'administration"} · du {formatDate(g.starts_at)}{" "}
                      {g.ends_at ? `au ${formatDate(g.ends_at)}` : "· sans limite"}
                      {g.note ? ` · ${g.note}` : ""}
                    </span>
                  </span>
                  <span className={`rounded-full px-3 py-1 text-[13px] font-medium ${tone}`}>{label}</span>
                  {!ended && (
                    <ActionForm action={revokePremium} submitLabel="Révoquer" className="flex items-center gap-2" subtle>
                      <input type="hidden" name="id" value={g.grant_id} />
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
