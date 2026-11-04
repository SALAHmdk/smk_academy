import Link from "next/link";
import { notFound } from "next/navigation";
import { createLesson, createQuiz, updateModule } from "@/app/admin/actions";
import { ActionForm, Field, TextArea } from "@/components/admin/action-form";
import { StatusBadge } from "@/components/admin/status-badge";
import { requireAdmin } from "@/lib/admin";

type Props = { params: Promise<{ id: string }>; searchParams: Promise<{ erreur?: string }> };

export default async function AdminModulePage({ params, searchParams }: Props) {
  const { id } = await params;
  const { supabase } = await requireAdmin(`/admin/modules/${id}`);
  const { erreur } = await searchParams;
  const { data: mod } = await supabase
    .from("modules")
    .select("id, title, description, position, status, course_id, courses(id, title), lessons(id, title, position, duration_minutes), quizzes(id, title, quiz_questions(id))")
    .eq("id", id)
    .maybeSingle();
  if (!mod) notFound();
  const course = mod.courses as unknown as { id: string; title: string };
  const lessons = ((mod.lessons as unknown as { id: string; title: string; position: number; duration_minutes: number }[]) ?? []).sort(
    (a, b) => a.position - b.position,
  );
  const quiz = (mod.quizzes as unknown as { id: string; title: string; quiz_questions: { id: string }[] } | null) ?? null;

  return (
    <>
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/admin" className="hover:text-ink">
          Administration
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <Link href={`/admin/formations/${course.id}`} className="hover:text-ink">
          {course.title}
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <span>Module {mod.position}</span>
      </nav>
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <h1 className="t-1">{mod.title}</h1>
        <StatusBadge status={mod.status} />
      </div>
      {erreur === "derniere-lecon" && (
        <p role="alert" className="mt-4 rounded-[var(--radius-md)] bg-red-soft px-4 py-3 text-red">
          Impossible de supprimer la dernière leçon d&apos;un module publié. Repassez d&apos;abord le module en brouillon.
        </p>
      )}

      <section aria-labelledby="lecons" className="mt-10">
        <h2 id="lecons" className="t-2">
          Leçons
        </h2>
        <ul className="surface mt-4 divide-y divide-line overflow-hidden">
          {lessons.map((l) => (
            <li key={l.id}>
              <Link href={`/admin/lecons/${l.id}`} className="flex min-h-[52px] items-center gap-4 px-5 py-3 hover:bg-surface-2">
                <span className="w-16 text-sm font-semibold text-blue">Leçon {l.position}</span>
                <span className="min-w-0 flex-1 truncate">{l.title}</span>
                <span className="text-[13px] text-ink-3">{l.duration_minutes} min</span>
              </Link>
            </li>
          ))}
          <li className="p-5">
            <form action={createLesson} className="flex flex-wrap items-end gap-3">
              <input type="hidden" name="module_id" value={mod.id} />
              <div className="flex-1">
                <Field label="Nouvelle leçon" name="title" required maxLength={160} />
              </div>
              <button className="btn btn-secondary">Ajouter</button>
            </form>
          </li>
        </ul>
      </section>

      <section aria-labelledby="quiz" className="mt-10">
        <h2 id="quiz" className="t-2">
          Quiz du module
        </h2>
        <div className="surface mt-4 p-5">
          {quiz ? (
            <Link href={`/admin/quiz/${quiz.id}`} className="flex items-center justify-between gap-4">
              <span>
                <span className="block font-medium">{quiz.title}</span>
                <span className="text-[13px] text-ink-3">{quiz.quiz_questions?.length ?? 0} question(s)</span>
              </span>
              <span className="btn btn-secondary">Modifier</span>
            </Link>
          ) : (
            <form action={createQuiz} className="flex items-center justify-between gap-4">
              <input type="hidden" name="module_id" value={mod.id} />
              <span className="text-ink-2">Ce module n&apos;a pas encore de quiz.</span>
              <button className="btn btn-secondary">Créer le quiz</button>
            </form>
          )}
        </div>
      </section>

      <section aria-labelledby="reglages" className="mt-10">
        <h2 id="reglages" className="t-2">
          Réglages du module
        </h2>
        <div className="surface mt-4 p-6 sm:p-8">
          <ActionForm action={updateModule} submitLabel="Enregistrer">
            <input type="hidden" name="id" value={mod.id} />
            <div className="grid gap-5 sm:grid-cols-[1fr_120px_240px]">
              <Field label="Titre" name="title" defaultValue={mod.title} required maxLength={120} />
              <Field label="Position" name="position" type="number" defaultValue={mod.position} />
              <div className="field">
                <label htmlFor="status">Statut</label>
                <select id="status" name="status" className="input" defaultValue={mod.status}>
                  <option value="draft">Brouillon</option>
                  <option value="coming_soon">Bientôt disponible</option>
                  <option value="published">Publié</option>
                </select>
              </div>
            </div>
            <TextArea label="Description" name="description" defaultValue={mod.description} rows={2} maxLength={400} />
          </ActionForm>
        </div>
      </section>
    </>
  );
}
