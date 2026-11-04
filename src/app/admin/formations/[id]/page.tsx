import Link from "next/link";
import { notFound } from "next/navigation";
import { createModule, deleteDraftCourse, updateCourse } from "@/app/admin/actions";
import { ActionForm, Field } from "@/components/admin/action-form";
import { CourseFields } from "@/components/admin/course-fields";
import { StatusBadge } from "@/components/admin/status-badge";
import { ChevronIcon } from "@/components/icons";
import { requireAdmin } from "@/lib/admin";

type Props = { params: Promise<{ id: string }>; searchParams: Promise<{ cree?: string }> };

export default async function AdminCoursePage({ params, searchParams }: Props) {
  const { id } = await params;
  const { supabase } = await requireAdmin(`/admin/formations/${id}`);
  const { cree } = await searchParams;
  const [{ data: course }, { data: categories }, { data: modules }] = await Promise.all([
    supabase.from("courses").select("*").eq("id", id).maybeSingle(),
    supabase.from("categories").select("id, slug, name, description, position").order("position"),
    supabase.from("modules").select("id, title, position, status, lessons(id), quizzes(id)").eq("course_id", id).order("position"),
  ]);
  if (!course) notFound();

  return (
    <>
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/admin" className="hover:text-ink">
          Administration
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>{course.title}</span>
      </nav>
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <h1 className="t-1">{course.title}</h1>
        <StatusBadge status={course.status} />
      </div>
      {course.status !== "draft" && (
        <Link href={`/formations/${course.slug}`} className="link-more">
          Voir la page publique <ChevronIcon className="h-4 w-4" />
        </Link>
      )}
      {cree && (
        <p role="status" className="mt-4 rounded-[var(--radius-md)] bg-green-soft px-4 py-3 text-green">
          Brouillon créé. Ajoutez maintenant un premier module.
        </p>
      )}

      <section aria-labelledby="modules" className="mt-10">
        <h2 id="modules" className="t-2">
          Modules
        </h2>
        <p className="mt-1 text-sm text-ink-2">
          Un module ne peut être publié qu&apos;avec au moins une leçon et un quiz dont toutes les questions ont un corrigé.
        </p>
        <ul className="surface mt-4 divide-y divide-line overflow-hidden">
          {(modules ?? []).map((m) => (
            <li key={m.id}>
              <Link href={`/admin/modules/${m.id}`} className="flex min-h-[56px] items-center gap-4 px-5 py-3 hover:bg-surface-2">
                <span className="w-16 text-sm font-semibold text-blue">Module {m.position}</span>
                <span className="min-w-0 flex-1 truncate">{m.title}</span>
                <span className="hidden text-[13px] text-ink-3 sm:inline">
                  {(m.lessons as unknown as unknown[] | null)?.length ?? 0} leçon(s), {m.quizzes ? "quiz" : "pas de quiz"}
                </span>
                <StatusBadge status={m.status} />
              </Link>
            </li>
          ))}
          <li className="p-5">
            <form action={createModule} className="flex flex-wrap items-end gap-3">
              <input type="hidden" name="course_id" value={course.id} />
              <div className="flex-1">
                <Field label="Nouveau module" name="title" required maxLength={120} />
              </div>
              <button className="btn btn-secondary">Ajouter</button>
            </form>
          </li>
        </ul>
      </section>

      <section aria-labelledby="infos" className="mt-12">
        <h2 id="infos" className="t-2">
          Fiche de la formation
        </h2>
        <div className="surface mt-4 p-6 sm:p-8">
          <ActionForm action={updateCourse} submitLabel="Enregistrer">
            <input type="hidden" name="id" value={course.id} />
            <div className="field max-w-sm">
              <label htmlFor="status">Statut</label>
              <select id="status" name="status" className="input" defaultValue={course.status}>
                <option value="draft">Brouillon (invisible)</option>
                <option value="coming_soon">Bientôt disponible (annoncée)</option>
                <option value="published">Publiée (accessible)</option>
              </select>
              <p className="text-sm text-ink-3">La publication est refusée tant qu&apos;aucun module complet n&apos;est publié.</p>
            </div>
            <CourseFields categories={categories ?? []} values={course} slugHint="Modifier le slug change l'adresse publique de la formation." />
          </ActionForm>
        </div>
      </section>

      {course.status === "draft" && (
        <section aria-labelledby="supprimer" className="mt-12">
          <h2 id="supprimer" className="t-3 text-red">
            Supprimer ce brouillon
          </h2>
          <div className="surface mt-4 p-6">
            <ActionForm action={deleteDraftCourse} submitLabel="Supprimer définitivement" danger className="grid gap-4 sm:max-w-md">
              <input type="hidden" name="id" value={course.id} />
              <Field label="Tapez SUPPRIMER pour confirmer" name="confirm" required />
            </ActionForm>
          </div>
        </section>
      )}
    </>
  );
}
