import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { enrollInCourse } from "@/app/actions/learning";
import { CourseCover } from "@/components/course-cover";
import { StatusDot } from "@/components/icons";
import { formatDuration, formatScore, LEVEL_LABEL, percent } from "@/lib/learning";
import { getCourseOutline, getUserCourseState, lessonHref, quizHref } from "@/lib/queries";
import { getCurrentUser } from "@/lib/supabase/server";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const outline = await getCourseOutline((await params).slug);
  if (!outline) return { title: "Formation introuvable" };
  return { title: outline.course.title, description: outline.course.description };
}

export default async function CoursePage({ params }: Props) {
  const { slug } = await params;
  const [outline, user] = await Promise.all([getCourseOutline(slug), getCurrentUser()]);
  if (!outline || outline.course.status === "draft") notFound();
  const upcoming = outline.course.status !== "published";

  const { course, modules, lessons, quizzes } = outline;
  const state = user && !upcoming
    ? await getUserCourseState(
        course.id,
        lessons.map((l) => l.id),
        quizzes.map((q) => q.id),
      )
    : null;

  const modulePos = new Map(modules.map((m) => [m.id, m.position]));
  const firstLesson = lessons[0];
  const nextLesson =
    lessons.find((l) => l.id === state?.lastLessonId && !state?.completedLessonIds.has(l.id)) ??
    lessons.find((l) => !state?.completedLessonIds.has(l.id)) ??
    firstLesson;
  const done = state ? lessons.filter((l) => state.completedLessonIds.has(l.id)).length : 0;
  const progress = percent(done, lessons.length);
  const publishedModules = modules.filter((m) => m.status === "published");

  return (
    <div className="mx-auto max-w-5xl px-5 pt-12">
      <nav aria-label="Fil d'Ariane" className="text-sm text-ink-2">
        <Link href="/formations" className="hover:text-ink">
          Formations
        </Link>
        <span className="mx-2 text-ink-3">/</span>
        <Link href={`/formations?categorie=${course.categories?.slug ?? ""}`} className="hover:text-ink">
          {course.categories?.name}
        </Link>
      </nav>

      <header className="mt-5 grid gap-8 md:grid-cols-[1.5fr_1fr] md:items-end">
        <div>
          <h1 className="t-1">{course.title}</h1>
          <p className="mt-4 max-w-[58ch] text-lg text-ink-2">{course.description}</p>
        </div>

        <div className="surface overflow-hidden">
          <div className="aspect-[16/7]">
            <CourseCover label={course.cover_label} category={course.categories?.slug} size="lg" muted={upcoming} />
          </div>
          <div className="p-6">
          <dl className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <dt className="text-ink-3">Niveau</dt>
              <dd className="mt-0.5 font-semibold">{LEVEL_LABEL[course.level]}</dd>
            </div>
            <div>
              <dt className="text-ink-3">Durée estimée</dt>
              <dd className="mt-0.5 font-semibold">{formatDuration(course.duration_minutes)}</dd>
            </div>
            <div>
              <dt className="text-ink-3">Accès</dt>
              <dd className="mt-0.5 font-semibold">{course.is_premium ? "Premium" : "Gratuit"}</dd>
            </div>
          </dl>

          {state?.enrolled && (
            <div className="mt-5">
              <div className="mb-1.5 flex justify-between text-sm">
                <span className="text-ink-2">Progression</span>
                <span className="font-semibold">{progress} %</span>
              </div>
              <div
                className="progress"
                data-complete={progress === 100}
                role="progressbar"
                aria-valuenow={progress}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label="Progression dans la formation"
              >
                <span style={{ width: `${progress}%` }} />
              </div>
            </div>
          )}

          <div className="mt-5">
            {upcoming ? (
              <div>
                <span className="btn w-full cursor-default bg-surface-2 text-ink-2" aria-disabled="true">
                  Bientôt disponible
                </span>
                <p className="mt-3 text-sm text-ink-2">
                  Le programme est défini et le contenu est en cours de rédaction. La formation s&apos;ouvrira dès que
                  ses premiers modules seront complets.
                </p>
              </div>
            ) : !user ? (
              <Link href={`/inscription?suite=/formations/${slug}`} className="btn btn-primary w-full">
                Créer un compte pour commencer
              </Link>
            ) : !state?.enrolled ? (
              <form action={enrollInCourse}>
                <input type="hidden" name="courseId" value={course.id} />
                <input
                  type="hidden"
                  name="next"
                  value={firstLesson ? lessonHref(slug, modulePos.get(firstLesson.module_id)!, firstLesson.slug) : `/formations/${slug}`}
                />
                <button type="submit" className="btn btn-primary w-full">
                  Commencer la formation
                </button>
              </form>
            ) : nextLesson ? (
              <Link
                href={lessonHref(slug, modulePos.get(nextLesson.module_id)!, nextLesson.slug)}
                className="btn btn-primary w-full"
              >
                {done === 0 ? "Commencer la première leçon" : "Reprendre ma formation"}
              </Link>
            ) : null}
          </div>
          </div>
        </div>
      </header>

      <div className="mt-12 grid gap-10 md:grid-cols-2">
        <section aria-labelledby="objectifs">
          <h2 id="objectifs" className="t-3">
            Ce que vous saurez faire
          </h2>
          <ul className="mt-3 space-y-2 text-ink-2">
            {course.objectives.map((o) => (
              <li key={o} className="flex gap-3">
                <span aria-hidden="true" className="mt-[0.6em] h-1.5 w-1.5 shrink-0 rounded-full bg-blue" />
                {o}
              </li>
            ))}
          </ul>
        </section>
        <section aria-labelledby="prerequis">
          <h2 id="prerequis" className="t-3">
            Prérequis
          </h2>
          <ul className="mt-3 space-y-2 text-ink-2">
            {course.prerequisites.map((p) => (
              <li key={p} className="flex gap-3">
                <span aria-hidden="true" className="mt-[0.6em] h-1.5 w-1.5 shrink-0 rounded-full bg-ink-3" />
                {p}
              </li>
            ))}
          </ul>
        </section>
      </div>

      {modules.length > 0 && (
      <section aria-labelledby="programme" className="mt-14">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 id="programme" className="t-2">
            Programme
          </h2>
          <p className="text-sm text-ink-2">
            {publishedModules.length} modules ouverts sur {modules.length}
          </p>
        </div>

        <ol className="mt-5 space-y-4">
          {modules.map((m) => {
            const modLessons = lessons.filter((l) => l.module_id === m.id);
            const quiz = quizzes.find((q) => q.module_id === m.id);
            const best = quiz ? state?.bestScoreByQuiz.get(quiz.id) : undefined;
            const open = m.status === "published";

            return (
              <li key={m.id} className="surface overflow-hidden">
                <div className="flex items-start justify-between gap-4 p-6 pb-4">
                  <div>
                    <p className="text-sm font-semibold text-blue">Module {m.position}</p>
                    <h3 className="t-3 mt-1">{m.title}</h3>
                    <p className="mt-1 text-ink-2">{m.description}</p>
                  </div>
                  {!open && (
                    <span className="shrink-0 rounded-full bg-surface-2 px-3 py-1 text-sm text-ink-2">En préparation</span>
                  )}
                </div>

                {open && !user && (
                  <p className="border-t border-line px-6 py-4 text-sm text-ink-2">
                    3 leçons, des exercices corrigés et un quiz noté sur 20.{" "}
                    <Link href={`/connexion?suite=/formations/${slug}`} className="font-medium text-blue">
                      Connectez-vous
                    </Link>{" "}
                    pour y accéder.
                  </p>
                )}

                {open && user && (
                  <ul className="border-t border-line">
                    {modLessons.map((l) => {
                      const st = state?.completedLessonIds.has(l.id)
                        ? "done"
                        : state?.lastLessonId === l.id
                          ? "current"
                          : "todo";
                      return (
                        <li key={l.id} className="border-b border-line last:border-b-0">
                          <Link
                            href={lessonHref(slug, m.position, l.slug)}
                            className="flex min-h-[56px] items-center gap-4 px-6 py-3 transition-colors hover:bg-surface-2"
                          >
                            <StatusDot state={st} />
                            <span className="flex-1">{l.title}</span>
                            <span className="text-sm text-ink-3">{l.duration_minutes} min</span>
                          </Link>
                        </li>
                      );
                    })}
                    {quiz && (
                      <li>
                        <Link
                          href={quizHref(slug, m.position)}
                          className="flex min-h-[56px] items-center gap-4 px-6 py-3 transition-colors hover:bg-surface-2"
                        >
                          <StatusDot state={best !== undefined && best >= quiz.pass_mark ? "done" : "todo"} />
                          <span className="flex-1 font-medium">{quiz.title}</span>
                          <span className="text-sm text-ink-2">
                            {best !== undefined ? `Meilleure note ${formatScore(best)}/20` : "Noté sur 20"}
                          </span>
                        </Link>
                      </li>
                    )}
                  </ul>
                )}
              </li>
            );
          })}
        </ol>
      </section>
      )}
    </div>
  );
}
