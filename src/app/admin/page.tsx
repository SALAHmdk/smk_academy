import Link from "next/link";
import { StatusBadge } from "@/components/admin/status-badge";
import { requireAdmin } from "@/lib/admin";
import { formatScore } from "@/lib/learning";

type Props = { searchParams: Promise<{ statut?: string; q?: string; supprime?: string }> };

const ENTITY: Record<string, string> = {
  courses: "Formation",
  modules: "Module",
  lessons: "Leçon",
  quizzes: "Quiz",
  quiz_questions: "Question",
  quiz_answer_keys: "Corrigé",
  categories: "Catégorie",
  profiles: "Profil",
};
const ACTION: Record<string, string> = { INSERT: "Création", UPDATE: "Modification", DELETE: "Suppression" };

export default async function AdminHome({ searchParams }: Props) {
  const { supabase } = await requireAdmin("/admin");
  const params = await searchParams;
  const [{ data: stats }, { data: courses }, { data: log }] = await Promise.all([
    supabase.rpc("admin_stats"),
    supabase
      .from("courses")
      .select("id, slug, title, status, topic, updated_at, categories(name), modules(id, status)")
      .order("position"),
    supabase.rpc("admin_audit_log", { p_limit: 15 }),
  ]);
  const s = (stats ?? {}) as Record<string, number | null>;
  const q = (params.q ?? "").toLowerCase();
  const list = (courses ?? []).filter(
    (c) => (!params.statut || c.status === params.statut) && (!q || c.title.toLowerCase().includes(q) || c.topic.toLowerCase().includes(q)),
  );

  const tiles = [
    ["Étudiants", s.students],
    ["Formations publiées", s.courses_published],
    ["Annoncées", s.courses_coming_soon],
    ["Brouillons", s.courses_draft],
    ["Inscriptions", s.enrollments],
    ["Quiz passés", s.quiz_attempts],
    ["Note moyenne", s.average_score === null || s.average_score === undefined ? "—" : `${formatScore(Number(s.average_score))}/20`],
  ] as const;

  return (
    <>
      {params.supprime && (
        <p role="status" className="mb-6 rounded-[var(--radius-md)] bg-surface-2 px-4 py-3">
          Brouillon supprimé.
        </p>
      )}
      <div className="flex flex-wrap items-end justify-between gap-4">
        <h1 className="t-1">Tableau de bord</h1>
        <Link href="/admin/formations/nouvelle" className="btn btn-primary">
          Nouvelle formation
        </Link>
      </div>

      <dl className="mt-8 grid grid-cols-2 gap-px overflow-hidden rounded-[var(--radius-lg)] bg-line sm:grid-cols-4 lg:grid-cols-7">
        {tiles.map(([label, value]) => (
          <div key={label} className="bg-surface p-4">
            <dt className="text-[13px] text-ink-2">{label}</dt>
            <dd className="mt-1 text-2xl font-bold tracking-tight">{value ?? 0}</dd>
          </div>
        ))}
      </dl>

      <section aria-labelledby="formations" className="mt-12">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h2 id="formations" className="t-2">
            Formations ({list.length})
          </h2>
          <form className="flex flex-wrap gap-2" action="/admin">
            <input name="q" defaultValue={params.q} placeholder="Rechercher" className="input !min-h-[40px] w-44" aria-label="Rechercher une formation" />
            <select name="statut" defaultValue={params.statut ?? ""} className="input !min-h-[40px] w-48" aria-label="Filtrer par statut">
              <option value="">Tous les statuts</option>
              <option value="published">Publiées</option>
              <option value="coming_soon">Bientôt disponibles</option>
              <option value="draft">Brouillons</option>
            </select>
            <button className="btn btn-secondary min-h-[40px] py-1.5">Filtrer</button>
          </form>
        </div>
        <ul className="surface mt-5 divide-y divide-line overflow-hidden">
          {list.map((c) => {
            const mods = (c.modules as unknown as { status: string }[]) ?? [];
            const pub = mods.filter((m) => m.status === "published").length;
            return (
              <li key={c.id}>
                <Link href={`/admin/formations/${c.id}`} className="flex min-h-[60px] flex-wrap items-center gap-x-4 gap-y-1 px-5 py-3 hover:bg-surface-2">
                  <span className="min-w-0 flex-1">
                    <span className="block truncate font-medium">{c.title}</span>
                    <span className="text-[13px] text-ink-3">
                      {(c.categories as unknown as { name: string } | null)?.name} · {pub}/{mods.length} modules publiés
                    </span>
                  </span>
                  <StatusBadge status={c.status} />
                </Link>
              </li>
            );
          })}
        </ul>
      </section>

      <section aria-labelledby="journal" className="mt-12">
        <h2 id="journal" className="t-2">
          Journal des modifications
        </h2>
        <p className="mt-1 text-sm text-ink-2">Créations, modifications et suppressions de contenu, de corrigés et de rôles.</p>
        {(log ?? []).length === 0 ? (
          <p className="mt-4 text-ink-2">Aucune modification enregistrée pour l&apos;instant.</p>
        ) : (
          <ul className="surface mt-5 divide-y divide-line text-[14px]">
            {(log ?? []).map((e, i) => {
              const summary = (e.summary ?? {}) as Record<string, string>;
              return (
                <li key={i} className="flex flex-wrap gap-x-4 gap-y-1 px-5 py-3">
                  <span className="w-36 shrink-0 text-ink-3">
                    {new Date(e.at).toLocaleString("fr-FR", { dateStyle: "short", timeStyle: "short", timeZone: "Europe/Paris" })}
                  </span>
                  <span className="min-w-0 flex-1">
                    {ACTION[e.action] ?? e.action} · {ENTITY[e.entity] ?? e.entity}
                    {summary.title ? ` « ${summary.title} »` : ""}
                    {summary.old_status && summary.status && summary.old_status !== summary.status ? ` (${summary.old_status} → ${summary.status})` : ""}
                    {summary.old_role && summary.role && summary.old_role !== summary.role ? ` (rôle ${summary.old_role} → ${summary.role})` : ""}
                  </span>
                  <span className="text-ink-3">{e.actor_email ?? "système"}</span>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </>
  );
}
