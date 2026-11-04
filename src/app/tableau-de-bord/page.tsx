import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { averageOfBest, formatScore, orderLessons, percent, type Module } from "@/lib/learning";
import { lessonHref } from "@/lib/queries";
import { createClient, getCurrentUser } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Tableau de bord", robots: { index: false } };

type Props = { searchParams: Promise<{ mdp?: string }> };

export default async function DashboardPage({ searchParams }: Props) {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion?suite=/tableau-de-bord");
  const { mdp } = await searchParams;

  const supabase = await createClient();
  const [{ data: profile }, { data: enrollments }, { data: attempts }, { data: progress }, { data: accessData }] = await Promise.all([
    supabase.from("profiles").select("full_name").eq("id", user.id).single(),
    supabase
      .from("enrollments")
      .select("course_id, last_lesson_id, last_activity_at, courses(id, slug, title, categories(name))")
      .order("last_activity_at", { ascending: false }),
    supabase
      .from("quiz_attempts")
      .select("id, quiz_id, score_20, passed, created_at, quizzes(title)")
      .order("created_at", { ascending: false })
      .limit(50),
    supabase.from("lesson_progress").select("lesson_id"),
    supabase.rpc("my_access"),
  ]);

  const courseIds = (enrollments ?? []).map((e) => e.course_id);
  const { data: modules } = courseIds.length
    ? await supabase
        .from("modules")
        .select("id, course_id, title, description, position, status")
        .in("course_id", courseIds)
        .eq("status", "published")
    : { data: [] as Module[] };
  const moduleIds = (modules ?? []).map((m) => m.id);
  const { data: lessons } = moduleIds.length
    ? await supabase.from("lessons").select("id, module_id, slug, title, position").in("module_id", moduleIds)
    : { data: [] as { id: string; module_id: string; slug: string; title: string; position: number }[] };

  const completed = new Set((progress ?? []).map((p) => p.lesson_id));
  const average = averageOfBest((attempts ?? []).map((a) => ({ quiz_id: a.quiz_id, score_20: Number(a.score_20) })));
  const passedQuizzes = new Set((attempts ?? []).filter((a) => a.passed).map((a) => a.quiz_id)).size;
  const firstName = profile?.full_name?.split(" ")[0];

  const courses = (enrollments ?? []).map((e) => {
    const course = e.courses as unknown as { id: string; slug: string; title: string; categories: { name: string } | null };
    const mods = (modules ?? []).filter((m) => m.course_id === e.course_id);
    const ordered = orderLessons(mods, (lessons ?? []).filter((l) => mods.some((m) => m.id === l.module_id)));
    const done = ordered.filter((l) => completed.has(l.id)).length;
    const resume =
      ordered.find((l) => l.id === e.last_lesson_id && !completed.has(l.id)) ??
      ordered.find((l) => !completed.has(l.id)) ??
      ordered.find((l) => l.id === e.last_lesson_id) ??
      ordered[0];
    const resumeMod = resume && mods.find((m) => m.id === resume.module_id);
    return {
      course,
      done,
      total: ordered.length,
      pct: percent(done, ordered.length),
      resume: resume && resumeMod ? { title: resume.title, href: lessonHref(course.slug, resumeMod.position, resume.slug) } : null,
    };
  });

  return (
    <div className="mx-auto max-w-5xl px-5 pt-12">
      {mdp === "ok" && (
        <p role="status" className="mb-6 rounded-[var(--radius-md)] bg-green-soft px-4 py-3 text-green">
          Mot de passe mis à jour.
        </p>
      )}
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="t-1">{firstName ? `Bonjour ${firstName}` : "Mon tableau de bord"}</h1>
          <p className="mt-2 text-ink-2">
            Offre {(accessData as { premium?: boolean } | null)?.premium ? "SMK Premium" : "SMK Free"}, connecté avec {user.email}
          </p>
        </div>
      </header>

      <dl className="mt-8 grid grid-cols-3 gap-px overflow-hidden rounded-[var(--radius-lg)] bg-line">
        <div className="bg-surface p-5 sm:p-6">
          <dt className="text-sm text-ink-2">Moyenne</dt>
          <dd className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">
            {average === null ? "—" : `${formatScore(average)}/20`}
          </dd>
        </div>
        <div className="bg-surface p-5 sm:p-6">
          <dt className="text-sm text-ink-2">Leçons terminées</dt>
          <dd className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">{completed.size}</dd>
        </div>
        <div className="bg-surface p-5 sm:p-6">
          <dt className="text-sm text-ink-2">Quiz validés</dt>
          <dd className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">{passedQuizzes}</dd>
        </div>
      </dl>

      <section aria-labelledby="mes-formations" className="mt-12">
        <h2 id="mes-formations" className="t-2">
          Mes formations
        </h2>
        {courses.length === 0 ? (
          <div className="surface mt-5 p-8">
            <p className="t-3">Vous n&apos;avez pas encore commencé de formation.</p>
            <p className="mt-2 text-ink-2">Choisissez-en une dans le catalogue : la première leçon prend une vingtaine de minutes.</p>
            <Link href="/formations" className="btn btn-primary mt-5">
              Parcourir les formations
            </Link>
          </div>
        ) : (
          <ul className="mt-5 space-y-4">
            {courses.map(({ course, done, total, pct, resume }) => (
              <li key={course.id} className="surface p-6 sm:p-7">
                <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-ink-3">{course.categories?.name}</p>
                    <Link href={`/formations/${course.slug}`} className="t-3 mt-1 block hover:text-blue">
                      {course.title}
                    </Link>
                    <div className="mt-4 flex items-center gap-3">
                      <div
                        className="progress flex-1"
                        data-complete={pct === 100}
                        role="progressbar"
                        aria-valuenow={pct}
                        aria-valuemin={0}
                        aria-valuemax={100}
                        aria-label={`Progression : ${course.title}`}
                      >
                        <span style={{ width: `${pct}%` }} />
                      </div>
                      <span className="w-28 text-right text-sm text-ink-2">
                        {done}/{total} leçons
                      </span>
                    </div>
                    {resume && <p className="mt-3 truncate text-sm text-ink-2">Prochaine étape : {resume.title}</p>}
                  </div>
                  {resume && (
                    <Link href={resume.href} className="btn btn-primary sm:ml-6">
                      Reprendre ma formation
                    </Link>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-labelledby="historique" className="mt-12">
        <h2 id="historique" className="t-2">
          Historique des quiz
        </h2>
        {(attempts ?? []).length === 0 ? (
          <p className="mt-3 text-ink-2">Vos notes apparaîtront ici après votre premier quiz.</p>
        ) : (
          <ul className="surface mt-5 overflow-hidden">
            {(attempts ?? []).slice(0, 10).map((a) => (
              <li key={a.id} className="border-b border-line last:border-b-0">
                <Link href={`/resultats/${a.id}`} className="flex min-h-[60px] items-center gap-4 px-6 py-3 hover:bg-surface-2">
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-medium">{(a.quizzes as unknown as { title: string } | null)?.title ?? "Quiz"}</p>
                    <p className="text-sm text-ink-3">
                      {new Date(a.created_at).toLocaleString("fr-FR", { dateStyle: "medium", timeStyle: "short", timeZone: "Europe/Paris" })}
                    </p>
                  </div>
                  <span className={`text-lg font-bold ${a.passed ? "text-green" : "text-ink-2"}`}>
                    {formatScore(Number(a.score_20))}/20
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
